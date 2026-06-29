#!/usr/bin/env python3
"""Voice index registry — row collection, YAML governance, markdown/JSON render."""
from __future__ import annotations

import json
import subprocess
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
VOICES_DIR = REPO_ROOT / "statecraft" / "voices"
DEFAULT_YAML = VOICES_DIR / "voice-index-registry.yml"
DEFAULT_ARCHIVE = REPO_ROOT / "source-archive" / "statecraft"

BUILDER_ALIASES: dict[str, str] = {
    "alkhorshid": "build_alkhorshid_guest_index.py",
    "davis": "build_davis_guest_index.py",
    "diesen": "build_diesen_guest_index.py",
    "mercouris": "build_mercouris_guest_index.py",
}

Parity = Literal["pass", "warn", "fail", "unknown"]

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]


@dataclass
class VoiceRegistryRow:
    voice: str
    primary_index: str
    listed_in_voices_router: bool
    builder: str | None
    audit_command: str
    eligible_captures: int
    indexed_captures: int
    parity: Parity
    broken_links: int
    companion_routes: list[str] = field(default_factory=list)
    exceptions: list[str] = field(default_factory=list)
    curated_overlays: list[str] = field(default_factory=list)
    last_rebuilt: str | None = None
    status: str = "canonical"
    index_kind: str = "primary"


@dataclass(frozen=True)
class AuditFindingLite:
    level: Literal["pass", "fail", "warn"]
    code: str
    message: str


def load_voice_index_registry_yaml(path: Path | None = None) -> dict[str, Any]:
    yaml_path = path or DEFAULT_YAML
    if yaml is None:
        raise RuntimeError("PyYAML required; install requirements-dev.txt")
    if not yaml_path.is_file():
        return {"schema_version": "1.0", "voices": {}}
    raw = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return {"schema_version": "1.0", "voices": {}}
    voices = raw.get("voices") or raw.get("shelves") or {}
    if not isinstance(voices, dict):
        voices = {}
    return {"schema_version": str(raw.get("schema_version") or "1.0"), "voices": voices}


def voice_yaml_entry(registry: dict[str, Any], slug: str) -> dict[str, Any]:
    voices = registry.get("voices") or {}
    entry = voices.get(slug)
    return entry if isinstance(entry, dict) else {}


def validate_yaml_code_exclusion_parity(registry: dict[str, Any] | None = None) -> list[AuditFindingLite]:
    import shelf_index_utils as shelf_utils  # noqa: WPS433

    reg = registry if registry is not None else load_voice_index_registry_yaml()
    findings: list[AuditFindingLite] = []
    missing: list[str] = []
    for slug in sorted(shelf_utils.CODE_EXCLUSION_SLUGS):
        entry = voice_yaml_entry(reg, slug)
        exclusions = entry.get("exclusions") or []
        if not isinstance(exclusions, list) or not exclusions:
            missing.append(slug)
    if missing:
        for slug in missing:
            findings.append(
                AuditFindingLite(
                    "fail",
                    "exception_registry",
                    f"{slug}: code exclusion in shelf_capture_excluded() but no YAML exclusions entry",
                )
            )
    else:
        findings.append(
            AuditFindingLite(
                "pass",
                "exception_registry",
                f"all {len(shelf_utils.CODE_EXCLUSION_SLUGS)} code-exclusion voices documented in YAML",
            )
        )
    return findings


def discover_builder_for_slug(slug: str, registry: dict[str, Any] | None = None) -> str | None:
    reg = registry if registry is not None else load_voice_index_registry_yaml()
    entry = voice_yaml_entry(reg, slug)
    builder = entry.get("builder")
    if isinstance(builder, str) and builder.strip():
        return builder.strip().replace("\\", "/")
    alias = BUILDER_ALIASES.get(slug)
    if alias and (SCRIPTS_DIR / alias).is_file():
        return f"scripts/{alias}"
    default = SCRIPTS_DIR / f"build_{slug}_index.py"
    if default.is_file():
        return f"scripts/build_{slug}_index.py"
    return None


def _last_rebuilt(index_path: Path) -> str | None:
    if not index_path.is_file():
        return None
    try:
        proc = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(index_path.relative_to(REPO_ROOT))],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()[:10]
    except (OSError, subprocess.TimeoutExpired):
        pass
    try:
        mtime = index_path.stat().st_mtime
        return datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%d")
    except OSError:
        return None


def build_archive_voice_index(
    archive_root: Path,
    *,
    slugs: frozenset[str] | None = None,
) -> dict[str, list[Path]]:
    import audit_statecraft_archive_index as audit  # noqa: WPS433
    import shelf_index_utils as shelf_utils  # noqa: WPS433
    import statecraft_writer_index as writer_idx  # noqa: WPS433
    from statecraft_day_archive import iter_source_files, parse_frontmatter, read_text  # noqa: WPS433

    if slugs is None:
        slugs = frozenset(
            slug
            for slug, _path, kind in audit.discover_voice_primary_indexes()
            if kind == "primary"
        )
    out: dict[str, list[Path]] = defaultdict(list)
    if not archive_root.is_dir():
        return dict(out)
    for day_dir in writer_idx.iter_all_day_dirs(archive_root):
        for path in iter_source_files(day_dir):
            meta = parse_frontmatter(path)
            body_snip = read_text(path)[:8000] if path.is_file() else ""
            for slug in slugs:
                if shelf_utils.capture_matches_shelf(slug, path, meta, body_snip):
                    out[slug].append(path)
    for slug in out:
        out[slug].sort(key=lambda p: (p.parent.name, p.name))
    return dict(out)


def _count_broken_links(index_path: Path) -> int:
    import validate_repo_routing as routing_val  # noqa: WPS433

    if not index_path.is_file():
        return 0
    errors: list[str] = []
    routing_val.validate_markdown_links([index_path], errors, strict=True)
    return len(errors)


def _companion_routes(slug: str, index_path: Path) -> list[str]:
    import shelf_index_utils as shelf_utils  # noqa: WPS433

    routes: list[str] = []
    shelf = index_path.parent
    for name in (f"{slug}-profile.md", f"{slug}-source-index.md"):
        p = shelf / name
        if p.is_file():
            routes.append(name)
    for p in shelf_utils.companion_paths(slug, VOICES_DIR):
        routes.append(p.name)
    return sorted(set(routes))


def _derive_parity(findings: list[Any], *, status: str, has_builder: bool) -> Parity:
    if any(f.level == "fail" for f in findings):
        return "fail"
    if any(f.code == "archive_unlisted" and f.level == "warn" for f in findings):
        return "fail"
    if any(f.level == "warn" for f in findings):
        return "warn"
    if status in ("compatibility", "review-needed", "deprecated"):
        return "warn"
    if status == "canonical" and not has_builder:
        return "warn"
    return "pass"


def collect_voice_registry_row(
    slug: str,
    *,
    archive_root: Path,
    registry: dict[str, Any] | None = None,
    archive_index: dict[str, list[Path]] | None = None,
) -> tuple[VoiceRegistryRow, list[Any]]:
    import audit_statecraft_archive_index as audit  # noqa: WPS433
    import shelf_index_utils as shelf_utils  # noqa: WPS433

    reg = registry if registry is not None else load_voice_index_registry_yaml()
    entry = voice_yaml_entry(reg, slug)
    index_path = audit.shelf_index_path(slug)
    primary_rel = (
        audit._posix_rel(index_path)
        if index_path.is_file()
        else f"statecraft/voices/{slug}/{slug}-index.md"
    )

    if not index_path.is_file():
        row = VoiceRegistryRow(
            voice=slug,
            primary_index=primary_rel,
            listed_in_voices_router=False,
            builder=discover_builder_for_slug(slug, reg),
            audit_command=f"python scripts/audit_statecraft_archive_index.py --shelf-index {slug}",
            eligible_captures=0,
            indexed_captures=0,
            parity="unknown",
            broken_links=0,
            status=str(entry.get("status") or "review-needed"),
        )
        return row, [
            audit.AuditFinding("fail", "missing_voice_index", f"missing {slug}/{slug}-index.md")
        ]

    findings = audit.audit_shelf_index(slug, archive_root=archive_root)
    broken = _count_broken_links(index_path)
    indexed = len(audit.parse_shelf_index_links(index_path))

    if archive_index is not None:
        disk_paths = archive_index.get(slug, [])
    else:
        disk_paths = audit.iter_archive_captures_for_shelf(slug, archive_root)

    eligible = 0
    for path in disk_paths:
        meta = audit.parse_frontmatter(path)
        body_snip = audit.read_text(path)[:8000] if path.is_file() else ""
        if shelf_utils.shelf_capture_excluded(slug, path, meta, body_snip):
            continue
        eligible += 1

    voice_rows = audit.collect_voice_index_rows()
    listed = next((r.listed for r in voice_rows if r.slug == slug), False)
    index_kind = next((r.index_kind for r in voice_rows if r.slug == slug), "primary")

    exceptions = [str(x) for x in (entry.get("exclusions") or []) if str(x).strip()]
    overlays = [str(x) for x in (entry.get("curated_overlays") or []) if str(x).strip()]
    status = str(entry.get("status") or ("canonical" if index_kind == "primary" else "compatibility"))
    builder = discover_builder_for_slug(slug, reg)
    parity = _derive_parity(findings, status=status, has_builder=bool(builder))

    row = VoiceRegistryRow(
        voice=slug,
        primary_index=primary_rel,
        listed_in_voices_router=listed,
        builder=builder,
        audit_command=f"python scripts/audit_statecraft_archive_index.py --shelf-index {slug}",
        eligible_captures=eligible,
        indexed_captures=indexed,
        parity=parity,
        broken_links=broken,
        companion_routes=_companion_routes(slug, index_path),
        exceptions=exceptions,
        curated_overlays=overlays,
        last_rebuilt=_last_rebuilt(index_path),
        status=status,
        index_kind=index_kind,
    )
    return row, findings


def collect_all_voice_registry_rows(
    *,
    archive_root: Path = DEFAULT_ARCHIVE,
    registry: dict[str, Any] | None = None,
    slug_filter: str | None = None,
) -> list[VoiceRegistryRow]:
    import audit_statecraft_archive_index as audit  # noqa: WPS433

    reg = registry if registry is not None else load_voice_index_registry_yaml()
    slugs = [
        slug
        for slug, _path, kind in audit.discover_voice_primary_indexes()
        if kind == "primary"
    ]
    if slug_filter:
        slug_filter = slug_filter.strip().casefold()
        slugs = [s for s in slugs if s == slug_filter]
    archive_index = build_archive_voice_index(archive_root, slugs=frozenset(slugs))
    rows: list[VoiceRegistryRow] = []
    for slug in slugs:
        row, _findings = collect_voice_registry_row(
            slug,
            archive_root=archive_root,
            registry=reg,
            archive_index=archive_index,
        )
        rows.append(row)
    return rows


def build_summary(rows: list[VoiceRegistryRow]) -> dict[str, int]:
    return {
        "voices_discovered": len(rows),
        "listed_in_voices_router": sum(1 for r in rows if r.listed_in_voices_router),
        "with_primary_index": sum(1 for r in rows if r.parity != "unknown"),
        "with_rebuild_script": sum(1 for r in rows if r.builder),
        "parity_pass": sum(1 for r in rows if r.parity == "pass"),
        "parity_warn": sum(1 for r in rows if r.parity == "warn"),
        "parity_fail": sum(1 for r in rows if r.parity == "fail"),
        "broken_links_total": sum(r.broken_links for r in rows),
        "documented_exceptions": sum(1 for r in rows if r.exceptions),
    }


def render_registry_markdown(rows: list[VoiceRegistryRow], summary: dict[str, int]) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "# Voice Index Parity Dashboard",
        "",
        "Do not edit by hand. Regenerate:",
        "",
        "```bash",
        "python3 scripts/build_voice_index_registry.py",
        "```",
        "",
        "Terminology: [`voice-index-registry.md`](../../statecraft/voices/voice-index-registry.md).",
        "",
        f"_Generated at {generated_at}_",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Voices discovered | {summary['voices_discovered']} |",
        f"| Listed in voices router | {summary['listed_in_voices_router']} |",
        f"| With primary voice index | {summary['with_primary_index']} |",
        f"| With rebuild script | {summary['with_rebuild_script']} |",
        f"| Parity pass | {summary['parity_pass']} |",
        f"| Parity warn | {summary['parity_warn']} |",
        f"| Parity fail | {summary['parity_fail']} |",
        f"| Broken links (total) | {summary['broken_links_total']} |",
        f"| Documented exceptions | {summary['documented_exceptions']} |",
        "",
        "## Voice registry",
        "",
        "| Voice | Primary index | Builder | Eligible | Indexed | Parity | Exceptions | Status |",
        "| --- | --- | --- | ---: | ---: | --- | --- | --- |",
    ]
    for row in sorted(rows, key=lambda r: r.voice):
        builder = row.builder or "—"
        if builder != "—" and not builder.startswith("`"):
            builder = f"`{builder}`"
        exc = "—" if not row.exceptions else "; ".join(row.exceptions[:2])
        if len(row.exceptions) > 2:
            exc += f" (+{len(row.exceptions) - 2})"
        exc = exc.replace("|", "\\|")
        idx = f"`{row.primary_index}`"
        lines.append(
            f"| {row.voice} | {idx} | {builder} | {row.eligible_captures} | "
            f"{row.indexed_captures} | {row.parity} | {exc} | {row.status} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_registry_json(rows: list[VoiceRegistryRow], summary: dict[str, int]) -> str:
    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "summary": summary,
        "voices": [asdict(r) for r in rows],
    }
    return json.dumps(payload, indent=2) + "\n"


def audit_all_voice_indexes(
    *,
    archive_root: Path = DEFAULT_ARCHIVE,
    registry: dict[str, Any] | None = None,
) -> list[Any]:
    import audit_statecraft_archive_index as audit  # noqa: WPS433

    reg = registry if registry is not None else load_voice_index_registry_yaml()
    all_findings: list[Any] = []
    rows = collect_all_voice_registry_rows(archive_root=archive_root, registry=reg)
    voice_router_findings = audit.audit_voice_index()
    all_findings.extend(voice_router_findings)

    parity_pass = sum(1 for r in rows if r.parity == "pass")
    parity_fail = sum(1 for r in rows if r.parity == "fail")
    if parity_fail:
        all_findings.append(
            audit.AuditFinding(
                "fail",
                "archive_parity",
                f"{parity_pass}/{len(rows)} voice indexes pass parity ({parity_fail} fail)",
            )
        )
    else:
        all_findings.append(
            audit.AuditFinding(
                "pass",
                "archive_parity",
                f"{parity_pass}/{len(rows)} voice indexes pass parity",
            )
        )

    broken_total = sum(r.broken_links for r in rows)
    if broken_total:
        all_findings.append(
            audit.AuditFinding("fail", "broken_link", f"{broken_total} broken link(s) across voice indexes")
        )
    else:
        all_findings.append(
            audit.AuditFinding("pass", "broken_link", "no broken links in voice indexes")
        )

    for lite in validate_yaml_code_exclusion_parity(reg):
        all_findings.append(audit.AuditFinding(lite.level, lite.code, lite.message))

    documented = sum(1 for r in rows if r.exceptions)
    if documented:
        all_findings.append(
            audit.AuditFinding(
                "pass",
                "exceptions",
                f"{documented} voice index(es) with documented YAML exclusions",
            )
        )
    return all_findings


def generate_outputs(
    *,
    archive_root: Path = DEFAULT_ARCHIVE,
    slug_filter: str | None = None,
) -> tuple[list[VoiceRegistryRow], str, str]:
    rows = collect_all_voice_registry_rows(archive_root=archive_root, slug_filter=slug_filter)
    summary = build_summary(rows)
    return rows, render_registry_markdown(rows, summary), render_registry_json(rows, summary)
