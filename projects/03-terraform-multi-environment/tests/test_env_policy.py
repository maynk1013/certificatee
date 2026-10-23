import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "policy" / "check_tags.py"
ENVS = [
    ROOT / "envs" / "dev" / "terraform.tfvars.json",
    ROOT / "envs" / "staging" / "terraform.tfvars.json",
    ROOT / "envs" / "prod" / "terraform.tfvars.json",
]


def test_committed_environments_have_owner_tags():
    completed = subprocess.run([sys.executable, str(CHECK), *map(str, ENVS)], capture_output=True, text=True)
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_missing_owner_is_rejected(tmp_path: Path):
    bad = tmp_path / "bad.tfvars.json"
    bad.write_text(json.dumps({"project": "x", "environment": "dev", "create_compute": False}), encoding="utf-8")
    completed = subprocess.run([sys.executable, str(CHECK), str(bad)], capture_output=True, text=True)
    assert completed.returncode == 1
    assert "missing owner" in completed.stdout


def test_committed_bad_fixture_is_rejected():
    bad = ROOT / "tests" / "fixtures" / "bad-tags.tfvars.json"
    completed = subprocess.run([sys.executable, str(CHECK), str(bad)], capture_output=True, text=True)
    assert completed.returncode == 1


def test_backend_example_uses_s3_lockfile():
    text = (ROOT / "backend" / "backend.s3.hcl.example").read_text(encoding="utf-8")
    assert "use_lockfile = true" in text
    assert "encrypt      = true" in text
    assert "REPLACE_WITH_PRIVATE_STATE_BUCKET" in text
