import json
from pathlib import Path

import pytest
from botocore.exceptions import ClientError

from costopt.aws_client import AwsCallError, call_with_retry
from costopt.notify import notify_slack
from costopt.remediation import RemediationRefused, build_plan, execute_plan
from costopt.reports import write_reports
from costopt.snapshot import analyze_snapshot, load_snapshot
from handler import handler

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "sample_data" / "inventory.json"


def test_sample_report_has_no_invented_savings(tmp_path):
    findings = analyze_snapshot(load_snapshot(SAMPLE), use_prices=False)
    payload = write_reports(findings, tmp_path)
    grouped: dict[str, list[dict]] = {}
    for row in payload["findings"]:
        grouped.setdefault(row["resource_id"], []).append(row)
    idle = next(row for row in grouped["i-idle"] if row["reason"].startswith("average CPU"))
    assert idle["estimated_monthly_savings_usd"] is None
    assert "i-busy" not in grouped
    assert "i-stopped" not in grouped
    assert "missing" in grouped["i-unknown"][0]["reason"].lower()
    assert grouped["vol-free"][0]["resource_type"] == "ebs-volume"
    assert "vol-used" not in grouped
    assert grouped["eipalloc-free"][0]["resource_type"] == "elastic-ip"
    assert "eipalloc-used" not in grouped
    assert all(row["estimated_monthly_savings_usd"] is None for row in payload["findings"])
    evidence = ROOT / "evidence" / "sample-report.json"
    evidence.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def test_supplied_price_is_labelled_as_estimate():
    snapshot = {
        "instances": [
            {"id": "i-1", "region": "ap-south-1", "state": "running", "instance_type": "fixture"}
        ],
        "cpu_averages": {"i-1": 1},
        "prices": {"fixture": 1.0},
    }
    finding = analyze_snapshot(snapshot, cpu_threshold=5, use_prices=True)[0]
    assert finding.estimated_monthly_savings_usd == 730.0
    assert "not a Cost Explorer result" in finding.estimate_basis


def test_remediation_is_off_by_default():
    findings = [item.as_dict() for item in analyze_snapshot(load_snapshot(SAMPLE))]
    plan = build_plan(findings)
    assert plan and plan[0]["executed"] is False
    with pytest.raises(RemediationRefused):
        execute_plan(plan, client=object(), allow=False, resource_ids={"i-idle"})


def test_remediation_stops_only_an_approved_id():
    calls = []

    class Client:
        def stop_instances(self, InstanceIds):
            calls.append(InstanceIds)

    plan = [{"action": "stop_instance", "resource_id": "i-idle", "region": "ap-south-1", "executed": False}]
    result = execute_plan(plan, Client(), allow=True, resource_ids={"i-idle"})
    assert calls == [["i-idle"]]
    assert result[0]["executed"] is True
    with pytest.raises(RemediationRefused):
        execute_plan(plan, Client(), allow=True, resource_ids=set())


def test_access_denied_and_throttle_retry():
    def denied():
        raise ClientError({"Error": {"Code": "AccessDenied", "Message": "no"}}, "DescribeInstances")

    with pytest.raises(AwsCallError):
        call_with_retry(denied)

    state = {"count": 0}

    def throttled():
        state["count"] += 1
        if state["count"] < 3:
            raise ClientError({"Error": {"Code": "Throttling", "Message": "slow"}}, "DescribeInstances")
        return "ok"

    assert call_with_retry(throttled, sleep=lambda _: None) == "ok"


def test_lambda_stays_in_dry_run():
    payload = handler({"snapshot": json.loads(SAMPLE.read_text(encoding="utf-8"))}, None)
    assert payload["dry_run"] is True
    assert payload["finding_count"] >= 4


def test_slack_is_skipped_when_webhook_is_empty():
    calls = []
    assert notify_slack("", "hello", calls.append) == {"sent": False, "reason": "webhook is empty"}
    assert calls == []
