#!/usr/bin/env python3
"""Audit statecraft transcript corpora for non-literal Strait of Hormuz ASR errors.

WORK only; not Record.

This is a detection-only audit. It looks for files where the intended phrase is
likely ``Strait of Hormuz`` even when the transcript does not literally contain
``Hormuz`` and instead uses a generic noun or phonetic near-miss.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
WJ_DIR = REPO_ROOT / "scripts" / "work_jiang"
if str(WJ_DIR) not in sys.path:
    sys.path.insert(0, str(WJ_DIR))

from asr_transcript_replacements import COMMON_REPLACEMENTS  # noqa: E402

DEFAULT_ROOT = REPO_ROOT / "source-archive" / "statecraft"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "artifacts" / "transcript-audits"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TITLE_RE = re.compile(r'^title:\s*"?(.*?)"?\s*$', re.MULTILINE)
KIND_RE = re.compile(r"^kind:\s*([^\n]+)$", re.MULTILINE)
SOURCE_TYPE_RE = re.compile(r"^source_type:\s*([^\n]+)$", re.MULTILINE)
TRANSCRIPT_HEAD_RE = re.compile(
    r"\b(straight|strait|straits|state|street|trade)\s+of\s+([A-Za-z][A-Za-z'-]*)\b",
    re.IGNORECASE,
)
SPLIT_HEAD_RE = re.compile(
    r"\b(straight|strait|straits|state|street|trade)\s+of\s*$",
    re.IGNORECASE,
)
ALLOWLIST = {
    ("strait", "hormuz"),
    ("straits", "hormuz"),
}
FIRST_WAVE_STRONG_TOKENS = {
    "humus",
    "homus",
    "hormos",
    "hormones",
    "hormone",
    "armus",
    "armors",
    "armoose",
    "foremost",
    "formos",
    "barmuz",
    "ormuz",
    "ormus",
    "harmuz",
    "ormuz",
    "ormos",
    "ormuz.",
    "ormuz,",
}
TRANSCRIPT_PREFIXES = (
    "transcript-",
    "youtube-",
    "judging-freedom-",
    "responsiblestatecraft-",
    "substack-",
)
CONTEXT_CUES = (
    "iran",
    "persian gulf",
    "gulf of oman",
    "tanker",
    "shipping",
    "oil",
    "lng",
    "blockade",
    "open",
    "close",
    "traffic",
    "waterway",
)


@dataclass(frozen=True)
class Finding:
    path: str
    tier: str
    match_text: str
    suspected_target: str
    reason_code: str
    line_number: int | None
    snippet: str


def rel_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _normalize_token(token: str) -> str:
    return token.strip(".,:;!?)]}\"'").casefold()


def _normalize_head(head: str) -> str:
    return head.casefold()


def load_hormuz_seed_patterns() -> set[str]:
    seeds: set[str] = set()
    for bad, good in COMMON_REPLACEMENTS:
        if "Strait of Hormuz" not in good:
            continue
        seeds.add(bad)
        match = re.search(r"\b(?:strait|straight|straits|state|street|trade)\s+of\s+([A-Za-z][A-Za-z'-]*)\b", bad, re.I)
        if match:
            seeds.add(match.group(1))
    return seeds


SEED_PATTERNS = load_hormuz_seed_patterns()
KNOWN_BAD_TOKENS = {
    _normalize_token(token)
    for token in SEED_PATTERNS
    if " " not in token
}.union(FIRST_WAVE_STRONG_TOKENS)
WEAK_BAD_TOKENS = {"hormis", "hormas", "hormone"}


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    raw = match.group(1)
    meta: dict[str, str] = {}
    title = TITLE_RE.search(raw)
    kind = KIND_RE.search(raw)
    source_type = SOURCE_TYPE_RE.search(raw)
    if title:
        meta["title"] = title.group(1).strip().strip('"')
    if kind:
        meta["kind"] = kind.group(1).strip().strip('"')
    if source_type:
        meta["source_type"] = source_type.group(1).strip().strip('"')
    return meta


def strip_frontmatter(text: str) -> str:
    match = FRONTMATTER_RE.match(text)
    return text[match.end() :] if match else text


def is_transcript_like(path: Path, text: str, meta: dict[str, str]) -> bool:
    if path.name == "README.md":
        return False
    kind = meta.get("kind", "").casefold()
    if "transcript" in kind:
        return True
    if meta.get("source_type"):
        return True
    if path.name.startswith(TRANSCRIPT_PREFIXES):
        return True
    lowered = strip_frontmatter(text).lower()
    if "not human-verified verbatim" in lowered:
        return True
    return False


def context_score(text: str) -> int:
    lowered = text.casefold()
    return sum(1 for cue in CONTEXT_CUES if cue in lowered)


def _make_snippet(lines: list[str], line_no: int) -> str:
    start = max(0, line_no - 2)
    end = min(len(lines), line_no + 1)
    snippet = " ⏎ ".join(line.strip() for line in lines[start:end] if line.strip())
    return snippet[:240]


def classify_direct_match(head: str, token: str, local_text: str, *, split_line: bool) -> tuple[str, str]:
    norm_head = _normalize_head(head)
    norm_token = _normalize_token(token)
    if split_line:
        return "high_confidence", "split_line_variant"
    if norm_token in WEAK_BAD_TOKENS:
        return "medium_confidence", "phonetic_variant"
    if norm_head in {"trade", "state", "street"}:
        return "high_confidence", "generic_noun_flattening"
    if norm_token in {"humus", "homus", "hormones", "hormone"}:
        return "high_confidence", "generic_noun_flattening"
    return "high_confidence", "phonetic_variant"


def find_direct_findings(path: Path, body: str) -> list[Finding]:
    lines = body.replace("\r", "").splitlines()
    findings: list[Finding] = []
    for idx, line in enumerate(lines):
        for match in TRANSCRIPT_HEAD_RE.finditer(line):
            head, token = match.group(1), match.group(2)
            norm_head = _normalize_head(head)
            norm_token = _normalize_token(token)
            if (norm_head, norm_token) in ALLOWLIST:
                continue
            if norm_token not in KNOWN_BAD_TOKENS:
                continue
            snippet = _make_snippet(lines, idx)
            tier, reason_code = classify_direct_match(head, token, snippet, split_line=False)
            findings.append(
                Finding(
                    path=rel_path(path),
                    tier=tier,
                    match_text=match.group(0),
                    suspected_target="Strait of Hormuz",
                    reason_code=reason_code,
                    line_number=idx + 1,
                    snippet=snippet,
                )
            )

        split_match = SPLIT_HEAD_RE.search(line)
        if not split_match or idx + 1 >= len(lines):
            continue
        next_line = lines[idx + 1].strip()
        if not next_line:
            continue
        token_match = re.match(r"^([A-Za-z][A-Za-z'-]*)\b", next_line)
        if not token_match:
            continue
        token = token_match.group(1)
        norm_token = _normalize_token(token)
        if norm_token not in KNOWN_BAD_TOKENS:
            continue
        snippet = _make_snippet(lines, idx)
        tier, reason_code = classify_direct_match(split_match.group(1), token, snippet, split_line=True)
        findings.append(
            Finding(
                path=rel_path(path),
                tier=tier,
                match_text=f"{split_match.group(1)} of / {token}",
                suspected_target="Strait of Hormuz",
                reason_code=reason_code,
                line_number=idx + 1,
                snippet=snippet,
            )
        )
    return findings


def find_context_only_finding(path: Path, text: str, meta: dict[str, str]) -> Finding | None:
    title = meta.get("title", "")
    titleish = f"{path.as_posix()} {title}".casefold()
    if "hormuz" not in titleish:
        return None
    body = strip_frontmatter(text)
    body_without_heading = re.sub(r"^\s*#.*(?:\n|$)", "", body, count=1)
    if "hormuz" in body_without_heading.casefold():
        return None
    score = context_score(body_without_heading)
    if score < 2:
        return None
    return Finding(
        path=rel_path(path),
        tier="context_only",
        match_text="",
        suspected_target="Strait of Hormuz",
        reason_code="title_body_divergence",
        line_number=None,
        snippet="Context-only review candidate: title/path references Hormuz but no direct malformed phrase matched.",
    )


def audit_path(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8", errors="replace")
    meta = parse_frontmatter(text)
    if not is_transcript_like(path, text, meta):
        return []
    body = strip_frontmatter(text)
    findings = find_direct_findings(path, body)
    if findings:
        return findings
    context_only = find_context_only_finding(path, text, meta)
    return [context_only] if context_only else []


def iter_transcript_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*.md")):
        files.append(path)
    return files


def build_summary(findings: list[Finding]) -> dict[str, Any]:
    variant_counts = Counter()
    tier_counts = Counter()
    file_counts = Counter()
    date_counts = Counter()
    review_needed: list[dict[str, Any]] = []
    for finding in findings:
        tier_counts[finding.tier] += 1
        file_counts[finding.path] += 1
        if finding.match_text:
            variant_counts[finding.match_text.casefold()] += 1
        parts = finding.path.split("/")
        if len(parts) >= 3 and re.fullmatch(r"\d{4}-\d{2}-\d{2}", parts[2]):
            date_counts[parts[2]] += 1
        if finding.tier != "high_confidence":
            review_needed.append(asdict(finding))
    highest_density = [
        {"path": path, "findings": count}
        for path, count in file_counts.most_common(15)
    ]
    by_date = [
        {"date": date, "findings": count}
        for date, count in date_counts.most_common(20)
    ]
    return {
        "total_findings": len(findings),
        "candidate_files": len(file_counts),
        "tier_counts": dict(tier_counts),
        "variant_family_counts": dict(variant_counts.most_common()),
        "highest_density_files": highest_density,
        "findings_by_date": by_date,
        "review_needed": review_needed[:50],
        "next_correction_candidates": [
            "straight of hormones -> Strait of Hormuz",
            "straight of Hormos -> Strait of Hormuz",
        "straight of Homus -> Strait of Hormuz",
        "trade of hormones -> Strait of Hormuz",
        "state/street of Ormuz -> Strait of Hormuz",
        "state of armus -> Strait of Hormuz",
        "street of armors -> Strait of Hormuz",
        "straight of Armoose -> Strait of Hormuz",
        "straight/trade of formos -> Strait of Hormuz",
        "straight of foremost -> Strait of Hormuz",
    ],
}


def render_report(root: Path, findings: list[Finding], summary: dict[str, Any]) -> str:
    lines = [
        "# Hormuz Mistranscription Audit",
        "",
        "WORK only; not Record.",
        "",
        f"- root: `{root.relative_to(REPO_ROOT).as_posix()}`",
        f"- total candidate files: `{summary['candidate_files']}`",
        f"- total findings: `{summary['total_findings']}`",
        "",
        "## Tier Counts",
        "",
    ]
    for tier, count in summary["tier_counts"].items():
        lines.append(f"- `{tier}`: `{count}`")
    lines.extend(["", "## Variant Family Counts", ""])
    for match_text, count in list(summary["variant_family_counts"].items())[:20]:
        lines.append(f"- `{match_text}`: `{count}`")
    lines.extend(["", "## Highest-Density Files", ""])
    for row in summary["highest_density_files"]:
        lines.append(f"- `{row['findings']}` - `{row['path']}`")
    lines.extend(["", "## Review-Needed Cases", ""])
    review_needed = summary["review_needed"] or []
    if not review_needed:
        lines.append("- none")
    else:
        for row in review_needed[:20]:
            lines.append(
                f"- `{row['tier']}` `{row['path']}`"
                + (f" line `{row['line_number']}`" if row["line_number"] else "")
                + f" - `{row['reason_code']}`"
            )
    lines.extend(["", "## File-Level Findings", ""])
    grouped: dict[str, list[Finding]] = defaultdict(list)
    for finding in findings:
        grouped[finding.path].append(finding)
    for path, rows in sorted(grouped.items()):
        lines.append(f"### `{path}`")
        for row in rows:
            prefix = f"- `{row.tier}`"
            if row.line_number:
                prefix += f" line `{row.line_number}`"
            detail = row.match_text or "context-only review candidate"
            lines.append(f"{prefix} - `{detail}` - `{row.reason_code}`")
            lines.append(f"  snippet: {row.snippet}")
        lines.append("")
    lines.extend(["## Next Correction Candidates", ""])
    for rule in summary["next_correction_candidates"]:
        lines.append(f"- `{rule}`")
    return "\n".join(lines).rstrip() + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Transcript root to audit.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory for audit artifacts.")
    parser.add_argument(
        "--prefix",
        default="statecraft-hormuz-mistranscriptions",
        help="Filename prefix for emitted JSON and Markdown artifacts.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    files = iter_transcript_files(root)
    findings: list[Finding] = []
    for path in files:
        findings.extend(audit_path(path))
    summary = build_summary(findings)
    payload = {
        "root": root.relative_to(REPO_ROOT).as_posix(),
        "seed_patterns": sorted(SEED_PATTERNS),
        "findings": [asdict(finding) for finding in findings],
        "summary": summary,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / f"{args.prefix}.json"
    md_path = args.output_dir / f"{args.prefix}.md"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_report(root, findings, summary), encoding="utf-8")
    print(
        json.dumps(
            {
                "json": json_path.relative_to(REPO_ROOT).as_posix(),
                "markdown": md_path.relative_to(REPO_ROOT).as_posix(),
                "total_findings": len(findings),
                "candidate_files": summary["candidate_files"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
