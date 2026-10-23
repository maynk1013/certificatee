from pathlib import Path

from observability_lab.lab import average_latency, evaluate_alerts, parse_metrics, query_logs

METRICS = """
# HELP demo_http_requests_total Total HTTP requests.
demo_http_requests_total{status="200"} 95
demo_http_requests_total{status="500"} 5
demo_http_request_duration_seconds_sum 10
demo_http_request_duration_seconds_count 100
"""

BAD_METRICS = """
demo_http_requests_total{status="200"} 10
demo_http_requests_total{status="500"} 10
demo_http_request_duration_seconds_sum 80
demo_http_request_duration_seconds_count 100
"""

LOGS = [
    '{"level":"info","message":"request","path":"/healthz"}',
    '{"level":"error","message":"simulated failure","path":"/api"}',
]


def test_metrics_and_logs_are_queryable():
    samples = parse_metrics(METRICS)
    assert sum(sample.value for sample in samples if sample.labels.get("status") == "500") == 5
    assert average_latency(samples) == 0.1
    errors = query_logs(LOGS, level="error", contains="simulated failure")
    assert len(errors) == 1


def test_healthy_sample_does_not_alert():
    alerts = evaluate_alerts(parse_metrics(METRICS), cpu_ratio=0.2)
    assert alerts == []


def test_bad_sample_fires_error_latency_and_cpu_alerts():
    alerts = evaluate_alerts(parse_metrics(BAD_METRICS), cpu_ratio=0.91)
    names = [alert.name for alert in alerts]
    assert names == ["DemoWebHighErrorRate", "DemoWebHighLatency", "NodeCpuPressure"]


def test_empty_traffic_does_not_pretend_to_be_healthy():
    assert evaluate_alerts(parse_metrics("")) == []


def test_reproducible_alert_scenario_writes_evidence():
    alerts = evaluate_alerts(parse_metrics(BAD_METRICS), cpu_ratio=0.91)
    lines = [f"{alert.name} severity={alert.severity} summary={alert.summary}" for alert in alerts]
    evidence = Path(__file__).resolve().parents[2] / "evidence" / "test-alert.log"
    evidence.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert "DemoWebHighErrorRate" in evidence.read_text(encoding="utf-8")
