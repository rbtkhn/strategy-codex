#!/usr/bin/env python3
"""Prose Forge — governed prose quality pass for strategy-codex.

Wraps prose_slop_lint (Phase 0) and optional Vale (Phase 1).
Class router (Phase 2) selects rule packs by artifact path.
Rewrite/compare/gate (Phase 3) stage candidates under runtime/artifacts/prose-forge/.

SSOT voice: docs/essay-voice.md, docs/skill-write/write-operator-preferences.md
Surface contract: docs/prose-forge.md

Usage:
  python3 scripts/prose_forge.py lint essays/draft.md
  python3 scripts/prose_forge.py lint --diff origin/main...HEAD essays/
  python3 scripts/prose_forge.py rewrite essays/draft.md --mode essay
  python3 scripts/prose_forge.py compare essays/draft.md runtime/artifacts/prose-forge/draft/candidate.md
  python3 scripts/prose_forge.py gate runtime/artifacts/prose-forge/draft/candidate.md
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from repo_io import ARTIFACTS_DIR

import prose_slop_lint  # noqa: E402

DENYLIST_PREFIXES = prose_slop_lint.DENYLIST_PREFIXES
ARTIFACTS_ROOT = ARTIFACTS_DIR / "prose-forge"
TEMPLATES_ROOT = REPO_ROOT / "templates" / "prose-forge"

@dataclass
class ProseClass:
    name: str
    vale_styles: list[str]
    slop_extended: bool

PROSE_CLASSES: dict[str, ProseClass] = {
    "essay": ProseClass("essay", ["StrategyCodex.EssaySlop", "StrategyCodex.AITexture"], False),
    "skill-write": ProseClass("skill-write", ["StrategyCodex.SkillWriteResidue", "StrategyCodex.AITexture"], True),
    "note": ProseClass("note", ["StrategyCodex.AITexture"], False),
    "doctrine": ProseClass("doctrine", ["StrategyCodex.AITexture"], False),
    "denied": ProseClass("denied", [], False),
}

def infer_prose_class(path: str) -> ProseClass:
    norm = prose_slop_lint.normalize_repo_path(path)
    if any(norm.startswith(p) for p in DENYLIST_PREFIXES):
        return PROSE_CLASSES["denied"]
    if norm.startswith("essays/"):
        return PROSE_CLASSES["essay"]
    if norm.startswith("docs/skill-write/"):
        return PROSE_CLASSES["skill-write"]
    if "/notes/" in norm:
        return PROSE_CLASSES["note"]
    if norm.startswith("docs/"):
        return PROSE_CLASSES["doctrine"]
    return PROSE_CLASSES["doctrine"]

def run_vale(paths: list[Path]) -> tuple[int, list[dict]]:
    vale = shutil.which("vale")
    if not vale:
        return 0, [{"rule_id": "VALE-SKIP", "message": "vale not installed; skipping", "severity": "info"}]

    cmd = [vale, "--output=JSON", *(str(p) for p in paths)]
    result = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    findings: list[dict] = []
    if result.stdout.strip():
        try:
            raw = json.loads(result.stdout)
            for item in raw if isinstance(raw, list) else []:
                findings.append(
                    {
                        "rule_id": f"VALE-{item.get('Check', 'unknown')}",
                        "line": item.get("Line", 0),
                        "message": item.get("Message", ""),
                        "severity": item.get("Severity", "warning"),
                        "artifact": item.get("Path", ""),
                    }
                )
        except json.JSONDecodeError:
            findings.append({"rule_id": "VALE-ERR", "message": result.stdout[:200], "severity": "error"})
    return result.returncode, findings

def cmd_lint(args: argparse.Namespace) -> int:
    if args.paths:
        paths = prose_slop_lint.collect_paths(args.paths)
    elif args.diff:
        changed = prose_slop_lint.get_changed_files_from_diff(args.diff)
        paths = [REPO_ROOT / f for f in changed if f.endswith(".md")]
    else:
        paths = list((REPO_ROOT / "essays").rglob("*.md"))

    paths = [p for p in paths if infer_prose_class(str(p)).name != "denied"]

    slop_cmd = [sys.executable, str(REPO_ROOT / "scripts" / "prose_slop_lint.py")]
    if args.diff:
        slop_cmd.extend(["--diff", args.diff])
    else:
        slop_cmd.extend(str(p.relative_to(REPO_ROOT)) for p in paths)
    if args.json:
        slop_cmd.append("--json")
    if args.full:
        slop_cmd.append("--full")
    if args.strict:
        slop_cmd.append("--strict")
    if args.rules == "extended":
        slop_cmd.extend(["--rules", "extended"])

    slop_result = subprocess.run(slop_cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, check=False)
    if args.json and slop_result.stdout.strip():
        try:
            slop_findings = json.loads(slop_result.stdout)
        except json.JSONDecodeError:
            slop_findings = []
    elif slop_result.stdout.strip() and slop_result.stdout.startswith("["):
        slop_findings = json.loads(slop_result.stdout)
    else:
        slop_findings = []

    if not args.no_vale:
        by_class: dict[str, list[Path]] = {}
        for p in paths:
            cls = infer_prose_class(str(p.relative_to(REPO_ROOT)))
            by_class.setdefault(cls.name, []).append(p)
        vale_findings: list[dict] = []
        for cls_name, cls_paths in by_class.items():
            _, vf = run_vale(cls_paths)
            vale_findings.extend(vf)
    else:
        vale_findings = []

    report = {
        "findings": slop_findings if isinstance(slop_findings, list) else [],
        "vale": vale_findings,
    }
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        if slop_result.stdout.strip():
            print(slop_result.stdout, end="" if slop_result.stdout.endswith("\n") else "\n")
        for row in vale_findings:
                if row.get("rule_id") != "VALE-SKIP":
                    print(f"vale: {row.get('rule_id')}: {row.get('message')}")
        if not slop_findings and all(r.get("rule_id") == "VALE-SKIP" for r in vale_findings):
            print("prose_forge lint: ok")

    has_warnings = bool(slop_findings) or any(
        r.get("severity") not in ("info",) for r in vale_findings if r.get("rule_id") != "VALE-SKIP"
    )
    return 1 if has_warnings else 0

def slug_from_path(path: Path) -> str:
    return re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")

def cmd_rewrite(args: argparse.Namespace) -> int:
    source = Path(args.path)
    if not source.is_absolute():
        source = REPO_ROOT / source
    norm = prose_slop_lint.normalize_repo_path(source)
    if infer_prose_class(norm).name == "denied":
        print(f"error: denied path {norm}", file=sys.stderr)
        return 2

    out_dir = ARTIFACTS_ROOT / slug_from_path(source)
    out_dir.mkdir(parents=True, exist_ok=True)

    candidate = out_dir / "candidate.md"
    report = out_dir / "prose-forge.report.json"
    review = out_dir / "review-note.md"
    prompt_tpl = TEMPLATES_ROOT / "rewrite-prompt.md"

    body = source.read_text(encoding="utf-8")
    candidate.write_text(body, encoding="utf-8")

    lint_before = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "prose_slop_lint.py"), "--json", str(source.relative_to(REPO_ROOT))],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    lint_json = json.loads(lint_before.stdout) if lint_before.stdout.strip().startswith("[") else []

    report.write_text(
        json.dumps(
            {
                "source": norm,
                "mode": args.mode,
                "class": infer_prose_class(norm).name,
                "staged": str(candidate.relative_to(REPO_ROOT)).replace("\\", "/"),
                "lint_before": lint_json,
                "llm_rewrite": "not_run",
                "note": "Candidate is a copy of source. Run external LLM with templates/prose-forge/rewrite-prompt.md; lint after edit.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    review.write_text(
        f"# Prose Forge review — {source.name}\n\n"
        f"**Date:** {date.today().isoformat()}\n"
        f"**Source:** `{norm}`\n"
        f"**Candidate:** `{candidate.relative_to(REPO_ROOT).as_posix()}`\n"
        f"**Mode:** {args.mode}\n\n"
        "## Checklist\n\n"
        "- [ ] Lint clean: `python3 scripts/prose_forge.py lint {candidate.relative_to(REPO_ROOT).as_posix()}`\n"
        "- [ ] Voice SSOT: docs/essay-voice.md (essays) or skill-write (public)\n"
        "- [ ] Operator promotes manually — no auto-merge\n",
        encoding="utf-8",
    )

    if prompt_tpl.is_file():
        print(f"Staged: {candidate.relative_to(REPO_ROOT)}")
        print(f"Report: {report.relative_to(REPO_ROOT)}")
        print(f"Prompt template: {prompt_tpl.relative_to(REPO_ROOT)}")
    else:
        print(f"Staged: {candidate.relative_to(REPO_ROOT)}")
    return 0

def cmd_compare(args: argparse.Namespace) -> int:
    left = Path(args.left)
    right = Path(args.right)
    if not left.is_absolute():
        left = REPO_ROOT / left
    if not right.is_absolute():
        right = REPO_ROOT / right
    result = subprocess.run(
        ["git", "diff", "--no-index", str(left), str(right)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    print(result.stdout or result.stderr)
    return 0 if result.returncode in (0, 1) else result.returncode

def cmd_gate(args: argparse.Namespace) -> int:
    candidate = Path(args.path)
    if not candidate.is_absolute():
        candidate = REPO_ROOT / candidate
    review = candidate.parent / "review-note.md"
    if not review.is_file():
        print(f"error: missing {review}", file=sys.stderr)
        return 2
    print(review.read_text(encoding="utf-8"))
    print("\n---\nGate: operator review only. No auto-merge.")
    return 0

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)

    lint = sub.add_parser("lint", help="Deterministic slop lint + optional Vale")
    lint.add_argument("paths", nargs="*", help="Files or dirs (default essays/)")
    lint.add_argument("--diff", metavar="BASE...HEAD")
    lint.add_argument("--json", action="store_true")
    lint.add_argument("--full", action="store_true")
    lint.add_argument("--strict", action="store_true")
    lint.add_argument("--rules", choices=["core", "extended"], default="core")
    lint.add_argument("--no-vale", action="store_true", help="Skip Vale even if installed")
    lint.set_defaults(func=cmd_lint)

    rewrite = sub.add_parser("rewrite", help="Stage rewrite candidate (no LLM call)")
    rewrite.add_argument("path")
    rewrite.add_argument("--mode", default="essay", choices=["essay", "skill-write", "note"])
    rewrite.set_defaults(func=cmd_rewrite)

    compare = sub.add_parser("compare", help="Diff source vs candidate")
    compare.add_argument("left")
    compare.add_argument("right")
    compare.set_defaults(func=cmd_compare)

    gate = sub.add_parser("gate", help="Print review note for staged candidate")
    gate.add_argument("path")
    gate.set_defaults(func=cmd_gate)

    args = ap.parse_args()
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())
