from __future__ import annotations

import csv
import json
from pathlib import Path

from costopt.models import Finding


FIELDS = [
    "resource_id",
    "resource_type",
    "region",
    "reason",
    "recommended_action",
    "estimated_monthly_savings_usd",
    "estimate_basis",
    "estimate_label",
]


def write_reports(findings: list[Finding], output_dir: Path, errors: list[dict] | None = None) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = [finding.as_dict() for finding in findings]
    json_path = output_dir / "report.json"
    csv_path = output_dir / "report.csv"
    payload = {
        "dry_run": True,
        "finding_count": len(rows),
        "errors": errors or [],
        "findings": rows,
        "note": "Savings values are estimates only when a price catalog was supplied.",
    }
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key) for key in FIELDS})
    return payload
