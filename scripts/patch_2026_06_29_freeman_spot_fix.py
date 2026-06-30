#!/usr/bin/env python3
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[1]
PATH = (
    "source-archive/statecraft/2026-06-29/"
    "source-glenn-diesen-chas-freeman-us-iran-resume-war-israel-lebanon-civil-war-2026-06-29.md"
)

SUBS = [
    ("straight of Huos", "Strait of Hormuz"),
    ("ships will be permitted out of the straight under", "ships will be permitted out of the Strait under"),
    ("Iranians were to open the straight uh", "Iranians were to open the Strait uh"),
    ("smashing asbalah", "smashing Hezbollah"),
    ("Marshall Pan", "Marshal Pétain"),
    ("the surviile nature", "the servile nature"),
    ("memorand memorandum", "memorandum"),
    ("poggrams", "pogroms"),
    ("the duma of", "the drama of"),
    ("control of the state of Hormuz", "control of the Strait of Hormuz"),
    ("Babel Mand Lumbok", "Bab el-Mandeb and Lombok"),
    ("the straight of Malaa", "the Strait of Malacca"),
    ("Sundown the straight of Taiwan", "Sunda, the Strait of Taiwan"),
    ("the Toral states", "the littoral states"),
    ("Hugo Gautius", "Hugo Grotius"),
    ("Mari Libram", "Mare Liberum"),
    ("Sykes Pikov", "Sykes-Picot"),
    ("the earliest China settlers", "the earliest Zionist settlers"),
    ("attributed to Müah", "attributed to MBS"),
    ("um Maja Kane had won", "um MBS had won"),
    ("crisp ball or", "crystal ball or"),
    ("Nostadus", "Nostradamus"),
    ("future of the straighter form", "future of the Strait of Hormuz"),
    ("under Ashara the former Al Galani", "under Ahmed al-Sharaa, the former al-Jolani"),
    ("Abdul Jalan the leader of the PKK", "Abdullah Öcalan, the leader of the PKK"),
    ("Straight of Hormone's closure", "Strait of Hormuz closure"),
    ("how does Iraq export its soil?", "how does Iraq export its oil?"),
    ("have disbulated Europe", "have destabilized Europe"),
    ("USIsrael split", "US-Israel split"),
    ("USIsrael split", "US-Israel split"),
    ("I think enough Bennett well", "I think Naftali Bennett well"),
    ("Navali Bennett says", "Naftali Bennett says"),
    ("a cold piece with it with Egypt", "a cold peace with Egypt"),
    ("David Sling", "David's Sling"),
    ("You're in Creed at the moment", "You're in Crete at the moment"),
    ("this aparate state", "this apartheid state"),
    ("witting accompllices", "witting accomplices"),
    ("the muchab identified now as say", "Khamenei, identified now as Sayyid"),
    ("let's kill Sinski", "let's kill Zelensky"),
    ("building up an archnic", "building up an atomic"),
    ("postcoldware", "post-Cold War"),
    ("global hedgeimon", "global hegemon"),
    ("president uh and his assistance", "president uh and his assistants"),
    ("straight of harmons under", "Strait of Hormuz under"),
    ("cut off of the straight hormones traffic", "cutoff of the Strait of Hormuz traffic"),
    ("youact um", "exact um"),
    ("wind in their sale", "wind in their sail"),
]

SPOT = (
    "2026-06-29 — Hormuz/Huos/harmons, Marshal Pétain, Hezbollah, Grotius/Sykes-Picot, "
    "al-Sharaa/Öcalan, Bennett, Khamenei/Sayyid, Zelensky, Kiev-adjacent Ukraine refs; "
    "MBS Borowitz gag; Müah→MBS"
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
    if "manual_asr_spot_fix:" not in body:
        body = body.replace("quality_note:", f"manual_asr_spot_fix: {SPOT}\nquality_note:", 1)
    else:
        body = re.sub(r"manual_asr_spot_fix:.*", f"manual_asr_spot_fix: {SPOT}", body, count=1)
    if "manual ASR spot-fix" not in body:
        body = body.replace(
            "not human-verified verbatim; verify before quotation.",
            "not human-verified verbatim; verify before quotation. · manual ASR spot-fix 2026-06-29.",
            1,
        )
    p.write_text(body, encoding="utf-8")
    print(f"{PATH}: {n} replacements")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
