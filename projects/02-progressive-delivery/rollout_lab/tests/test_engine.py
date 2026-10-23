from pathlib import Path

from rollout_lab.engine import Observation, run_blue_green, run_canary
from rollout_lab.__main__ import main


def test_canary_promotes_when_error_rate_stays_under_threshold():
    result = run_canary(
        [Observation(True, 0.0, "v2") for _ in range(4)],
        weights=[10, 30, 50, 100],
    )
    assert result.status == "promoted"
    assert result.active_version == "v2"
    assert result.weight_on_candidate == 100
    assert [entry.weight for entry in result.history] == [10, 30, 50, 100]


def test_canary_rolls_back_after_repeated_errors():
    result = run_canary(
        [
            Observation(True, 0.0, "v2"),
            Observation(True, 0.4, "v2"),
            Observation(True, 0.5, "v2"),
        ],
        failure_limit=1,
    )
    assert result.status == "rolled_back"
    assert result.active_version == "v1"
    assert result.weight_on_candidate == 0
    assert result.history[-1].decision == "rollback"


def test_unready_preview_does_not_switch_blue_green_traffic():
    result = run_blue_green(Observation(False, 0.0, "v2"))
    assert result.status == "rolled_back"
    assert result.active_version == "v1"
    assert result.weight_on_candidate == 0


def test_blue_green_switch_requires_explicit_promotion():
    paused = run_blue_green(Observation(True, 0.0, "v2"), promote=False)
    assert paused.status == "paused"
    assert paused.active_version == "v1"
    promoted = run_blue_green(Observation(True, 0.01, "v2"), promote=True)
    assert promoted.status == "promoted"
    assert promoted.active_version == "v2"


def test_cli_writes_failure_log(capsys):
    assert main(["canary-failure"]) == 0
    captured = capsys.readouterr().out
    assert "status=rolled_back" in captured
    assert "decision=rollback" in captured


def test_record_evidence_files(tmp_path, monkeypatch):
    evidence = Path(__file__).resolve().parents[2] / "evidence"
    # The CLI is deterministic. Calling it records the same log a reviewer can rerun.
    from rollout_lab.__main__ import SCENARIOS

    for name in ("canary-success", "canary-failure", "blue-green-success", "blue-green-failure"):
        text = SCENARIOS[name]().render()
        (evidence / f"{name}.log").write_text(text, encoding="utf-8")
        assert "status=" in text
    monkeypatch.chdir(tmp_path)
