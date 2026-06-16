#!/usr/bin/env python3
"""Apply bounded common-ASR entity repairs across statecraft transcript corpora.

WORK only; not Record.

This pass targets a small set of high-confidence recurring name and chokepoint
garbles in transcript-bearing statecraft files.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = REPO_ROOT / "source-archive" / "statecraft"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
KIND_RE = re.compile(r"^kind:\s*([^\n]+)$", re.MULTILINE)
SOURCE_TYPE_RE = re.compile(r"^source_type:\s*([^\n]+)$", re.MULTILINE)
TRANSCRIPT_PREFIXES = (
    "transcript-",
    "youtube-",
    "judging-freedom-",
    "responsiblestatecraft-",
    "substack-",
)


@dataclass(frozen=True)
class ReplacementSpec:
    pattern: re.Pattern[str]
    replacement: str
    label: str


REPLACEMENT_SPECS: tuple[ReplacementSpec, ...] = (
    ReplacementSpec(
        re.compile(
            r"\b(?:straight|strait|street|trade|state)\s+of\s+(?:Hermuz|Hermus|Hermoose|moose|her\s+moose|her\s+mus|her\s+um)\b",
            re.IGNORECASE,
        ),
        "Strait of Hormuz",
        "hormuz_proper_noun_family",
    ),
    ReplacementSpec(re.compile(r"\bXiinping\b", re.IGNORECASE), "Xi Jinping", "xi_jinping"),
    ReplacementSpec(re.compile(r"\bWangi\b", re.IGNORECASE), "Wang Yi", "wang_yi"),
    ReplacementSpec(
        re.compile(r"\b(?:Bundra|Bund|Bunder|Bender|Bond|Bonder|Bander|Bad)\s+Abbas\b", re.IGNORECASE),
        "Bandar Abbas",
        "bandar_abbas",
    ),
    ReplacementSpec(
        re.compile(r"\b(?:Witgo|Witgov|Witoff|Witkov|Witco|Witcof|Witcoff|Whitov|Whitoff|Wickoff)\b", re.IGNORECASE),
        "Witkoff",
        "witkoff_name",
    ),
    ReplacementSpec(re.compile(r"\bKarg\s+Island\b", re.IGNORECASE), "Kharg Island", "kharg_island"),
    ReplacementSpec(re.compile(r"\bKarg\b", re.IGNORECASE), "Kharg", "kharg_island"),
    ReplacementSpec(
        re.compile(r"\b(?:Netanyao|Netanyah|Netanyo|Netanyahi|Netanyo|Netanyao's|Netanyah's|Netanyo's)\b", re.IGNORECASE),
        "Netanyahu",
        "netanyahu_name",
    ),
    ReplacementSpec(
        re.compile(r"\b(?:Ayatah|Ayatollah)\s+Ham\b", re.IGNORECASE),
        "Ayatollah Khamenei",
        "khamenei_title_name",
    ),
    ReplacementSpec(re.compile(r"\bKhamanei\b", re.IGNORECASE), "Khamenei", "khamenei_title_name"),
    ReplacementSpec(re.compile(r"\bWit\s+Gulf\b", re.IGNORECASE), "Witkoff", "witkoff_name"),
    ReplacementSpec(
        re.compile(r"\b(?:Npalitano|Napalitano|Napitano|Napolitono)\b", re.IGNORECASE),
        "Napolitano",
        "napolitano_name",
    ),
    ReplacementSpec(
        re.compile(r"\b(?:Abbas\s+Arachi|Abbas\s+Aragchi|Abbas\s+Araqchi)\b", re.IGNORECASE),
        "Abbas Araghchi",
        "araghchi_name",
    ),
    ReplacementSpec(
        re.compile(
            r"\b(?:Arachi|Aragchi|Araqchi|Arakchi|Arashi|Zarachi|Al\s+Arachi)\b",
            re.IGNORECASE,
        ),
        "Araghchi",
        "araghchi_name",
    ),
    ReplacementSpec(
        re.compile(
            r"\b(?:Peskin|Peskan|Peskian|Peskoff|Pesken|Peskyan|Pezishan|Pzishkan|Pzashkan|Pzeshkin|Pezkan|Peskran|Puzeshkian|Pezan|Pezishan|Pzishan|Pzeshkan|Peskian|Peskian)\b",
            re.IGNORECASE,
        ),
        "Pezeshkian",
        "pezeshkian_name",
    ),
    ReplacementSpec(re.compile(r"\bHexath\b", re.IGNORECASE), "Hegseth", "hegseth_hexath"),
    ReplacementSpec(re.compile(r"\bHegs\b", re.IGNORECASE), "Hegseth", "hegseth_hegs"),
    ReplacementSpec(re.compile(r"\bHexa\b", re.IGNORECASE), "Hegseth", "hegseth_hexa"),
    ReplacementSpec(re.compile(r"\bHacket\b", re.IGNORECASE), "Hegseth", "hegseth_hacket"),
    ReplacementSpec(re.compile(r"\bheg\s+Seth\b", re.IGNORECASE), "Hegseth", "hegseth_split"),
    ReplacementSpec(re.compile(r"\bheith\b", re.IGNORECASE), "Hegseth", "hegseth_heith"),
    ReplacementSpec(
        re.compile(r"\b(?:Hexeth|Hexth|Hexed|Hexedh|Hegsth|Hegth|Hegathth|Hgsith|Hegsef|Hagseth)\b", re.IGNORECASE),
        "Hegseth",
        "hegseth_tail_token",
    ),
    ReplacementSpec(
        re.compile(
            r"\b(?:Pete|Peter)\s+(?:Haga|Hax|Haxet|Hexet|Hexit|Hexith|Hexed|Hexeth|Hgse|Hegsth|Hagsth)\b",
            re.IGNORECASE,
        ),
        "Pete Hegseth",
        "hegseth_pete_variant",
    ),
    ReplacementSpec(
        re.compile(r"\bPete\s+Heg\s+says\b", re.IGNORECASE),
        "Pete Hegseth says",
        "hegseth_pete_phrase",
    ),
    ReplacementSpec(
        re.compile(r"\bPete\s+Hex(?:'s)?\s+head\b", re.IGNORECASE),
        "Pete Hegseth's head",
        "hegseth_pete_phrase",
    ),
    ReplacementSpec(
        re.compile(r"\bSecretary\s+of\s+War\s+Hagel\s+said\b", re.IGNORECASE),
        "Secretary of War Hegseth said",
        "hegseth_title_phrase",
    ),
    ReplacementSpec(re.compile(r"\bHegath\b", re.IGNORECASE), "Hegseth", "hegseth_hegath"),
    ReplacementSpec(re.compile(r"\bPete\s+Het\b", re.IGNORECASE), "Pete Hegseth", "hegseth_pete_variant"),
    ReplacementSpec(re.compile(r"\bHexith\b", re.IGNORECASE), "Hegseth", "hegseth_hexith"),
    ReplacementSpec(re.compile(r"\bSecretary\s+Hicks\b", re.IGNORECASE), "Secretary Hegseth", "hegseth_secretary_hicks"),
    ReplacementSpec(re.compile(r"\bSecretary\s+Hex\b", re.IGNORECASE), "Secretary Hegseth", "hegseth_secretary_hex"),
    ReplacementSpec(
        re.compile(
            r"\b(?:straight|strait)\s+of\s+(?:Formuz|Hermos|Hormos|Hormuse|form|horm)\b",
            re.IGNORECASE,
        ),
        "Strait of Hormuz",
        "hormuz_form_variant",
    ),
    ReplacementSpec(
        re.compile(r"\b(?:straight|strait)\s+of\s+horror\s+moves\b", re.IGNORECASE),
        "Strait of Hormuz",
        "hormuz_horror_moves",
    ),
    ReplacementSpec(
        re.compile(r"\b(?:straight|strait)\s+form\b", re.IGNORECASE),
        "Strait of Hormuz",
        "hormuz_straight_form",
    ),
    ReplacementSpec(re.compile(r"\bMcronone\b", re.IGNORECASE), "Macron", "macron_mcronone"),
    ReplacementSpec(re.compile(r"\bManuel\s+Mcronone\b", re.IGNORECASE), "Emmanuel Macron", "macron_manuel"),
    ReplacementSpec(re.compile(r"\bMorandi\b", re.IGNORECASE), "Marandi", "marandi_morandi"),
    ReplacementSpec(re.compile(r"\bMandi\b", re.IGNORECASE), "Marandi", "marandi_mandi"),
    ReplacementSpec(re.compile(r"\bMirandi\b", re.IGNORECASE), "Marandi", "marandi_mirandi"),
    ReplacementSpec(re.compile(r"\bZalinsky\b", re.IGNORECASE), "Zelensky", "zelensky_zalinsky"),
    ReplacementSpec(re.compile(r"\bZilinsky\b", re.IGNORECASE), "Zelensky", "zelensky_zilinsky"),
    ReplacementSpec(re.compile(r"\bGalibaf\b", re.IGNORECASE), "Qalibaf", "qalibaf_galibaf"),
    ReplacementSpec(re.compile(r"\bSmootrich\b", re.IGNORECASE), "Smotrich", "smotrich_smooth"),
    ReplacementSpec(re.compile(r"\bBen\s+Gabir\b", re.IGNORECASE), "Ben-Gvir", "ben_gvir_gabir"),
    ReplacementSpec(re.compile(r"\bBen\s+Gavir\b", re.IGNORECASE), "Ben-Gvir", "ben_gvir_gavir"),
    ReplacementSpec(re.compile(r"\bFouchy\b", re.IGNORECASE), "Fauci", "fauci_fouchy"),
    ReplacementSpec(re.compile(r"\bJen\s+Saki\b", re.IGNORECASE), "Jen Psaki", "psaki_jen_saki"),
    ReplacementSpec(re.compile(r"\bGabbert\b", re.IGNORECASE), "Gabbard", "gabbard_gabbert"),
    ReplacementSpec(re.compile(r"\bGambert\b", re.IGNORECASE), "Gabbard", "gabbard_gambert"),
    ReplacementSpec(re.compile(r"\bGammer\b", re.IGNORECASE), "Gabbard", "gabbard_gammer"),
    ReplacementSpec(re.compile(r"\bTelsey\b", re.IGNORECASE), "Tulsi Gabbard", "gabbard_telsey"),
    ReplacementSpec(re.compile(r"\bbolabs\b", re.IGNORECASE), "biolabs", "biolab_bolabs"),
    ReplacementSpec(re.compile(r"\bbolab\b", re.IGNORECASE), "biolab", "biolab_bolab"),
    ReplacementSpec(re.compile(r"\bThran\b", re.IGNORECASE), "Tehran", "tehran_thran"),
    ReplacementSpec(re.compile(r"\bNatani\s+River\b", re.IGNORECASE), "Litani River", "litani_natani"),
    ReplacementSpec(re.compile(r"\bhourong\b", re.IGNORECASE), "hour-long", "hourong"),
    ReplacementSpec(re.compile(r"\bEzbollah\b", re.IGNORECASE), "Hezbollah", "hezbollah_ezbollah"),
    ReplacementSpec(
        re.compile(r"\bcontrol\s+of\s+Isra\b", re.IGNORECASE),
        "control of Hormuz",
        "hormuz_isra_truncation",
    ),
    ReplacementSpec(
        re.compile(r"\b(?:straight|strait)\s+of\s+was\b", re.IGNORECASE),
        "Strait of Hormuz was",
        "hormuz_straight_of_was",
    ),
    ReplacementSpec(
        re.compile(r"\bthe\s+pay\s+um\s+uh\s+faction\b", re.IGNORECASE),
        "the Pezeshkian faction",
        "pezeshkian_pay_faction",
    ),
    ReplacementSpec(
        re.compile(
            r"\b(?:straight|strait|rate|trade)\s+of\s+(?:Formos|Formooze|Formoose|formos|foremost|home\s+moves|Horos|Hormosi|hormones|hormoose|firm)\b",
            re.IGNORECASE,
        ),
        "Strait of Hormuz",
        "hormuz_jun14_variant",
    ),
    ReplacementSpec(
        re.compile(r"\bstraight\s+of\s+horm\b", re.IGNORECASE),
        "Strait of Hormuz",
        "hormuz_straight_horm",
    ),
    ReplacementSpec(re.compile(r"\bAragshi\b", re.IGNORECASE), "Araghchi", "araghchi_aragshi"),
    ReplacementSpec(re.compile(r"\btulls\b", re.IGNORECASE), "tolls", "tolls_tulls"),
    ReplacementSpec(re.compile(r"\bNadia\b", re.IGNORECASE), "Netanyahu", "netanyahu_nadia"),
    ReplacementSpec(re.compile(r"\bNatalo\b", re.IGNORECASE), "Netanyahu", "netanyahu_natalo"),
    ReplacementSpec(re.compile(r"\bmarava\b", re.IGNORECASE), "Merkava", "merkava_marava"),
    ReplacementSpec(re.compile(r"\bNetno\b", re.IGNORECASE), "Netanyahu", "netanyahu_netno"),
    ReplacementSpec(
        re.compile(r"\b(?:straight|strait|trade|thread)\s+of\s+(?:formos|form\s+on|homes)\b", re.IGNORECASE),
        "Strait of Hormuz",
        "hormuz_formos_on",
    ),
    ReplacementSpec(
        re.compile(r"\b(?:trade|thread)\s+of\s+hormones\b", re.IGNORECASE),
        "Strait of Hormuz",
        "hormuz_thread_hormones",
    ),
    ReplacementSpec(
        re.compile(
            r"\b(?:Straighter?|straighter?)\s+(?:Hermoose|kmoose|kamoose|Hormoose)\b",
            re.IGNORECASE,
        ),
        "Strait of Hormuz",
        "hormuz_straighter_variant",
    ),
    ReplacementSpec(
        re.compile(
            r"\b(?:straight|strait)\s+(?:of\s+)?(?:kmoose|hermoose|hormoose|kamoose)\b",
            re.IGNORECASE,
        ),
        "Strait of Hormuz",
        "hormuz_kmoose_variant",
    ),
    ReplacementSpec(
        re.compile(r"\bstraight\s+hormuse\b", re.IGNORECASE),
        "Strait of Hormuz",
        "hormuz_straight_hormuse",
    ),
    ReplacementSpec(re.compile(r"\bFormoose\b", re.IGNORECASE), "Hormuz", "formoose_word"),
    ReplacementSpec(re.compile(r"\bBabel\s+Mandab\b", re.IGNORECASE), "Bab el-Mandeb", "bab_el_mandeb"),
)


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    raw = match.group(1)
    meta: dict[str, str] = {}
    kind = KIND_RE.search(raw)
    source_type = SOURCE_TYPE_RE.search(raw)
    if kind:
        meta["kind"] = kind.group(1).strip().strip('"')
    if source_type:
        meta["source_type"] = source_type.group(1).strip().strip('"')
    return meta


def is_transcript_like(path: Path, text: str) -> bool:
    if path.name == "README.md":
        return False
    meta = parse_frontmatter(text)
    kind = meta.get("kind", "").casefold()
    if "transcript" in kind:
        return True
    if meta.get("source_type"):
        return True
    if path.name.startswith(TRANSCRIPT_PREFIXES):
        return True
    if "not human-verified verbatim" in text.lower():
        return True
    return False


def apply_replacements(text: str) -> tuple[str, Counter[str]]:
    counts: Counter[str] = Counter()
    for spec in REPLACEMENT_SPECS:
        text, n = spec.pattern.subn(spec.replacement, text)
        if n:
            counts[spec.label] += n
    return text, counts


def fix_root(root: Path, *, write: bool) -> dict[str, object]:
    changed_files = 0
    total_replacements: Counter[str] = Counter()
    file_rows: list[dict[str, object]] = []
    for path in sorted(root.rglob("*.md")):
        original = path.read_text(encoding="utf-8", errors="replace")
        if not is_transcript_like(path, original):
            continue
        updated, counts = apply_replacements(original)
        if not counts:
            continue
        changed_files += 1
        total_replacements.update(counts)
        file_rows.append(
            {
                "path": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
                "replacements": dict(counts),
            }
        )
        if write:
            path.write_text(updated, encoding="utf-8", newline="\n")
    return {
        "changed_files": changed_files,
        "replacement_counts": dict(total_replacements),
        "files": file_rows,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Root directory to scan.")
    parser.add_argument("--write", action="store_true", help="Write fixes in place. Omit for dry run.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = fix_root(args.root.resolve(), write=args.write)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
