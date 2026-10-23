"""Local metrics, log query, and alert evaluation.

The cluster charts are separate. This module is the part that can run without
Kubernetes. It does not claim those queries were served by Prometheus or Loki.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Sample:
    name: str
    labels: dict[str, str]
    value: float


@dataclass(frozen=True)
class Alert:
    name: str
    severity: str
    summary: str


def parse_metrics(text: str) -> list[Sample]:
    samples: list[Sample] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "{" in line:
            name, rest = line.split("{", 1)
            label_text, value_text = rest.split("}", 1)
            labels = {}
            for part in label_text.split(","):
                if not part.strip():
                    continue
                key, value = part.split("=", 1)
                labels[key.strip()] = value.strip().strip('"')
            samples.append(Sample(name.strip(), labels, float(value_text.strip())))
        else:
            name, value_text = line.rsplit(" ", 1)
            samples.append(Sample(name.strip(), {}, float(value_text)))
    return samples


def counter_total(samples: list[Sample], name: str, label_match: dict[str, str] | None = None) -> float:
    total = 0.0
    for sample in samples:
        if sample.name != name:
            continue
        if label_match and any(sample.labels.get(key) != value for key, value in label_match.items()):
            continue
        total += sample.value
    return total


def error_ratio(samples: list[Sample], name: str = "demo_http_requests_total") -> float | None:
    series = [sample for sample in samples if sample.name == name]
    if not series:
        return None
    total = sum(sample.value for sample in series)
    if total == 0:
        return None
    errors = sum(sample.value for sample in series if sample.labels.get("status", "").startswith("5"))
    return errors / total


def average_latency(samples: list[Sample]) -> float | None:
    total = counter_total(samples, "demo_http_request_duration_seconds_sum")
    count = counter_total(samples, "demo_http_request_duration_seconds_count")
    if count == 0:
        return None
    return total / count


def query_logs(lines: list[str], level: str | None = None, contains: str | None = None) -> list[str]:
    matched = []
    for line in lines:
        if level and f'"level":"{level}"' not in line and f'"level": "{level}"' not in line:
            continue
        if contains and contains not in line:
            continue
        matched.append(line)
    return matched


def evaluate_alerts(
    samples: list[Sample],
    *,
    cpu_ratio: float | None = None,
    error_threshold: float = 0.05,
    latency_threshold: float = 0.5,
    cpu_threshold: float = 0.8,
) -> list[Alert]:
    alerts: list[Alert] = []
    ratio = error_ratio(samples)
    if ratio is not None and ratio > error_threshold:
        alerts.append(Alert("DemoWebHighErrorRate", "warning", "5xx ratio is above the example threshold"))
    latency = average_latency(samples)
    if latency is not None and latency > latency_threshold:
        alerts.append(Alert("DemoWebHighLatency", "warning", "average latency is above the example threshold"))
    if cpu_ratio is not None and cpu_ratio > cpu_threshold:
        alerts.append(Alert("NodeCpuPressure", "warning", "CPU ratio is above the example threshold"))
    return alerts
