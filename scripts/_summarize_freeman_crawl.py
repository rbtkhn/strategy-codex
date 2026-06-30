#!/usr/bin/env python3
"""Print operator audit summary for freeman-prediction-crawl.json."""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / "runtime" / "artifacts" / "freeman-prediction-crawl.json"

ORDER = [
    "israel_self_destruction_trajectory",
    "ukraine_escalation_russian_capitulation",
    "gaza_hostage_deal_jan_2025",
    "gaza_ceasefire_holds_2025",
    "us_israel_iran_war_preparation_2025",
    "iran_great_power_direct_war_entry",
    "china_tariff_capitulation_2025",
]


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = data["rows"]
    meta = data.get("_meta", {})
    by_event: dict[str, list] = defaultdict(list)
    for row in rows:
        by_event[row["event_id"]].append(row)

    print("=== Freeman crawl manifest — audit summary ===")
    print(f"Meta capture_count: {meta.get('capture_count')}")
    print(f"Manifest rows: {len(rows)}")
    print(f"Global audit_status: {dict(Counter(r.get('audit_status') for r in rows))}")
    print(f"Global match_method: {dict(Counter(r.get('match_method') for r in rows))}")
    print()
    print("| event_id | rows | pending | approved | rejected | defer | date range |")
    print("| --- | ---: | ---: | ---: | ---: | ---: | --- |")
    for eid in ORDER:
        ev = by_event.get(eid, [])
        st = Counter(r.get("audit_status") for r in ev)
        dates = [r["pub_date"] for r in ev] if ev else ["—"]
        dr = f"{min(dates)}..{max(dates)}" if ev else "—"
        print(
            f"| `{eid}` | {len(ev)} | {st.get('pending', 0)} | "
            f"{st.get('approved', 0)} | {st.get('rejected', 0)} | "
            f"{st.get('defer', 0)} | {dr} |"
        )
    print()

    for eid in ORDER:
        ev = sorted(by_event.get(eid, []), key=lambda r: (r["pub_date"], r["source"]))
        if not ev:
            continue
        meth = Counter(r.get("match_method") for r in ev)
        print(f"### {eid} ({len(ev)} rows) — match_method {dict(meth)}")
        for row in ev[:4]:
            slug = Path(row["source"]).name
            sug = row.get("suggested_speech_act") or "—"
            print(f"- {row['pub_date']} · `{row['match_method']}` · sug={sug} · `{slug}`")
        if len(ev) > 6:
            print(f"- … ({len(ev) - 6} more)")
            for row in ev[-2:]:
                slug = Path(row["source"]).name
                sug = row.get("suggested_speech_act") or "—"
                print(f"- {row['pub_date']} · `{row['match_method']}` · sug={sug} · `{slug}`")
        elif len(ev) > 4:
            for row in ev[4:]:
                slug = Path(row["source"]).name
                sug = row.get("suggested_speech_act") or "—"
                print(f"- {row['pub_date']} · `{row['match_method']}` · sug={sug} · `{slug}`")
        print()

    pairs = Counter((r["source"], r["event_id"]) for r in rows)
    dups = sum(1 for v in pairs.values() if v > 1)
    print(f"Duplicate (source, event_id) pairs: {dups}")
    print()
    print("**Seed notes (9) are excluded** from manifest — already materialized.")
    print("**Next:** edit manifest `audit_status` / `audit_stance` / `audit_speech_act` per row, then materialize.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
