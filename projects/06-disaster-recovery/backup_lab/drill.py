"""Local backup metadata check and restore drill for synthetic data."""

from __future__ import annotations

import hashlib
import json
import shutil
import time
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def create_backup(source: Path, backup_dir: Path) -> dict:
    backup_dir.mkdir(parents=True, exist_ok=True)
    destination = backup_dir / source.name
    shutil.copyfile(source, destination)
    metadata = {
        "source_name": source.name,
        "sha256": sha256(destination),
        "bytes": destination.stat().st_size,
        "retention_days": 35,
        "cross_region": False,
    }
    (backup_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return metadata


def validate_backup(backup_dir: Path) -> list[str]:
    metadata_path = backup_dir / "metadata.json"
    errors = []
    if not metadata_path.exists():
        return ["metadata.json is missing"]
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    for key in ("source_name", "sha256", "bytes", "retention_days"):
        if key not in metadata:
            errors.append(f"missing {key}")
    data_path = backup_dir / metadata.get("source_name", "")
    if not data_path.exists():
        errors.append("backup payload is missing")
        return errors
    if sha256(data_path) != metadata.get("sha256"):
        errors.append("checksum does not match the payload")
    if metadata.get("retention_days", 0) < 7:
        errors.append("retention is below the 7 day minimum")
    return errors


def restore_drill(backup_dir: Path, restore_dir: Path) -> dict:
    errors = validate_backup(backup_dir)
    if errors:
        raise RuntimeError("; ".join(errors))
    metadata = json.loads((backup_dir / "metadata.json").read_text(encoding="utf-8"))
    restore_dir.mkdir(parents=True, exist_ok=True)
    target = restore_dir / metadata["source_name"]
    if target.exists():
        target.write_text("corrupt\n", encoding="utf-8")
    started = time.perf_counter()
    shutil.copyfile(backup_dir / metadata["source_name"], target)
    elapsed = time.perf_counter() - started
    restored_hash = sha256(target)
    return {
        "ok": restored_hash == metadata["sha256"],
        "sha256": restored_hash,
        "local_restore_seconds": elapsed,
        "label": "local synthetic restore elapsed time, not an AWS RTO measurement",
        "cross_region_tested": False,
    }
