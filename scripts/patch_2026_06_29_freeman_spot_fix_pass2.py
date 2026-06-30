#!/usr/bin/env python3
"""Second-pass ASR spot-fix — Freeman 2026-06-29 (Lebanon/Syria/Turkey + residual garbles)."""
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[1]
PATH = (
    "source-archive/statecraft/2026-06-29/"
    "source-glenn-diesen-chas-freeman-us-iran-resume-war-israel-lebanon-civil-war-2026-06-29.md"
)

SUBS = [
    ("defining ing it", "defining it"),
    ("quite messed >>", "quite a mess >>"),
    ("the earliest China\nsettlers", "the earliest Zionist settlers"),
    ("the earliest China\r\nsettlers", "the earliest Zionist settlers"),
    ("one straight great great war", "one sustained great war"),
    ("whether it's Hamas, Hzbollah,", "whether it's Hamas, Hezbollah,"),
    ("negotiate with a Um and", "negotiate with a fool and"),
    ("the FSB con well they confirmed", "the FSB confirmed"),
    ("this low in low intensity will also low in Russia", "this low-intensity war will also stay low-intensity in Russia"),
    ("you know seed this kind of control", "you know cede this kind of control"),
    ("um are in contained in a kaleidoscope", "um are contained in a kaleidoscope"),
    ("they're also very he heavily involved", "they're also very heavily involved"),
    ("development that is uh in before Iran was", "development that is uh before Iran was"),
    ("avoid a challenge to tur Turkey", "avoid a challenge to Turkey"),
    ("in the enmity open enmity to Hezbollah", "in open enmity to Hezbollah"),
    ("part of that government me represented", "part of that government and is represented"),
    ("threats um to reign in Israel", "threats um to rein in Israel"),
    ("I don't know think that happened", "I don't think that happened"),
    ("running out of sto stored oil", "running out of stored oil"),
    ("that is a m matter of faith", "that is a matter of faith"),
    ("Donald Trump in mega movement", "Donald Trump in the MAGA movement"),
    ("and from Iran Iran and from", "and from Iran and from"),
    ("get out of this uh victorious and it victoriously?", "get out of this uh victoriously?"),
    ("Israel is engaged in a now engaged in a multiffront", "Israel is now engaged in a multi-front"),
    ("weapons twothirds or more", "weapons two-thirds or more"),
    ("authorize uh David the Iron Dome payments", "authorize the Iron Dome payments"),
    ("if you put your hair to the window", "if you put your ear to the window"),
    ("apartheid state which is now picked to fight with", "apartheid state which has now picked fights with"),
    ("support for for Israel", "support for Israel"),
    ("um is are trends toward greater support from for Israel either within within Israel", "um are trends toward greater support for Israel either within Israel"),
    ("acts of contempt of report", "acts of contempt of court"),
    ("at the moment? would would have to", "at the moment? You would have to"),
    ("because this going to be proven wrong", "because this is going to be proven wrong"),
    ("I didn't check up with the original media", "I didn't check with the original media"),
    ("that you know we would do need a nuclear weapon", "that you know we would need a nuclear weapon"),
    ("but it was a stride the world like a colossus", "but it strode the world like a colossus"),
    ("historically the have a reason to worry", "historically the Russians have a reason to worry"),
    ("European diplomacy at the m foreign policy", "European diplomacy in their foreign policy"),
    ("we took an Iran Iran we didn't want it to get nuclear weapons", "we took an Iran we didn't want to get nuclear weapons"),
    ("been able to trans transition from", "been able to transition from"),
    ("They're the one being proven right", "They're the ones being proven right"),
    (">> Enjoy creed.", ">> Enjoy Crete."),
    # pass-2b (Hzbollah variant missed first run)
    ("in the enmity open enmity to Hzbollah", "in open enmity to Hezbollah"),
    ("but more most likely uh production", "but most likely uh production"),
    ("is that they they're both being set up", "is that they're both being set up"),
    ("was supposed to be a meeting negotiating meeting", "was supposed to be a negotiating meeting"),
    ("which was fed by and um so and of course", "which was fed by Western policy and, of course"),
]

PASS2 = (
    "pass-2: Zionist settlers (line-break), Hzbollah, Syria/Turkey/Kurds, Lebanon civil-war, "
    "MAGA, rein/cede, colossus strode, contempt of court, Crete sign-off, residual dupes"
)


def main() -> int:
    p = REPO / PATH
    body = p.read_text(encoding="utf-8")
    n = 0
    for old, new in SUBS:
        c = body.count(old)
        if c:
            body = body.replace(old, new)
            n += c
    if "pass-2:" not in body:
        body = re.sub(
            r"(manual_asr_spot_fix: [^\n]+)",
            rf"\1 · {PASS2}",
            body,
            count=1,
        )
    if "manual ASR spot-fix pass-2" not in body:
        body = body.replace(
            "manual ASR spot-fix 2026-06-29.",
            "manual ASR spot-fix 2026-06-29; pass-2 Lebanon/Syria/residual.",
            1,
        )
    p.write_text(body, encoding="utf-8")
    print(f"{PATH}: {n} replacements (pass-2)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
