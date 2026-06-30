#!/usr/bin/env python3
"""Thread- and channel-scoped ASR replacement tiers for source-clean."""

from __future__ import annotations

import re
from typing import Any

# (pattern, replacement, flags) — high-confidence mechanical fixes only.
TierPair = tuple[str, str, int]

COMMON_EXPERT_NAMES: list[TierPair] = [
    (r"Professor John Mirshimer", "Professor John Mearsheimer", 0),
    (r"Professor Mir Shimemer", "Professor Mearsheimer", 0),
    (r"Prof\. Mir Shimemer", "Prof. Mearsheimer", 0),
    (r"Professor Mio Shimmer", "Professor Mearsheimer", 0),
    (r"Professor Mio Shimmer", "Professor Mearsheimer", 0),
    (r"Mir Shimemer", "Mearsheimer", 0),
    (r"Mirshimer", "Mearsheimer", 0),
]

# Persian Gulf oil-terminal island — ASR often drifts to Kerguelen (subantarctic) or Karkand.
# Distinct from Kish (Hormuz-mouth); do not conflate. Receipt: Jermy Davis 2026-03-18 intake.
KHARG_TIER: list[TierPair] = [
    (r"\bKerguelen\b", "Kharg Island", 0),
    (r"\bKarkand Island\b", "Kharg Island", 0),
    (r"\bCarg Island\b", "Kharg Island", re.IGNORECASE),
    (r"\bKarkand\b", "Kharg", 0),
]

COMMON_GEO_TIERS: list[TierPair] = list(KHARG_TIER)

MEARSHEIMER_TIER: list[TierPair] = [
    (
        r"let's say about co pe pe pe pe pe pe pe pe pe pe pe pe pe pe pe\s*pe pe pe pe pe peaceful coexistence",
        "let's say about peaceful coexistence",
        re.IGNORECASE,
    ),
    (r"Manuria", "Manchuria", 0),
    (r"Skaku Islands", "Senkaku Islands", 0),
    (r"Dao Islands", "Diaoyu Islands", 0),
    (r"regional hegeimon", "regional hegemon", re.IGNORECASE),
    (r"regional hedgeimon", "regional hegemon", re.IGNORECASE),
    (r"a regional Herman", "a regional hegemon", re.IGNORECASE),
    (r"regional Herman", "regional hegemon", re.IGNORECASE),
    (r"hegeimon", "hegemon", re.IGNORECASE),
    (r"hedgeimon", "hegemon", re.IGNORECASE),
    (r"great paral politics", "great power politics", re.IGNORECASE),
    (r"Nom Chsky", "Chomsky", 0),
    (r"\bChsky\b", "Chomsky", 0),
    (r"Jeffree Sax", "Jeffrey Sachs", 0),
    (r"pit hexet", "Pete Hegseth", re.IGNORECASE),
    (r"Peter Hexith", "Pete Hegseth", 0),
    (r"\bHexith\b", "Hegseth", 0),
    (r"mchaveli", "Machiavelli", re.IGNORECASE),
    (r"machaveli", "Machiavelli", re.IGNORECASE),
    (r"makavelli", "Machiavelli", re.IGNORECASE),
    (r"Lynden Johnson", "Lyndon Johnson", 0),
    (r"four oblaststs", "four oblasts", re.IGNORECASE),
    (r"four oblassts", "four oblasts", re.IGNORECASE),
    (r"four oblas\b(?!t)", "four oblasts", re.IGNORECASE),
    (r"sweep system", "SWIFT system", re.IGNORECASE),
    (r"weapons grade file material", "weapons-grade fissile material", re.IGNORECASE),
    (r"weaponsgrade fizzol material", "weapons-grade fissile material", re.IGNORECASE),
    (r"produce fizzile material", "produce fissile material", re.IGNORECASE),
    (r"produce the file material", "produce the fissile material", re.IGNORECASE),
    (r"the file material", "the fissile material", re.IGNORECASE),
    (r"\bOkas\b", "AUKUS", 0),
    (r"\bAlcus\b", "AUKUS", 0),
    (r"rolling bricks together", "in BRICS together", re.IGNORECASE),
    (r"context of bricks", "context of BRICS", re.IGNORECASE),
    (r"per capita GMPP", "per capita GDP", re.IGNORECASE),
    (r"Rwan genocide", "Rwanda genocide", 0),
    (r"Tel Aiv", "Tel Aviv", re.IGNORECASE),
    (r"Anti S400", "S-400", 0),
    (r"postc colonial", "post-colonial", re.IGNORECASE),
    (r"nation stim", "nation-states", re.IGNORECASE),
    (r"South China Sina", "South China Sea", re.IGNORECASE),
    (r"milliondoll question", "million-dollar question", re.IGNORECASE),
    (r"visa v", "vis-à-vis", re.IGNORECASE),
    (r"ethnic Hungar ethnic", "ethnic Ukrainian", re.IGNORECASE),
    (r"IndiaPakistan", "India-Pakistan", 0),
    (r"USRussia", "US-Russia", 0),
    (r"handsoff", "hands-off", re.IGNORECASE),
    (r"chapter in verse", "chapter and verse", re.IGNORECASE),
    (r"zero some game", "zero-sum game", re.IGNORECASE),
    (r"before the Drake uh government drake government", "before the Derg government", re.IGNORECASE),
]

NAPOLITANO_TIER: list[TierPair] = [
    (r"Professor Mir Shimemer", "Professor Mearsheimer", 0),
    (r"Prof\. Mir Shimemer", "Prof. Mearsheimer", 0),
    (r"Mir Shimemer", "Mearsheimer", 0),
    (r"sumearily", "summarily", re.IGNORECASE),
]

INDIA_GLOBAL_LEFT_TIER: list[TierPair] = []

THREAD_TIERS: dict[str, list[TierPair]] = {
    "mearsheimer": MEARSHEIMER_TIER,
    "napolitano": NAPOLITANO_TIER,
    "mercouris": COMMON_EXPERT_NAMES,
    "diesen": COMMON_EXPERT_NAMES,
    "sachs": [
        (r"Jeffree Sax", "Jeffrey Sachs", 0),
        (r"Jeffrey Sax", "Jeffrey Sachs", 0),
    ],
    "freeman": [
        (r"Ambassador Chas Freeman", "Ambassador Chas Freeman", 0),
    ],
    "ritter": [
        (r"Scott Ritter", "Scott Ritter", 0),
    ],
    "kharg": KHARG_TIER,
}

CHANNEL_TIERS: dict[str, list[TierPair]] = {
    "india-global-left": INDIA_GLOBAL_LEFT_TIER,
    "judging-freedom": NAPOLITANO_TIER,
}

GUEST_TIER_ALIASES: dict[str, str] = {
    "john mearsheimer": "mearsheimer",
    "mearsheimer": "mearsheimer",
    "judge andrew napolitano": "napolitano",
    "napolitano": "napolitano",
}

def _parse_scalar_list(block: str, key: str) -> list[str]:
    lines = block.splitlines()
    in_key = False
    items: list[str] = []
    for line in lines:
        if re.match(rf"^{re.escape(key)}:\s*$", line):
            in_key = True
            continue
        if in_key:
            m = re.match(r"^\s+-\s+(.+)$", line)
            if m:
                items.append(m.group(1).strip().strip('"'))
                continue
            if re.match(r"^\S", line):
                break
        m = re.match(rf'^{re.escape(key)}:\s*"?([^"\n]+)"?\s*$', line)
        if m:
            return [m.group(1).strip()]
    return items

def parse_frontmatter(text: str) -> dict[str, Any]:
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    block = m.group(1)
    meta: dict[str, Any] = {}
    for key in (
        "thread",
        "thread_expert",
        "guest",
        "host",
        "channel_slug",
        "show_title",
        "channel_name",
    ):
        vals = _parse_scalar_list(block, key)
        if vals:
            meta[key] = vals[0] if len(vals) == 1 else vals
    for key in ("threads", "guest_people"):
        vals = _parse_scalar_list(block, key)
        if vals:
            meta[key] = vals
    return meta

def resolve_tier_keys(meta: dict[str, Any]) -> list[str]:
    keys: list[str] = []
    for field in ("thread_expert", "thread"):
        val = meta.get(field)
        if isinstance(val, str) and val.strip():
            keys.append(val.strip().lower())
    threads = meta.get("threads")
    if isinstance(threads, list):
        keys.extend(str(t).strip().lower() for t in threads if str(t).strip())
    guest = meta.get("guest")
    if isinstance(guest, str):
        alias = GUEST_TIER_ALIASES.get(guest.strip().lower())
        if alias:
            keys.append(alias)
    guest_people = meta.get("guest_people")
    if isinstance(guest_people, list):
        for g in guest_people:
            alias = GUEST_TIER_ALIASES.get(str(g).strip().lower())
            if alias:
                keys.append(alias)
    channel = meta.get("channel_slug")
    if isinstance(channel, str) and channel.strip():
        keys.append(f"channel:{channel.strip().lower()}")
    # de-dupe preserve order
    seen: set[str] = set()
    out: list[str] = []
    for k in keys:
        if k not in seen:
            seen.add(k)
            out.append(k)
    return out

def collect_tier_pairs(meta: dict[str, Any]) -> list[TierPair]:
    pairs: list[TierPair] = list(COMMON_GEO_TIERS)
    keys = resolve_tier_keys(meta)
    for key in keys:
        if key.startswith("channel:"):
            slug = key.split(":", 1)[1]
            pairs.extend(CHANNEL_TIERS.get(slug, []))
        else:
            pairs.extend(THREAD_TIERS.get(key, []))
    # Always run common expert name pass when any mapped guest/thread present
    if any(k in THREAD_TIERS or k.startswith("channel:") for k in keys):
        pairs = COMMON_EXPERT_NAMES + pairs
    # de-dupe pairs by pattern
    seen_pat: set[str] = set()
    unique: list[TierPair] = []
    for pat, repl, flags in pairs:
        if pat in seen_pat:
            continue
        seen_pat.add(pat)
        unique.append((pat, repl, flags))
    return unique

def apply_tier_pairs(text: str, pairs: list[TierPair]) -> tuple[str, int, dict[str, int]]:
    counts: dict[str, int] = {}
    total = 0
    out = text
    for pat, repl, flags in pairs:
        out, n = re.subn(pat, repl, out, flags=flags)
        if n:
            counts[pat[:40]] = n
            total += n
    return out, total, counts
