"""Shared link graph, broken-link spec, registry rows, and dashboard for statecraft notes."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES_ROOT = REPO_ROOT / "statecraft" / "notes"

LINK_RE = re.compile(r"\]\(([^)]+)\)")
ARCHIVE_PATH_RE = re.compile(r"source-archive/statecraft/[^\s)\]`\"']+")
SYNTHESIS_PATH_RE = re.compile(r"statecraft/synthesis/[^\s)\]`\"']+")

TIER_B_SUBFOLDERS = frozenset({"wire", "watch", "reentry", "intake"})
AUTHORITY_LEVELS = frozenset({"draft", "review-needed", "shelf-native", "deprecated"})


def resolve_link(from_path: Path, target: str) -> Path | None:
    t = target.strip().split("#")[0].strip()
    if not t or t.startswith("#") or "://" in t:
        return None
    candidate = (from_path.parent / t).resolve()
    try:
        candidate.relative_to(REPO_ROOT.resolve())
    except ValueError:
        return None
    return candidate


def archive_paths_in_text(text: str) -> list[str]:
    found: list[str] = []
    for match in ARCHIVE_PATH_RE.findall(text):
        normalized = match.replace("\\", "/").rstrip(").,")
        if normalized not in found:
            found.append(normalized)
    return found


def synthesis_paths_in_text(text: str) -> list[str]:
    return list(dict.fromkeys(SYNTHESIS_PATH_RE.findall(text.replace("\\", "/"))))


def resolved_archive_anchors(meta: Any, text: str) -> list[str]:
    anchors = list(getattr(meta, "archive_links", []) or []) + list(getattr(meta, "nodes", []) or [])
    for item in archive_paths_in_text(text):
        if item not in anchors:
            anchors.append(item)
    resolved: list[str] = []
    for item in anchors:
        p = REPO_ROOT / item.replace("\\", "/")
        if p.exists():
            resolved.append(item.replace("\\", "/"))
    return resolved


def build_inbound_note_links(
    paths: list[Path],
    *,
    classify_tier: Callable[[Path], str],
) -> dict[str, int]:
    note_rels = {p.relative_to(REPO_ROOT).as_posix() for p in paths if classify_tier(p) == "A"}
    inbound: dict[str, int] = {rel: 0 for rel in note_rels}
    for path in paths:
        if classify_tier(path) != "A":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        from_rel = path.relative_to(REPO_ROOT).as_posix()
        for raw in LINK_RE.findall(text):
            resolved = resolve_link(path, raw)
            if not resolved or not resolved.is_file():
                continue
            target_rel = resolved.relative_to(REPO_ROOT).as_posix()
            if target_rel in inbound and target_rel != from_rel:
                inbound[target_rel] += 1
    return inbound


def count_outbound_note_links(from_path: Path, text: str, tier_a_rels: set[str]) -> int:
    from_rel = from_path.relative_to(REPO_ROOT).as_posix()
    count = 0
    for raw in LINK_RE.findall(text):
        resolved = resolve_link(from_path, raw)
        if not resolved or not resolved.is_file():
            continue
        target_rel = resolved.relative_to(REPO_ROOT).as_posix()
        if target_rel in tier_a_rels and target_rel != from_rel:
            count += 1
    return count


def _path_under_notes(path: Path) -> bool:
    try:
        path.resolve().relative_to(NOTES_ROOT.resolve())
        return True
    except ValueError:
        return False


def count_broken_note_links(from_path: Path, text: str) -> tuple[int, list[str]]:
    """Return (count, broken targets) per broken-link spec."""
    broken: list[str] = []
    notes_root = NOTES_ROOT.resolve()

    for raw in LINK_RE.findall(text):
        t = raw.strip()
        if not t or t.startswith("#") or "://" in t:
            continue
        target = t.split("#")[0].strip()
        if not target:
            continue

        lower = target.lower()
        is_md_target = lower.endswith(".md")
        is_relative = target.startswith("./") or target.startswith("../") or (
            not target.startswith("/") and not target.startswith("#")
        )

        resolved = resolve_link(from_path, target)

        if is_md_target:
            if resolved is None or not resolved.is_file():
                broken.append(raw)
            continue

        if not is_relative:
            continue

        check = resolved
        if check is None and not lower.endswith(".md"):
            check = resolve_link(from_path, target + ".md")

        if check is not None and check.is_file():
            continue

        candidates: list[Path] = []
        if check is not None:
            candidates.append(check)
        else:
            base = (from_path.parent / target).resolve()
            candidates.append(base)
            if not lower.endswith(".md"):
                candidates.append((from_path.parent / (target + ".md")).resolve())

        for cand in candidates:
            if _path_under_notes(cand) and not cand.is_file():
                broken.append(raw)
                break

    return len(broken), broken


def apply_dates(meta: Any, merged: dict[str, Any]) -> None:
    for key in ("created_at", "updated_at"):
        val = merged.get(key)
        if val is not None and str(val).strip():
            setattr(meta, key, str(val).strip())


def collect_warning_tags(
    meta: Any,
    text: str,
    *,
    inbound_count: int,
    validate_issues: list[str],
    tier: str,
) -> list[str]:
    tags: list[str] = []
    rel = getattr(meta, "rel", "")

    if tier == "B":
        if validate_issues:
            tags.append("missing_contract")
        return tags

    if any("missing note_type" in i or "missing source_basis" in i or "missing authority_level" in i for i in validate_issues):
        tags.append("missing_contract")
    if any("prefix implies" in i for i in validate_issues):
        tags.append("prefix_mismatch")
    if any("archive anchor" in i or "synthesis link" in i or "requires archive" in i for i in validate_issues):
        tags.append("weak_anchor")
    if any("essay_candidate requires" in i for i in validate_issues):
        tags.append("essay_underproof")
    if any("orphan shelf-native" in i for i in validate_issues):
        tags.append("orphan")

    broken_count, _ = count_broken_note_links(meta.path, text)
    if broken_count:
        tags.append("broken_links")

    authority = getattr(meta, "authority_level", None) or ""
    if authority == "review-needed":
        tags.append("stale_review")

    out_links = [raw for raw in LINK_RE.findall(text) if resolve_link(meta.path, raw) is not None]
    if (
        authority == "shelf-native"
        and inbound_count == 0
        and not out_links
        and "orphan" not in tags
    ):
        tags.append("orphan")

    if not tags and validate_issues:
        for issue in validate_issues:
            if issue.startswith(rel):
                tags.append("missing_contract")
                break

    return sorted(set(tags))


@dataclass
class RegistryRow:
    tier: str
    path: str
    title: str
    note_type: str
    authority_level: str
    source_basis: str
    archive_anchor_count: int
    inbound_links: int
    outbound_links: int
    broken_links: int
    essay_candidate: bool
    updated_at: str
    warnings: list[str] = field(default_factory=list)
    subfolder: str = ""

    def to_json_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["essay_candidate"] = self.essay_candidate
        return d


def tier_b_subfolder(rel: str) -> str:
    parts = rel.split("/")
    if len(parts) >= 3 and parts[0] == "statecraft" and parts[1] == "notes":
        sub = parts[2]
        if sub in TIER_B_SUBFOLDERS:
            return sub
    return ""


def build_registry_row(
    meta: Any,
    text: str,
    *,
    inbound_count: int,
    tier_a_rels: set[str],
    validate_issues: list[str],
    orphan_issue: str | None = None,
) -> RegistryRow:
    issues = list(validate_issues)
    if orphan_issue:
        issues.append(orphan_issue)

    archives = resolved_archive_anchors(meta, text)
    broken_count, _ = count_broken_note_links(meta.path, text)
    warnings = collect_warning_tags(
        meta,
        text,
        inbound_count=inbound_count,
        validate_issues=issues,
        tier=meta.tier,
    )

    return RegistryRow(
        tier=meta.tier,
        path=meta.rel,
        title=meta.path.stem,
        note_type=meta.note_type or "",
        authority_level=meta.authority_level or "",
        source_basis=meta.source_basis or "",
        archive_anchor_count=len(set(archives)),
        inbound_links=inbound_count,
        outbound_links=count_outbound_note_links(meta.path, text, tier_a_rels),
        broken_links=broken_count,
        essay_candidate=bool(meta.essay_candidate),
        updated_at=getattr(meta, "updated_at", None) or "",
        warnings=warnings,
        subfolder=tier_b_subfolder(meta.rel) if meta.tier == "B" else "",
    )


def build_dashboard(rows: list[RegistryRow]) -> dict[str, Any]:
    tier_a = [r for r in rows if r.tier == "A"]
    tier_b = [r for r in rows if r.tier == "B"]

    authority_counts = {level: 0 for level in sorted(AUTHORITY_LEVELS)}
    for row in tier_a:
        if row.authority_level in authority_counts:
            authority_counts[row.authority_level] += 1

    essay_candidates = [r for r in tier_a if r.essay_candidate]
    orphans = [r for r in tier_a if "orphan" in r.warnings]
    weak_anchor = [r for r in tier_a if "weak_anchor" in r.warnings]
    stale_review = [r for r in tier_a if "stale_review" in r.warnings]
    contract_violations = [r for r in tier_a if r.warnings]
    broken_total = sum(r.broken_links for r in tier_a)

    tier_b_counts = {sub: 0 for sub in sorted(TIER_B_SUBFOLDERS)}
    for row in tier_b:
        if row.subfolder in tier_b_counts:
            tier_b_counts[row.subfolder] += 1
    tier_b_gaps = sum(1 for r in tier_b if "missing_contract" in r.warnings)

    essay_paths = {r.path for r in tier_a if r.essay_candidate}
    return {
        "tier_a": {
            "total": len(tier_a),
            "authority": authority_counts,
            "essay_candidates": len(essay_candidates),
            "orphan_shelf_native": len(orphans),
            "missing_anchors": len(weak_anchor),
            "broken_internal_note_links": broken_total,
            "stale_review_needed": len(stale_review),
            "contract_warnings": len(contract_violations),
        },
        "tier_b_summary": {
            "total": len(tier_b),
            "wire": tier_b_counts["wire"],
            "watch": tier_b_counts["watch"],
            "reentry": tier_b_counts["reentry"],
            "intake": tier_b_counts["intake"],
            "contract_gaps": tier_b_gaps,
        },
        "essay_queue": [
            {"path": r.path, "title": r.title, "archive_anchor_count": r.archive_anchor_count, "inbound_links": r.inbound_links}
            for r in sorted(essay_candidates, key=lambda x: x.path)
        ],
        "attention_queue": [
            {"path": r.path, "title": r.title, "warnings": r.warnings}
            for r in sorted(tier_a, key=lambda x: x.path)
            if r.warnings and r.path not in essay_paths
        ],
    }


def _dashboard_md_block(dashboard: dict[str, Any]) -> list[str]:
    ta = dashboard["tier_a"]
    tb = dashboard["tier_b_summary"]
    auth = ta["authority"]
    lines = [
        "## 1. Tier A health",
        "",
        "```text",
        "Statecraft Notes Health (Tier A)",
        f"- Tier A notes: {ta['total']}",
        f"- Shelf-native / draft / review-needed / deprecated: "
        f"{auth.get('shelf-native', 0)} / {auth.get('draft', 0)} / "
        f"{auth.get('review-needed', 0)} / {auth.get('deprecated', 0)}",
        f"- Essay candidates: {ta['essay_candidates']}",
        f"- Orphan shelf-native: {ta['orphan_shelf_native']}",
        f"- Missing archive/synthesis anchors (shelf-native): {ta['missing_anchors']}",
        f"- Broken internal note links: {ta['broken_internal_note_links']}",
        f"- Stale review-needed: {ta['stale_review_needed']}",
        f"- Contract violations (Tier A warn-equivalent): {ta['contract_warnings']}",
        "",
        "Tier B summary (operational subfolders)",
        f"- Tier B notes: {tb['total']} (wire: {tb['wire']} · watch: {tb['watch']} · "
        f"reentry: {tb['reentry']} · intake: {tb['intake']})",
        f"- Tier B contract gaps: {tb['contract_gaps']}",
        "```",
        "",
    ]
    return lines


def render_registry_markdown(rows: list[RegistryRow], dashboard: dict[str, Any]) -> str:
    tier_a = sorted([r for r in rows if r.tier == "A"], key=lambda r: (r.note_type, r.title))
    tier_b = sorted([r for r in rows if r.tier == "B"], key=lambda r: r.path)

    lines = [
        "# Statecraft notes registry (generated)",
        "",
        "Do not edit by hand. Regenerate:",
        "",
        "```bash",
        "python3 scripts/reindex_notes.py",
        "```",
        "",
        "Discovery stub: [`statecraft/notes/INDEX.md`](../../statecraft/notes/INDEX.md).",
        "",
    ]
    lines.extend(_dashboard_md_block(dashboard))

    lines.extend(
        [
            "## 2. Tier A registry",
            "",
            "| title | path | note_type | authority | source_basis | archive_anchors | inbound | outbound | broken | essay | updated_at | warnings |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in tier_a:
        link = f"[{row.title}](../../{row.path})"
        warn = ", ".join(row.warnings) if row.warnings else ""
        essay = "true" if row.essay_candidate else "false"
        lines.append(
            f"| {row.title} | {link} | {row.note_type} | {row.authority_level} | {row.source_basis} | "
            f"{row.archive_anchor_count} | {row.inbound_links} | {row.outbound_links} | {row.broken_links} | "
            f"{essay} | {row.updated_at} | {warn} |"
        )

    lines.extend(["", "## 3. Tier A forks", ""])
    lines.append("### Essay candidate queue")
    lines.append("")
    eq = dashboard["essay_queue"]
    if eq:
        for item in eq:
            lines.append(f"- [{item['title']}](../../{item['path']}) — anchors: {item['archive_anchor_count']}, inbound: {item['inbound_links']}")
    else:
        lines.append("_None._")
    lines.append("")
    lines.append("### Attention queue (warnings)")
    lines.append("")
    aq = dashboard["attention_queue"]
    if aq:
        for item in aq:
            warn = ", ".join(item["warnings"])
            lines.append(f"- [{item['title']}](../../{item['path']}) — {warn}")
    else:
        lines.append("_None._")

    lines.extend(
        [
            "",
            "## 4. Tier B summary",
            "",
            f"Total Tier B notes: {dashboard['tier_b_summary']['total']}.",
            "",
            "| path | note_type | subfolder |",
            "| --- | --- | --- |",
        ]
    )
    for row in tier_b:
        link = f"[{row.title}](../../{row.path})"
        lines.append(f"| {link} | {row.note_type} | {row.subfolder} |")
    lines.append("")
    return "\n".join(lines)


def render_registry_json(rows: list[RegistryRow], dashboard: dict[str, Any]) -> str:
    payload = {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "generator": "scripts/reindex_notes.py",
        "dashboard": {
            "tier_a": dashboard["tier_a"],
            "tier_b_summary": dashboard["tier_b_summary"],
        },
        "notes": [row.to_json_dict() for row in sorted(rows, key=lambda r: r.path)],
    }
    return json.dumps(payload, indent=2, sort_keys=False) + "\n"
