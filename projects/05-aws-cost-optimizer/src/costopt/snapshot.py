from __future__ import annotations

import json
from pathlib import Path

from costopt.detectors import (
    find_idle_instances,
    find_tag_issues,
    find_unattached_addresses,
    find_unattached_volumes,
)
from costopt.models import Finding


def load_snapshot(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def analyze_snapshot(
    snapshot: dict,
    *,
    cpu_threshold: float = 5.0,
    use_prices: bool = False,
) -> list[Finding]:
    prices = snapshot.get("prices") if use_prices else None
    findings: list[Finding] = []
    findings.extend(
        find_idle_instances(
            snapshot.get("instances", []),
            snapshot.get("cpu_averages", {}),
            cpu_threshold=cpu_threshold,
            prices=prices,
        )
    )
    findings.extend(find_unattached_volumes(snapshot.get("volumes", []), prices))
    findings.extend(find_unattached_addresses(snapshot.get("addresses", []), prices))
    findings.extend(find_tag_issues(snapshot.get("resources", [])))
    return findings
