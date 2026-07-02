#!/usr/bin/env python3
"""Validate epistemic plugin enriched artifact — advisory only."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ENRICHED = REPO_ROOT / "runtime" / "artifacts" / "epistemic_enriched.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from prediction.plugins.base import MAX_PLUGIN_INFLUENCE  # noqa: E402
from prediction.run_pipeline import check_enriched_artifacts  # noqa: E402

def validate_enriched(payload: dict) -> list[str]:
    issues: list[str] = []
    if payload.get("interpretation") != "epistemic_enriched":
        issues.append("interpretation must be epistemic_enriched")

    meta = payload.get("_meta")
    if not isinstance(meta, dict):
        issues.append("missing _meta")
    else:
        cap = meta.get("plugin_influence_cap")
        if cap != MAX_PLUGIN_INFLUENCE:
            issues.append(f"_meta.plugin_influence_cap must be {MAX_PLUGIN_INFLUENCE}")
        if not isinstance(meta.get("plugins_applied"), list):
            issues.append("_meta.plugins_applied must be list")

    objects = payload.get("objects")
    if not isinstance(objects, list):
        issues.append("objects must be a list")
        return issues

    for idx, block in enumerate(objects):
        if not isinstance(block, dict):
            issues.append(f"objects[{idx}] must be object")
            continue
        for field in ("core", "plugin_results", "merged"):
            if field not in block:
                issues.append(f"objects[{idx}] missing {field}")
        core = block.get("core") if isinstance(block.get("core"), dict) else {}
        merged = block.get("merged") if isinstance(block.get("merged"), dict) else {}
        core_label = str((core.get("regime") or {}).get("label") or "")
        merged_regime = merged.get("regime") if isinstance(merged.get("regime"), dict) else {}
        if core_label and str(merged_regime.get("label") or "") != core_label:
            issues.append(f"objects[{idx}] merged regime label must match core")

    return issues

def run_check(*, enriched_path: Path | None = None, advisory: bool = False) -> int:
    target = enriched_path or DEFAULT_ENRICHED
    if not target.is_file():
        msg = f"missing {target.relative_to(REPO_ROOT)}"
        if advisory:
            print(f"WARN: {msg}", file=sys.stderr)
            return 0
        print(f"error: {msg}", file=sys.stderr)
        return 1

    payload = json.loads(target.read_text(encoding="utf-8"))
    issues = validate_enriched(payload)
    for issue in issues:
        line = f"{'WARN' if advisory else 'error'}: {issue}"
        print(line, file=sys.stderr)

    if issues and not advisory:
        return 1

    rc = check_enriched_artifacts()
    if rc != 0 and advisory:
        print("WARN: enriched artifact drift (advisory)", file=sys.stderr)
        return 0
    if rc == 0:
        print("[ok] epistemic plugin layer valid" + (" (advisory)" if advisory else ""))
    return rc

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--advisory", action="store_true", help="WARN only, exit 0")
    ap.add_argument("--path", type=Path, default=None, help="path to epistemic_enriched.json")
    args = ap.parse_args()
    return run_check(enriched_path=args.path, advisory=args.advisory)

if __name__ == "__main__":
    raise SystemExit(main())
