#!/usr/bin/env python3
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[1]

def patch(path: str, subs: list[tuple[str, str]], spot_note: str) -> None:
    p = REPO / path
    body = p.read_text(encoding="utf-8")
    n = 0
    for old, new in subs:
        c = body.count(old)
        if c:
            body = body.replace(old, new)
            n += c
    if "manual_asr_spot_fix:" not in body:
        body = body.replace(
            "quality_note:",
            f"manual_asr_spot_fix: {spot_note}\nquality_note:",
            1,
        )
    else:
        body = re.sub(
            r"manual_asr_spot_fix:.*",
            f"manual_asr_spot_fix: {spot_note}",
            body,
            count=1,
        )
    if "manual ASR spot-fix" not in body:
        body = body.replace(
            "not human-verified verbatim; verify before quotation.",
            "not human-verified verbatim; verify before quotation. · manual ASR spot-fix 2026-06-29.",
            1,
        )
    p.write_text(body, encoding="utf-8")
    print(f"{path}: {n} replacements")

johnson = [
    ("Operation Barbaroso", "Operation Barbarossa"),
    ("followed it to Kev and", "followed it to Kiev and"),
    ("Alistister Crook", "Alastair Crooke"),
    ("Peshkov", "Peskov"),
    ("Lavro,", "Lavrov,"),
    ("sumi through kkefe down to daets", "Sumy through Kharkov down to Donetsk"),
    ("mostly it's all daets because", "mostly it's all Donetsk because"),
    (
        "controlled luhans and into zaparisia and kerosan",
        "controlled Luhansk and into Zaporizhia and Kherson",
    ),
    ("coming out of Keev is", "coming out of Kiev is"),
    ("Medvidev", "Medvedev"),
    ("devastating blow on Kee?", "devastating blow on Kiev?"),
    ("General Garasimoff", "General Gerasimov"),
    ("Latafia", "Latvia"),
    ("Ali Salm", "Ali al-Salem"),
    ("Issa air base", "Isa Air Base"),
    ("We control the Straight of Hormuz", "We control the Strait of Hormuz"),
    ("mariner.com", "marinetraffic.com"),
    ("Camsh Island", "Qeshm Island"),
    ("Cassab", "Khasab"),
    ("Pete Heads", "Hegseth"),
    ("Aldid Air Force Base", "Al Udeid Air Force Base"),
    (" chaok ", " CAOC "),
    ("the kayak has", "the CAOC has"),
    ("uh at alouded", "uh at Al Udeid"),
    ("helium uh sulfur and ura,", "helium, sulfur, and urea,"),
]

crooke = [
    ("Alistister Crook", "Alastair Crooke"),
    ("Alistar Crook", "Alastair Crooke"),
    ("in HOS where", "in Hormuz where"),
    ("in Homos is", "in Hormuz, the"),
    ("about uh Homos.", "about Hormuz."),
    ("Galibbath Araghchi Pezeshkian", "Ghalibaf, Araghchi, and Pezeshkian"),
    ("set by the Sun.", "set by the Supreme Leader."),
    ("talks with Graci?", "talks with Araghchi?"),
    ("air awax helicopters", "AWACS helicopters"),
    ("the IEA inspectors", "the IAEA inspectors"),
    ("prime minister ali is", "Prime Minister Sudani is"),
    ("General Aun", "Michel Aoun"),
    ("Mertz, Stalmer", "Merz, Starmer"),
    ("Kellok philosophy", "Kellogg philosophy"),
    ("Wow. Alistia,", "Wow. Alastair,"),
]

def main() -> int:
    patch(
        "source-archive/statecraft/2026-06-29/source-judging-freedom-johnson-trump-mou-unraveling-2026-06-29.md",
        johnson,
        "2026-06-29 — Kiev/Kharkov/Donetsk, Peskov/Lavrov/Gerasimov, Al Udeid/CAOC/Ali al-Salem/Isa, Hegseth, Crooke ref, marinetraffic/Qeshm/Khasab; Jesuid 2006 Iraq ref left tentative",
    )
    patch(
        "source-archive/statecraft/2026-06-29/source-judging-freedom-crooke-russia-ready-for-war-with-europe-2026-06-29.md",
        crooke,
        "2026-06-29 — Crooke name, Hormuz, Ghalibaf/Araghchi/Pezeshkian, Supreme Leader, IAEA/AWACS, Merz/Starmer/Kellogg, Aoun/Sudani",
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
