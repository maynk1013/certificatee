import json
from pathlib import Path

from backup_lab.drill import create_backup, restore_drill, validate_backup

FIXTURE = Path(__file__).resolve().parents[2] / "fixtures" / "app-data" / "orders.json"


def test_backup_checksum_and_restore(tmp_path):
    backup = tmp_path / "backup"
    metadata = create_backup(FIXTURE, backup)
    assert validate_backup(backup) == []
    result = restore_drill(backup, tmp_path / "restore")
    assert result["ok"] is True
    assert result["sha256"] == metadata["sha256"]
    assert result["cross_region_tested"] is False
    assert result["local_restore_seconds"] >= 0
    evidence = Path(__file__).resolve().parents[2] / "evidence" / "local-restore-drill.json"
    evidence.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


def test_tampered_backup_fails_validation(tmp_path):
    backup = tmp_path / "backup"
    create_backup(FIXTURE, backup)
    payload = backup / "orders.json"
    payload.write_text("tampered\n", encoding="utf-8")
    errors = validate_backup(backup)
    assert "checksum does not match the payload" in errors
