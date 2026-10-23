"""Tests for the demo web process. No cluster and no AWS account are required."""

from __future__ import annotations

import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

from app import AppConfig, Metrics, build_handler


def _start(config: AppConfig):
    server = ThreadingHTTPServer(("127.0.0.1", 0), build_handler(config, Metrics(), started_at=0))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def _get(server: ThreadingHTTPServer, path: str):
    port = server.server_address[1]
    with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}") as response:
        return response.status, response.read().decode("utf-8")


def test_health_and_version_endpoints():
    server = _start(AppConfig({"APP_VERSION": "1.2.3"}))
    try:
        status, body = _get(server, "/healthz")
        assert status == 200
        assert json.loads(body)["status"] == "ok"
        status, body = _get(server, "/")
        assert json.loads(body)["version"] == "1.2.3"
        status, body = _get(server, "/readyz")
        assert status == 200
    finally:
        server.shutdown()


def test_ready_and_api_failure_flags():
    server = _start(AppConfig({"FAIL_READY": "true", "FAIL_API": "true"}))
    try:
        port = server.server_address[1]
        with pytest.raises(urllib.error.HTTPError) as ready_error:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/readyz")
        assert ready_error.value.code == 503
        with pytest.raises(urllib.error.HTTPError) as api_error:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/api")
        assert api_error.value.code == 500
    finally:
        server.shutdown()


def test_metrics_count_requests():
    server = _start(AppConfig({}))
    try:
        _get(server, "/healthz")
        _, metrics = _get(server, "/metrics")
        assert 'demo_http_requests_total{method="GET",path="/healthz",status="200"} 1' in metrics
        # The metrics snapshot is built before the current request is recorded.
        assert "demo_http_request_duration_seconds_count 1" in metrics
    finally:
        server.shutdown()
