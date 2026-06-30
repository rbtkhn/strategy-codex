#!/usr/bin/env python3
"""Backfill note contract frontmatter on a bounded shelf-native batch."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES_ROOT = REPO_ROOT / "statecraft" / "notes"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from check_statecraft_notes import (  # noqa: E402
    FRONTMATTER_RE,
    STUB_MARKER,
    classify_tier,
    parse_note_metadata,
    validate_note,
    build_inbound_note_links,
)
from notes_registry_lib import ARCHIVE_PATH_RE, SYNTHESIS_PATH_RE  # noqa: E402

# README MOU enforcement cluster (exemplars already contract-complete omitted)
MOU_ENFORCEMENT_BATCH: dict[str, str] = {
    "risk-mou-enforcement.md": "risk",
    "risk-hormuz-chokepoint.md": "risk",
    "june-18-2026-mou-convergence.md": "synthesis",
    "june-18-2026-mou-guest-pair-citation-split.md": "compare",
    "june-18-2026-mou-material-vs-sabotage-lens.md": "compare",
    "june-18-2026-mou-falsifier-3-standoff-watch.md": "mechanism",
    "june-18-2026-mou-hormuz-governance-armistice-note.md": "mechanism",
    "june-18-2026-mou-dahhiya-backfire-mou-terms-note.md": "mechanism",
    "june-17-2026-mou-dem-co-ownership-torpedo-note.md": "mechanism",
    "us-israel-military-integration-captured-command-risk.md": "mechanism",
}

# README Hormuz / chokepoint + May Iran compare + March benchmark (exemplars omitted)
IRAN_THEATER_BATCH: dict[str, str] = {
    "2026-02-17-iran-bench-weave-marandi-mearsheimer-helmer.md": "synthesis",
    "2026-03-24-helmer-marandi-energy-hormuz-five-terms-weave.md": "synthesis",
    "arc-helmer-iran-five-terms.md": "arc",
    "iran-war-inquiry-ladder-stress-test.md": "synthesis",
    "jiang-vs-johnson-2026-05.md": "compare",
    "jiang-vs-johnson-others-2026-05.md": "compare",
    "march-2026-benchmark-note.md": "synthesis",
}

# README Artificial intelligence cluster (exemplars + legacy redirects omitted)
AI_CLUSTER_BATCH: dict[str, str] = {
    "risk-artificial-intelligence.md": "risk",
    "pape-on-china-ai.md": "mechanism",
    "jiang-on-ai.md": "mechanism",
    "barnes-on-ai.md": "mechanism",
    "ritter-on-ai.md": "mechanism",
    "weichert-on-ai.md": "mechanism",
    "sachs-on-ai.md": "mechanism",
    "gulf-ai-architecture.md": "mechanism",
    "minab-palantir-four-voice-compare.md": "compare",
    "june-19-2026-moonshots-export-control-sovereign-ai-crossover.md": "bridge",
}

# README Month-Maturity Routing (march benchmark omitted — iran-theater batch)
MONTH_MATURITY_BATCH: dict[str, str] = {
    "month-maturity-routing-registry.md": "synthesis",
    "november-2025-benchmark-note.md": "synthesis",
    "december-2025-benchmark-note.md": "synthesis",
    "january-2026-benchmark-note.md": "synthesis",
    "february-2026-benchmark-note.md": "synthesis",
    "june-2026-opening-watchlist.md": "synthesis",
}

# README Speaker-Derived — Mercouris / Mearsheimer opening watchlists + repair notes
SPEAKER_WATCHLIST_BATCH: dict[str, str] = {
    "mercouris-february-2025-opening-watchlist.md": "synthesis",
    "mercouris-june-2025-opening-watchlist.md": "synthesis",
    "mercouris-october-2025-repair-note.md": "synthesis",
    "mercouris-november-2025-opening-watchlist.md": "synthesis",
    "mercouris-november-2025-repair-note.md": "synthesis",
    "mercouris-september-2025-repair-note.md": "synthesis",
    "mearsheimer-march-2025-opening-watchlist.md": "synthesis",
    "mearsheimer-march-2025-repair-note.md": "synthesis",
    "mearsheimer-july-2025-opening-watchlist.md": "synthesis",
    "mearsheimer-april-2025-opening-watchlist.md": "synthesis",
    "mearsheimer-april-2025-repair-note.md": "synthesis",
    "mearsheimer-september-2025-opening-watchlist.md": "synthesis",
    "mearsheimer-october-2025-opening-watchlist.md": "synthesis",
    "mearsheimer-december-2025-opening-watchlist.md": "synthesis",
    "mearsheimer-december-2025-repair-note.md": "synthesis",
}

# README Closure And Audit
CLOSURE_AUDIT_BATCH: dict[str, str] = {
    "march-2026-closure-method-application.md": "synthesis",
    "may-2026-closure-method-application.md": "synthesis",
    "april-2026-wilkerson-intake-sequence-postmortem.md": "synthesis",
    "statecraft-participant-index-audit-2026-06-03.md": "synthesis",
    "wilkerson-april-2026-contradiction-audit.md": "synthesis",
    "parsi-wilkerson-may-2026-backfill-attention.md": "synthesis",
}

# Legacy *-weave.md / *-register* / pre-recanonical *-arc* (README thread/arc absorption cluster)
WEAVE_REGISTER_BATCH: dict[str, str | dict[str, str]] = {
    # Moved stubs → deprecated bridge redirects
    "2025-02-ritter-india-global-left-trump-pivot-arc.md": {"note_type": "bridge", "authority_level": "deprecated"},
    "2025-11-06-jermy-mercouris-pokrovsk-strategic-weave.md": {"note_type": "bridge", "authority_level": "deprecated"},
    "2026-01-22-to-2026-03-18-jermy-neutrality-decision-naval-arc-weave.md": {"note_type": "bridge", "authority_level": "deprecated"},
    "2026-02-28-pape-smart-bomb-trap-trilogy-weave.md": {"note_type": "bridge", "authority_level": "deprecated"},
    "2026-02-freeman-india-global-left-iran-war-arc.md": {"note_type": "bridge", "authority_level": "deprecated"},
    "2026-02-helmer-feb3-mar24-power-terms-arc.md": {"note_type": "bridge", "authority_level": "deprecated"},
    "2026-02-ritter-india-global-left-iran-war-arc.md": {"note_type": "bridge", "authority_level": "deprecated"},
    "2026-03-01-to-2026-03-18-jermy-diesen-naval-arc-weave.md": {"note_type": "bridge", "authority_level": "deprecated"},
    "2026-03-18-to-2026-04-28-jermy-iran-energy-arc-weave.md": {"note_type": "bridge", "authority_level": "deprecated"},
    "2026-03-helmer-mar17-mar24-two-week-clock-arc.md": {"note_type": "bridge", "authority_level": "deprecated"},
    "2026-03-helmer-mar3-mar24-russia-china-two-track-arc.md": {"note_type": "bridge", "authority_level": "deprecated"},
    # Substantive legacy weaves / registers / arcs
    "2025-12-12-jermy-mercouris-siversk-nss-weave.md": "synthesis",
    "2025-freeman-igl-gaza-ceasefire-register.md": "synthesis",
    "2025-freeman-igl-iran-war-push-register.md": "synthesis",
    "2025-vs-2026-freeman-igl-register-seam.md": "synthesis",
    "2025-vs-2026-ritter-india-global-left-register-seam.md": "synthesis",
    "2026-01-08-jermy-mercouris-crooke-greenland-venezuela-weave.md": "synthesis",
    "2026-01-20-greenland-same-day-weave-helmer-freeman.md": "synthesis",
    "2026-01-30-jermy-mercouris-iran-armada-kiev-weave.md": "synthesis",
    "2026-02-17-geneva-day-weave-helmer-mercouris.md": "synthesis",
    "2026-02-28-pape-crooke-opening-strike-bench-weave.md": "synthesis",
    "2026-03-03-crooke-pape-simplicius-air-power-survival-bench-weave.md": "synthesis",
    "2026-03-03-davis-macgregor-henningsen-iran-war-bench-weave.md": "synthesis",
    "2026-03-03-iran-war-weave-helmer-marandi.md": "conflict",
    "2026-03-17-iran-war-bench-weave-helmer-crooke-napolitano.md": "synthesis",
    "2026-03-18-diesen-marandi-jermy-energy-infrastructure-weave.md": "synthesis",
    "2026-03-18-jermy-mercouris-iran-energy-arsenal-weave.md": "synthesis",
    "2026-06-13-jiang-ph-mad-king-boomer-hell-cross-weave.md": "synthesis",
    "2026-06-14-lebanon-enforcement-nima-host-arc.md": "arc",
}

# Compare / wedge / mosaic-trap cluster (same-moment allocation + mechanism seams)
COMPARE_WEDGE_BATCH: dict[str, str | dict[str, str]] = {
    "2026-01-20-davos-dmitriev-helmer-mercouris-comparison.md": {"note_type": "bridge", "authority_level": "deprecated"},
    "thread-pape-2026-02-28-to-2026-03-16-smart-bomb-trap.md": {"note_type": "bridge", "authority_level": "deprecated"},
    "2026-02-03-helmer-marandi-turkey-kurd-regional-wedge.md": "compare",
    "2026-02-17-freeman-mearsheimer-kabuki-vs-empire-geneva-week.md": "compare",
    "2026-03-03-mercouris-wilkerson-attrition-downed-warplanes-wedge.md": "compare",
    "2026-03-16-pape-vs-crooke-mosaic-trap.md": "compare",
    "2026-03-16-ritter-implementation-trap-mosaic.md": "compare",
    "2026-03-17-davis-henningsen-global-reset-wedge.md": "compare",
    "2026-03-19-dollar-hormuz-terms-trap-mosaic-lattice.md": "synthesis",
    "2026-03-23-postol-vs-ritter-implementation-battlefield.md": "compare",
    "2026-03-24-mercouris-helmer-marandi-dimona-ground-wedge.md": "compare",
    "2026-03-24-pape-deployments-gamblers-conceit-mercouris-wedge.md": "compare",
    "2026-05-29-pape-vs-freeman-sachs-marandi.md": {"note_type": "compare", "authority_level": "review-needed"},
    "2026-05-31-barnes-aguilar-captured-command-vs-degraded-carry.md": {"note_type": "compare", "authority_level": "review-needed"},
    "2026-05-31-rome-america-carrier-capture-vs-sovereign-burden-bearing.md": {"note_type": "compare", "authority_level": "review-needed"},
    "2026-05-31-weichert-barnes-logistics-ceiling-vs-dib-lock-in.md": "compare",
    "2026-06-06-persia-lebanon-first-gate-vs-hormuz-mechanics.md": "compare",
    "2026-06-07-barnes-aguilar-sanctions-enforceability-vs-capture-fork.md": "compare",
    "2026-06-07-parsi-nima-mcgovern-third-party-deterrence-vs-recognition-gate.md": "compare",
    "2026-06-08-crooke-napolitano-vs-hedges-permanent-security.md": "compare",
    "2026-06-08-persia-marandi-deal-floor-vs-lebanon-gate-clauses.md": "compare",
    "2026-06-12-johnson-wilkerson-aguilar-mou-gate-comparison.md": "compare",
    "2026-06-17-dialogue-works-quartet-mou-clause-comparison.md": "compare",
    "internal-vs-public-vocabulary.md": {"note_type": "mechanism", "authority_level": "review-needed"},
    "kent-restraint-lever-walk-away-vs-weichert-collapse-2026-06.md": "compare",
    "recognition-threshold-vs-settlement-architecture.md": {"note_type": "mechanism", "authority_level": "review-needed"},
}

BATCHES: dict[str, dict[str, str | dict[str, str]]] = {
    "mou-enforcement": MOU_ENFORCEMENT_BATCH,
    "iran-theater": IRAN_THEATER_BATCH,
    "ai-cluster": AI_CLUSTER_BATCH,
    "month-maturity": MONTH_MATURITY_BATCH,
    "speaker-watchlist": SPEAKER_WATCHLIST_BATCH,
    "closure-audit": CLOSURE_AUDIT_BATCH,
    "weave-register": WEAVE_REGISTER_BATCH,
    "compare-wedge": COMPARE_WEDGE_BATCH,
    "prefixed-canonical": {},
    "dated-slug": {},
    "other-slug": {},
    "tier-b-operational": {},
    "arc-continuity-repair": {},
}

DISCOVERED_BATCHES = frozenset(
    {"prefixed-canonical", "dated-slug", "other-slug", "tier-b-operational", "arc-continuity-repair"}
)

PREFIX_BATCH_PREFIXES: tuple[tuple[str, str], ...] = (
    ("thread-", "thread"),
    ("arc-", "arc"),
    ("trend-", "trend"),
    ("conflict-", "conflict"),
    ("risk-", "risk"),
)

DATE_SLUG_RE = re.compile(r"^20\d{2}-\d{2}(-\d{2})?")

def infer_dated_slug_type(stem: str) -> str:
    lower = stem.lower()
    if "bridge" in lower:
        return "bridge"
    if "conflict" in lower or "mou-art" in lower:
        return "conflict"
    if "fork" in lower or "-vs-" in lower or "comparison" in lower:
        return "compare"
    if "convergence" in lower or "synthesis" in lower:
        return "synthesis"
    return "mechanism"

def infer_other_slug_type(stem: str, rel: str) -> str:
    if rel.startswith("compacts/") and stem == "README":
        return "synthesis"
    lower = stem.lower()
    if "bridge" in lower or "correspondence" in lower:
        return "bridge"
    if "compare" in lower or "-vs-" in lower or "orthogonality" in lower:
        return "compare"
    if "doctrine-arc" in lower or (lower.startswith("arc-") is False and "-arc-" in lower):
        return "arc"
    if any(
        token in lower
        for token in (
            "watchlist",
            "audit",
            "recursive-learning",
            "executive-synthesis",
            "repair-routing",
            "upgrade-plan",
            "scorecard",
            "workflow",
            "transaction",
            "inquiry-ladder",
        )
    ):
        return "synthesis"
    return "mechanism"

def discover_other_slug_batch() -> dict[str, str]:
    """Remaining Tier A notes (non-dated, non-prefixed root slugs + compacts README)."""
    batch: dict[str, str] = {}
    for path in sorted(NOTES_ROOT.rglob("*.md")):
        if classify_tier(path) != "A":
            continue
        rel = path.relative_to(NOTES_ROOT).as_posix()
        stem = path.stem
        if DATE_SLUG_RE.match(stem) and path.parent == NOTES_ROOT:
            continue
        if path.parent == NOTES_ROOT:
            if any(stem.startswith(prefix) for prefix, _ in PREFIX_BATCH_PREFIXES):
                continue
            if any(x in stem for x in ("weave", "register")) or "wedge" in stem:
                continue
            if "comparison" in stem or "-vs-" in stem:
                continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if STUB_MARKER in text:
            continue
        meta = parse_note_metadata(path, text)
        if meta.authority_level and meta.source_basis and meta.note_type:
            continue
        batch[rel] = infer_other_slug_type(stem, rel)
    return batch

def discover_dated_slug_batch() -> dict[str, str]:
    """Tier A root notes with date-leading slugs missing contract fields."""
    batch: dict[str, str] = {}
    for path in sorted(NOTES_ROOT.glob("*.md")):
        if classify_tier(path) != "A":
            continue
        stem = path.stem
        if not DATE_SLUG_RE.match(stem):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if STUB_MARKER in text:
            continue
        meta = parse_note_metadata(path, text)
        if meta.authority_level and meta.source_basis and meta.note_type:
            continue
        batch[path.name] = infer_dated_slug_type(stem)
    return batch

def discover_prefixed_canonical_batch() -> dict[str, str]:
    """Tier A root notes with forward prefix (or *bench*) missing contract fields."""
    batch: dict[str, str] = {}
    for path in sorted(NOTES_ROOT.glob("*.md")):
        if classify_tier(path) != "A":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if STUB_MARKER in text:
            continue
        meta = parse_note_metadata(path, text)
        if meta.authority_level and meta.source_basis and meta.note_type:
            continue
        stem = path.stem
        note_type = meta.note_type or meta.prefix_inferred_type
        if not note_type and "bench" in stem:
            note_type = "synthesis"
        if not note_type:
            for prefix, inferred in PREFIX_BATCH_PREFIXES:
                if stem.startswith(prefix):
                    note_type = inferred
                    break
        if not note_type:
            continue
        batch[path.name] = note_type
    return batch

TIER_B_TYPE_MAP = {"wire": "wire", "watch": "watch", "reentry": "reentry", "intake": "intake"}

def discover_tier_b_operational_batch() -> dict[str, str]:
    """Tier B operational subfolders (wire / watch / reentry / intake) missing contract."""
    batch: dict[str, str] = {}
    for path in sorted(NOTES_ROOT.rglob("*.md")):
        if classify_tier(path) != "B":
            continue
        rel = path.relative_to(NOTES_ROOT)
        sub = rel.parts[0] if rel.parts else ""
        note_type = TIER_B_TYPE_MAP.get(sub)
        if not note_type:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if STUB_MARKER in text:
            continue
        meta = parse_note_metadata(path, text)
        if meta.note_type and meta.source_basis:
            continue
        batch[rel.as_posix()] = note_type
    return batch

def resolve_batch(name: str) -> dict[str, str | dict[str, str]]:
    if name == "prefixed-canonical":
        return discover_prefixed_canonical_batch()
    if name == "dated-slug":
        return discover_dated_slug_batch()
    if name == "other-slug":
        return discover_other_slug_batch()
    if name == "tier-b-operational":
        return discover_tier_b_operational_batch()
    if name == "arc-continuity-repair":
        return discover_arc_continuity_repair_batch()
    return BATCHES[name]

DATE_IN_NAME = re.compile(r"(\d{4}-\d{2}-\d{2})")
NOTE_LINK_RE = re.compile(r"\]\(\./([^)]+\.md)")

def _batch_entry(spec: str | dict[str, str]) -> tuple[str, str, list[str]]:
    if isinstance(spec, str):
        return spec, "shelf-native", []
    return (
        spec.get("note_type", "synthesis"),
        spec.get("authority_level", "shelf-native"),
        list(spec.get("archive_links", []) or []),
    )

def _archives_from_linked_synthesis(text: str, from_path: Path, *, limit: int = 8) -> list[str]:
    links: list[str] = []
    for raw in re.findall(r"\]\(([^)]+\.md)\)", text.replace("\\", "/")):
        if "synthesis/" not in raw:
            continue
        target = (from_path.parent / raw.split("#")[0]).resolve()
        if not target.is_file():
            continue
        body = target.read_text(encoding="utf-8", errors="replace")
        for item in _extract_archive_links(body, limit=limit):
            if item not in links:
                links.append(item)
            if len(links) >= limit:
                return links
    return links

def _canonical_archive_links(text: str, from_path: Path, *, limit: int = 8) -> list[str]:
    links = _extract_archive_links(text, limit=limit)
    if len(links) >= limit:
        return links
    for item in _archives_from_linked_synthesis(text, from_path, limit=limit):
        if item not in links:
            links.append(item)
        if len(links) >= limit:
            return links
    for match in NOTE_LINK_RE.findall(text.replace("\\", "/")):
        target = NOTES_ROOT / match.split("#")[0]
        if not target.is_file():
            continue
        body = target.read_text(encoding="utf-8", errors="replace")
        for item in _extract_archive_links(body, limit=limit):
            if item not in links:
                links.append(item)
            if len(links) >= limit:
                return links
    return links

UNCLOSED_MD_LINK = re.compile(r"(\]\([^)]+\.md)(?<!\))$")

def fix_unclosed_md_links(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.rstrip()
        if UNCLOSED_MD_LINK.search(stripped):
            line = stripped + ")"
        lines.append(line)
    trailing = "\n" if text.endswith("\n") else ""
    return "\n".join(lines) + trailing

def _archives_from_note_links(
    text: str,
    from_path: Path,
    *,
    limit: int = 8,
    depth: int = 0,
) -> list[str]:
    if depth > 2:
        return []
    links: list[str] = []
    for raw in re.findall(r"\]\(([^)]+)\)", text.replace("\\", "/")):
        target = raw.split("#")[0].strip()
        if not target.lower().endswith(".md"):
            continue
        resolved = (from_path.parent / target).resolve()
        if not resolved.is_file():
            continue
        body = resolved.read_text(encoding="utf-8", errors="replace")
        for item in _extract_archive_links(body, limit=limit):
            if item not in links:
                links.append(item)
            if len(links) >= limit:
                return links
        for item in _archives_from_note_links(body, resolved, limit=limit, depth=depth + 1):
            if item not in links:
                links.append(item)
            if len(links) >= limit:
                return links
    return links

def _speaker_slug_from_arc_stem(stem: str) -> str | None:
    if stem.startswith("arc-") and stem.endswith("-continuity"):
        return stem.removeprefix("arc-").removesuffix("-continuity")
    return None

def _ensure_voice_routing_links(text: str, speaker: str) -> str:
    routing = f"../voices/{speaker}/{speaker}-routing.md"
    index = f"../voices/{speaker}/{speaker}-index.md"
    if f"voices/{speaker}/" in text.replace("\\", "/"):
        return text
    block = (
        f"\n\nOpen alongside:\n\n"
        f"- [{speaker} routing]({routing})\n"
        f"- [{speaker} index]({index})\n"
    )
    return block + text

def _ensure_notes_readme_link(text: str) -> str:
    if "statecraft/notes/README.md" in text.replace("\\", "/") or "](./README.md" in text:
        return text
    block = "\n\nSee [notes taxonomy](./README.md#thread-and-arc-canonical-draft).\n"
    return block + text

def _upsert_frontmatter_fields(
    text: str,
    *,
    archive_links: list[str],
    authority_level: str | None = None,
    source_basis: str | None = None,
) -> str:
    fm = FRONTMATTER_RE.match(text.lstrip("\ufeff"))
    if not fm:
        return text
    lines: list[str] = []
    skip_archive = False
    for line in fm.group(1).rstrip().splitlines():
        if line.strip().startswith("archive_links:"):
            skip_archive = True
            continue
        if skip_archive and line.startswith("  - "):
            continue
        if skip_archive and not line.startswith("  "):
            skip_archive = False
        if authority_level and line.startswith("authority_level:"):
            lines.append(f"authority_level: {authority_level}")
            continue
        if source_basis and line.startswith("source_basis:"):
            lines.append(f"source_basis: {source_basis}")
            continue
        if not skip_archive:
            lines.append(line)
    if archive_links:
        lines.append("archive_links:")
        for link in archive_links[:8]:
            lines.append(f"  - {link}")
    elif authority_level == "review-needed":
        lines = [ln for ln in lines if not ln.startswith("archive_links:")]
    new_fm = "\n".join(lines) + "\n"
    return f"---\n{new_fm}---\n{text[fm.end():]}"

def discover_arc_continuity_repair_batch() -> dict[str, str]:
    """Tier A arc / routing notes failing weak-anchor or orphan validation."""
    batch: dict[str, str] = {}
    inbound = build_inbound_note_links(list(NOTES_ROOT.rglob("*.md")))
    for path in sorted(NOTES_ROOT.rglob("*.md")):
        if classify_tier(path) != "A":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if STUB_MARKER in text:
            continue
        meta = parse_note_metadata(path, text)
        issues = validate_note(meta, text=text, inbound_count=inbound.get(meta.rel, 0))
        if not issues:
            continue
        if any(
            token in issue
            for issue in issues
            for token in ("missing note_type", "missing source_basis", "missing authority_level")
        ):
            continue
        note_type = meta.note_type or "arc"
        batch[path.relative_to(NOTES_ROOT).as_posix()] = note_type
    return batch

def _sanitize_archive_path(raw: str) -> str:
    path = raw.split("#")[0].strip().rstrip("#")
    return path.replace("\\", "/")

def _resolved_archive_list(candidates: list[str]) -> list[str]:
    resolved: list[str] = []
    for raw in candidates:
        path = _sanitize_archive_path(raw)
        if not path.startswith("source-archive/"):
            continue
        if (REPO_ROOT / path).is_file() and path not in resolved:
            resolved.append(path)
    return resolved

def repair_arc_continuity_file(path: Path, *, updated_at: str, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    meta = parse_note_metadata(path, text)
    fixed = fix_unclosed_md_links(text)
    speaker = _speaker_slug_from_arc_stem(path.stem)
    if speaker:
        fixed = _ensure_voice_routing_links(fixed, speaker)
    if path.stem in {"instrument-bench-maturity-audit", "statecraft-multi-lens-bench-pressure-test-2026-05"}:
        fixed = _ensure_notes_readme_link(fixed)

    archives = _extract_archive_links(fixed, limit=8)
    for item in _archives_from_linked_synthesis(fixed, path, limit=8):
        if item not in archives:
            archives.append(item)
    for item in _archives_from_note_links(fixed, path, limit=8):
        if item not in archives:
            archives.append(item)
    for item in _canonical_archive_links(fixed, path, limit=8):
        if item not in archives:
            archives.append(item)
    fm_archives = list(getattr(meta, "archive_links", []) or [])
    for item in _resolved_archive_list(fm_archives):
        if item not in archives:
            archives.append(item)
    archives = _resolved_archive_list(archives)

    authority = meta.authority_level or "shelf-native"
    basis = meta.source_basis or _source_basis(fixed, archives)
    if authority == "shelf-native" and not archives:
        authority = "review-needed"
        basis = meta.source_basis or "mixed"

    new_text = _upsert_frontmatter_fields(
        fixed,
        archive_links=archives,
        authority_level=authority,
        source_basis=basis,
    )
    if "updated_at:" in new_text.split("---")[1]:
        new_text = re.sub(
            r"^updated_at:.*$",
            f"updated_at: {updated_at}",
            new_text,
            count=1,
            flags=re.MULTILINE,
        )

    if new_text == text:
        return False
    if dry_run:
        print(f"would repair: {path.relative_to(REPO_ROOT)}")
        return True
    path.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"repaired: {path.relative_to(REPO_ROOT)}")
    return True

def _infer_created_at(stem: str) -> str:
    match = DATE_IN_NAME.search(stem)
    return match.group(1) if match else "2026-06-18"

def _extract_archive_links(text: str, *, limit: int = 8) -> list[str]:
    links: list[str] = []
    for match in ARCHIVE_PATH_RE.findall(text.replace("\\", "/")):
        path = match.rstrip(").,")
        if path not in links:
            links.append(path)
        if len(links) >= limit:
            break
    return links

def _source_basis(text: str, archives: list[str]) -> str:
    if SYNTHESIS_PATH_RE.search(text.replace("\\", "/")) and archives:
        return "mixed"
    if archives:
        return "source-archive"
    if SYNTHESIS_PATH_RE.search(text.replace("\\", "/")):
        return "synthesis"
    return "mixed"

def _render_frontmatter(
    *,
    note_id: str,
    note_type: str,
    authority_level: str,
    source_basis: str,
    created_at: str,
    updated_at: str,
    archive_links: list[str],
) -> str:
    lines = [
        "---",
        f"note_id: {note_id}",
        f"note_type: {note_type}",
        f"authority_level: {authority_level}",
        f"source_basis: {source_basis}",
        "essay_candidate: false",
        f"created_at: {created_at}",
        f"updated_at: {updated_at}",
    ]
    if archive_links:
        lines.append("archive_links:")
        for link in archive_links[:8]:
            lines.append(f"  - {link}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)

def _patch_frontmatter_block(
    existing: str,
    *,
    note_type: str,
    authority_level: str,
    source_basis: str,
    created_at: str,
    updated_at: str,
    archive_links: list[str],
    meta: object,
) -> str:
    lines = existing.rstrip().splitlines()
    keys = {
        line.split(":", 1)[0].strip()
        for line in lines
        if ":" in line and not line.startswith(" ") and not line.startswith("-")
    }

    def add(key: str, value: str) -> None:
        if key not in keys:
            lines.append(f"{key}: {value}")
            keys.add(key)

    if not getattr(meta, "note_type", None):
        add("note_type", note_type)
    add("authority_level", authority_level)
    add("source_basis", source_basis)
    add("essay_candidate", "false")
    add("created_at", created_at)
    add("updated_at", updated_at)
    if archive_links and "archive_links" not in keys:
        lines.append("archive_links:")
        for link in archive_links[:8]:
            lines.append(f"  - {link}")
    return "\n".join(lines) + "\n"

def backfill_file(
    path: Path,
    spec: str | dict[str, str],
    *,
    updated_at: str,
    dry_run: bool,
) -> bool:
    note_type, authority_level, extra_archives = _batch_entry(spec)
    text = path.read_text(encoding="utf-8", errors="replace")
    meta = parse_note_metadata(path, text)
    tier = meta.tier or classify_tier(path)
    if tier == "B":
        if meta.note_type and meta.source_basis:
            return False
        authority_level = "draft"
    elif meta.authority_level and meta.source_basis and meta.note_type:
        return False

    archives = _canonical_archive_links(text, path)
    for item in extra_archives:
        if item not in archives:
            archives.append(item)
    basis = _source_basis(text, archives)
    if authority_level == "shelf-native" and not archives:
        authority_level = "review-needed"
    created = _infer_created_at(path.stem)
    effective_type = meta.note_type or note_type
    block = _render_frontmatter(
        note_id=path.stem,
        note_type=effective_type,
        authority_level=authority_level,
        source_basis=basis,
        created_at=created,
        updated_at=updated_at,
        archive_links=archives,
    )

    fm = FRONTMATTER_RE.match(text.lstrip("\ufeff"))
    if fm:
        patched = _patch_frontmatter_block(
            fm.group(1),
            note_type=effective_type,
            authority_level=authority_level,
            source_basis=basis,
            created_at=created,
            updated_at=updated_at,
            archive_links=archives,
            meta=meta,
        )
        new_text = f"---\n{patched}---\n{text[fm.end():]}"
    elif text.lstrip("\ufeff").startswith("---"):
        return False
    else:
        new_text = block + text

    if dry_run:
        print(f"would backfill: {path.relative_to(REPO_ROOT)}")
        return True

    path.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"backfilled: {path.relative_to(REPO_ROOT)}")
    return True

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--batch",
        choices=tuple(BATCHES),
        default="mou-enforcement",
        help="Named shelf-native batch from notes/README clusters",
    )
    ap.add_argument("--updated-at", default="2026-06-28")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify", action="store_true", help="Validate batch after backfill")
    args = ap.parse_args()

    batch = resolve_batch(args.batch)
    changed = 0
    repair_batch = args.batch == "arc-continuity-repair"
    for rel_name, spec in batch.items():
        path = NOTES_ROOT / rel_name
        if not path.is_file():
            print(f"missing: {rel_name}", file=sys.stderr)
            continue
        if repair_batch:
            if repair_arc_continuity_file(path, updated_at=args.updated_at, dry_run=args.dry_run):
                changed += 1
        elif backfill_file(path, spec, updated_at=args.updated_at, dry_run=args.dry_run):
            changed += 1

    print(f"batch {args.batch}: {changed} file(s) {'would change' if args.dry_run else 'updated'}")
    if args.verify and not args.dry_run:
        inbound = build_inbound_note_links(list(NOTES_ROOT.rglob("*.md")))
        failures = 0
        for rel_name in batch:
            path = NOTES_ROOT / rel_name
            text = path.read_text(encoding="utf-8")
            meta = parse_note_metadata(path, text)
            issues = validate_note(meta, text=text, inbound_count=inbound.get(meta.rel, 0))
            if issues:
                failures += 1
                print(f"FAIL {rel_name}:", file=sys.stderr)
                for issue in issues:
                    print(f"  {issue}", file=sys.stderr)
        return 1 if failures else 0
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
