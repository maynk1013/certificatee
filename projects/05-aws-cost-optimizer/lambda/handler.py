"""Optional Lambda entry point.

The handler returns a dry-run report. It does not stop or delete resources.
EventBridge scheduling is not created by this repository.
"""

from __future__ import annotations

from costopt.snapshot import analyze_snapshot


def handler(event, context):
    del context
    findings = analyze_snapshot(event.get("snapshot", {}), cpu_threshold=event.get("cpu_threshold", 5.0))
    return {
        "dry_run": True,
        "finding_count": len(findings),
        "findings": [finding.as_dict() for finding in findings],
    }
