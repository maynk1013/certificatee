#!/usr/bin/env python3
"""Check committed environment files for required ownership fields."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED = ("project", "environment", "owner")
ALLOWED_ENVIRONMENTS = {"dev", "staging", "prod"}


def check_file(path: Path) -> list[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    errors = []
    for key in REQUIRED:
        value = payload.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{path}: missing {key}")
    environment = payload.get("environment")
    if environment not in ALLOWED_ENVIRONMENTS:
        errors.append(f"{path}: environment must be one of {sorted(ALLOWED_ENVIRONMENTS)}")
    if payload.get("create_compute") is True:
        errors.append(f"{path}: create_compute must stay false in committed examples")
    return errors


def main(argv: list[str]) -> int:
    if not argv:
        raise SystemExit("pass one or more tfvars json files")
    errors: list[str] = []
    for item in argv:
        errors.extend(check_file(Path(item)))
    if errors:
        print("\n".join(errors))
        return 1
    print(f"checked {len(argv)} environment file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
