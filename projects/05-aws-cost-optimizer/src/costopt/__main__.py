"""Dry-run cost report CLI. It does not change AWS resources."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from costopt.reports import write_reports
from costopt.snapshot import analyze_snapshot, load_snapshot

LOGGER = logging.getLogger("costopt")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a dry-run AWS waste report from a snapshot")
    parser.add_argument("--input", required=True, help="Snapshot JSON path")
    parser.add_argument("--output", required=True, help="Directory for CSV and JSON reports")
    parser.add_argument("--cpu-threshold", type=float, default=5.0)
    parser.add_argument(
        "--use-supplied-prices",
        action="store_true",
        help="Use prices embedded in the snapshot. Those figures are estimates, not a bill.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format='{"logger":"costopt","message":"%(message)s"}')
    args = build_parser().parse_args(argv)
    snapshot = load_snapshot(Path(args.input))
    findings = analyze_snapshot(
        snapshot,
        cpu_threshold=args.cpu_threshold,
        use_prices=args.use_supplied_prices,
    )
    payload = write_reports(findings, Path(args.output))
    LOGGER.info("wrote dry-run report findings=%s", payload["finding_count"])
    json.dump({"finding_count": payload["finding_count"], "dry_run": True}, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
