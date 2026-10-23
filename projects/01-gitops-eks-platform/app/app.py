#!/usr/bin/env python3
"""Small demo web service used by the GitOps platform.

The process exposes health, readiness, a version page, and Prometheus text
metrics. Configuration comes from environment variables. The process does not
read cloud credentials.
"""

from __future__ import annotations

import json
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Mapping


class AppConfig:
    def __init__(self, env: Mapping[str, str] | None = None) -> None:
        source = os.environ if env is None else env
        self.version = source.get("APP_VERSION", "1.0.0")
        self.fail_health = _as_bool(source.get("FAIL_HEALTH", "false"))
        self.fail_ready = _as_bool(source.get("FAIL_READY", "false"))
        self.fail_api = _as_bool(source.get("FAIL_API", "false"))
        self.ready_delay_seconds = float(source.get("READY_DELAY_SECONDS", "0"))


class Metrics:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._requests: dict[tuple[str, str, str], int] = {}
        self._latency_sum = 0.0
        self._latency_count = 0

    def observe(self, method: str, path: str, status: int, elapsed: float) -> None:
        key = (method, path, str(status))
        with self._lock:
            self._requests[key] = self._requests.get(key, 0) + 1
            self._latency_sum += elapsed
            self._latency_count += 1

    def render(self) -> str:
        lines = [
            "# HELP demo_http_requests_total Total HTTP requests.",
            "# TYPE demo_http_requests_total counter",
        ]
        with self._lock:
            items = sorted(self._requests.items())
            latency_sum = self._latency_sum
            latency_count = self._latency_count
        for (method, path, status), count in items:
            lines.append(
                "demo_http_requests_total"
                f'{{method="{method}",path="{path}",status="{status}"}} {count}'
            )
        lines.extend(
            [
                "# HELP demo_http_request_duration_seconds_sum Total request time.",
                "# TYPE demo_http_request_duration_seconds_sum counter",
                f"demo_http_request_duration_seconds_sum {latency_sum:.6f}",
                "# HELP demo_http_request_duration_seconds_count Observed requests.",
                "# TYPE demo_http_request_duration_seconds_count counter",
                f"demo_http_request_duration_seconds_count {latency_count}",
            ]
        )
        return "\n".join(lines) + "\n"


def _as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def build_handler(config: AppConfig, metrics: Metrics, started_at: float):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, fmt: str, *args) -> None:
            payload = {
                "logger": "demo-web",
                "message": "request",
                "method": self.command,
                "path": self.path.split("?", 1)[0],
                "status": args[1] if len(args) > 1 else None,
            }
            print(json.dumps(payload), flush=True)

        def do_GET(self) -> None:  # noqa: N802
            started = time.perf_counter()
            path = self.path.split("?", 1)[0]
            status, body, content_type = self._route(path)
            elapsed = time.perf_counter() - started
            metrics.observe("GET", path, status, elapsed)
            encoded = body.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(encoded)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(encoded)

        def _route(self, path: str) -> tuple[int, str, str]:
            if path == "/healthz":
                if config.fail_health:
                    return 500, json.dumps({"status": "down"}), "application/json"
                return 200, json.dumps({"status": "ok"}), "application/json"
            if path == "/readyz":
                warmed = (time.time() - started_at) >= config.ready_delay_seconds
                if config.fail_ready or not warmed:
                    return 503, json.dumps({"status": "not-ready"}), "application/json"
                return 200, json.dumps({"status": "ready"}), "application/json"
            if path == "/metrics":
                return 200, metrics.render(), "text/plain; version=0.0.4"
            if path == "/api":
                if config.fail_api:
                    return 500, json.dumps({"error": "simulated failure"}), "application/json"
                return 200, json.dumps({"ok": True, "version": config.version}), "application/json"
            if path == "/":
                body = json.dumps(
                    {
                        "service": "demo-web",
                        "version": config.version,
                        "message": "GitOps demo application",
                    }
                )
                return 200, body, "application/json"
            return 404, json.dumps({"error": "not found"}), "application/json"

    return Handler


def serve(host: str = "0.0.0.0", port: int = 8080, config: AppConfig | None = None) -> None:
    selected = config or AppConfig()
    server = ThreadingHTTPServer((host, port), build_handler(selected, Metrics(), time.time()))
    print(
        json.dumps({"logger": "demo-web", "message": "listening", "host": host, "port": port}),
        flush=True,
    )
    server.serve_forever()


if __name__ == "__main__":
    serve(port=int(os.environ.get("PORT", "8080")))
