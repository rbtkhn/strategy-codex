#!/usr/bin/env python3
"""Fix ph-civ validate gate: boundary leaks and chapter-folder LLM prompts."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROOT = REPO / "public" / "ph-civ"

LLM_BLOCK = """

## LLM Prompt

Paste this folder link into ChatGPT, Claude, or Grok and ask:

> Guide me through this chapter folder as a public study packet. Start with the transcript, then use the commentary canvas and orientation/card guardrails. Keep review status visible and separate lecture representation from verification.
>
> Use a source-lattice reading order: README first, transcript second, commentary/card third, and broader interpretation only after the source floor is stable.
"""

REPLACEMENTS: dict[Path, list[tuple[str, str]]] = {
    ROOT / "docs/study-edition.md": [
        ("`strategy-codex` paths", "`private operator workspace` paths"),
        ("strategy-codex imports", "upstream workshop imports"),
    ],
    ROOT / "data/corridors/homer-to-dante.md": [
        ("Archive anchor (strategy-codex):", "Archive anchor (operator source archive):"),
        (
            "`source-archive/statecraft/2026-05-26/source-gb-12-dante-in-paradise-2026-05-26.md`",
            "gb-12 public source capture (see Part VI hybrid readiness)",
        ),
    ],
    ROOT / "book/volume-i-civilization/parts/PART-06-HYBRID-READINESS.md": [
        (
            "Source archive lives in **strategy-codex** (parent repo), not ph-civ mirror.",
            "Extended Dante source archive lives outside this public mirror until promoted.",
        ),
    ],
    ROOT / "book/volume-v/gb-11/README.md": [
        (
            "Promoted from strategy-codex source archive 2026-06-09.",
            "Promoted from operator source archive 2026-06-09.",
        ),
    ],
    ROOT / "book/volume-v/gb-11/gb-11-transcript.md": [
        (
            "promoted_from: strategy-continuity/source-archive/statecraft/2026-05-26/source-gb-11-dantes-revolution-2026-05-26.md",
            "promoted_from: operator-source-archive/statecraft/2026-05-26/source-gb-11-dantes-revolution-2026-05-26.md",
        ),
        (
            "promoted from strategy-codex source archive",
            "promoted from operator source archive",
        ),
    ],
    ROOT / "docs/jiang-classroom-rhetoric.md": [
        (
            "- the raw [gb-12 Dante capture](/C:/dev/strategy-continuity/source-archive/statecraft/2026-05-26/source-gb-12-dante-in-paradise-2026-05-26.md)",
            "- [gb-12-transcript.md](../book/volume-v/gb-12/gb-12-transcript.md)",
        ),
    ],
    ROOT / "docs/jiang-analysis-index.md": [
        (
            "- [Strategy-Codex Bridge](strategy-codex-bridge.md)  \n"
            "  The boundary between the public mirror and live strategy-codex work.",
            "- [Operator workspace bridge](strategy-codex-bridge.md)  \n"
            "  The boundary between the public mirror and live operator workspace work.",
        ),
    ],
}

def remove_civ_state_bridge_sections() -> int:
    bridge_re = re.compile(r"\n## CIV-STATE Bridge\n.*?(?=\n## |\Z)", re.DOTALL)
    count = 0
    for path in ROOT.glob("book/**/README.md"):
        text = path.read_text(encoding="utf-8")
        if "## CIV-STATE Bridge" not in text:
            continue
        new = bridge_re.sub("\n", text, count=1)
        if new != text:
            path.write_text(new.rstrip() + "\n", encoding="utf-8")
            count += 1
    return count

def add_missing_llm_prompts() -> int:
    marker = "Paste this folder link into ChatGPT, Claude, or Grok"
    cards_path = ROOT / "data" / "cards.jsonl"
    cards = [
        json.loads(line)
        for line in cards_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    count = 0
    for card in cards:
        transcript_path = card["source_paths"]["source_chapter_path"]
        commentary_path = card["source_paths"]["commentary_path"]
        folder = "/".join(transcript_path.split("/")[:-1])
        source_id = card["source_id"]
        if not folder.endswith(f"/{source_id}") or not commentary_path.startswith(f"{folder}/"):
            continue
        readme = ROOT / folder / "README.md"
        if not readme.exists():
            continue
        text = readme.read_text(encoding="utf-8")
        if marker in text:
            continue
        if "## Guardrails" in text:
            text = text.replace("## Guardrails", LLM_BLOCK + "\n## Guardrails", 1)
        else:
            text = text.rstrip() + LLM_BLOCK + "\n"
        readme.write_text(text, encoding="utf-8")
        count += 1
    return count

def apply_text_replacements() -> int:
    count = 0
    for path, pairs in REPLACEMENTS.items():
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in pairs:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            count += 1
    return count

def main() -> int:
    bridge = remove_civ_state_bridge_sections()
    prompts = add_missing_llm_prompts()
    docs = apply_text_replacements()
    print(f"bridge_sections_removed={bridge}")
    print(f"llm_prompts_added={prompts}")
    print(f"doc_files_patched={docs}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
