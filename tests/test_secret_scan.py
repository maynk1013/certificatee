from pathlib import Path

from tools.secret_scan import scan


def test_scanner_flags_a_generated_sample(tmp_path: Path):
    sample = tmp_path / "sample.txt"
    sample.write_text("prefix " + "AKIA" + "ABCDEFGHIJKLMNOP" + " suffix", encoding="utf-8")
    findings = scan(tmp_path)
    assert any("aws-access-key-id" in item for item in findings)


def test_repository_scan_is_clean():
    root = Path(__file__).resolve().parents[1]
    assert scan(root) == []
