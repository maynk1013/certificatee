import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

CHART = Path(__file__).resolve().parents[2] / "helm" / "demo-rollout"


def _render(values_file: str):
    helm = shutil.which("helm")
    if helm is None:
        pytest.skip("helm is not installed")
    completed = subprocess.run(
        [helm, "template", "demo", str(CHART), "-f", str(CHART / "values.yaml"), "-f", str(CHART / values_file)],
        check=True,
        capture_output=True,
        text=True,
    )
    return [item for item in yaml.safe_load_all(completed.stdout) if item]


def test_canary_chart_has_weight_steps_and_analysis():
    documents = _render("values-canary.yaml")
    rollout = next(item for item in documents if item["kind"] == "Rollout")
    steps = rollout["spec"]["strategy"]["canary"]["steps"]
    weights = [step["setWeight"] for step in steps if "setWeight" in step]
    assert weights == [10, 30, 50, 100]
    assert any("analysis" in step for step in steps)


def test_blue_green_chart_does_not_auto_promote():
    documents = _render("values-bluegreen.yaml")
    rollout = next(item for item in documents if item["kind"] == "Rollout")
    blue_green = rollout["spec"]["strategy"]["blueGreen"]
    assert blue_green["autoPromotionEnabled"] is False
    assert blue_green["activeService"] == "demo-active"
    assert blue_green["previewService"] == "demo-preview"


def test_failure_values_set_ready_failure_flag():
    documents = _render("values-canary-failure.yaml")
    rollout = next(item for item in documents if item["kind"] == "Rollout")
    env = {
        item["name"]: item["value"]
        for item in rollout["spec"]["template"]["spec"]["containers"][0]["env"]
    }
    assert env["FAIL_READY"] == "True" or env["FAIL_READY"] == "true"
