#!/usr/bin/env python3
"""source-section batch — May 28, 2026 Nawfal triple (Barnes + Parsi + Kent).

Verify: python scripts/patch_2026_05_28_nawfal_triple_sections.py --check-anchors
Apply:  python scripts/patch_2026_05_28_nawfal_triple_sections.py --apply
Apply one: python scripts/patch_2026_05_28_nawfal_triple_sections.py --apply --only barnes
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcript_section_curation import (  # noqa: E402
    find_anchor_pos,
    normalize_for_anchor,
    write_sectioned_capture,
)

CAPTURES: dict[str, dict] = {
    "barnes": {
        "rel": (
            "source-archive/statecraft/2026-05-28/"
            "source-barnes-mario-nawfal-reports-iran-attacks-u-s-ships-2026-05-28.md"
        ),
        "titles": [
            "IRGC Warning Shot Open — Bushier Missile, Reaper Drone, Deal-Optimism Cycle",
            "Rugpull Presidency — Vance April Deal, Exit Strategy, Joe Kent Frame",
            "TACO Index — 10-Year Bond, Democratic Tsunami, Prediction Markets",
            "Filter Loss — Oman Threat, Saudi Humiliation, Dementia Tell",
            "Galibaf Assassination Pitch — Classified Report, Salem / Brad Parscale",
            "Fox-Hannity Loop — Gaza-Lebanon Toll, Reagan Stand-Down, Massie Primary",
            "VFT / Gorka Targeting — Surveillance State, Palantir, Tucker List",
            "Munitions CSIS — MIC Broken, Interceptor Drain, Supply-Chain Crisis",
            "Late-Stage Empire — Blockade Legal Frame, Allies Exit, Vance Embitterment",
            "Iran International — Saudi Caymans Funding, Rubio Visa Weaponization",
            "Civil Rights Capture — IRS Slush Fund, Antitrust Pay-for-Play, Corruption Close",
        ],
        "anchors": [
            "Well, I I think before the markets open tomorrow morning",
            "So Deutsche Bank created this pressure index",
            "Is that what he said? No. Kiss his ass.",
            "Israel privately pressing the US to kill Galibbah",
            "Here's Lindsey Graham. Here's Sean Hannity at night",
            "Seb Gawk, have you seen it? Seb Gawker working with some agency",
            "US munition stock paths won't recover for years after Iran war",
            "Oh, no doubt. It's very much latestage empire decline",
            "Iran International reportedly received $825 million in debt relief",
            "Oh, the only other thing really is that the administration is to give another example",
        ],
        "note": "Eleven sections. Pair §2 with Kent May 28 · §7 with May 31 Barnes §6–§8 stack.",
    },
    "parsi": {
        "rel": (
            "source-archive/statecraft/2026-05-28/"
            "source-mario-nawfal-parsi-breaking-trump-iran-close-to-deal-2026-05-28.md"
        ),
        "titles": [
            "Deal Rumor Open — Bessent Free Passage, Tasnim Denial, Perpetual Cycle",
            "Public Negotiation Trap — Quiet JCPA/Cuba Contrast, Self-Inflicted Wounds",
            "Iranian Suspicion — Midterm Window, Araghchi-Qatar, Bad-Faith Memory",
            "Close to Deal — Abraham Accords Pit Stop, Cold-Feet Clock",
            "Probing Deterrence — Kuwait Strike, Syria Normalization Pattern",
            "UAE Substack — Lebanon-for-UAE Formula, Regional Ceasefire Demand",
            "Abraham Accords Legacy — Gatekeeper Myth, UAE Target Consequence",
            "Trump-Netanyahu Leverage — Beirut Restraint, Muted Israeli Sabotage",
            "Escalation Risks — False Flag, Busher Probing, Joe Kent No Military Option",
            "Regional Architecture — Tripolar Skepticism, IRGC Elimination Rhetoric Close",
        ],
        "anchors": [
            "Let me first start off by saying this, Mario. If this negotiation wasn't taking place",
            "There has been some sort of a deal in which the Iranians needed to respond",
            "Is it fair to say that they are close to a deal or would you disagree even there?",
            "What do you make? Why why are we seeing those clashes like what happened yesterday",
            "What what did they strike in Kuwait? Do we know because it was intercepted?",
            "So, I wrote this on my Substack a couple of days ago",
            "It's what a world we live in how the region has changed",
            "What can go wrong? Because me and you are more on the optimistic side",
            "another thing I'm trying to understand now is how, because I'm in the camp that this the war is pretty much wrapping up",
        ],
        "note": "Ten sections. §6 = Substack UAE/Lebanon stack · pair Diesen/Johnson May 31 parliament arc.",
    },
    "kent": {
        "rel": (
            "source-archive/statecraft/2026-05-28/"
            "source-mario-nawfal-kent-trumps-life-is-under-threat-2026-05-28.md"
        ),
        "titles": [
            "VFT Open — Vine and Fig Tree, NSC AI Video, Dissident-Right Target List",
            "Gorka CT Blur — Massie Demographics, Donor-Class Counter-Messaging Fear",
            "Iran Stuck — Trump Paper Win, Abraham Accords Flail, Stray Fire Risk",
            "Abraham Accords Absurd — Post-Gaza Impossible, Trump Lifeline Search",
            "Influence Scale — Netanyahu 5–7, US Not Calling Shots",
            "Security Duress — Assassination Attempts, Kirk, Not Kompromat",
            "Israel ROI — Rubin Benefits Frame, Five Eyes Contrast, Existential Lobby",
            "Deal Chicken — NBC Doha Closed, IRGC Rhetoric, Pragmatic Leave Case",
            "Butler Block — FBI/NCTC Obstruction, Krooks Links, Tulsi Resign Close",
        ],
        "anchors": [
            "and there's a few tweets under it. Um, so this is this is part of a broader topic",
            "Yeah, I think they're concerned too because if you look at the demographic breakdown in Massiey's race",
            "So, I'm trying to see everything unfold and make sense of it",
            "Yeah. The Abraham's Accords is is beyond bizarre",
            "I'm going to ask you just kind of try to give me a number",
            "There's um I have one more question and then I'm going to ask you",
            "There's something Dave Rubin told me",
            "I've got another piece of news as well just came in literally as we're speaking",
        ],
        "note": "Nine sections. §1 VFT/Gorka · §5 influence scale · §8 Doha deal · pair Barnes May 28 §2.",
    },
}

TRANSCRIPT_MARKER = "## Transcript\n"
LEGACY_SPLIT = "---\n\n"

def extract_flat_body(doc: str) -> str:
    if TRANSCRIPT_MARKER in doc:
        return doc.split(TRANSCRIPT_MARKER, 1)[1]
    if LEGACY_SPLIT in doc:
        return doc.split(LEGACY_SPLIT, 1)[1]
    raise ValueError("no transcript body (expected ## Transcript or legacy --- split)")

def flatten_sectioned_body(body: str) -> str:
    body = body.strip()
    if "### " not in body:
        return body
    while True:
        new = re.sub(r"^### [^\n]+\n+", "", body)
        new = re.sub(r"\n+### [^\n]+\n+", "\n\n", new)
        if new == body:
            break
        body = new
    return body.strip()

def ensure_flat_transcript(path: Path) -> None:
    doc = path.read_text(encoding="utf-8")
    if TRANSCRIPT_MARKER not in doc:
        return
    head, body = doc.split(TRANSCRIPT_MARKER, 1)
    flat = flatten_sectioned_body(body)
    if flat == body.strip():
        return
    path.write_text(f"{head}{TRANSCRIPT_MARKER}\n\n{flat}\n", encoding="utf-8", newline="\n")

def check_spec(path: Path, spec: dict) -> bool:
    doc = path.read_text(encoding="utf-8")
    body = flatten_sectioned_body(extract_flat_body(doc).strip())
    pos = 0
    ok = True
    print(f"=== {path.name} ({len(spec['titles'])} sections) ===")
    for i, anchor in enumerate(spec["anchors"], start=1):
        try:
            pos = find_anchor_pos(body, anchor, pos) + len(normalize_for_anchor(anchor))
            print(f"  anchor {i} -> section {i + 1}: {spec['titles'][i]}")
        except ValueError as exc:
            ok = False
            print(f"  {i}. FAIL — {exc}")
    print(f"  -> {spec['titles'][-1]} (EOF)")
    if spec.get("note"):
        print(f"  note: {spec['note']}")
    print()
    return ok

def apply_spec(path: Path, spec: dict) -> None:
    ensure_flat_transcript(path)
    write_sectioned_capture(
        path,
        spec["titles"],
        spec["anchors"],
        reject_if_sectioned=False,
    )

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--check-anchors", action="store_true")
    parser.add_argument("--only", choices=list(CAPTURES))
    args = parser.parse_args()

    if not args.apply and not args.check_anchors:
        args.check_anchors = True

    keys = [args.only] if args.only else list(CAPTURES)
    ok_all = True
    for key in keys:
        spec = CAPTURES[key]
        path = ROOT / spec["rel"]
        if not path.is_file():
            print(f"MISSING {spec['rel']}", file=sys.stderr)
            ok_all = False
            continue
        if args.apply:
            apply_spec(path, spec)
            print(f"sectioned {spec['rel']}")
        else:
            ok_all = check_spec(path, spec) and ok_all

    if not args.apply:
        print("Pass --apply after operator approval to ship.")
    return 0 if ok_all else 1

if __name__ == "__main__":
    raise SystemExit(main())
