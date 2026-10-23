"""Optional Slack notification. The webhook is never written to the log."""

from __future__ import annotations

import json
from urllib.request import Request


def notify_slack(webhook_url: str, text: str, opener) -> dict:
    if not webhook_url:
        return {"sent": False, "reason": "webhook is empty"}
    payload = json.dumps({"text": text}).encode("utf-8")
    request = Request(webhook_url, data=payload, method="POST")
    request.add_header("Content-Type", "application/json")
    opener(request)
    return {"sent": True}
