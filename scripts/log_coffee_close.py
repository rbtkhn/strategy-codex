#!/usr/bin/env python3
"""Append a validated coffee_close cadence receipt.

The receipt is WORK-only cadence telemetry. It records what a coffee-selected
branch actually settled, without editing Record surfaces.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from log_cadence_event import KNOWN_CONDUCTOR_SLUGS, append_cadence_event
from cadence_learning import log_coffee_resolution_from_close
from repo_io import DEFAULT_PROFILE_ID

PICKED_VALUES = frozenset({"A", "B", "C", "D", "conductor"})
OUTCOMES = frozenset({"done", "partial", "blocked", "parked"})
READINESS_VALUES = frozenset({"orientation", "execution_ready", "ship_ready", "blocked"})
CONDUCTOR_STATES = frozenset({"open", "closed", "none"})


def _join_tokens(values: list[str] | None, comma_values: str | None = None) -> str:
    tokens: list[str] = []
    for value in values or []:
        tokens.extend(part.strip() for part in str(value).split(","))
    if comma_values:
        tokens.extend(part.strip() for part in str(comma_values).split(","))
    return ",".join(token for token in tokens if token)


def build_coffee_close_kv(
    *,
    picked: str,
    outcome: str,
    readiness: str,
    artifacts: list[str] | None = None,
    artifacts_csv: str | None = None,
    loops: list[str] | None = None,
    loops_csv: str | None = None,
    next_slug: str | None = None,
    conductor: str | None = None,
    conductor_state: str = "none",
) -> dict[str, str]:
    """Validate and normalize coffee_close key-values."""
    picked = str(picked).strip()
    outcome = str(outcome).strip()
    readiness = str(readiness).strip()
    conductor = (conductor or "").strip()
    conductor_state = str(conductor_state or "none").strip()

    if picked not in PICKED_VALUES:
        raise ValueError(f"picked must be one of {sorted(PICKED_VALUES)}, got {picked!r}")
    if outcome not in OUTCOMES:
        raise ValueError(f"outcome must be one of {sorted(OUTCOMES)}, got {outcome!r}")
    if readiness not in READINESS_VALUES:
        raise ValueError(
            f"readiness must be one of {sorted(READINESS_VALUES)}, got {readiness!r}"
        )
    if conductor_state not in CONDUCTOR_STATES:
        raise ValueError(
            f"conductor_state must be one of {sorted(CONDUCTOR_STATES)}, got {conductor_state!r}"
        )
    if picked == "conductor" and not conductor:
        raise ValueError("picked=conductor requires conductor=<slug>")
    if conductor_state in {"open", "closed"} and not conductor:
        raise ValueError("conductor_state=open|closed requires conductor=<slug>")
    if conductor and conductor not in KNOWN_CONDUCTOR_SLUGS:
        raise ValueError(
            "conductor must be one of "
            + ", ".join(sorted(KNOWN_CONDUCTOR_SLUGS))
            + f", got {conductor!r}"
        )

    kv: dict[str, str] = {
        "picked": picked,
        "outcome": outcome,
        "readiness": readiness,
    }
    artifacts_value = _join_tokens(artifacts, artifacts_csv)
    if artifacts_value:
        kv["artifacts"] = artifacts_value
    loops_value = _join_tokens(loops, loops_csv)
    if loops_value:
        kv["loops"] = loops_value
    if next_slug and str(next_slug).strip():
        kv["next"] = str(next_slug).strip()
    if conductor:
        kv["conductor"] = conductor
    if conductor_state != "none":
        kv["conductor_state"] = conductor_state
    return kv


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-u", "--user", default=os.getenv("COMPANION_USER_ID", DEFAULT_PROFILE_ID))
    parser.add_argument("--picked", required=True, choices=sorted(PICKED_VALUES))
    parser.add_argument("--outcome", required=True, choices=sorted(OUTCOMES))
    parser.add_argument("--readiness", required=True, choices=sorted(READINESS_VALUES))
    parser.add_argument("--artifact", action="append", default=[], help="Artifact path/ref; repeatable")
    parser.add_argument("--artifacts", default=None, help="Comma-separated artifact paths/refs")
    parser.add_argument("--loop", action="append", default=[], help="Unresolved loop slug; repeatable")
    parser.add_argument("--loops", default=None, help="Comma-separated unresolved loop slugs")
    parser.add_argument("--next", dest="next_slug", default=None, help="Short next-move slug")
    parser.add_argument("--conductor", default=None, choices=sorted(KNOWN_CONDUCTOR_SLUGS))
    parser.add_argument("--conductor-state", default="none", choices=sorted(CONDUCTOR_STATES))
    parser.add_argument("--cursor-model", default=None)
    parser.add_argument("--model-tier", default=None, choices=["frontier", "fast", "unknown"])
    args = parser.parse_args()

    kv = build_coffee_close_kv(
        picked=args.picked,
        outcome=args.outcome,
        readiness=args.readiness,
        artifacts=args.artifact,
        artifacts_csv=args.artifacts,
        loops=args.loop,
        loops_csv=args.loops,
        next_slug=args.next_slug,
        conductor=args.conductor,
        conductor_state=args.conductor_state,
    )
    path = append_cadence_event(
        "coffee_close",
        args.user.strip(),
        ok=True,
        kv=kv,
        cursor_model=(args.cursor_model.strip() if args.cursor_model else None),
        model_tier=args.model_tier,
    )
    try:
        artifact_tokens = list(args.artifact or [])
        if args.artifacts:
            artifact_tokens.extend(part.strip() for part in str(args.artifacts).split(",") if part.strip())
        loop_tokens = list(args.loop or [])
        if args.loops:
            loop_tokens.extend(part.strip() for part in str(args.loops).split(",") if part.strip())
        log_coffee_resolution_from_close(
            args.user.strip(),
            picked=args.picked,
            outcome=args.outcome,
            readiness=args.readiness,
            artifacts=[item for item in artifact_tokens if str(item).strip()],
            loops=[item for item in loop_tokens if str(item).strip()],
            next_slug=args.next_slug,
        )
    except Exception:
        pass
    print(path.relative_to(Path(__file__).resolve().parent.parent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
