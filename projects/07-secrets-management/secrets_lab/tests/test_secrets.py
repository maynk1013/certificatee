import json
import logging
from pathlib import Path

import pytest
from botocore.exceptions import ClientError

from secrets_lab.app import AwsSecretsProvider, DemoApp
from secrets_lab.store import FileSecretStore, rotate

ROOT = Path(__file__).resolve().parents[2]


def test_app_reads_secret_without_logging_it(tmp_path, caplog):
    store = FileSecretStore(tmp_path / "secrets.json")
    store.put("local-test-secret-value")
    caplog.set_level(logging.INFO)
    status = DemoApp(store).reveal_status()
    assert status == {"secret_present": True, "secret_length": len("local-test-secret-value")}
    rendered = caplog.text
    assert "local-test-secret-value" not in rendered
    assert "secret_present" in rendered


def test_rotation_and_failed_rotation_rollback(tmp_path):
    store = FileSecretStore(tmp_path / "secrets.json")
    store.put("version-one-value")
    rotated = rotate(store, "version-two-value", verify=lambda value: value.startswith("version-two"))
    assert rotated["status"] == "rotated"
    assert store.get() == "version-two-value"
    failed = rotate(store, "bad-value", verify=lambda value: False)
    assert failed["status"] == "rolled_back"
    assert store.get() == "version-two-value"


def test_aws_provider_reads_and_hides_access_errors():
    class Client:
        def get_secret_value(self, SecretId):
            assert SecretId == "demo/app"
            return {"SecretString": "aws-test-secret"}

    assert AwsSecretsProvider(Client(), "demo/app").get() == "aws-test-secret"

    class Denied:
        def get_secret_value(self, SecretId):
            raise ClientError({"Error": {"Code": "AccessDeniedException", "Message": "no"}}, "GetSecretValue")

    with pytest.raises(RuntimeError) as exc:
        AwsSecretsProvider(Denied(), "demo/app").get()
    assert "AccessDeniedException" in str(exc.value)
    assert "aws-test-secret" not in str(exc.value)


def test_generated_kubernetes_manifest_has_no_secret_value():
    text = (ROOT / "k8s" / "deployment.yaml").read_text(encoding="utf-8")
    assert "secretKeyRef" in text
    assert "local-test-secret-value" not in text
    assert "aws-test-secret" not in text


def test_rotation_evidence(tmp_path):
    store = FileSecretStore(tmp_path / "secrets.json")
    store.put("version-one-value")
    result = rotate(store, "version-two-value", verify=lambda value: len(value) > 8)
    evidence = ROOT / "evidence" / "rotation.json"
    evidence.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    assert "version-two-value" not in evidence.read_text(encoding="utf-8")
