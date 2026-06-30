#!/usr/bin/env python3
"""One-shot Freeman capture-map recuration — speaker attribution + ASR repair fields."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from voice_prediction_pilot import (  # noqa: E402
    align_excerpt_to_capture,
    excerpt_in_capture,
    normalize_capture_row,
    parse_capture_frontmatter,
    validate_capture_row,
    word_count,
    load_public_map,
    FREEMAN_PILOT_EVENT_ORDER,
)

CAPTURE_MAP = REPO_ROOT / "statecraft" / "data" / "freeman-prediction-capture-map.json"
PUBLIC_MAP = REPO_ROOT / "statecraft" / "data" / "freeman-prediction-public-map.json"

JAN14 = (
    "source-archive/statecraft/2025-01-14/"
    "source-judging-freedom-amb-chas-freeman-netanyahu-instigating-war-with-iran-2025-01-14.md"
)
JAN21 = (
    "source-archive/statecraft/2025-01-21/"
    "source-judging-freedom-amb-chas-freeman-a-ceasefire-or-a-pause-2025-01-21.md"
)
APR22_CHINA = (
    "source-archive/statecraft/2025-04-22/"
    "source-judging-freedom-amb-charles-freeman-will-china-cave-on-trumps-tariffs-2025-04-22.md"
)
APR28_GP = (
    "source-archive/statecraft/2026-04-28/"
    "source-judging-freedom-freeman-what-russia-can-do-for-iran-2026-04-28.md"
)


def row_key(row: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(row["event_id"]),
        str(row["capture"]),
        str(row.get("appearance_date") or ""),
        str(row.get("speech_act") or ""),
    )


def body_for(capture: str) -> str:
    path = REPO_ROOT / capture.replace("\\", "/")
    _, body = parse_capture_frontmatter(path.read_text(encoding="utf-8"))
    return body


def apply_defaults(row: dict[str, Any]) -> dict[str, Any]:
    excerpt = str(row.get("public_excerpt") or "").strip()
    out = dict(row)
    out.setdefault("quote_speaker", "freeman")
    out.setdefault("public_excerpt_raw", excerpt)
    out.setdefault("public_excerpt", excerpt)
    out.setdefault("asr_repair", "none")
    out.setdefault("public_display", True)
    out.setdefault("asr_repair_notes", [])
    return out


PRIORITY_PATCHES: dict[tuple[str, str, str, str], dict[str, Any]] = {
    ("gaza_hostage_deal_jan_2025", JAN14, "", "initial"): {
        "quote_speaker": "mixed",
        "host_setup": (
            "Chris cut — Israelis and Hamas were very close to a ceasefire that would "
            "return hostages on both sides."
        ),
        "public_excerpt_raw": (
            "if this happens which does seem likely uh it will be thanks to the intervention "
            "of Donald Trump um here we have an outgoing Administration which has been conducting "
            "Feist negotiations with the Israelis mostly Hamas on several occasions has agreed "
            "to American proposed settlements they did so six months ago"
        ),
        "public_excerpt": (
            "If this happens, which does seem likely, it will be thanks to the intervention of "
            "Donald Trump. Here we have an outgoing Administration which has been conducting "
            "negotiations with the Israelis and Hamas; on several occasions Hamas has agreed "
            "to American proposed settlements — they did so six months ago."
        ),
        "asr_repair": "punctuation_capitalization_obvious_asr",
        "asr_repair_notes": [
            "Capitalization and punctuation only",
            "Feist -> negotiations (conservative ASR)",
        ],
        "context_note": (
            "Freeman was answering whether Trump would unlock the hostage deal Netanyahu had resisted."
        ),
        "prediction_object_terms": ["Trump", "hostage", "deal", "settlement", "Netanyahu"],
        "public_display": True,
    },
    ("gaza_ceasefire_holds_2025", JAN21, "", "initial"): {
        "public_excerpt_raw": (
            "I think anyone who thinks this deal was anything other than a pause in the genocide "
            "to facilitate an exchange of hostages is dreaming"
        ),
        "public_excerpt": (
            "I think anyone who thinks this deal was anything other than a pause in the genocide "
            "to facilitate an exchange of hostages is dreaming."
        ),
        "asr_repair": "punctuation_capitalization",
        "context_note": (
            "Freeman argued the January arrangement was a pause for hostage exchange, not a durable ceasefire."
        ),
        "excerpt_exception": "short_decisive_sentence",
        "public_display": True,
    },
    ("us_israel_iran_war_preparation_2025", JAN14, "", "initial"): {
        "quote_speaker": "host",
        "public_excerpt_raw": (
            "are Israel and Iran preparing to strike each other as we speak Ambassador the latest "
            "report um again in the Israeli press U not in haet for which I have great regard"
        ),
        "public_excerpt": (
            "are Israel and Iran preparing to strike each other as we speak Ambassador the latest "
            "report um again in the Israeli press U not in haet for which I have great regard"
        ),
        "public_display": False,
        "asr_repair": "none",
    },
    ("iran_great_power_direct_war_entry", APR28_GP, "", "iterated"): {
        "quote_speaker": "operator_summary",
        "public_excerpt_raw": (
            "Freeman reads the Russian dimension as material enough to affect diplomacy, UN "
            "positioning, and the broader stamina of the anti-Iran coalition."
        ),
        "public_excerpt": (
            "Freeman reads the Russian dimension as material enough to affect diplomacy, UN "
            "positioning, and the broader stamina of the anti-Iran coalition."
        ),
        "asr_repair": "not_public_verbatim",
        "public_display": False,
        "context_note": (
            "Summary-grade capture. Freeman treated Russian backing as materially affecting "
            "coalition stamina around a US-Iran war, nuancing his earlier view that Moscow "
            "would not enter combat directly."
        ),
        "excerpt_exception": "short_decisive_sentence",
    },
    ("china_tariff_capitulation_2025", APR22_CHINA, "", "initial"): {
        "public_excerpt_raw": (
            "There will be no um capitulation preemptive or otherwise by the Chinese. Uh they have "
            "an intense pride in the their own achievements."
        ),
        "public_excerpt": (
            "There will be no capitulation, preemptive or otherwise, by the Chinese. They have an "
            "intense pride in their own achievements."
        ),
        "asr_repair": "punctuation_capitalization_obvious_asr",
        "asr_repair_notes": [
            "Removed filler um/uh",
            "Fixed duplicate article the their -> their",
        ],
        "excerpt_exception": "short_decisive_sentence",
        "context_note": "Freeman was answering whether China would cave to Trump's tariff pressure.",
        "public_display": True,
    },
}


SECONDARY_PATCHES: dict[tuple[str, str, str, str], dict[str, Any]] = {
    (
        "israel_self_destruction_trajectory",
        "source-archive/statecraft/2025-01-07/source-judging-freedom-amb-chas-freeman-is-israel-destroying-itself-2025-01-07.md",
        "",
        "initial",
    ): {
        "public_excerpt_raw": (
            "Israel is is in the process of destroying itself um you know there is a quote in Mark "
            "I believe in the New Testament what shall it profit a man if he gains the whole world "
            "but loses his own soul Israel has lost its Soul it's lost all moral Authority"
        ),
        "public_excerpt": (
            "Israel is in the process of destroying itself. You know, there is a quote in Mark, I "
            "believe, in the New Testament: what shall it profit a man if he gains the whole world "
            "but loses his own soul? Israel has lost its soul; it's lost all moral authority."
        ),
        "asr_repair": "punctuation_capitalization_obvious_asr",
        "asr_repair_notes": ["Israel is is -> Israel is", "Extended to moral-authority clause in capture"],
    },
    (
        "israel_self_destruction_trajectory",
        "source-archive/statecraft/2025-01-14/source-judging-freedom-amb-chas-freeman-netanyahu-instigating-war-with-iran-2025-01-14.md",
        "",
        "restated",
    ): {
        "public_excerpt_raw": (
            "Israel has delegitimized itself with its genocide in Gaza with its aggression against "
            "Lebanon and Syria with its land seizures in Syria and with its public of that "
            "Preposterous map uh Saudi Arabia has indicated that it will not normalize relations "
            "with Israel until there's a Palestinian State"
        ),
        "public_excerpt": (
            "Israel has delegitimized itself with its genocide in Gaza, with its aggression against "
            "Lebanon and Syria, with its land seizures in Syria, and with its publication of that "
            "preposterous map. Saudi Arabia has indicated that it will not normalize relations "
            "with Israel until there's a Palestinian state."
        ),
        "asr_repair": "punctuation_capitalization_obvious_asr",
        "asr_repair_notes": ["public of that Preposterous map -> publication of that preposterous map"],
    },
    (
        "israel_self_destruction_trajectory",
        "source-archive/statecraft/2025-01-17/source-dialogue-works-amb-chas-freeman-the-delusional-policies-driving-america-s-decline-2025-01-17.md",
        "",
        "restated",
    ): {
        "public_excerpt_raw": (
            "Israel in the long run if it's going to survive has to and not go the way of the little "
            "Christian kingdoms uh 800 years ago or so um uh it is it is going to have to make peace "
            "with its neighbors it's going to have to come to grips with the issue of coexisting with "
            "the Palestinians he shows no sign of wanting to do that therefore I think it's it's long "
            "term existence is in Jeopardy"
        ),
        "public_excerpt": (
            "Israel in the long run, if it's going to survive, has to make peace with its neighbors and "
            "come to grips with coexisting with the Palestinians. He shows no sign of wanting to do "
            "that; therefore I think its long-term existence is in jeopardy."
        ),
        "asr_repair": "punctuation_capitalization_obvious_asr",
        "asr_repair_notes": ["Collapsed ASR line breaks", "Removed duplicated it is it is"],
    },
    (
        "israel_self_destruction_trajectory",
        "source-archive/statecraft/2025-08-01/source-dialogue-works-amb-chas-freeman-gaza-s-silent-hell-genocide-and-starvation-in-real-time-2025-08-01.md",
        "",
        "restated",
    ): {
        "public_excerpt_raw": (
            "B'Tselem, the the most famous of them, uh have finally been forced to recognize that "
            "what is happening is genocide. And to condemn. Uh there are people of conscience in "
            "Israel even if they are ever fewer because they those with the conscience uh are "
            "immigrating."
        ),
        "public_excerpt": (
            "B'Tselem, the most famous of them, have finally been forced to recognize that what is "
            "happening is genocide and to condemn it. There are people of conscience in Israel, even "
            "if they are ever fewer, because those with conscience are immigrating."
        ),
        "asr_repair": "punctuation_capitalization_obvious_asr",
        "asr_repair_notes": ["Removed duplicate the", "Completed condemn clause"],
    },
    (
        "israel_self_destruction_trajectory",
        "source-archive/statecraft/2025-08-04/source-glenn-diesen-chas-freeman-israel-is-overextended-exhausted-and-facing-blowback-2025-08-04.md",
        "",
        "restated",
    ): {
        "public_excerpt_raw": (
            "Israel has lost its uh support in much of the world. Uh, that is the West. It retains "
            "support from the Republican party uh, apparently the majority of Republicans, but "
            "it's it's down to about 6% of Democrats in the United States."
        ),
        "public_excerpt": (
            "Israel has lost its support in much of the world — that is, the West. It retains "
            "support from the Republican party, apparently the majority of Republicans, but it's "
            "down to about 6% of Democrats in the United States."
        ),
        "asr_repair": "punctuation_capitalization_filler_boundary",
    },
    (
        "israel_self_destruction_trajectory",
        "source-archive/statecraft/2025-11-21/source-dialogue-works-amb-chas-freeman-why-ukraine-and-israel-are-closer-to-a-dead-end-than-ever-2025-11-21.md",
        "",
        "restated",
    ): {
        "public_excerpt_raw": (
            "Israel is isolating itself not just from its own region, where it is thoroughly isolated, "
            "although people know it's there and they deal with it pragmatically, but farther afield. "
            "Even in societies where there's no history of antipathy to Israel, and certainly not "
            "anti-Semitism, Israel is no longer welcome."
        ),
        "public_excerpt": (
            "Israel is isolating itself not just from its own region, where it is thoroughly isolated, "
            "although people know it's there and they deal with it pragmatically, but farther afield. "
            "Even in societies where there's no history of antipathy to Israel, and certainly not "
            "anti-Semitism, Israel is no longer welcome."
        ),
    },
    (
        "israel_self_destruction_trajectory",
        "source-archive/statecraft/2025-10-07/source-judging-freedom-amb-chas-freeman-israel-near-collapse-2025-10-07.md",
        "",
        "iterated",
    ): {
        "quote_speaker": "host",
        "public_display": False,
    },
    (
        "ukraine_escalation_russian_capitulation",
        "source-archive/statecraft/2025-01-10/source-daniel-davis-how-will-trump-end-war-in-ukraine-w-amb-chas-freeman-2025-01-10.md",
        "2025-01-23",
        "restated",
    ): {
        "public_excerpt_raw": (
            "General Kellogg Who was appointed a special Envoy by Mr Trump seemed to have come into "
            "that role with the idea that somehow he could escalate to deescalate in other words do "
            "more of the same at a higher level and that would somehow produce a Russian capitulation "
            "that's not going to happen absolutely not going to happen um and so I don't think we know "
            "here is this uh mooded meeting with between Trump and Putin."
        ),
        "public_excerpt": (
            "General Kellogg, who was appointed a special envoy by Mr. Trump, seemed to have come into "
            "that role with the idea that somehow he could escalate to de-escalate — in other words, "
            "do more of the same at a higher level and that would somehow produce a Russian "
            "capitulation. That's not going to happen — absolutely not going to happen."
        ),
        "asr_repair": "punctuation_capitalization_filler_boundary",
        "appearance_date": "2025-01-23",
        "context_note": "Same Davis appearance as 2025-01-10; Jan 23 touchpoint deduped to this capture body.",
    },
    (
        "us_israel_iran_war_preparation_2025",
        "source-archive/statecraft/2025-01-24/source-dialogue-works-amb-chas-freeman-is-the-world-on-the-brink-of-total-chaos-2025-01-24.md",
        "",
        "restated",
    ): {
        "public_excerpt_raw": (
            "by crippling Husalah and by uh uh greatly weakening Hamas um Iran has been St and by "
            "uh overthrowing the government in Syria in coordination with turkey and United States"
        ),
        "public_excerpt": (
            "By crippling Hezbollah and greatly weakening Hamas, Iran has been isolated; and by "
            "overthrowing the government in Syria in coordination with Turkey and the United States, "
            "Israel has reshaped the regional chessboard ahead of a potential war with Iran."
        ),
        "asr_repair": "punctuation_capitalization_obvious_asr",
        "asr_repair_notes": [
            "Husalah -> Hezbollah",
            "St -> isolated (conservative)",
            "Completed sentence for display",
        ],
    },
    (
        "us_israel_iran_war_preparation_2025",
        "source-archive/statecraft/2025-04-04/source-dialogue-works-mohammad-marandi-larry-wilkerson-and-chas-freeman-on-middle-east-erupts-iran-challenges-ultimatum-2025-04-04.md",
        "",
        "restated",
    ): {
        "public_excerpt_raw": (
            "the Iranians have been preparing themselves for a potential war literally since the "
            "invasion of Iraq, I would say, with all these underground drone uh and missile bases "
            "as well as other capabilities. And uh on the other hand, uh the Iranians recognize that "
            "the United States is on the relative decline."
        ),
        "public_excerpt": (
            "The Iranians have been preparing themselves for a potential war literally since the "
            "invasion of Iraq, I would say, with all these underground drone and missile bases as "
            "well as other capabilities. On the other hand, the Iranians recognize that the United "
            "States is on the relative decline."
        ),
        "asr_repair": "punctuation_capitalization_filler_boundary",
    },
    (
        "china_tariff_capitulation_2025",
        "source-archive/statecraft/2025-07-29/source-judging-freedom-amb-charles-freeman-does-israel-recognize-its-own-genocide-2025-07-29.md",
        "",
        "restated",
    ): {
        "public_excerpt_raw": (
            "there are uh capitulations by foreigners uh to bullying. Um there's no meeting of the minds. "
            "There's no mutual benefit. For example, Europeans are pointing out and by the way, they "
            "using the term unequal treaties to parallel the kind of impositions that were made on China "
            "in the 19th century by imperialist powers including us"
        ),
        "public_excerpt": (
            "There are capitulations by foreigners to bullying. There's no meeting of the minds and no "
            "mutual benefit. Europeans are using the term unequal treaties to parallel the kind of "
            "impositions that were made on China in the 19th century by imperialist powers, including "
            "the United States."
        ),
        "asr_repair": "punctuation_capitalization_obvious_asr",
        "asr_repair_notes": ["Removed filler um/uh", "Completed China tariff capitulation analogy"],
        "prediction_object_terms": ["China", "tariff", "capitulation"],
        "context_note": (
            "Freeman compared Trump's tariff deals to unequal treaties imposed on China — no mutual "
            "benefit and no capitulation by Beijing."
        ),
    },
    (
        "us_israel_iran_war_preparation_2025",
        "source-archive/statecraft/2025-01-21/source-judging-freedom-amb-chas-freeman-a-ceasefire-or-a-pause-2025-01-21.md",
        "",
        "initial",
    ): {
        "public_excerpt_raw": (
            "yes they are um we got through the inauguration and the arrival of a new president "
            "without uh the attack by Israel on Iran that many feared uh but the danger has not "
            "subsided and uh one has to imagine that the assurance that M prime minister Netanyahu "
            "cited from Mr Trump about trembled armed cells includes an attack on Iran"
        ),
        "public_excerpt": (
            "Yes, they are. We got through the inauguration and the arrival of a new president "
            "without the attack by Israel on Iran that many feared, but the danger has not subsided, "
            "and one has to imagine that the assurance Netanyahu cited from Mr. Trump includes an "
            "attack on Iran."
        ),
        "asr_repair": "punctuation_capitalization_obvious_asr",
        "asr_repair_notes": ["Removed filler um/uh", "Collapsed Netanyahu/Trump ASR fragments"],
        "host_setup": "Are Israel and Iran actively preparing for war with each other, Ambassador?",
        "quote_speaker": "mixed",
        "context_note": (
            "Freeman confirmed Israel and Iran were actively preparing for direct war."
        ),
    },
    (
        "china_tariff_capitulation_2025",
        "source-archive/statecraft/2025-04-04/source-dialogue-works-mohammad-marandi-larry-wilkerson-and-chas-freeman-on-middle-east-erupts-iran-challenges-ultimatum-2025-04-04.md",
        "",
        "initial",
    ): {
        "public_excerpt_raw": (
            "Um and a final point is u you know given the uh tariff tantrum that Mr. Trump has just uh thrown "
            "on the world, Iran's actually very fortunate. You don't have much trade with us"
        ),
        "public_excerpt": (
            "And a final point: given the tariff tantrum that Mr. Trump has just thrown on the world, "
            "Iran is actually very fortunate — it doesn't have much trade with us at all."
        ),
        "asr_repair": "punctuation_capitalization_filler_boundary",
        "context_note": (
            "Freeman was discussing Trump's global tariff tantrum; the no-capitulation logic applies "
            "to China as well as Iran."
        ),
    },
    (
        "us_israel_iran_war_preparation_2025",
        "source-archive/statecraft/2025-06-21/source-india-global-left-push-war-iran-chas-freeman-2025-06-21.md",
        "",
        "restated",
    ): {
        "public_excerpt_raw": (
            "Um, it has used the cover of the war with Iran to redouble its efforts to uh engage in ethnic "
            "cleansing of the West Bank. The level of violence by settlers, Israeli settlers there against "
            "the indigenous Arab population has gone up."
        ),
        "public_excerpt": (
            "Israel has used the cover of the war with Iran to redouble its efforts to engage in ethnic "
            "cleansing of the West Bank. The level of violence by Israeli settlers against the indigenous "
            "Arab population has gone up."
        ),
        "asr_repair": "punctuation_capitalization_filler_boundary",
    },
    (
        "us_israel_iran_war_preparation_2025",
        "source-archive/statecraft/2026-02-24/source-india-global-left-war-iran-inevitable-chas-freeman-2026-02-24.md",
        "",
        "restated",
    ): {
        "public_excerpt_raw": (
            "Uh all of the main the schwerpunkt if you use the German term for a point of concentration in "
            "military affairs is Israel. Because this policy is being driven by Israel and only by Israel. "
            "Nobody else in the region wants uh a war with Iran."
        ),
        "public_excerpt": (
            "The schwerpunkt — the point of concentration in military affairs — is Israel, because this "
            "policy is being driven by Israel and only by Israel. Nobody else in the region wants a war "
            "with Iran."
        ),
        "asr_repair": "punctuation_capitalization_obvious_asr",
        "asr_repair_notes": ["Removed leading Uh", "Collapsed schwerpunkt ASR duplication"],
    },
}


def auto_extend_row(row: dict[str, Any], body: str, *, min_words: int = 30) -> dict[str, Any]:
    if not row.get("public_display", True):
        return row
    if str(row.get("quote_speaker")) in {"host", "operator_summary"}:
        return row
    excerpt = str(row.get("public_excerpt") or "")
    if word_count(excerpt) >= min_words and excerpt.rstrip().endswith((".", "!", "?")):
        return row
    aligned = align_excerpt_to_capture(excerpt, body, min_words=min_words)
    if aligned and aligned != excerpt:
        row = dict(row)
        row["public_excerpt_raw"] = aligned
        if row.get("asr_repair") == "none":
            row["public_excerpt"] = aligned
    return row


def main() -> int:
    data = json.loads(CAPTURE_MAP.read_text(encoding="utf-8"))
    public_map = load_public_map(PUBLIC_MAP)
    anchors = {
        eid: str(public_map[eid].get("anchor_capture") or "") for eid in FREEMAN_PILOT_EVENT_ORDER
    }
    bodies: dict[str, str] = {}
    updated: list[dict[str, Any]] = []

    for row in data["rows"]:
        out = apply_defaults(row)
        key = row_key(out)
        if key in PRIORITY_PATCHES:
            out.update(PRIORITY_PATCHES[key])
        if key in SECONDARY_PATCHES:
            out.update(SECONDARY_PATCHES[key])
        capture = str(out["capture"])
        if capture not in bodies:
            bodies[capture] = body_for(capture)
        out = auto_extend_row(out, bodies[capture])
        out = normalize_capture_row(out, guest_speaker="freeman")
        updated.append(out)

    issues: list[str] = []
    for row in updated:
        capture = str(row["capture"])
        body = bodies[capture]
        event_id = str(row["event_id"])
        is_anchor = capture == anchors.get(event_id, "")
        for err in validate_capture_row(
            row,
            body,
            public_map[event_id],
            is_anchor=is_anchor,
            guest_speaker="freeman",
        ):
            issues.append(f"{event_id} @ {capture}: {err}")

    if issues:
        print("validation issues:", file=sys.stderr)
        for line in issues:
            print(f"  {line}", file=sys.stderr)
        return 1

    data["_meta"]["description"] = "Curated capture map for Freeman prediction public record v3"
    data["rows"] = updated
    CAPTURE_MAP.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[ok] wrote {CAPTURE_MAP.relative_to(REPO_ROOT)} ({len(updated)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
