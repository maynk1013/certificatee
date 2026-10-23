#!/usr/bin/env python3
"""Small secret scanner for this portfolio. It is not a replacement for a full DLP product."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".terraform", ".venv", "__pycache__", ".pytest_cache"}
PATTERNS = [
    ("private-key", re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----")),
    ("aws-access-key-id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("slack-webhook", re.compile(r"https://hooks\.slack\.com/services/[A-Z0-9]{6,}/[A-Z0-9]{6,}/[A-Za-z0-9]{10,}")),
]


def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.stat().st_size > 1_000_000:
            continue
        yield path


def scan(root: Path) -> list[str]:
    findings = []
    for path in iter_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in PATTERNS:
            if pattern.search(text):
                findings.append(f"{name}: {path.relative_to(root)}")
    return findings


def main() -> int:
    findings = scan(ROOT)
    if findings:
        print("\n".join(findings))
        return 1
    print("secret scan found no matched patterns")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
