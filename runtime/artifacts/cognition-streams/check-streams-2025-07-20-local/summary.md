# check-streams 2025-07-20 local summary

Run date: 2026-05-20

Scope: `check-streams july 20 2025`

## Discovery Status

- Live audit attempted with `py scripts/cognition_streams_audit.py --start 2025-07-20 --end 2025-07-20 --recent-start 2025-07-20`.
- The live audit timed out after repeated YouTube bot-check failures.
- It left partial discovery receipts for Daniel Davis and Glenn Diesen only.
- Trusted entries below come from local cached channel indexes with exact `2025-07-20` date ties and direct YouTube watch URLs.
- A narrow web check found a third-party repost of the Glenn Diesen candidate, but did not safely date-tie the upload to `2025-07-20`.

## Aired / Trusted Set

| Channel | Video ID | Title | Duration | URL | Classification |
| --- | --- | --- | ---: | --- | --- |
| Daniel Davis / Deep Dive | `StRoCjG5o-Y` | Col Doug Macgregor: MORE WEAPONS for UKRAINE is MEANINGLESS | 1039s | https://www.youtube.com/watch?v=StRoCjG5o-Y | main / short standalone |
| Daniel Davis / Deep Dive | `38x09G1qLJI` | John Mearsheimer: TRUMP will be facing ENDLESS TROUBLE /Putin Won't Relent in 50 Days | 1125s | https://www.youtube.com/watch?v=38x09G1qLJI | main / short standalone |
| Dialogue Works | `WzbfmCkBkXc` | Iran, Russia & China UNLEASH Epic Counterstrike Against the West! \| Alex Krainer | 2836s | https://www.youtube.com/watch?v=WzbfmCkBkXc | main; partial operator paste |
| Dialogue Works | `bSsKJL-Y_sU` | Israel WON’T Survive Next War with Iran – Yemen Proved It \| Larry C. Johnson & Col. Larry Wilkerson | 2037s | https://www.youtube.com/watch?v=bSsKJL-Y_sU | main; captured via operator paste |
| Alex Mercouris / The Duran | `CDeCU5yJ8Uc` | Pokrovsk Siege Tightens, Alarmed US Orders Zelensky Restart Istanbul Talks; China Buys Russian Oil | 5422s | https://www.youtube.com/watch?v=CDeCU5yJ8Uc | main; captured via operator paste |

## Suspected Clips / Highlights

None confidently separated from the trusted set. The Daniel Davis items are short standalone uploads rather than obvious clipped highlights based on local index metadata.

## Date-Ambiguous / Unresolved

- Glenn Diesen: live audit surfaced `TS6TY75l2Pw`, title `George Beebe: Europe-Russia War as the U.S. Pulls Back?`, URL https://www.youtube.com/watch?v=TS6TY75l2Pw, duration `1975s`, but the audit could not resolve the upload date because YouTube bot-check blocked metadata. Treat as date-ambiguous until independently date-tied.
- Judging Freedom / Judge Napolitano: no trusted `2025-07-20` YouTube watch URL recovered from local cached indexes, RSS/audit, or web search in this pass.

## Manual-Fetch Queue

Trusted date-tied URLs:

- Captured: https://www.youtube.com/watch?v=CDeCU5yJ8Uc
- Captured: https://www.youtube.com/watch?v=bSsKJL-Y_sU
- Partial: https://www.youtube.com/watch?v=WzbfmCkBkXc

Remaining:

- https://www.youtube.com/watch?v=StRoCjG5o-Y
- https://www.youtube.com/watch?v=38x09G1qLJI

Date-ambiguous candidate, not in trusted queue:

- https://www.youtube.com/watch?v=TS6TY75l2Pw

## Operator-Paste Repair

- `CDeCU5yJ8Uc` captured to `codex/years/2026/raw-input/2025-07-20/youtube-alex-mercouris-pokrovsk-siege-tightens-alarmed-us-orders-zelensky-restart-istanbul-talks-china-buys-russian-oil-2025-07-20.md`
- Receipt: `runtime/artifacts/cognition-streams/check-streams-2025-07-20-local/operator-paste-receipt-CDeCU5yJ8Uc.md`
- Source/body verification: `sourceChars=57062; bodyChars=57062; exactMatch=True before normalized proper-name repairs`
- Quality: `transcript-bearing`; word count `9902`; residual noise `none`
- `bSsKJL-Y_sU` captured to `codex/years/2026/raw-input/2025-07-20/youtube-dialogue-works-israel-wont-survive-next-war-with-iran-yemen-proved-it-larry-c-johnson-col-larry-wilkerson-2025-07-20.md`
- Receipt: `runtime/artifacts/cognition-streams/check-streams-2025-07-20-local/operator-paste-receipt-bSsKJL-Y_sU.md`
- Source/body verification: `sourceChars=27417; bodyChars=27417; exactMatch=True against local Codex session operator paste`
- Quality: `transcript-bearing`; word count `4965`; routeable `yes`; unresolved speaker `no`; residual noise `none`
- `WzbfmCkBkXc` partially captured to `codex/years/2026/raw-input/2025-07-20/youtube-dialogue-works-iran-russia-china-unleash-epic-counterstrike-against-the-west-alex-krainer-2025-07-20.md`
- Receipt: `runtime/artifacts/cognition-streams/check-streams-2025-07-20-local/operator-paste-receipt-WzbfmCkBkXc.md`
- Source/body verification: `sourceChars=36822; bodyChars=36822; exactMatch=True against local Codex session operator paste`
- Quality: `transcript-bearing`; word count `6818`; routeable `yes`; unresolved speaker `no`; residual noise `none`; capture status `partial-operator-paste`

## Notes

One transcript/raw-input file was materialized for this date in this pass. If the operator pastes transcripts for the remaining watch URLs above, capture each as `youtube_transcript_operator_paste` and write a matching operator-paste receipt.
