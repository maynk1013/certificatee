"""Render the Helm chart and check the runtime safety fields."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

CHART = Path(__file__).resolve().parents[2] / "helm" / "demo-web"
ROOT = Path(__file__).resolve().parents[2]


def test_helm_template_contains_probes_and_resources():
    helm = shutil.which("helm")
    if helm is None:
        pytest.skip("helm is not installed")
    rendered = subprocess.run(
        [
            helm,
            "template",
            "demo",
            str(CHART),
            "-f",
            str(CHART / "values.yaml"),
            "-f",
            str(CHART / "values-dev.yaml"),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    documents = [item for item in yaml.safe_load_all(rendered.stdout) if item]
    deployment = next(item for item in documents if item["kind"] == "Deployment")
    container = deployment["spec"]["template"]["spec"]["containers"][0]
    assert container["livenessProbe"]["httpGet"]["path"] == "/healthz"
    assert container["readinessProbe"]["httpGet"]["path"] == "/readyz"
    assert container["resources"]["requests"]["cpu"] == "50m"
    assert container["resources"]["limits"]["memory"] == "128Mi"
    assert deployment["spec"]["strategy"]["rollingUpdate"]["maxUnavailable"] == 0
    kinds = {item["kind"] for item in documents}
    assert "ServiceMonitor" in kinds


def test_gitops_application_points_at_chart():
    text = (ROOT / "gitops" / "argocd" / "application-demo-web.yaml").read_text(encoding="utf-8")
    assert "kind: Application" in text
    assert "projects/01-gitops-eks-platform/helm/demo-web" in text
    assert "selfHeal: true" in text
    assert "hooks.slack.com/services/" not in text
