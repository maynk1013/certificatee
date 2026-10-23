from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class Finding:
    resource_id: str
    resource_type: str
    region: str
    reason: str
    recommended_action: str
    estimated_monthly_savings_usd: float | None
    estimate_basis: str

    def as_dict(self) -> dict:
        payload = asdict(self)
        payload["estimate_label"] = (
            "estimate" if self.estimated_monthly_savings_usd is not None else "not_estimated"
        )
        return payload
