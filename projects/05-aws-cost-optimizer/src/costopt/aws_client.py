"""Optional live collection. Tests use snapshots instead of this module."""

from __future__ import annotations

import time
from typing import Callable

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:  # pragma: no cover - boto3 is installed for tests
    BotoCoreError = Exception  # type: ignore[misc, assignment]
    ClientError = Exception  # type: ignore[misc, assignment]


class AwsCallError(RuntimeError):
    pass


def call_with_retry(func: Callable, *, attempts: int = 3, sleep=time.sleep):
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            return func()
        except (ClientError, BotoCoreError) as exc:
            last_error = exc
            code = ""
            if hasattr(exc, "response"):
                code = exc.response.get("Error", {}).get("Code", "")
            if code not in {"Throttling", "RequestLimitExceeded", "TooManyRequestsException"}:
                raise AwsCallError(f"AWS call failed: {code or exc.__class__.__name__}") from exc
            if attempt == attempts:
                break
            sleep(0.01 * attempt)
    raise AwsCallError("AWS call was throttled") from last_error
