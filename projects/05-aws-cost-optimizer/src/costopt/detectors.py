"""Detectors over a snapshot. They do not call AWS by themselves."""

from __future__ import annotations

from costopt.models import Finding

REQUIRED_TAGS = ("Environment", "Project", "Owner")
ALLOWED_ENVIRONMENTS = {"dev", "staging", "prod"}


def _estimate(hourly_usd: float | None, hours: int = 730) -> tuple[float | None, str]:
    if hourly_usd is None:
        return None, "pricing catalog was not supplied; no savings figure is shown"
    return round(hourly_usd * hours, 4), (
        f"estimate from the supplied hourly price times {hours} hours; not a Cost Explorer result"
    )


def find_idle_instances(
    instances: list[dict],
    metrics: dict[str, float | None],
    *,
    cpu_threshold: float,
    prices: dict[str, float] | None = None,
) -> list[Finding]:
    findings: list[Finding] = []
    prices = prices or {}
    for instance in instances:
        instance_id = instance["id"]
        region = instance["region"]
        state = instance.get("state", "unknown")
        if state != "running":
            continue
        cpu = metrics.get(instance_id)
        if cpu is None:
            findings.append(
                Finding(
                    instance_id,
                    "ec2-instance",
                    region,
                    "CPU average is missing for the lookback window",
                    "collect more CloudWatch data before treating this instance as idle",
                    None,
                    "insufficient data; no savings figure",
                )
            )
            continue
        if cpu < cpu_threshold:
            savings, basis = _estimate(prices.get(instance.get("instance_type", "")))
            findings.append(
                Finding(
                    instance_id,
                    "ec2-instance",
                    region,
                    f"average CPU {cpu:.2f} is below threshold {cpu_threshold:.2f}",
                    "review the workload, then stop it only through the opt-in remediation command",
                    savings,
                    basis,
                )
            )
    return findings


def find_unattached_volumes(volumes: list[dict], prices: dict[str, float] | None = None) -> list[Finding]:
    prices = prices or {}
    findings = []
    for volume in volumes:
        if volume.get("attachments"):
            continue
        size = float(volume.get("size_gib", 0))
        monthly = prices.get("ebs_gp3_gib_month")
        savings = round(size * monthly, 4) if monthly is not None else None
        basis = (
            "estimate from supplied gp3 gib-month price times volume size; not a bill"
            if savings is not None
            else "pricing catalog was not supplied; no savings figure is shown"
        )
        findings.append(
            Finding(
                volume["id"],
                "ebs-volume",
                volume["region"],
                "volume status is available and it has no attachments",
                "snapshot it if the data matters, then delete it only after approval",
                savings,
                basis,
            )
        )
    return findings


def find_unattached_addresses(addresses: list[dict], prices: dict[str, float] | None = None) -> list[Finding]:
    prices = prices or {}
    findings = []
    hourly = prices.get("unattached_eip_hour")
    savings, basis = _estimate(hourly)
    for address in addresses:
        if address.get("association_id") or address.get("instance_id"):
            continue
        findings.append(
            Finding(
                address["allocation_id"],
                "elastic-ip",
                address["region"],
                "Elastic IP is not associated with an instance or network interface",
                "release it only after confirming no failover runbook needs it",
                savings,
                basis,
            )
        )
    return findings


def find_tag_issues(resources: list[dict]) -> list[Finding]:
    findings = []
    for resource in resources:
        tags = resource.get("tags") or {}
        missing = [key for key in REQUIRED_TAGS if not str(tags.get(key, "")).strip()]
        environment = str(tags.get("Environment", "")).strip()
        inconsistent = environment and environment not in ALLOWED_ENVIRONMENTS
        if not missing and not inconsistent:
            continue
        reason_parts = []
        if missing:
            reason_parts.append("missing tags: " + ", ".join(missing))
        if inconsistent:
            reason_parts.append(f"Environment tag {environment!r} is outside dev, staging, prod")
        findings.append(
            Finding(
                resource["id"],
                resource.get("resource_type", "resource"),
                resource["region"],
                "; ".join(reason_parts),
                "add Project, Environment, and Owner tags before using the resource in a cost report",
                None,
                "tag findings do not include a savings estimate",
            )
        )
    return findings
