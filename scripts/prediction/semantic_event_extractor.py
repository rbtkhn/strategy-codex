"""Phase 3 stub — registry-first; returns empty candidates until Phase 3b."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT = _REPO_ROOT / "runtime" / "artifacts" / "event-candidates.json"


def extract_candidates(
    captures: list[dict[str, Any]] | None = None,
    notes: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Stub: no NLP extraction in Phase 3a."""
    _ = captures, notes
    return []


def build_payload(candidates: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    items = candidates if candidates is not None else extract_candidates()
    return {
        "_meta": {
            "generated": True,
            "source": "scripts/prediction/semantic_event_extractor.py",
            "phase": "3a-stub",
            "description": "Registry-first; extractor returns empty until Phase 3b",
        },
        "candidates": items,
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    payload = build_payload()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[ok] wrote {args.output} ({len(payload['candidates'])} candidates)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
