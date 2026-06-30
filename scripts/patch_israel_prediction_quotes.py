#!/usr/bin/env python3
"""Patch tier-4 Quote (audit) blocks on materialized Israel prediction notes."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES = REPO_ROOT / "statecraft" / "notes" / "predictions"

# Curated verbatim (lightly normalized ASR) from source captures.
QUOTES: dict[str, str] = {
    "2025-01-14": (
        "Israel has delegitimized itself with its genocide in Gaza with its aggression against "
        "Lebanon and Syria with its land seizures in Syria and with its public of that Preposterous "
        "map… Israel has really now extended itself so far beyond what is reasonable it has lost "
        "the moral High Ground internationally… and I think Israel is more and more isolated."
    ),
    "2025-01-17": (
        "Israel in the long run if it's going to survive has to… come to grips with the issue of "
        "coexisting with the Palestinians… he shows no sign of wanting to do that therefore I think "
        "it's long term existence is in Jeopardy and Mr Netanyahu has done more than anyone else to "
        "create that situation."
    ),
    "2025-01-21": (
        "The way the hostages were released was a dramatic demonstration of the utter failure of "
        "the use of force by Israel in Gaza to secure the release of hostages."
    ),
    "2025-07-29": (
        "Does Israel now itself recognize the genocide, the war crimes that it has perpetrated in Gaza?"
    ),
    "2025-08-01": (
        "Israeli human rights organization like B'Tselem… have finally been forced to recognize that "
        "what is happening is genocide."
    ),
    "2025-08-04": (
        "Israel has lost its support in much of the world. That is the West."
    ),
    "2025-10-07": (
        "He has no plan for the day after Hamas and Gaza other than to eradicate Gaza and allow "
        "Jared Kushner to develop it."
    ),
    "2025-10-31": (
        "Indications of a society under extreme stress — a society that is basically failing to "
        "sustain itself. People are immigrating in large numbers. The economy is in deep trouble."
    ),
    "2025-11-21": (
        "Israel is isolating itself not just from its own region, where it is thoroughly isolated… "
        "Even in Europe and the United States, Israel is losing its clout, its support."
    ),
    "2025-12-05": (
        "Israel is now a moral pariah. Nobody wants to have anything to do with it."
    ),
    "2026-05-01": (
        "Israel is internationally isolated and it is now a pariah."
    ),
    "2026-05-26": (
        "Internationally, Israel is now a global pariah. The United States is following it into "
        "that position."
    ),
}

def patch_note(path: Path, quote: str) -> bool:
    text = path.read_text(encoding="utf-8")
    new_block = f"## Quote (audit)\n\n{quote}\n"
    patched, count = re.subn(
        r"## Quote \(audit\)\s*\n+.*?(?=\n## |\Z)",
        new_block,
        text,
        count=1,
        flags=re.DOTALL,
    )
    if count != 1:
        return False
    path.write_text(patched, encoding="utf-8")
    return True

def main() -> int:
    updated = 0
    for pub_date, quote in QUOTES.items():
        path = NOTES / f"israel-self-destruction-freeman-{pub_date}.md"
        if not path.is_file():
            print(f"skip missing {path.name}", file=sys.stderr)
            continue
        if patch_note(path, quote):
            updated += 1
            print(f"[ok] {path.name}")
        else:
            print(f"fail {path.name}", file=sys.stderr)
            return 1
    print(f"[ok] patched {updated} Israel quote blocks")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
