#!/usr/bin/env python3
"""Approve 2026-06-06 Greater Israel collapsing rows (one-off bump).

Prefer `materialize_freeman_predictions.py` for new work — it groups duplicate
(event_id, pub_date, youtube_id) rows and picks canonical host captures.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "runtime" / "artifacts" / "freeman-prediction-crawl.json"
NOTE_PATH = REPO_ROOT / "statecraft" / "notes" / "predictions" / "israel-self-destruction-freeman-2026-06-06.md"
NOTE_REL = "statecraft/notes/predictions/israel-self-destruction-freeman-2026-06-06.md"
CANONICAL_SOURCE = (
    "source-archive/statecraft/2026-06-06/"
    "source-glenn-diesen-chas-freeman-the-greater-israel-project-is-collapsing-2026-06-06.md"
)
ALIAS_SOURCE = (
    "source-archive/statecraft/2026-06-06/"
    "source-dialogue-works-freeman-the-greater-israel-project-is-collapsing-2026-06-06.md"
)
QUOTE = (
    "I think the Israelis have finally reached a moment when they have placed the dream "
    "that some of them have of a greater Israel in grave jeopardy."
)

NOTE_BODY = f"""---
note_type: prediction
event_id: israel_self_destruction_trajectory
speaker: freeman
date_made: 2026-06-06
stance: yes
confidence: high
source: {CANONICAL_SOURCE}
speech_act: iterated
---

WORK only; not Record.

# Freeman — Israel self-destruction (2026-06-06)

## Quote (audit)

{QUOTE}

## Tier-3 context (audit — not stance)

Alias capture (same episode `HuhJinByAEg`): `{ALIAS_SOURCE}` — Dialogue Works mis-file; canonical host capture is Diesen source above.
"""


def main() -> int:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    targets = {
        CANONICAL_SOURCE,
        ALIAS_SOURCE,
    }
    touched = 0
    for row in payload.get("rows") or []:
        if row.get("event_id") != "israel_self_destruction_trajectory":
            continue
        if str(row.get("source") or "").replace("\\", "/") not in targets:
            continue
        row["audit_status"] = "approved"
        row["audit_stance"] = "yes"
        row["audit_speech_act"] = "iterated"
        row["reject_reason"] = None
        row["needs_human"] = False
        row["note_file"] = NOTE_REL
        touched += 1

    if touched != 2:
        print(f"error: expected 2 rows, updated {touched}", file=sys.stderr)
        return 1

    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.write_text(NOTE_BODY, encoding="utf-8")
    MANIFEST.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[ok] approved 2 manifest rows; wrote {NOTE_REL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
