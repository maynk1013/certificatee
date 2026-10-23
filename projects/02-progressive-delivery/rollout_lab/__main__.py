"""Print a rollout log for a named scenario."""

from __future__ import annotations

import argparse
import sys

from rollout_lab.engine import Observation, run_blue_green, run_canary


SCENARIOS = {
    "canary-success": lambda: run_canary(
        [
            Observation(True, 0.0, "v2"),
            Observation(True, 0.01, "v2"),
            Observation(True, 0.0, "v2"),
            Observation(True, 0.0, "v2"),
        ]
    ),
    "canary-failure": lambda: run_canary(
        [
            Observation(True, 0.01, "v2"),
            Observation(True, 0.40, "v2"),
            Observation(True, 0.50, "v2"),
        ]
    ),
    "blue-green-success": lambda: run_blue_green(Observation(True, 0.0, "v2"), promote=True),
    "blue-green-failure": lambda: run_blue_green(Observation(False, 0.80, "v2"), promote=True),
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a local rollout scenario")
    parser.add_argument("scenario", choices=sorted(SCENARIOS))
    args = parser.parse_args(argv)
    sys.stdout.write(SCENARIOS[args.scenario]().render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
