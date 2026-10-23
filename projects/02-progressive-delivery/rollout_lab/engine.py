"""Local model of blue-green and canary decisions.

This does not move packets on a cluster. It records the same kind of decision
an Argo Rollouts analysis would make from readiness and error ratio.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Observation:
    ready: bool
    error_rate: float
    version: str


@dataclass
class HistoryEntry:
    step: str
    active_version: str
    candidate_version: str
    weight: int
    decision: str
    detail: str


@dataclass
class RolloutResult:
    strategy: str
    status: str
    active_version: str
    candidate_version: str
    weight_on_candidate: int
    history: list[HistoryEntry] = field(default_factory=list)

    def render(self) -> str:
        lines = [
            f"strategy={self.strategy}",
            f"status={self.status}",
            f"active_version={self.active_version}",
            f"candidate_version={self.candidate_version}",
            f"weight_on_candidate={self.weight_on_candidate}",
        ]
        for index, entry in enumerate(self.history, start=1):
            lines.append(
                f"{index}. step={entry.step} active={entry.active_version} "
                f"candidate={entry.candidate_version} weight={entry.weight} "
                f"decision={entry.decision} detail={entry.detail}"
            )
        return "\n".join(lines) + "\n"


def run_canary(
    observations: list[Observation],
    weights: list[int] | None = None,
    error_threshold: float = 0.05,
    failure_limit: int = 1,
) -> RolloutResult:
    if not observations:
        raise ValueError("canary rollout needs at least one observation")
    steps = weights or [10, 30, 50, 100]
    candidate = observations[0].version
    history: list[HistoryEntry] = []
    failures = 0
    for index, weight in enumerate(steps):
        observation = observations[min(index, len(observations) - 1)]
        healthy = observation.ready and observation.error_rate <= error_threshold
        if healthy:
            failures = 0
            history.append(
                HistoryEntry(
                    step=f"setWeight:{weight}",
                    active_version="v1" if weight < 100 else observation.version,
                    candidate_version=candidate,
                    weight=weight,
                    decision="continue",
                    detail=f"error_rate={observation.error_rate:.4f}",
                )
            )
            continue
        failures += 1
        history.append(
            HistoryEntry(
                step=f"analysis:{weight}",
                active_version="v1",
                candidate_version=candidate,
                weight=weight,
                decision="fail",
                detail=(
                    f"ready={observation.ready} error_rate={observation.error_rate:.4f} "
                    f"failures={failures}"
                ),
            )
        )
        if failures > failure_limit:
            history.append(
                HistoryEntry(
                    step="rollback",
                    active_version="v1",
                    candidate_version=candidate,
                    weight=0,
                    decision="rollback",
                    detail="failure limit reached; candidate receives no traffic",
                )
            )
            return RolloutResult("canary", "rolled_back", "v1", candidate, 0, history)
    return RolloutResult("canary", "promoted", candidate, candidate, 100, history)


def run_blue_green(
    preview: Observation,
    error_threshold: float = 0.05,
    promote: bool = True,
) -> RolloutResult:
    history = [
        HistoryEntry(
            step="deploy-preview",
            active_version="v1",
            candidate_version=preview.version,
            weight=0,
            decision="hold",
            detail="active service still points at v1",
        )
    ]
    healthy = preview.ready and preview.error_rate <= error_threshold
    if not healthy:
        history.append(
            HistoryEntry(
                step="pre-promotion-analysis",
                active_version="v1",
                candidate_version=preview.version,
                weight=0,
                decision="rollback",
                detail=f"ready={preview.ready} error_rate={preview.error_rate:.4f}",
            )
        )
        return RolloutResult("blue-green", "rolled_back", "v1", preview.version, 0, history)
    if not promote:
        history.append(
            HistoryEntry(
                step="wait-for-approval",
                active_version="v1",
                candidate_version=preview.version,
                weight=0,
                decision="pause",
                detail="preview is healthy and active traffic was not switched",
            )
        )
        return RolloutResult("blue-green", "paused", "v1", preview.version, 0, history)
    history.append(
        HistoryEntry(
            step="switch-active-service",
            active_version=preview.version,
            candidate_version=preview.version,
            weight=100,
            decision="promote",
            detail="active service selector moved to the preview version",
        )
    )
    return RolloutResult("blue-green", "promoted", preview.version, preview.version, 100, history)
