#!/usr/bin/env python3
"""
Export Civilizational Statecraft public book from statecraft/states/.

Usage:
  python scripts/export_civilizational_statecraft_public.py
  python scripts/export_civilizational_statecraft_public.py --dry-run
  python scripts/export_civilizational_statecraft_public.py --output path/to/civ-state-clone
  python scripts/export_civilizational_statecraft_public.py --volume china
  python scripts/export_civilizational_statecraft_public.py --output path/to/civ-state-clone --legacy-archive-only
  python scripts/validate_civilizational_statecraft_public.py [--exclude PREFIX ...] [--no-default-exclude] [export_dir]
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "config" / "civilizational_statecraft_public_export.yaml"
SOURCE_ROOT = REPO_ROOT / "statecraft" / "states"
TEMPLATE_ROOT = SOURCE_ROOT / "export-templates"

VOLUME_PREFIX_RE = re.compile(
    r"^civ-state-(?P<slug>china|persia|rome|russia|america)-"
)


def load_manifest() -> dict:
    if yaml is None:
        raise SystemExit("PyYAML required: pip install pyyaml")
    with MANIFEST_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def strip_work_fence(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if re.match(r"^\s*WORK only;?\s*not Record\.?\s*$", line, re.I):
            continue
        lines.append(line)
    out = "\n".join(lines).strip() + "\n"
    return re.sub(r"\n{3,}", "\n\n", out)


def rewrite_volume_links(text: str, volume_slugs: dict[str, str]) -> str:
    for folder, slug in volume_slugs.items():
        text = text.replace(f"volumes/{folder}/", f"volumes/{slug}/")
        text = text.replace(f"../volumes/{folder}/", f"../volumes/{slug}/")
        text = text.replace(f"../../volumes/{folder}/", f"../../volumes/{slug}/")
        text = text.replace(f"CIV-STATE {slug.title()}", slug.title())
        text = text.replace(f"[{slug.title()}]", f"[{slug.title()}]")
    text = re.sub(r"CIV-STATE ([A-Za-z]+)", lambda m: m.group(1), text)
    return text


def strip_operator_links(text: str) -> str:
    patterns = [
        r"^\s*- .*\[.*\]\([^)]*statecraft/[^)]+\).*\n",
        r"^\s*- .*\[.*\]\([^)]*singularity/workshop[^)]*\).*\n",
        r"^\s*- .*\[.*\]\([^)]*\.cursor/[^)]*\).*\n",
        r"^\s*- .*\[.*\]\([^)]*recursion-gate[^)]*\).*\n",
        r"^\s*- .*\[.*\]\([^)]*indexes/source-retrieval-matrix[^)]*\).*\n",
        r"^\s*- .*\[.*\]\([^)]*review-queue[^)]*\).*\n",
        r"^\s*- .*\[.*\]\([^)]*ph-civ[^)]*\).*\n",
        r"^\s*- .*\[.*\]\([^)]*game-substrate[^)]*\).*\n",
        r"^\s*- .*\[.*\]\([^)]*civ-state-game-systems-mapping[^)]*\).*\n",
        r"^\s*\d+\. .*\[.*\]\([^)]*game-substrate[^)]*\).*\n",
        r"^\s*\d+\. .*\[.*\]\([^)]*civ-state-game-systems-mapping[^)]*\).*\n",
    ]
    for pat in patterns:
        text = re.sub(pat, "", text, flags=re.I | re.M)
    text = re.sub(
        r"\[([^\]]+)\]\([^)]*statecraft/[^)]+\)",
        r"\1",
        text,
    )
    return text


def strip_ph_civ_prose(text: str) -> str:
    text = re.sub(r"(?i)PH-CIV", "public lecture corpus", text)
    text = re.sub(r"(?i)`ph-civ`", "external corpus", text)
    text = re.sub(r"(?i)ph-civ", "external corpus", text)
    text = re.sub(r"(?i)civ-mem", "evidence spine", text)
    text = re.sub(r"(?i)CIV-MEM", "evidence spine", text)
    return text


def rewrite_public_volume_asset_links(text: str, volume_slugs: dict[str, str]) -> str:
    for slug in volume_slugs.values():
        text = re.sub(
            rf"volumes/{re.escape(slug)}/civ-state-{re.escape(slug)}-shelf-reader\.md",
            f"volumes/{slug}/shelf-reader.md",
            text,
        )
        text = re.sub(
            rf"volumes/{re.escape(slug)}/civ-state-{re.escape(slug)}-bibliography\.md",
            f"volumes/{slug}/bibliography.md",
            text,
        )
    return text


def transform_toc_public(text: str, manifest: dict, volume_slugs: dict[str, str]) -> str:
    text = strip_work_fence(text)
    text = rewrite_volume_links(text, volume_slugs)
    text = rewrite_public_volume_asset_links(text, volume_slugs)

    public_appendix = """## Appendix. Whole-Work Apparatus

Use this layer when the problem is retrieval, comparison, or vocabulary rather than one civilization volume alone.

1. [Glossary](glossary.md)
2. [Volume Map](volumes/README.md)
3. [Civilizational Motion](framework/civilizational-motion.md)
4. [Civilizational Statecraft Framework](framework/civilization-empire-faith-science-memory-desire.md)
5. [Era Law](framework/era-law.md)
6. [Hybrid References](hybrid-references.md)
7. [Comparative Continuity](comparative/continuity-mechanism.md)
8. [Pattern Library](comparative/pattern-library/README.md)
9. [Index](index.md)
10. [Source-Lattice](source-lattice.md)

"""

    if "## Appendix. Whole-Work Apparatus" in text:
        text = re.sub(
            r"## Appendix\. Whole-Work Apparatus\n\n.*?(?=## Retrieval Order)",
            public_appendix,
            text,
            flags=re.S,
        )
    else:
        # Legacy two-volume TOC fallback
        block = re.search(
            r"(### Volume II\. Civilizational Statecraft and Retrieval\n\n"
            r"This volume teaches[^\n]+\n\n)"
            r"(1\. .*\n)"
            r"(2\. .*\n)"
            r"(3\. .*\n)"
            r"(4\. .*\n)"
            r"(5\. .*\n)?"
            r"(6\. .*\n)?"
            r"(7\. .*\n)?"
            r"(8\. .*\n)?",
            text,
            re.S,
        )
        if block:
            replacement = (
                block.group(1)
                + "1. [Civilizational Statecraft Framework](framework/civilization-empire-faith-science-memory-desire.md)\n"
                + "2. [Hybrid References](hybrid-references.md)\n"
                + "3. [Index](index.md)\n"
                + "4. [Source-Lattice](source-lattice.md)\n"
                + "5. [Comparative Continuity](comparative/continuity-mechanism.md)\n"
                + "6. [Pattern Library](comparative/pattern-library/README.md)\n"
            )
            text = text[: block.start()] + replacement + text[block.end() :]
        text = re.sub(
            r"5\. \[Source Retrieval Matrix\][^\n]+\n",
            "",
            text,
        )

    text = re.sub(
        r"(## Retrieval Order\n\nUse the whole-work apparatus[^\n]+\n\n)"
        r"(1\. \[Civilization and Empire\][^\n]+\n)"
        r"(2\. \[Reader Guide\][^\n]+\n)"
        r"(3\. \[Table of Contents\][^\n]+\n)"
        r"(4\. the relevant volume[^\n]+\n)"
        r"(5\. the relevant[^\n]+\n)"
        r"6\. the relevant volume `sacred-grammar\.md`[^\n]+\n"
        r"7\. \[Source Retrieval Matrix\][^\n]+\n",
        r"\1\2\3\4\5\6. the relevant volume [sacred-grammar.md](reader-guide.md#sacred-grammar-volume-local) when legitimacy governs\n"
        r"7. [Source-Lattice](source-lattice.md) when the volume front door alone is too broad\n",
        text,
        count=1,
    )
    return strip_operator_links(strip_ph_civ_prose(text))


def transform_index_public(text: str, manifest: dict, volume_slugs: dict[str, str]) -> str:
    text = strip_work_fence(text)
    text = rewrite_volume_links(text, volume_slugs)
    drop_lines = [
        "ph-civ-promotion-ledger",
        "ph-civ-to-civ-state-bridge",
        "review-queue",
        "source-retrieval-matrix",
        "game-substrate",
        "civ-state-game-systems-mapping",
        "PH-CIV",
        "ph-civ",
    ]
    lines = []
    for line in text.splitlines():
        if any(d in line for d in drop_lines):
            continue
        lines.append(line)
    text = "\n".join(lines) + "\n"
    text = re.sub(
        r"pattern-library/",
        "comparative/pattern-library/",
        text,
    )
    text = re.sub(
        r"\]\(continuity-mechanism\.md\)",
        "](comparative/continuity-mechanism.md)",
        text,
    )
    text = re.sub(
        r"\]\(high-skill-labor-compression",
        "](comparative/high-skill-labor-compression",
        text,
    )
    return strip_ph_civ_prose(strip_operator_links(text))


def transform_hybrid_references_public(text: str, manifest: dict, volume_slugs: dict[str, str]) -> str:
    text = strip_work_fence(text)
    text = rewrite_volume_links(text, volume_slugs)
    # Remove Upstream Authority Layers section through CIV-STATE paragraph header
    text = re.sub(
        r"## Upstream Authority Layers\n\n.*?## Primary-Source Preference\n",
        "## Primary-Source Preference\n",
        text,
        flags=re.S,
    )
    text = re.sub(
        r"## Companion Surfaces\n\n.*",
        "",
        text,
        flags=re.S,
    )
    text = strip_ph_civ_prose(strip_operator_links(text))
    text = re.sub(
        r"pattern-library/",
        "comparative/pattern-library/",
        text,
    )
    return text


def rewrite_absolute_links(text: str, volume_slugs: dict[str, str]) -> str:
    for folder, slug in volume_slugs.items():
        text = re.sub(
            rf"\]\(/C:/dev/strategy-codex/statecraft/states/volumes/{re.escape(folder)}/README\.md\)",
            r"](README.md)",
            text,
        )
        text = re.sub(
            rf"\]\(/C:/dev/strategy-codex/statecraft/states/volumes/{re.escape(folder)}/([^)]+)\)",
            rf"](\1)",
            text,
        )
        text = re.sub(
            rf"\]\(/C:/dev/strategy-codex/statecraft/states/volumes/{re.escape(folder)}/sacred-grammar\.md\)",
            r"](sacred-grammar.md)",
            text,
        )
    text = re.sub(
        r"\[[^\]]+\]\(/C:/dev/strategy-codex/research/repos/civilization_memory[^)]+\)",
        "the volume bibliography and primary shelves",
        text,
    )
    text = re.sub(r"\]\(/C:/dev/strategy-codex/[^)]+\)", r"](README.md)", text)
    text = re.sub(r"(?i)strategy-codex", "upstream workshop", text)
    return text


def public_surface_transform(text: str, manifest: dict, volume_slugs: dict[str, str]) -> str:
    text = strip_work_fence(text)
    text = rewrite_volume_links(text, volume_slugs)
    text = rewrite_absolute_links(text, volume_slugs)
    text = strip_operator_links(text)
    text = strip_ph_civ_prose(text)
    return text


def transform_reader_guide_public(text: str, manifest: dict, volume_slugs: dict[str, str]) -> str:
    return public_surface_transform(text, manifest, volume_slugs)


def transform_high_skill_public(text: str, manifest: dict, volume_slugs: dict[str, str]) -> str:
    text = public_surface_transform(text, manifest, volume_slugs)
    text = re.sub(
        r"^\s*- .*\[.*\]\(\.\./\.\./essays/[^)]+\).*\n",
        "",
        text,
        flags=re.M,
    )
    return text


def transform_hormuz_public(text: str, manifest: dict, volume_slugs: dict[str, str]) -> str:
    text = public_surface_transform(text, manifest, volume_slugs)
    text = text.replace(
        "3. Cite PH-CIV or legacy CIV-MEM only when upstream provenance is needed and no CIV-STATE object yet carries the claim.",
        "3. Cite primary sources and volume-local shelves when upstream provenance is needed and this comparative object alone does not carry the claim.",
    )
    text = re.sub(
        r"2\. Cite lane-local Iran geo, peace, helix, and transaction files[^\n]+\n",
        "2. Cite Persia volume geo-strategy, statecraft, and shelf layers for operational translation.\n",
        text,
    )
    return strip_ph_civ_prose(strip_operator_links(text))


TRANSFORMS = {
    "strip_work_fence": lambda t, m, vs: strip_work_fence(t),
    "toc_public": transform_toc_public,
    "index_public": transform_index_public,
    "hybrid_references_public": transform_hybrid_references_public,
    "reader_guide_public": transform_reader_guide_public,
    "high_skill_public": transform_high_skill_public,
    "hormuz_public": transform_hormuz_public,
}


def apply_transform(name: str, text: str, manifest: dict) -> str:
    volume_slugs = manifest["volume_slugs"]
    fn = TRANSFORMS.get(name, lambda t, m, vs: strip_work_fence(t))
    return fn(text, manifest, volume_slugs)


def link_prefix(dest_rel: Path) -> str:
    depth = len(dest_rel.parts) - 1
    return "../" * depth


def finalize_public_markdown(text: str, dest_rel: Path, volume_slugs: dict[str, str]) -> str:
    prefix = link_prefix(dest_rel)
    for folder, slug in volume_slugs.items():
        text = text.replace(f"volumes/{folder}/", f"volumes/{slug}/")
        text = re.sub(
            rf"volumes/{re.escape(folder)}/{re.escape(folder)}-bibliography\.md",
            f"volumes/{slug}/bibliography.md",
            text,
        )
        text = re.sub(
            rf"volumes/{re.escape(slug)}/civ-state-{slug}-bibliography\.md",
            f"volumes/{slug}/bibliography.md",
            text,
        )
        text = re.sub(
            rf"volumes/{re.escape(slug)}/civ-state-{slug}-primary-sources-([a-z]+)\.md",
            rf"volumes/{slug}/sources/primary/\1.md",
            text,
        )
        text = re.sub(
            rf"volumes/{re.escape(slug)}/civ-state-{slug}-secondary-sources-([a-z]+)\.md",
            rf"volumes/{slug}/sources/secondary/\1.md",
            text,
        )
        text = re.sub(
            rf"\.\./volumes/{re.escape(folder)}/civ-state-{slug}-primary-sources-([a-z]+)\.md",
            rf"../volumes/{slug}/sources/primary/\1.md",
            text,
        )
        text = re.sub(
            rf"\.\./volumes/{re.escape(folder)}/civ-state-{slug}-secondary-sources-([a-z]+)\.md",
            rf"../volumes/{slug}/sources/secondary/\1.md",
            text,
        )

    framework = f"{prefix}framework/civilization-empire-faith-science-memory-desire.md"
    text = re.sub(
        r"\]\((?:\.\./)*(?:framework/)?civilization-empire-faith-science-memory-desire\.md\)",
        f"]({framework})",
        text,
    )
    if dest_rel.parts[:1] == ("comparative",):
        comparative_path = "continuity-mechanism.md"
    else:
        comparative_path = f"{prefix}comparative/continuity-mechanism.md"
    text = re.sub(
        r"\]\((?:\.\./)*continuity-mechanism\.md\)",
        f"]({comparative_path})",
        text,
    )
    text = re.sub(
        r"\]\((?:\.\./)*pattern-library/",
        f"]({prefix}comparative/pattern-library/",
        text,
    )
    if dest_rel.parts[:1] == ("framework",):
        for root_doc in (
            "reader-guide.md",
            "glossary.md",
            "index.md",
            "table-of-contents.md",
            "introduction.md",
            "hybrid-references.md",
            "volumes/README.md",
        ):
            text = re.sub(
                rf"\]\((?:\.\./)*{re.escape(root_doc)}",
                f"](../{root_doc}",
                text,
            )
        text = re.sub(
            r"\]\(\.\./framework/civilization-empire-faith-science-memory-desire\.md\)",
            "](civilization-empire-faith-science-memory-desire.md)",
            text,
        )
        text = re.sub(
            r"\]\(\.\./civilization-empire-faith-science-memory-desire\.md\)",
            "](civilization-empire-faith-science-memory-desire.md)",
            text,
        )
        text = re.sub(
            r"\]\((?:\.\./)*framework/era-law\.md\)",
            "](era-law.md)",
            text,
        )
        text = re.sub(
            r"\]\((?:\.\./)*framework/civilizational-motion\.md\)",
            "](civilizational-motion.md)",
            text,
        )
    if dest_rel.parts[:1] == ("comparative",):
        readme = "../README.md"
    elif dest_rel.parts[:1] == ("framework",):
        readme = "../README.md"
    elif dest_rel.parts[:2] == ("volumes",):
        readme = "../../README.md"
    else:
        readme = "README.md"
    text = re.sub(r"\]\((?:\.\./)*README\.md\)", f"]({readme})", text)

    strip_targets = (
        "indexes/",
        "migration/",
        "research/",
        "statecraft/",
        "../statecraft",
        "../../persia/",
        "../../china/",
        "../../america/",
        "../../russia/",
        "../../iran/",
        "../../../iran/",
        "../../rome/",
        "../../../rome/",
        "../iran/",
        "transactions/",
        "../sheets/",
        "current-sovereign-heads",
        "sovereign-continuity.md",
        "sovereign-continuity-of-the-civ",
        "civilization_memory",
        "/C:/",
    )

    def strip_bad_link(match: re.Match[str]) -> str:
        label, target = match.group(1), match.group(2)
        if any(bad in target for bad in strip_targets):
            return label
        return match.group(0)

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", strip_bad_link, text)
    for slug in volume_slugs.values():
        text = re.sub(
            rf"\]\(civ-state-{slug}-primary-sources-([a-z]+)\.md\)",
            r"](sources/primary/\1.md)",
            text,
        )
        text = re.sub(
            rf"\]\(civ-state-{slug}-secondary-sources-([a-z]+)\.md\)",
            r"](sources/secondary/\1.md)",
            text,
        )
        text = re.sub(
            rf"\]\(civ-state-{slug}-shelf-reader\.md\)",
            r"](shelf-reader.md)",
            text,
        )
        text = re.sub(
            rf"\]\(civ-state-{slug}-bibliography\.md\)",
            r"](bibliography.md)",
            text,
        )

    if dest_rel.parts[:1] == ("volumes",) and "sources" in dest_rel.parts:
        ups = "../" * (len(dest_rel.parts) - 3)
        text = re.sub(
            r"\]\((bibliography\.md|civilization-[^)]+\.md|empire-[^)]+\.md|introduction\.md|shelf-reader\.md)\)",
            rf"]({ups}\1)",
            text,
        )
        if "secondary" in dest_rel.parts:
            text = re.sub(r"\]\(sources/primary/", r"](../primary/", text)

    depth = len(dest_rel.parts) - 1
    up = "../" * depth if depth else ""
    if depth == 1 and dest_rel.parts[0] == "comparative" and len(dest_rel.parts) == 2:
        text = re.sub(r"\]\(volumes/", r"](../volumes/", text)
    if depth >= 2:
        text = re.sub(r"\]\(\.\./volumes/", f"]({'../' * depth}volumes/", text)
        text = re.sub(r"\]\(\.\./glossary\.md\)", f"]({'../' * depth}glossary.md)", text)
        text = re.sub(
            r"\]\(continuity-mechanism\.md\)",
            f"]({'../' * (depth - 1)}continuity-mechanism.md)",
            text,
        )
    text = re.sub(
        r"with retrieval discipline reinforced by [^.]+\.",
        "with retrieval discipline reinforced by the index and source-lattice.",
        text,
    )
    return text


def write_public_file(output: Path, dest_rel: Path, content: str, manifest: dict, dry_run: bool) -> None:
    content = finalize_public_markdown(content, dest_rel, manifest["volume_slugs"])
    write_text(output / dest_rel, content, dry_run)


VOLUME_WORKSHOP_ONLY = frozenset({"sovereign-continuity.md"})


def should_export_volume_file(src_name: str, slug: str, manifest: dict) -> bool:
    if src_name in VOLUME_WORKSHOP_ONLY or src_name.startswith("statecraft-"):
        return False
    if src_name == "README.md":
        return True
    if src_name.startswith(f"civ-state-{slug}-"):
        return True
    for pattern in manifest.get("volume_essay_globs", []):
        if fnmatch.fnmatch(src_name, pattern):
            return True
    return False


def prune_legacy_volume_artifacts(output: Path, manifest: dict, dry_run: bool) -> list[str]:
    """Remove workshop-only volume files that must not ship in the public book."""
    removed: list[str] = []
    for slug in manifest.get("volume_slugs", {}).values():
        vol_dir = output / "volumes" / slug
        if not vol_dir.is_dir():
            continue
        for pattern in ("statecraft-*.md", "sovereign-continuity.md"):
            for path in vol_dir.glob(pattern):
                rel = str(path.relative_to(output))
                if not dry_run:
                    path.unlink()
                removed.append(rel)
    return removed


def volume_dest_path(src_name: str, vol_folder: str, slug: str) -> Path | None:
    if src_name == "README.md":
        return Path("volumes") / slug / "README.md"
    m = VOLUME_PREFIX_RE.match(src_name)
    if m and m.group("slug") == slug:
        rest = src_name[len(f"civ-state-{slug}-") :]
        if rest == "shelf-reader.md":
            return Path("volumes") / slug / "shelf-reader.md"
        if rest == "bibliography.md":
            return Path("volumes") / slug / "bibliography.md"
        pm = re.match(r"primary-sources-([a-z]+)\.md$", rest)
        if pm:
            return Path("volumes") / slug / "sources" / "primary" / f"{pm.group(1)}.md"
        sm = re.match(r"secondary-sources-([a-z]+)\.md$", rest)
        if sm:
            return Path("volumes") / slug / "sources" / "secondary" / f"{sm.group(1)}.md"
    if src_name.endswith(".md") and not src_name.startswith("civ-state-"):
        return Path("volumes") / slug / src_name
    return None


def export_volume(vol_folder: str, slug: str, manifest: dict, output: Path, dry_run: bool) -> list[str]:
    written: list[str] = []
    src_dir = SOURCE_ROOT / "volumes" / vol_folder
    if not src_dir.is_dir():
        return written
    essay_globs = manifest.get("volume_essay_globs", ["*.md"])
    for path in sorted(src_dir.iterdir()):
        if not path.is_file() or path.suffix != ".md":
            continue
        if not should_export_volume_file(path.name, slug, manifest):
            continue
        dest_rel = volume_dest_path(path.name, vol_folder, slug)
        if dest_rel is None:
            continue
        content = read_text(path)
        content = apply_transform("reader_guide_public", content, manifest)
        if slug == "rome" and path.name == "README.md":
            caveat = manifest.get("volume_stubs", {}).get("rome", {}).get("reader_caveat", "")
            if caveat and "**Preview**" not in content:
                content = content.replace(
                    "# CIV-STATE Rome",
                    "# Rome\n\n**Preview volume.** " + caveat.strip(),
                    1,
                )
                content = content.replace("# CIV-STATE Rome", "# Rome", 1)
        write_public_file(output, dest_rel, content, manifest, dry_run)
        written.append(str(dest_rel))
    return written


def render_template(name: str, manifest: dict) -> str:
    path = TEMPLATE_ROOT / name
    text = read_text(path)
    return text.replace("{{RELEASE_TAG}}", manifest.get("release_tag", "v0.1.0"))


def export_apparatus(manifest: dict, output: Path, dry_run: bool) -> list[str]:
    written: list[str] = []
    for item in manifest.get("apparatus", []):
        src = SOURCE_ROOT / item["src"]
        dest = output / item["dest"]
        if not src.is_file():
            print(f"WARN missing apparatus source: {src}", file=sys.stderr)
            continue
        content = apply_transform(item["transform"], read_text(src), manifest)
        dest_rel = Path(item["dest"])
        write_public_file(output, dest_rel, content, manifest, dry_run)
        written.append(item["dest"])
    for item in manifest.get("directories", []):
        src_dir = SOURCE_ROOT / item["src"]
        dest_dir = output / item["dest"]
        if not src_dir.is_dir():
            continue
        for path in sorted(src_dir.rglob("*.md")):
            rel = path.relative_to(src_dir)
            dest_rel = Path(item["dest"]) / rel
            content = apply_transform(item["transform"], read_text(path), manifest)
            write_public_file(output, dest_rel, content, manifest, dry_run)
            written.append(str(dest_rel))
    return written


def export_generated(manifest: dict, output: Path, dry_run: bool, written: list[str]) -> None:
    for item in manifest.get("generated", []):
        dest = output / item["dest"]
        gen = item.get("generator")
        if gen == "manifest_snapshot":
            snap = {
                "schema_version": manifest.get("schema_version"),
                "release_tag": manifest.get("release_tag"),
                "canonical_public_repo": manifest.get("canonical_public_repo"),
                "volume_slugs": manifest.get("volume_slugs"),
                "era_spine": manifest.get("era_spine"),
                "volume_stubs": manifest.get("volume_stubs", {}),
            }
            content = "# Public export manifest snapshot\n\n```yaml\n" + yaml.dump(snap, sort_keys=False) + "```\n"
        elif gen == "export_receipt":
            content = (
                f"# Export Receipt\n\n"
                f"- **Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n"
                f"- **Release tag:** {manifest.get('release_tag')}\n"
                f"- **Files written:** {len(written)}\n"
                f"- **Manifest:** `config/civilizational_statecraft_public_export.yaml`\n"
                f"- **Script:** `scripts/export_civilizational_statecraft_public.py`\n"
            )
        elif gen == "version_stamp":
            content = manifest.get("release_tag", "v0.1.0") + "\n"
        else:
            content = render_template(item["template"], manifest)
        write_text(dest, content, dry_run)
        written.append(item["dest"])


def lint_output(
    output: Path, manifest: dict, exclude_prefixes: tuple[str, ...] = ()
) -> list[str]:
    errors: list[str] = []
    patterns = manifest.get("forbidden_patterns", [])
    for path in output.rglob("*.md"):
        rel = path.relative_to(output)
        if is_excluded(rel, exclude_prefixes):
            continue
        text = read_text(path)
        for pat in patterns:
            if pat.lower() in text.lower():
                errors.append(f"{rel}: forbidden pattern `{pat}`")
    return errors


def is_excluded(rel: Path, exclude_prefixes: tuple[str, ...]) -> bool:
    if not exclude_prefixes:
        return False
    rel_posix = rel.as_posix()
    parts = rel_posix.split("/")
    if parts and parts[0] in exclude_prefixes:
        return True
    return any(rel_posix.startswith(f"{p}/") for p in exclude_prefixes)


LEGACY_LINK_STRIP_TARGETS = (
    "indexes/",
    "migration/",
    "research/",
    "statecraft/",
    "../statecraft",
    "../../persia/",
    "../../china/",
    "../../america/",
    "../../russia/",
    "../../iran/",
    "../../../iran/",
    "../../rome/",
    "../../../rome/",
    "../iran/",
    "transactions/",
    "../sheets/",
    "../../sheets/",
    "../../../sheets/",
    "speakers/",
    "years/",
    "singularity/",
    "current-sovereign-heads",
    "sovereign-continuity-of-the-civ",
    "civilization_memory",
    "/C:/",
    ".cursor/",
    "recursion-gate",
    "ph-civ",
    "templates/",
    "lenses/",
    "../lenses/",
    "hormuz-strait-transit",
    "hormuz-reciprocal-transit",
    "strategy-codex",
)


def strip_legacy_links(text: str) -> str:
    def strip_bad_link(match: re.Match[str]) -> str:
        label, target = match.group(1), match.group(2)
        lower = target.lower()
        if target.startswith("http"):
            if "ph-civ" in lower or "strategy-codex" in lower:
                return label
            return match.group(0)
        if any(bad in target for bad in LEGACY_LINK_STRIP_TARGETS):
            return label
        return match.group(0)

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", strip_bad_link, text)


def strip_unresolvable_relative_links(text: str, file_path: Path, root: Path) -> str:
    link_re = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    def fix(match: re.Match[str]) -> str:
        label, target = match.group(1), match.group(2)
        if target.startswith("http") or target.startswith("#"):
            return match.group(0)
        clean = target.split("#")[0]
        if not clean:
            return match.group(0)
        dest = (file_path.parent / clean).resolve()
        try:
            dest.relative_to(root.resolve())
        except ValueError:
            return label
        if not dest.exists():
            return label
        return match.group(0)

    return link_re.sub(fix, text)


def sanitize_legacy_markdown(text: str, manifest: dict) -> str:
    volume_slugs = manifest["volume_slugs"]
    text = strip_work_fence(text)
    text = rewrite_volume_links(text, volume_slugs)
    text = rewrite_absolute_links(text, volume_slugs)
    text = strip_operator_links(text)
    text = strip_ph_civ_prose(text)
    text = re.sub(r"(?i)strategy-codex", "upstream workshop", text)
    text = re.sub(r"(?i)WORK only;?\s*not Record\.?", "", text)
    text = strip_legacy_links(text)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def sanitize_legacy_archive(archive_root: Path, manifest: dict, dry_run: bool) -> list[str]:
    touched: list[str] = []
    if not archive_root.is_dir():
        return touched
    for path in sorted(archive_root.rglob("*.md")):
        rel = path.relative_to(archive_root)
        original = read_text(path)
        content = sanitize_legacy_markdown(original, manifest)
        content = strip_unresolvable_relative_links(content, path, archive_root)
        if content != original:
            write_text(path, content, dry_run)
            touched.append(str(rel))
    return touched


def resolve_legacy_archive_dir(output: Path, manifest: dict) -> Path | None:
    legacy = manifest.get("legacy_archive") or {}
    rel = legacy.get("rel_path")
    if not rel:
        return None
    candidate = output / rel
    return candidate if candidate.is_dir() else None


def hash_tree(output: Path) -> str:
    h = hashlib.sha256()
    for path in sorted(output.rglob("*")):
        if path.is_file():
            h.update(str(path.relative_to(output)).encode())
            h.update(path.read_bytes())
    return h.hexdigest()[:16]


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Civilizational Statecraft public book")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--volume", choices=["china", "persia", "rome", "russia", "america"], default=None)
    parser.add_argument("--skip-lint", action="store_true")
    parser.add_argument(
        "--sanitize-legacy-archive",
        action="store_true",
        help="Sanitize archive/helix-lane-v1/legacy-cut under --output when present.",
    )
    parser.add_argument(
        "--legacy-archive-only",
        action="store_true",
        help="Only sanitize legacy archive under --output; skip book export.",
    )
    args = parser.parse_args()

    manifest = load_manifest()
    output = args.output or REPO_ROOT / manifest.get("default_output", "artifacts/civilizational-statecraft-public")
    volume_slugs = manifest["volume_slugs"]
    legacy_cfg = manifest.get("legacy_archive") or {}
    should_sanitize = args.sanitize_legacy_archive or legacy_cfg.get("sanitize", False)

    if args.legacy_archive_only:
        archive_dir = resolve_legacy_archive_dir(output, manifest)
        if archive_dir is None:
            print(f"Legacy archive not found under {output}", file=sys.stderr)
            return 1
        touched = sanitize_legacy_archive(archive_dir, manifest, args.dry_run)
        if args.dry_run:
            print(f"DRY RUN would sanitize {len(touched)} files under {archive_dir}")
            return 0
        if not args.skip_lint:
            errors = lint_output(output, manifest)
            if errors:
                print("LEGACY ARCHIVE LINT FAILED:", file=sys.stderr)
                for err in errors[:40]:
                    print(f"  {err}", file=sys.stderr)
                return 1
        print(f"Sanitized {len(touched)} legacy archive files under {archive_dir}")
        return 0

    if not args.dry_run and output.exists() and args.volume is None:
        shutil.rmtree(output)
    if not args.dry_run:
        output.mkdir(parents=True, exist_ok=True)

    written: list[str] = []

    if args.volume is None:
        written.extend(export_apparatus(manifest, output, args.dry_run))
        export_generated(manifest, output, args.dry_run, written)
        vol_items = volume_slugs.items()
    else:
        vol_items = [(k, v) for k, v in volume_slugs.items() if v == args.volume]

    for vol_folder, slug in vol_items:
        written.extend(export_volume(vol_folder, slug, manifest, output, args.dry_run))

    if not args.dry_run:
        pruned = prune_legacy_volume_artifacts(output, manifest, False)
        if pruned:
            print(f"Pruned {len(pruned)} legacy volume file(s)")

    if args.dry_run:
        print(f"DRY RUN would write {len(written)} files to {output}")
        return 0

    archive_dir = resolve_legacy_archive_dir(output, manifest)
    if should_sanitize and archive_dir is not None:
        touched = sanitize_legacy_archive(archive_dir, manifest, False)
        if touched:
            print(f"Sanitized {len(touched)} legacy archive files under {archive_dir}")

    if not args.skip_lint:
        errors = lint_output(output, manifest)
        if errors:
            print("EXPORT LINT FAILED:", file=sys.stderr)
            for err in errors[:40]:
                print(f"  {err}", file=sys.stderr)
            if len(errors) > 40:
                print(f"  ... and {len(errors) - 40} more", file=sys.stderr)
            return 1

    tree_hash = hash_tree(output)
    receipt_path = output / "EXPORT-RECEIPT.md"
    if receipt_path.exists():
        extra = f"- **Tree hash:** `{tree_hash}`\n"
        prev = read_text(receipt_path)
        if "**Tree hash:**" not in prev:
            write_text(receipt_path, prev.rstrip() + "\n" + extra, False)

    print(f"Exported {len(written)} files to {output}")
    print(f"Tree hash: {tree_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
