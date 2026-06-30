#!/usr/bin/env python3
"""Pass-2 residual ASR spot-fix — Crooke + Johnson JF 2026-06-29."""
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[1]

PASS2 = (
    "pass-2: Hormuz/Strait dupes, hegemony, Bessent, battlespace, Iraq Kurds, "
    "petrochemical, Fujairah, waive, Peskov, Ponzi dupes, tour de force"
)

def patch(path: str, subs: list[tuple[str, str]], base_note: str) -> int:
    p = REPO / path
    body = p.read_text(encoding="utf-8")
    n = 0
    for old, new in subs:
        c = body.count(old)
        if c:
            body = body.replace(old, new)
            n += c
    note = f"{base_note} · {PASS2}"
    if "pass-2:" not in body:
        body = re.sub(r"manual_asr_spot_fix:.*", f"manual_asr_spot_fix: {note}", body, count=1)
    if "pass-2" not in body.split("---", 1)[0]:
        body = body.replace(
            "manual ASR spot-fix 2026-06-29.",
            "manual ASR spot-fix 2026-06-29; pass-2 residual.",
            1,
        )
    p.write_text(body, encoding="utf-8")
    print(f"{path}: {n} replacements (pass-2)")
    return n

CROOKE = [
    ("oil is about to hit on hit the", "oil is about to hit the"),
    ("Ayatollus, Grand Ayatollus", "Ayatollahs, Grand Ayatollahs"),
    ("left o of metal distillates", "left of middle distillates"),
    ("there are been talks", "there have been talks"),
    ("both Sunnis and some she but", "both Sunnis and some Shia but"),
    ("response is going to be to this big the sweep", "response is going to be to this big sweep"),
    ("a foothold uh in Iran and the Iran Iranians", "a foothold uh in Iraq and the Iranians"),
    ("twothirds majority", "two-thirds majority"),
    ("10point plans", "10-point plans"),
    ("Trump is is more or less sort of giving up on his hopes of of getting a a sort of a victory", "Trump is more or less sort of giving up on his hopes of getting a sort of victory"),
    ("hedgemony", "hegemony"),
    ("interest rates um are can be kept lower", "interest rates can be kept lower"),
    ("19 billions of um short shorts put on", "19 billion of um short positions put on"),
    ("according to best of course China's", "according to Bessent, of course China's"),
    ("scope of uh dollar hedge money", "scope of uh dollar hegemony"),
    ("that'll be turn ugly", "that'll turn ugly"),
    ("by pressure uh a and also by manipulation", "by pressure and also by manipulation"),
    ("That was a the whole setup", "That was the whole setup"),
    ("about preparing the a battlescape", "about preparing the battlespace"),
    ("Europeans have been doing is been putting", "Europeans have been doing has been putting"),
    ("war, crime, tribunals", "war-crime tribunals"),
    ("a tour to force today", "a tour de force today"),
    ("Bye, Char.", "Bye, Judge."),
]

JOHNSON = [
    ("memorandum of understanding and the straight of war moves", "memorandum of understanding and the Strait of Hormuz moves"),
    ("Peskov the spokesman for Trump for Putin", "Peskov, the spokesman for Putin"),
    ("decimate Ukraine without just mercilessly", "decimate Ukraine mercilessly"),
    ("if you had to weigh the chance for is is a global war going to going to break out", "if you had to weigh the chance for a global war going to break out"),
    ("United States sends to Ukraine uh that a the portion of it siphoned", "United States sends to Ukraine uh that a portion of it is siphoned"),
    ("once the pro pro they put it in buy the buy the property", "once they put it in, buy the property"),
    ("There travel today talk tomorrow", "They travel today, talk tomorrow"),
    ("weekend in which the United here's how the United States", "weekend — here's how the United States"),
    ("transiting the straight of Hormuz", "transiting the Strait of Hormuz"),
    ("you go through frying go through the waters", "you go through, go through the waters"),
    ("they they're refusing to travel", "they're refusing to travel"),
    ("the US would wave sanctions", "the US would waive sanctions"),
    ("the prochemical sector", "the petrochemical sector"),
    ("the uh prochemical industry", "the petrochemical industry"),
    ("look at look also look at clause five", "look also at clause five"),
    ("the uh straight of Hormuz", "the Strait of Hormuz"),
    ("through the straight of Hormuz and through the out out of", "through the Strait of Hormuz and through the out of"),
    ("at sonar 21 your website", "at Sonar21 your website"),
    ("If a dam ship's damaged", "If the ship's damaged"),
    ("look at the straight of Hormuz", "look at the Strait of Hormuz"),
    ("the uh the straight is quite low", "the Strait is quite low"),
    ("going to Faraja, United Arab Emirates", "going to Fujairah, United Arab Emirates"),
    ("this billiond dollar radar", "this billion-dollar radar"),
    ("prochemical processes", "petrochemical processes"),
    ("Trump has an econ a serious economic problem", "Trump has a serious economic problem"),
    ("full a tanker load of oil", "full tanker load of oil"),
]

CROOKE_PATH = (
    "source-archive/statecraft/2026-06-29/"
    "source-judging-freedom-crooke-russia-ready-for-war-with-europe-2026-06-29.md"
)
JOHNSON_PATH = (
    "source-archive/statecraft/2026-06-29/"
    "source-judging-freedom-johnson-trump-mou-unraveling-2026-06-29.md"
)

CROOKE_NOTE = (
    "2026-06-29 — Crooke name, Hormuz, Ghalibaf/Araghchi/Pezeshkian, Supreme Leader, "
    "IAEA/AWACS, Merz/Starmer/Kellogg, Aoun/Sudani"
)
JOHNSON_NOTE = (
    "2026-06-29 — Kiev/Kharkov/Donetsk, Peskov/Lavrov/Gerasimov, Al Udeid/CAOC/Ali al-Salem/Isa, "
    "Hegseth, Crooke ref, marinetraffic/Qeshm/Khasab; Jesuid 2006 Iraq ref left tentative"
)

def main() -> int:
    n = 0
    n += patch(CROOKE_PATH, CROOKE, CROOKE_NOTE)
    n += patch(JOHNSON_PATH, JOHNSON, JOHNSON_NOTE)
    print(f"total: {n} replacements")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
