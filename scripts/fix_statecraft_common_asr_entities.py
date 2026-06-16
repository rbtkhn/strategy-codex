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
POLICY_SKIP_PATHS = frozenset(
    {
        ".cursor/rules/strategy-codex-kiev-spelling.mdc",
        "docs/skill-write/write-operator-preferences.md",
    }
)
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
    ReplacementSpec(re.compile(r"\bAmmanis\b", re.IGNORECASE), "Omanis", "omanis_ammanis"),
    ReplacementSpec(re.compile(r"\bArmanis\b", re.IGNORECASE), "Omanis", "omanis_armanis"),
    ReplacementSpec(re.compile(r"\bRick states\b", re.IGNORECASE), "BRICS states", "brics_rick_states"),
    ReplacementSpec(
        re.compile(r"\bdestabilization of the bricks payment\b", re.IGNORECASE),
        "destabilization of the BRICS payment",
        "brics_bricks_payment_destabilization",
    ),
    ReplacementSpec(re.compile(r"\bbricks payment\b", re.IGNORECASE), "BRICS payment", "brics_bricks_payment"),
    ReplacementSpec(re.compile(r"\bcrisis in the bricks\b", re.IGNORECASE), "crisis in BRICS", "brics_bricks_crisis"),
    ReplacementSpec(
        re.compile(r"\bin the bricks or in the BRICS payment\b", re.IGNORECASE),
        "in BRICS or in the BRICS payment",
        "brics_bricks_or_payment",
    ),
    ReplacementSpec(re.compile(r"\bConstantinfka\b", re.IGNORECASE), "Konstantinovka", "konstantinovka_constantinfka"),
    ReplacementSpec(re.compile(r"\bConstantinovka\b", re.IGNORECASE), "Konstantinovka", "konstantinovka_typo"),
    ReplacementSpec(
        re.compile(r"\bConstantin Donets(?:'s|'s)?\s+people's republic\b", re.IGNORECASE),
        "Konstantinovka, Donetsk People's Republic",
        "konstantinovka_constantin_donets",
    ),
    ReplacementSpec(re.compile(r"\bRudovka\b", re.IGNORECASE), "Readovka", "readovka_rudovka"),
    ReplacementSpec(re.compile(r"\bRayovka\b", re.IGNORECASE), "Readovka", "readovka_rayovka"),
    ReplacementSpec(re.compile(r"\bReedovska\b", re.IGNORECASE), "Readovka", "readovka_reedovska"),
    ReplacementSpec(re.compile(r"\bRaidovka\b", re.IGNORECASE), "Readovka", "readovka_raidovka"),
    ReplacementSpec(re.compile(r"\bReadofa\b", re.IGNORECASE), "Readovka", "readovka_readofa"),
    ReplacementSpec(re.compile(r"\bRaovvka\b", re.IGNORECASE), "Readovka", "readovka_raovvka"),
    ReplacementSpec(re.compile(r"\bReovka\b", re.IGNORECASE), "Readovka", "readovka_reovka"),
    ReplacementSpec(re.compile(r"\bRaovka\b", re.IGNORECASE), "Readovka", "readovka_raovka"),
    ReplacementSpec(re.compile(r"\bPakarovsk\b", re.IGNORECASE), "Pokrovsk", "pokrovsk_pakarovsk"),
    ReplacementSpec(re.compile(r"\bPakovsk\b", re.IGNORECASE), "Pokrovsk", "pokrovsk_pakovsk"),
    ReplacementSpec(re.compile(r"\bPacross\b", re.IGNORECASE), "Pokrovsk", "pokrovsk_pacross"),
    ReplacementSpec(re.compile(r"\bBakarovsk\b", re.IGNORECASE), "Pokrovsk", "pokrovsk_bakarovsk"),
    ReplacementSpec(
        re.compile(r"\bProsk and Mirnoglad\b", re.IGNORECASE),
        "Pokrovsk and Myrnohrad",
        "pokrovsk_prosk_mirnoglad",
    ),
    ReplacementSpec(re.compile(r"\bMirnoglad\b", re.IGNORECASE), "Myrnohrad", "myrnohrad_mirnoglad"),
    ReplacementSpec(re.compile(r"\bMirinoglad\b", re.IGNORECASE), "Myrnohrad", "myrnohrad_mirinoglad"),
    ReplacementSpec(re.compile(r"\bMir noad\b", re.IGNORECASE), "Myrnohrad", "myrnohrad_mir_noad"),
    ReplacementSpec(re.compile(r"\bMin Lugrad\b", re.IGNORECASE), "Myrnohrad", "myrnohrad_min_lugrad"),
    ReplacementSpec(re.compile(r"\bChasfya\b", re.IGNORECASE), "Chasiv Yar", "chasiv_yar_chasfya"),
    ReplacementSpec(re.compile(r"\bAmmani\b", re.IGNORECASE), "Omani", "omani_ammani"),
    ReplacementSpec(
        re.compile(r"\b(?:straight|strait)\s+of\s+corals\b", re.IGNORECASE),
        "Strait of Hormuz",
        "hormuz_corals_variant",
    ),
    ReplacementSpec(re.compile(r"\bfor the bricks\b", re.IGNORECASE), "for BRICS", "brics_for_the_bricks"),
    ReplacementSpec(re.compile(r"\bthe bricks and\b", re.IGNORECASE), "BRICS and", "brics_the_bricks_and"),
    ReplacementSpec(re.compile(r"\bunbalance balance the bricks\b", re.IGNORECASE), "unbalance the BRICS bloc", "brics_unbalance_bricks"),
    ReplacementSpec(re.compile(r"\bdevelopment of the of the bricks\b", re.IGNORECASE), "development of BRICS", "brics_development_bricks"),
    ReplacementSpec(re.compile(r"\bNetanyahuu+\b", re.IGNORECASE), "Netanyahu", "netanyahu_netanyahuu"),
    ReplacementSpec(re.compile(r"\bbricks order\b", re.IGNORECASE), "BRICS order", "brics_bricks_order"),
    ReplacementSpec(re.compile(r"\bScott Bessie\b", re.IGNORECASE), "Scott Bessent", "bessent_bessie"),
    ReplacementSpec(re.compile(r"\ball Ron's\b", re.IGNORECASE), "Iran's", "iran_all_rons"),
    ReplacementSpec(re.compile(r"\bZalinsk's\b", re.IGNORECASE), "Zelensky's", "zelensky_zalinsk_poss"),
    ReplacementSpec(re.compile(r"\bZalinsk\b", re.IGNORECASE), "Zelensky", "zelensky_zalinsk"),
    ReplacementSpec(re.compile(r"\bZilinski's\b", re.IGNORECASE), "Zelensky's", "zelensky_zilinski_poss"),
    ReplacementSpec(re.compile(r"\bZilinski\b", re.IGNORECASE), "Zelensky", "zelensky_zilinski"),
    ReplacementSpec(re.compile(r"\bZilinsk's\b", re.IGNORECASE), "Zelensky's", "zelensky_zilinsk_poss"),
    ReplacementSpec(re.compile(r"\bZilinsk\b", re.IGNORECASE), "Zelensky", "zelensky_zilinsk"),
    ReplacementSpec(re.compile(r"\bZalinski\b", re.IGNORECASE), "Zelensky", "zelensky_zalinski"),
    ReplacementSpec(re.compile(r"\bThrron\b", re.IGNORECASE), "Tehran", "tehran_thrron"),
    ReplacementSpec(re.compile(r"\bthis rate\b", re.IGNORECASE), "the Strait", "hormuz_this_rate"),
    ReplacementSpec(re.compile(r"\bConstantinoka\b", re.IGNORECASE), "Konstantinovka", "konstantinovka_constantinoka"),
    ReplacementSpec(re.compile(r"\bConstantineka\b", re.IGNORECASE), "Konstantinovka", "konstantinovka_constantineka"),
    ReplacementSpec(re.compile(r"\bChasfy\b", re.IGNORECASE), "Chasiv Yar", "chasiv_yar_chasfy"),
    ReplacementSpec(re.compile(r"\bChasy\b", re.IGNORECASE), "Chasiv Yar", "chasiv_yar_chasy"),
    ReplacementSpec(re.compile(r"\bKamatsk\b", re.IGNORECASE), "Kramatorsk", "kramatorsk_kamatsk"),
    # strategy-codex canonical spelling (operator policy): Kiev, not Kyiv, until revised.
    ReplacementSpec(re.compile(r"\bKyiv's\b", re.IGNORECASE), "Kiev's", "kiev_kyiv_poss"),
    ReplacementSpec(re.compile(r"\bKyiv\b", re.IGNORECASE), "Kiev", "kiev_kyiv_canonical"),
    ReplacementSpec(re.compile(r"\bKief\b", re.IGNORECASE), "Kiev", "kiev_kief_asr"),
    # strategy-codex canonical spelling (operator policy): Kharkov, not Kharkiv.
    ReplacementSpec(re.compile(r"\bKharkiv's\b", re.IGNORECASE), "Kharkov's", "kharkov_kharkiv_poss"),
    ReplacementSpec(re.compile(r"\bKharkiv\b", re.IGNORECASE), "Kharkov", "kharkov_kharkiv_canonical"),
    ReplacementSpec(re.compile(r"\bKharkof\b", re.IGNORECASE), "Kharkov", "kharkov_kharkof_asr"),
    ReplacementSpec(re.compile(r"\bKharkoff\b", re.IGNORECASE), "Kharkov", "kharkov_kharkoff_asr"),
    ReplacementSpec(re.compile(r"\bMirrad\b", re.IGNORECASE), "Myrnohrad", "myrnohrad_mirrad"),
)


def is_policy_skip(path: Path) -> bool:
    try:
        rel = path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return False
    return rel in POLICY_SKIP_PATHS


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
    if path.name.startswith("source-"):
        return True
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


def select_specs(only_labels: set[str] | None) -> tuple[ReplacementSpec, ...]:
    if not only_labels:
        return REPLACEMENT_SPECS
    return tuple(spec for spec in REPLACEMENT_SPECS if spec.label in only_labels)


URL_SEGMENT_RE = re.compile(r"https?://[^\s)>\]\"']+", re.IGNORECASE)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]\n]*\]\([^)\n]+\)")


def _merged_protected_spans(text: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    for pattern in (URL_SEGMENT_RE, MARKDOWN_LINK_RE):
        for match in pattern.finditer(text):
            spans.append((match.start(), match.end()))
    if not spans:
        return []
    spans.sort(key=lambda item: item[0])
    merged: list[tuple[int, int]] = [spans[0]]
    for start, end in spans[1:]:
        prev_start, prev_end = merged[-1]
        if start <= prev_end:
            merged[-1] = (prev_start, max(prev_end, end))
        else:
            merged.append((start, end))
    return merged


def _subn_outside_protected(text: str, spec: ReplacementSpec) -> tuple[str, int]:
    spans = _merged_protected_spans(text)
    if not spans:
        return spec.pattern.subn(spec.replacement, text)
    parts: list[str] = []
    total = 0
    cursor = 0
    for start, end in spans:
        chunk = text[cursor:start]
        chunk, n = spec.pattern.subn(spec.replacement, chunk)
        total += n
        parts.append(chunk)
        parts.append(text[start:end])
        cursor = end
    tail = text[cursor:]
    tail, n = spec.pattern.subn(spec.replacement, tail)
    total += n
    parts.append(tail)
    return "".join(parts), total


def apply_replacements(
    text: str,
    specs: tuple[ReplacementSpec, ...] | None = None,
) -> tuple[str, Counter[str]]:
    if specs is None:
        specs = REPLACEMENT_SPECS
    counts: Counter[str] = Counter()
    for spec in specs:
        text, n = _subn_outside_protected(text, spec)
        if n:
            counts[spec.label] += n
    return text, counts


def fix_root(
    root: Path,
    *,
    write: bool,
    any_markdown: bool = False,
    only_labels: set[str] | None = None,
) -> dict[str, object]:
    specs = select_specs(only_labels)
    changed_files = 0
    total_replacements: Counter[str] = Counter()
    file_rows: list[dict[str, object]] = []
    for path in sorted(root.rglob("*.md")):
        if is_policy_skip(path):
            continue
        original = path.read_text(encoding="utf-8", errors="replace")
        if not any_markdown and not is_transcript_like(path, original):
            continue
        updated, counts = apply_replacements(original, specs)
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
    parser.add_argument(
        "--any-markdown",
        action="store_true",
        help="Process any *.md under --root (not only transcript-like surfaces).",
    )
    parser.add_argument(
        "--only-labels",
        default="",
        help="Comma-separated replacement labels to apply (default: all).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    only_labels = {label.strip() for label in args.only_labels.split(",") if label.strip()} or None
    result = fix_root(
        args.root.resolve(),
        write=args.write,
        any_markdown=args.any_markdown,
        only_labels=only_labels,
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
