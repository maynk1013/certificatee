"""Static checks for the Dockerfile. This is not a vulnerability scan."""

from pathlib import Path


DOCKERFILE = Path(__file__).resolve().parents[1] / "Dockerfile"


def test_image_policy():
    text = DOCKERFILE.read_text(encoding="utf-8")
    assert "python:3.12.11-slim" in text
    assert ":latest" not in text
    assert "USER 10001" in text
    assert "HEALTHCHECK" in text
    assert "ADD " not in text
