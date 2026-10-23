"""Application that reads a secret and logs only whether it was present."""

from __future__ import annotations

import json
import logging

LOGGER = logging.getLogger("secrets-demo")


class AwsSecretsProvider:
    def __init__(self, client, secret_id: str) -> None:
        self.client = client
        self.secret_id = secret_id

    def get(self) -> str:
        try:
            response = self.client.get_secret_value(SecretId=self.secret_id)
        except Exception as exc:
            code = getattr(exc, "response", {}).get("Error", {}).get("Code", exc.__class__.__name__)
            raise RuntimeError(f"secret read failed: {code}") from exc
        value = response.get("SecretString")
        if not isinstance(value, str) or not value:
            raise RuntimeError("secret read failed: empty response")
        return value


class DemoApp:
    def __init__(self, provider) -> None:
        self.provider = provider

    def reveal_status(self) -> dict:
        secret = self.provider.get()
        status = {"secret_present": True, "secret_length": len(secret)}
        LOGGER.info(json.dumps({"message": "secret status", "secret_present": True}))
        return status
