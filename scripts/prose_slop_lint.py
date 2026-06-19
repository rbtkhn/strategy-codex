#!/usr/bin/env python3
"""Template-slop lint for repo-root essays (Phase 0 prose-forge).

SSOT: docs/essay-voice.md — Template slop (SLOP-01..08; SLOP-03 deferred).

Usage:
  python3 scripts/prose_slop_lint.py essays/draft.md
  python3 scripts/prose_slop_lint.py --diff origin/main...HEAD essays/
  python3 scripts/prose_slop_lint.py --json --full essays/foo.md
  python3 scripts/prose_slop_lint.py --rules extended essays/foo.md
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOC_ANCHOR = "docs/essay-voice.md#template-slop-comparative-voice-ledes"

DENYLIST_PREFIXES = (
    "source-archive/",
    "archive/queues/review-queue/",
    "statecraft/daily/",
)

ESSAY_PREFIX = "essays/"

NAMES_VERB = re.compile(r"\b\w+\s+names\s+(?!three\b)", re.IGNORECASE)
ESSAY_META = re.compile(
    r"\bthis essay (compares|explores|discusses|examines|will examine|argues that)\b",
    re.IGNORECASE,
)
META_CONVERGE = re.compile(
    r"\bthree registers,?\s+one (refusal|constraint|spine)\b",
    re.IGNORECASE,
)
THIS_PAPER = re.compile(r"^this (paper|piece|note) ", re.IGNORECASE | re.MULTILINE)
TRI_MIND = re.compile(r"\b(tri-mind|tri-frame|roundtable)\b", re.IGNORECASE)
ROSTER_START = re.compile(r"^(Pope |Robert |Jiang |Leo |Barnes )", re.IGNORECASE)
SPINE_VERBS = re.compile(
    r"\b(scaling faster|refuses|converge|constraint|answerability)\b",
    re.IGNORECASE,
)

CLICHE_01 = re.compile(
    r"\b("
    r"delve into|rapidly evolving landscape|it is important to note|"
    r"plays a crucial role|robust framework|multifaceted"
    r")\b",
    re.IGNORECASE,
)
WRITE_01 = re.compile(
    r"(the analytic point is|ground claims|equilibrium / entropy)",
    re.IGNORECASE,
)

LEGACY_ALLOWLIST: frozenset[str] = frozenset()


@dataclass
class Finding:
    rule_id: str
    line: int
    excerpt: str
    message: str
    doc_anchor: str = DOC_ANCHOR
    severity: str = "warning"


def normalize_repo_path(path: str | Path) -> str:
    p = Path(path)
    try:
        p = p.resolve().relative_to(REPO_ROOT.resolve())
    except ValueError:
        pass
    normalized = str(p).replace("\\", "/").lstrip("./")
    return re.sub(r"/+", "/", normalized)


def is_denied_path(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in DENYLIST_PREFIXES)


def is_essay_path(path: str) -> bool:
    return path.startswith(ESSAY_PREFIX) and path.endswith(".md")


def strip_fenced_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def strip_blockquote_lines(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.lstrip().startswith(">"):
            continue
        lines.append(line)
    return "\n".join(lines)


def opening_block(text: str, max_chars: int = 1500) -> str:
    """Text before first ## heading, after title line, capped."""
    body = text
    if body.startswith("#"):
        first_nl = body.find("\n")
        if first_nl != -1:
            body = body[first_nl + 1 :]
    heading_idx = body.find("\n## ")
    if heading_idx == -1:
        chunk = body.strip()
    else:
        chunk = body[:heading_idx].strip()
    if len(chunk) > max_chars:
        chunk = chunk[:max_chars]
    return chunk


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'])", text)
    return [p.strip() for p in parts if p.strip()]


def line_number_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, max(0, offset)) + 1


def find_line_excerpt(lines: list[str], line_no: int, width: int = 120) -> str:
    if line_no < 1 or line_no > len(lines):
        return ""
    return lines[line_no - 1].strip()[:width]


def check_slop_01(opening: str, lines: list[str]) -> list[Finding]:
    matches = [
        m for m in NAMES_VERB.finditer(opening) if "name three kinds" not in m.group(0).lower()
    ]
    if len(matches) < 2:
        return []
    line_no = 1
    for i, ln in enumerate(lines, 1):
        if matches[0].group(0) in ln:
            line_no = i
            break
    return [
        Finding(
            rule_id="SLOP-01",
            line=line_no,
            excerpt=find_line_excerpt(lines, line_no),
            message=f'Mechanical "names" triad: {len(matches)} occurrences in opening block.',
        )
    ]


def check_slop_02(opening: str, lines: list[str]) -> list[Finding]:
    stripped = strip_blockquote_lines(opening)
    emdash_sents = [s for s in split_sentences(stripped) if "—" in s or " -- " in s]
    if len(emdash_sents) >= 3:
        for i, ln in enumerate(lines, 1):
            if "—" in ln or " -- " in ln:
                return [
                    Finding(
                        rule_id="SLOP-02",
                        line=i,
                        excerpt=find_line_excerpt(lines, i),
                        message=f"Parallel em-dash rhythm: {len(emdash_sents)} em-dash sentences in opening.",
                    )
                ]
    return []


def check_slop_04(opening: str, lines: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    for m in ESSAY_META.finditer(opening):
        line_no = 1
        for i, ln in enumerate(lines, 1):
            if m.group(0).lower() in ln.lower():
                line_no = i
                break
        findings.append(
            Finding(
                rule_id="SLOP-04",
                line=line_no,
                excerpt=find_line_excerpt(lines, line_no),
                message='Meta signpost ("This essay compares/explores…"); show comparison in prose.',
            )
        )
    return findings


def check_slop_05(opening: str, lines: list[str]) -> list[Finding]:
    sents = split_sentences(opening)
    if not sents:
        return []
    first = sents[0]
    if not ROSTER_START.match(first):
        return []
    first_two = " ".join(sents[:2])
    if SPINE_VERBS.search(first_two):
        return []
    return [
        Finding(
            rule_id="SLOP-05",
            line=1,
            excerpt=first[:120],
            message="Roster before claim: name-led opening without spine verbs in first two sentences.",
        )
    ]


def check_slop_06(opening: str, lines: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    for m in META_CONVERGE.finditer(opening):
        line_no = 1
        for i, ln in enumerate(lines, 1):
            if m.group(0).lower() in ln.lower():
                line_no = i
                break
        findings.append(
            Finding(
                rule_id="SLOP-06",
                line=line_no,
                excerpt=find_line_excerpt(lines, line_no),
                message='Meta convergence line ("three registers, one …"); perform convergence in prose.',
            )
        )
    for m in THIS_PAPER.finditer(opening):
        line_no = line_number_for_offset(opening, m.start())
        findings.append(
            Finding(
                rule_id="SLOP-06",
                line=line_no,
                excerpt=m.group(0)[:120],
                message='Weak meta opener ("This paper/piece/note …").',
            )
        )
    return findings


def check_slop_07(full_text: str, lines: list[str]) -> list[Finding]:
    tail = full_text
    for marker in ("## Return paths", "## Legacy slug", "## Support surfaces"):
        idx = tail.find(marker)
        if idx != -1:
            tail = tail[:idx]
    prose_lines = [
        ln.strip()
        for ln in tail.splitlines()
        if ln.strip() and not ln.strip().startswith("#") and not ln.strip().startswith("- [")
    ]
    if not prose_lines:
        return []
    last = prose_lines[-1]
    if last.endswith("?"):
        line_no = len(lines)
        for i in range(len(lines), 0, -1):
            if lines[i - 1].strip() == last:
                line_no = i
                break
        return [
            Finding(
                rule_id="SLOP-07",
                line=line_no,
                excerpt=last[:120],
                message="Rhetorical question closer; use declarative Kissinger warning (essay-voice law 8).",
            )
        ]
    return []


def check_slop_08(text: str, lines: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    for m in TRI_MIND.finditer(text):
        line_no = line_number_for_offset(text, m.start())
        for i, ln in enumerate(lines, 1):
            if m.group(0).lower() in ln.lower():
                line_no = i
                break
        findings.append(
            Finding(
                rule_id="SLOP-08",
                line=line_no,
                excerpt=find_line_excerpt(lines, line_no),
                message="Tri-mind / roundtable residue; essays compare registers, not host dialogue.",
            )
        )
    return findings


def check_cliche_01(text: str, lines: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    for m in CLICHE_01.finditer(text):
        line_no = line_number_for_offset(text, m.start())
        for i, ln in enumerate(lines, 1):
            if m.group(0).lower() in ln.lower():
                line_no = i
                break
        findings.append(
            Finding(
                rule_id="CLICHÉ-01",
                line=line_no,
                excerpt=find_line_excerpt(lines, line_no),
                message=f"Generic AI-texture phrase: {m.group(0)!r}.",
                doc_anchor="docs/prose-forge.md",
            )
        )
    return findings


def check_write_01(text: str, lines: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    for m in WRITE_01.finditer(text):
        line_no = line_number_for_offset(text, m.start())
        for i, ln in enumerate(lines, 1):
            if m.group(0).lower() in ln.lower():
                line_no = i
                break
        findings.append(
            Finding(
                rule_id="WRITE-01",
                line=line_no,
                excerpt=find_line_excerpt(lines, line_no),
                message="Skill-write analyst residue in essay body.",
                doc_anchor="docs/skill-write/write-operator-preferences.md",
            )
        )
    return findings


def lint_text(
    text: str,
    *,
    opening_only: bool = True,
    full: bool = False,
    extended: bool = False,
    path: str = "",
) -> list[Finding]:
    text = strip_fenced_code(text)
    lines = text.splitlines()
    opening = opening_block(text)
    scan_body = opening if opening_only and not full else text

    findings: list[Finding] = []
    findings.extend(check_slop_01(opening, lines))
    findings.extend(check_slop_02(opening, lines))
    findings.extend(check_slop_04(opening, lines))
    findings.extend(check_slop_05(opening, lines))
    findings.extend(check_slop_06(opening, lines))
    findings.extend(check_slop_08(scan_body, lines))
    if full or not opening_only:
        findings.extend(check_slop_07(text, lines))
    if extended:
        findings.extend(check_cliche_01(text, lines))
        findings.extend(check_write_01(text, lines))
    return findings


def should_lint_essay(path: str, *, strict: bool, diff_mode: bool) -> bool:
    norm = normalize_repo_path(path)
    if diff_mode or strict:
        return True
    if norm in LEGACY_ALLOWLIST:
        return False
    return True


def lint_file(
    path: Path,
    *,
    opening_only: bool = True,
    full: bool = False,
    extended: bool = False,
    strict: bool = False,
    diff_mode: bool = False,
    diff_lines: set[int] | None = None,
) -> list[Finding]:
    norm = normalize_repo_path(path)
    if is_denied_path(norm):
        return []
    if not is_essay_path(norm) and not norm.startswith("docs/skill-write/"):
        if not extended:
            return []

    if is_essay_path(norm) and not should_lint_essay(norm, strict=strict, diff_mode=diff_mode):
        return []

    text = path.read_text(encoding="utf-8")
    findings = lint_text(
        text,
        opening_only=opening_only,
        full=full,
        extended=extended,
        path=norm,
    )
    if diff_lines is not None:
        findings = [f for f in findings if f.line in diff_lines]
    return findings


def get_diff_changed_lines(path: Path, diff_spec: str) -> set[int] | None:
    """Return 1-based line numbers changed in path for diff_spec, or None if not in diff."""
    norm = normalize_repo_path(path)
    result = subprocess.run(
        ["git", "diff", "-U0", diff_spec, "--", norm],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    changed: set[int] = set()
    current_new = 0
    for line in result.stdout.splitlines():
        if line.startswith("@@"):
            m = re.search(r"\+(\d+)", line)
            if m:
                current_new = int(m.group(1)) - 1
        elif line.startswith("+") and not line.startswith("+++"):
            current_new += 1
            changed.add(current_new)
        elif line.startswith(" ") and not line.startswith("---"):
            current_new += 1
    return changed if changed else None


def get_changed_files_from_diff(diff_spec: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", diff_spec],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git diff failed for {diff_spec!r}")
    return [normalize_repo_path(p) for p in result.stdout.splitlines() if p.strip()]


def collect_paths(args_paths: list[str]) -> list[Path]:
    paths: list[Path] = []
    for raw in args_paths:
        p = Path(raw)
        if not p.is_absolute():
            p = REPO_ROOT / p
        if p.is_dir():
            paths.extend(sorted(p.rglob("*.md")))
        elif p.is_file():
            paths.append(p)
    return paths


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="Markdown files or directories (default: essays/)")
    ap.add_argument("--diff", metavar="BASE...HEAD", help="Only lint changed lines in diff range")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--opening-only", action="store_true", default=True, help="Opening block only (default)")
    ap.add_argument("--full", action="store_true", help="Full file (includes SLOP-07 closer)")
    ap.add_argument("--strict", action="store_true", help="Lint legacy allowlist files too")
    ap.add_argument("--rules", choices=["core", "extended"], default="core", help="Rule set")
    args = ap.parse_args()

    if args.full:
        args.opening_only = False

    extended = args.rules == "extended"

    all_findings: list[dict] = []

    if args.diff:
        diff_mode = True
        try:
            changed_files = get_changed_files_from_diff(args.diff)
        except RuntimeError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        targets = [
            REPO_ROOT / f
            for f in changed_files
            if is_essay_path(f) or f.startswith("docs/skill-write/")
        ]
    else:
        diff_mode = False
        raw_paths = args.paths or ["essays/"]
        targets = [p for p in collect_paths(raw_paths) if p.suffix == ".md"]

    for path in targets:
        norm = normalize_repo_path(path.relative_to(REPO_ROOT))
        diff_lines = None
        if args.diff:
            diff_lines = get_diff_changed_lines(path, args.diff)
            if diff_lines is None:
                continue
        findings = lint_file(
            path,
            opening_only=not args.full,
            full=args.full,
            extended=extended,
            strict=args.strict,
            diff_mode=diff_mode,
            diff_lines=diff_lines,
        )
        for f in findings:
            row = asdict(f)
            row["artifact"] = norm
            all_findings.append(row)

    if args.json:
        print(json.dumps(all_findings, indent=2))
    else:
        for row in all_findings:
            print(
                f"{row['artifact']}:{row['line']}: {row['rule_id']} {row['severity']}: "
                f"{row['message']} | {row['excerpt'][:80]}"
            )
        if not all_findings:
            print("prose_slop_lint: ok (no warnings)")

    return 1 if all_findings else 0


if __name__ == "__main__":
    sys.exit(main())
