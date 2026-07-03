#!/usr/bin/env python3
"""
Render human-readable markdown from control-plane YAML.

Usage:
  python scripts/work_dev/render_control_plane_docs.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CONTROL_PLANE = REPO_ROOT / "docs" / "skill-work" / "work-dev" / "control-plane"
OUT_DIR = REPO_ROOT / "docs" / "skill-work" / "work-dev" / "generated"

BANNER = (
    "<!-- GENERATED FILE — do not edit by hand. "
    "Source: docs/archive/skill-work-legacy/work-dev/control-plane/*.yaml — "
    "run: python scripts/work_dev/render_control_plane_docs.py -->\n\n"
)

def render_integration_status() -> str:
    data = yaml.safe_load((CONTROL_PLANE / "integration_status.yaml").read_text(encoding="utf-8"))
    lines = [
        BANNER,
        "# Integration status (generated)\n",
        "Status vocabulary: `implemented`, `partial`, `documented_only`, `needs_verification`, `blocked`.\n",
        "\n| id | title | surface | status |\n|---|---|---|---|\n",
    ]
    for it in sorted(data.get("items") or [], key=lambda x: str(x.get("id"))):
        lines.append(
            f"| `{it.get('id')}` | {it.get('title')} | {it.get('surface')} | `{it.get('status')}` |\n"
        )
    lines.append("\n## Details\n\n")
    for it in sorted(data.get("items") or [], key=lambda x: str(x.get("id"))):
        lines.append(f"### `{it.get('id')}`\n\n")
        lines.append(f"- **Status:** `{it.get('status')}`\n")
        sot = it.get("source_of_truth") or []
        lines.append("- **Source of truth:** " + ", ".join(f"`{p}`" for p in sot) + "\n")
        for n in it.get("notes") or []:
            lines.append(f"- {n}\n")
        lines.append("\n")
    return "".join(lines)

def render_known_gaps() -> str:
    data = yaml.safe_load((CONTROL_PLANE / "known_gaps.yaml").read_text(encoding="utf-8"))
    lines = [BANNER, "# Known gaps (generated)\n\n"]
    lines.append("| id | area | status | problem |\n|---|---|---|---|\n")
    for g in sorted(data.get("items") or [], key=lambda x: str(x.get("id"))):
        prob = (g.get("problem") or "").replace("|", "\\|")
        lines.append(f"| `{g.get('id')}` | {g.get('area')} | `{g.get('status')}` | {prob} |\n")
    return "".join(lines)

def render_target_registry() -> str:
    data = yaml.safe_load((CONTROL_PLANE / "target_registry.yaml").read_text(encoding="utf-8"))
    lines = [BANNER, "# Target registry (generated)\n\n"]
    lines.append("| id | label | status | buyer |\n|---|---|---|---|\n")
    for s in sorted(data.get("segments") or [], key=lambda x: str(x.get("id"))):
        lines.append(
            f"| `{s.get('id')}` | {s.get('label')} | `{s.get('status')}` | {s.get('buyer_role')} |\n"
        )
    return "".join(lines)

def render_proof_ledger() -> str:
    data = yaml.safe_load((CONTROL_PLANE / "proof_ledger.yaml").read_text(encoding="utf-8"))
    lines = [BANNER, "# Proof ledger (generated)\n\n"]
    lines.append("| id | context | external_use_status | summary |\n|---|---|---|---|\n")
    for e in sorted(data.get("entries") or [], key=lambda x: str(x.get("id"))):
        summ = (e.get("summary") or "").replace("|", "\\|")
        lines.append(
            f"| `{e.get('id')}` | {e.get('context')} | `{e.get('external_use_status')}` | {summ} |\n"
        )
    return "".join(lines)

def main() -> int:
    ap = argparse.ArgumentParser(description="Render control plane markdown.")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument("--check", action="store_true", help="Verify generated markdown matches control-plane YAML")
    args = ap.parse_args()
    outputs = {
        "integration-status.generated.md": render_integration_status,
        "known-gaps.generated.md": render_known_gaps,
        "target-registry.generated.md": render_target_registry,
        "proof-ledger.generated.md": render_proof_ledger,
    }
    if args.check:
        rc = 0
        for name, render_fn in outputs.items():
            path = OUT_DIR / name
            expected = render_fn()
            if not path.is_file():
                print(f"error: missing {path.relative_to(REPO_ROOT)}", file=sys.stderr)
                rc = 1
                continue
            if path.read_text(encoding="utf-8") != expected:
                print(
                    f"error: {path.relative_to(REPO_ROOT)} is out of date; "
                    "run render_control_plane_docs.py",
                    file=sys.stderr,
                )
                rc = 1
        return rc
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, render_fn in outputs.items():
        (OUT_DIR / name).write_text(render_fn(), encoding="utf-8")
    print("render_control_plane_docs: OK -> docs/archive/skill-work-legacy/work-dev/generated/")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
