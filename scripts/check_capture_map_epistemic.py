#!/usr/bin/env python3
"""Advisory WARNs linking epistemic_state rows to capture-map recuration queue."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STATE = REPO_ROOT / "runtime" / "artifacts" / "epistemic_state.json"
ENTROPY_THRESHOLD = 1.2

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from voice_prediction_pilot import VOICE_REGISTRY, get_voice_config, load_capture_map  # noqa: E402

def _capture_row_index() -> dict[tuple[str, str, str, str], dict]:
    index: dict[tuple[str, str, str, str], dict] = {}
    for speaker in sorted(VOICE_REGISTRY.keys()):
        cfg = get_voice_config(speaker)
        if not cfg.capture_map_path.is_file():
            continue
        for row in load_capture_map(cfg.capture_map_path, guest_speaker=speaker):
            if not isinstance(row, dict):
                continue
            event_id = str(row.get("event_id") or "")
            capture = str(row.get("capture") or "").replace("\\", "/")
            key = (speaker, event_id, capture, "")
            index[(speaker, event_id, capture, str(row.get("appearance_date") or "")[:10])] = row
            index[(speaker, event_id, capture, "")] = row
    return index

def collect_warnings(
    objects: list[dict],
    *,
    row_index: dict[tuple[str, str, str, str], dict] | None = None,
) -> list[str]:
    idx = row_index if row_index is not None else _capture_row_index()
    warnings: list[str] = []

    for obj in objects:
        if not isinstance(obj, dict):
            continue
        voice = str(obj.get("voice") or "")
        capture = str(obj.get("capture") or "").replace("\\", "/")
        timestamp = str(obj.get("timestamp") or "")
        event_id = str(obj.get("capture_map_event_id") or "")
        entropy = float(obj.get("alignment_entropy") or 0.0)
        regime = str((obj.get("regime") or {}).get("label") or "")
        primary = str(obj.get("primary_event_id") or "")
        stance = str(obj.get("stance") or "")

        row = idx.get((voice, event_id, capture, timestamp)) or idx.get((voice, event_id, capture, ""))
        quote_speaker = str((row or {}).get("quote_speaker") or obj.get("quote_speaker") or voice)
        public_display = (row or {}).get("public_display", obj.get("public_display", True))

        base = (
            f"{voice} {event_id} @ {timestamp} — "
            f"entropy {entropy:.4f} nats; capture {capture}"
        )

        if entropy > ENTROPY_THRESHOLD:
            warnings.append(f"WARN: high binding ambiguity — {base}")
        if regime == "fragmentation":
            warnings.append(
                f"WARN: fragmentation regime (primary {primary}) — {base}"
            )
        if quote_speaker == "host" and stance.lower() == "yes":
            warnings.append(f"WARN: excerpt/speaker may not support stance yes — {base}")
        if public_display is False and entropy > ENTROPY_THRESHOLD:
            warnings.append(
                f"WARN: hidden row load-bearing for inference — {base}"
            )

    return warnings

def run_check(
    *,
    state_path: Path | None = None,
    advisory: bool = True,
    top: int | None = None,
) -> int:
    target = state_path or DEFAULT_STATE
    if not target.is_file():
        msg = f"missing {target.relative_to(REPO_ROOT)}"
        if advisory:
            print(f"WARN: {msg}", file=sys.stderr)
            return 0
        print(f"error: {msg}", file=sys.stderr)
        return 1

    payload = json.loads(target.read_text(encoding="utf-8"))
    objects = payload.get("objects") if isinstance(payload, dict) else []
    if not isinstance(objects, list):
        print("error: epistemic_state objects must be a list", file=sys.stderr)
        return 1 if not advisory else 0

    warnings = collect_warnings(objects)
    if top is not None and top > 0:
        warnings = warnings[:top]

    for line in warnings:
        print(line, file=sys.stderr)

    if not warnings:
        print("[ok] capture-map epistemic advisory (no WARNs)")
    return 0

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--path", type=Path, default=DEFAULT_STATE)
    ap.add_argument("--advisory", action="store_true", default=True)
    ap.add_argument("--top", type=int, default=None)
    args = ap.parse_args()
    return run_check(state_path=args.path, advisory=args.advisory, top=args.top)

if __name__ == "__main__":
    raise SystemExit(main())
