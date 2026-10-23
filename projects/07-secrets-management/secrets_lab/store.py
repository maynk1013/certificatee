"""File-backed secret versions for local rotation drills."""

from __future__ import annotations

import json
from pathlib import Path


class RotationError(RuntimeError):
    pass


class FileSecretStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        if not path.exists():
            path.write_text(json.dumps({"current": 0, "versions": []}) + "\n", encoding="utf-8")

    def _read(self) -> dict:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write(self, payload: dict) -> None:
        self.path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def put(self, value: str) -> int:
        if not value or "\n" in value:
            raise RotationError("secret value must be a single non-empty line")
        payload = self._read()
        payload["versions"].append(value)
        payload["current"] = len(payload["versions"]) - 1
        self._write(payload)
        return payload["current"]

    def get(self) -> str:
        payload = self._read()
        versions = payload["versions"]
        if not versions:
            raise RotationError("no secret version is stored")
        return versions[payload["current"]]

    def rollback(self) -> None:
        payload = self._read()
        if payload["current"] == 0:
            raise RotationError("no previous version is available")
        payload["current"] -= 1
        self._write(payload)


def rotate(store: FileSecretStore, new_value: str, verify) -> dict:
    try:
        previous = store.get()
    except RotationError:
        previous = None
    version = store.put(new_value)
    try:
        if verify(store.get()) is not True:
            raise RotationError("verification returned false")
    except Exception as exc:
        if previous is None:
            raise RotationError("rotation failed and no previous version exists") from exc
        store.rollback()
        return {
            "status": "rolled_back",
            "version": version,
            "detail": "verification failed; current pointer moved to the previous version",
        }
    return {"status": "rotated", "version": version, "detail": "verification passed"}
