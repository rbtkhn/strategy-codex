#!/usr/bin/env python3
"""Bootstrap and validate freeman-prediction-capture-map.json from v1 touchpoints."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from freeman_prediction_pilot import (  # noqa: E402
    FREEMAN_CAPTURE_MAP,
    FREEMAN_PREDICTIONS_JSON,
    excerpt_in_capture,
    parse_capture_frontmatter,
    validate_public_excerpt,
    word_count,
)

# Curated capture-verified excerpts keyed by (event_id, capture).
EXCERPT_OVERRIDES: dict[tuple[str, str], dict] = {
    (
        "israel_self_destruction_trajectory",
        "source-archive/statecraft/2025-01-07/source-judging-freedom-amb-chas-freeman-is-israel-destroying-itself-2025-01-07.md",
    ): {
        "public_excerpt": (
            "Israel is is in the process of destroying itself um you know there is a quote in Mark "
            "I believe in the New Testament what shall it profit a man if he gains the whole world "
            "and loses his own soul."
        ),
    },
    (
        "israel_self_destruction_trajectory",
        "source-archive/statecraft/2025-06-10/source-judging-freedom-amb-charles-freeman-israel-destroying-itself-2025-06-10.md",
    ): {
        "public_excerpt": "Israel is on a path to self-destruction.",
        "excerpt_exception": "short_decisive_sentence",
    },
    (
        "israel_self_destruction_trajectory",
        "source-archive/statecraft/2025-07-29/source-judging-freedom-amb-charles-freeman-does-israel-recognize-its-own-genocide-2025-07-29.md",
    ): {
        "public_excerpt": (
            "he can stand there with the a poem that he did um and and lie in that manner um suggests either "
            "that he's dis disconnected uh from reality completely uh or that he is uh uh someone with no "
            "credibility at all. None."
        ),
    },
    (
        "israel_self_destruction_trajectory",
        "source-archive/statecraft/2025-08-01/source-dialogue-works-amb-chas-freeman-gaza-s-silent-hell-genocide-and-starvation-in-real-time-2025-08-01.md",
    ): {
        "public_excerpt": (
            "Israeli human rights organization like uh B'Tselem, the the most famous of them, uh have "
            "finally been forced to recognize that what is happening is genocide."
        ),
    },
    (
        "israel_self_destruction_trajectory",
        "source-archive/statecraft/2025-08-04/source-glenn-diesen-chas-freeman-israel-is-overextended-exhausted-and-facing-blowback-2025-08-04.md",
    ): {
        "public_excerpt": "Israel has lost its uh support in much of the world. Uh, that is the West.",
        "excerpt_exception": "under_30_verified",
    },
    (
        "israel_self_destruction_trajectory",
        "source-archive/statecraft/2025-10-31/source-dialogue-works-amb-chas-freeman-israel-may-not-survive-this-china-and-trump-make-their-move-2025-10-31.md",
    ): {
        "public_excerpt": (
            "indications of a society under extreme stress a society that is basically failing to sustain "
            "itself. People are immigrating in large numbers. The economy is in deep trouble."
        ),
    },
    (
        "israel_self_destruction_trajectory",
        "source-archive/statecraft/2026-05-01/source-dialogue-works-amb-chas-freeman-israel-s-grand-plan-collapsed-in-record-time-2026-05-01.md",
    ): {
        "public_excerpt": "Israel is internationally isolated and um it is now a pariah.",
        "excerpt_exception": "under_30_verified",
    },
    (
        "israel_self_destruction_trajectory",
        "source-archive/statecraft/2026-06-06/source-glenn-diesen-chas-freeman-the-greater-israel-project-is-collapsing-2026-06-06.md",
    ): {
        "public_excerpt": "the dream that some of them have of a Israel greater Israel uh in grave jeopardy.",
        "excerpt_exception": "under_30_verified",
    },
    (
        "ukraine_escalation_russian_capitulation",
        "source-archive/statecraft/2025-01-10/source-daniel-davis-how-will-trump-end-war-in-ukraine-w-amb-chas-freeman-2025-01-10.md",
    ): {
        "public_excerpt": (
            "General Kellogg Who was appointed a special Envoy by Mr Trump seemed to have come into that "
            "role with the idea that somehow he could escalate at a higher level and that would somehow "
            "produce a Russian capitulation that's not going to happen absolutely not going to happen"
        ),
    },
    (
        "ukraine_escalation_russian_capitulation",
        "source-archive/statecraft/2025-01-23/source-daniel-davis-ukraine-russia-war-showdown-w-chas-freeman-2025-01-23.md",
    ): {
        "public_excerpt": (
            "The idea that escalation at a higher level would somehow produce a Russian capitulation "
            "that's not going to happen absolutely not going to happen."
        ),
        "excerpt_exception": "stub_capture",
        "context_note": "Capture body is metadata-only; excerpt carried from paired 2025-01-10 appearance.",
    },
    (
        "gaza_hostage_deal_jan_2025",
        "source-archive/statecraft/2025-01-14/source-judging-freedom-amb-chas-freeman-netanyahu-instigating-war-with-iran-2025-01-14.md",
    ): {
        "public_excerpt": (
            "if this happens which does seem likely uh it will be thanks to the intervention of Donald "
            "Trump um here we have an outgoing Administration which has been conducting a war indirectly "
            "through proxies in Ukraine and in Gaza"
        ),
    },
    (
        "gaza_ceasefire_holds_2025",
        "source-archive/statecraft/2025-01-21/source-judging-freedom-amb-chas-freeman-a-ceasefire-or-a-pause-2025-01-21.md",
    ): {
        "public_excerpt": (
            "anything other than a pause in the genocide to facilitate an exchange of hostages is dreaming"
        ),
        "excerpt_exception": "under_30_verified",
    },
    (
        "gaza_ceasefire_holds_2025",
        "source-archive/statecraft/2025-10-10/source-india-global-left-gaza-ceasefire-wont-last-chas-freeman-2025-10-10.md",
    ): {
        "public_excerpt": (
            "I'm not, uh, convinced that this is more than another, um, misleading flash in the pan."
        ),
        "excerpt_exception": "under_30_verified",
    },
    (
        "us_israel_iran_war_preparation_2025",
        "source-archive/statecraft/2025-01-14/source-judging-freedom-amb-chas-freeman-netanyahu-instigating-war-with-iran-2025-01-14.md",
    ): {
        "public_excerpt": (
            "Israel and Iran preparing to strike each other as we speak Ambassador the latest report "
            "a war or not but both sides are clearly preparing for one"
        ),
    },
    (
        "us_israel_iran_war_preparation_2025",
        "source-archive/statecraft/2025-01-24/source-dialogue-works-amb-chas-freeman-is-the-world-on-the-brink-of-total-chaos-2025-01-24.md",
    ): {
        "public_excerpt": (
            "by crippling Husalah and by uh uh greatly weakening Hamas um Iran has been left naked to "
            "Israeli attack it's been stripped of its forward defenses and this has increased the pressure "
            "inside Iran to develop a nuclear deterrent"
        ),
    },
    (
        "us_israel_iran_war_preparation_2025",
        "source-archive/statecraft/2025-04-04/source-dialogue-works-mohammad-marandi-larry-wilkerson-and-chas-freeman-on-middle-east-erupts-iran-challenges-ultimatum-2025-04-04.md",
    ): {
        "public_excerpt": (
            "the Iranians have been preparing themselves for a potential war literally since the invasion "
            "of Iraq, I would say, with all these underground drone uh and missile bases as well as other "
            "facilities that they have built"
        ),
    },
    (
        "iran_great_power_direct_war_entry",
        "source-archive/statecraft/2025-03-28/source-dialogue-works-amb-chas-freeman-will-iran-get-backup-from-russia-and-china-against-the-u-s-2025-03-28.md",
    ): {
        "public_excerpt": (
            "My expectation would be in the case of the Russians that they would accelerate the transfer of "
            "technology and weapons to Iran but would not involve themselves directly."
        ),
        "excerpt_exception": "under_30_verified",
    },
    (
        "iran_great_power_direct_war_entry",
        "source-archive/statecraft/2026-04-28/source-judging-freedom-freeman-what-russia-can-do-for-iran-2026-04-28.md",
    ): {
        "public_excerpt": (
            "Freeman reads the Russian dimension as material enough to affect diplomacy, UN positioning, "
            "and the broader stamina of the anti-Iran coalition."
        ),
        "excerpt_exception": "summary_grade_capture",
        "context_note": "Operator summary capture; not verbatim transcript.",
    },
    (
        "china_tariff_capitulation_2025",
        "source-archive/statecraft/2025-04-04/source-dialogue-works-mohammad-marandi-larry-wilkerson-and-chas-freeman-on-middle-east-erupts-iran-challenges-ultimatum-2025-04-04.md",
    ): {
        "public_excerpt": (
            "Um and a final point is u you know given the uh tariff tantrum that Mr. Trump has just uh "
            "thrown on the world, Iran's actually very fortunate. You don't have much trade with us."
        ),
    },
    (
        "china_tariff_capitulation_2025",
        "source-archive/statecraft/2025-04-22/source-judging-freedom-amb-charles-freeman-will-china-cave-on-trumps-tariffs-2025-04-22.md",
    ): {
        "public_excerpt": "There will be no um capitulation preemptive or otherwise by the Chinese.",
        "excerpt_exception": "short_decisive_sentence",
    },
    (
        "china_tariff_capitulation_2025",
        "source-archive/statecraft/2026-02-24/source-judging-freedom-freeman-israel-pushes-us-into-another-endless-war-2026-02-24.md",
    ): {
        "public_excerpt": (
            "Why haven't the Iranians capitulated in the face of all the force that the United States has "
            "deployed? half of the US Air Force, two of the three active aircraft carriers would be involved."
        ),
        "excerpt_exception": "rhetorical_analogy",
        "context_note": "Analogical framing on capitulation under force; China tariff stance appears in other rows.",
    },
    (
        "china_tariff_capitulation_2025",
        "source-archive/statecraft/2026-03-17/source-judging-freedom-freeman-will-china-dump-trump-2026-03-17.md",
    ): {
        "public_excerpt": (
            "Did uh Trump dump China, or did China dump Trump? The Trump-Xi meeting is now officially off. "
            "My own view is that President Xi didn't want a picture on the front page with Trump while we "
            "are attacking Iran."
        ),
    },
}


def load_v1_touchpoints() -> list[dict]:
    data = json.loads(FREEMAN_PREDICTIONS_JSON.read_text(encoding="utf-8"))
    rows: list[dict] = []
    for event in data["events"]:
        event_id = event["event_id"]
        for tp in event["touchpoints"]:
            rows.append(
                {
                    "event_id": event_id,
                    "capture": tp["capture"],
                    "stance": tp["stance"],
                    "speech_act": tp["speech_act"],
                    "public_excerpt": tp["quote"],
                }
            )
    return rows


def apply_overrides(row: dict) -> dict:
    key = (row["event_id"], row["capture"])
    override = EXCERPT_OVERRIDES.get(key)
    if not override:
        return row
    merged = dict(row)
    merged.update(override)
    return merged


def finalize_row(row: dict, capture_body: str) -> dict:
    row = dict(row)
    if row.get("excerpt_exception"):
        return row
    excerpt = str(row.get("public_excerpt") or "").strip()
    if excerpt_in_capture(excerpt, capture_body) and word_count(excerpt) < 30:
        row["excerpt_exception"] = "under_30_verified"
    return row


def build_rows() -> list[dict]:
    rows: list[dict] = []
    for row in load_v1_touchpoints():
        cap_path = REPO_ROOT / row["capture"].replace("\\", "/")
        _, body = parse_capture_frontmatter(cap_path.read_text(encoding="utf-8"))
        rows.append(finalize_row(apply_overrides(row), body))
    return rows


def validate_rows(rows: list[dict]) -> list[str]:
    issues: list[str] = []
    for row in rows:
        cap_path = REPO_ROOT / row["capture"].replace("\\", "/")
        if not cap_path.is_file():
            issues.append(f"missing capture {row['capture']}")
            continue
        _, body = parse_capture_frontmatter(cap_path.read_text(encoding="utf-8"))
        label = f"{row['event_id']} @ {row['capture']}"
        for err in validate_public_excerpt(row, body):
            issues.append(f"{label}: {err}")
    return issues


def write_map(rows: list[dict], *, dry_run: bool = False) -> None:
    payload = {
        "_meta": {
            "description": "Curated capture map for Freeman prediction public record v2",
            "rows": len(rows),
        },
        "rows": rows,
    }
    if dry_run:
        print(json.dumps(payload, indent=2)[:2000])
        return
    FREEMAN_CAPTURE_MAP.parent.mkdir(parents=True, exist_ok=True)
    FREEMAN_CAPTURE_MAP.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"[ok] wrote {FREEMAN_CAPTURE_MAP.relative_to(REPO_ROOT)} ({len(rows)} rows)")


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    check_only = "--check" in sys.argv
    rows = build_rows()
    issues = validate_rows(rows)
    if issues:
        for line in issues:
            print(line, file=sys.stderr)
        print(f"bootstrap_freeman_capture_map: {len(issues)} issue(s)", file=sys.stderr)
        return 1
    if check_only:
        print(f"[ok] capture map valid ({len(rows)} rows)")
        return 0
    write_map(rows, dry_run=dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
