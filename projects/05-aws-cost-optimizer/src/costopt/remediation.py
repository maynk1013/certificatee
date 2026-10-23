"""Opt-in plans. The default path never calls a mutating AWS API."""

from __future__ import annotations

MUTATING_TYPES = {"ec2-instance": "stop_instance"}


class RemediationRefused(RuntimeError):
    pass


def build_plan(findings: list[dict]) -> list[dict]:
    plan = []
    for finding in findings:
        action = MUTATING_TYPES.get(finding["resource_type"])
        if action is None:
            continue
        if "below threshold" not in finding["reason"]:
            continue
        plan.append(
            {
                "action": action,
                "resource_id": finding["resource_id"],
                "region": finding["region"],
                "executed": False,
            }
        )
    return plan


def execute_plan(plan: list[dict], client, *, allow: bool, resource_ids: set[str]) -> list[dict]:
    if not allow:
        raise RemediationRefused("remediation is disabled; pass the explicit allow switch")
    if client is None:
        raise RemediationRefused("no AWS client was provided")
    results = []
    for item in plan:
        if item["resource_id"] not in resource_ids:
            raise RemediationRefused(f"{item['resource_id']} is not in the approved id list")
        if item["action"] != "stop_instance":
            raise RemediationRefused(f"unsupported action {item['action']}")
        client.stop_instances(InstanceIds=[item["resource_id"]])
        updated = dict(item)
        updated["executed"] = True
        results.append(updated)
    return results
