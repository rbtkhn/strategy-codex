# check-streams 2025-06-20 local summary

Run date: 2026-05-20

Scope: `check-streams june 20 2025`

## Discovery Status

- Live audit attempted with `py scripts/cognition_streams_audit.py --start 2025-06-20 --end 2025-06-20 --recent-start 2025-06-20`.
- The live audit timed out after repeated YouTube bot-check failures and did not leave a durable day receipt directory.
- Trusted entries below come from local cached channel indexes with exact `2025-06-20` date ties and direct YouTube watch URLs.
- RSS checks did not return same-day historical hits for the unresolved channels.

## Aired / Trusted Set

| Channel | Video ID | Title | Duration | URL | Classification |
| --- | --- | --- | ---: | --- | --- |
| Daniel Davis / Deep Dive | `91LFeY6sOHk` | Iran-Israel Conflict ALREADY a PROXY WAR /Lt Col Daniel Davis & Patrick Henningsen | 972s | https://www.youtube.com/watch?v=91LFeY6sOHk | main / short standalone |
| Daniel Davis / Deep Dive | `ksStl8ytXzk` | Lt Col Daniel Davis: Iran-Israel War - DON'T ENTER into IT | 977s | https://www.youtube.com/watch?v=ksStl8ytXzk | main / short standalone; partial operator paste |
| Daniel Davis / Deep Dive | `t9BYlOyyh18` | Lt Col Daniel Davis: ISRAEL's NOT AS STRONG as You May Think | 920s | https://www.youtube.com/watch?v=t9BYlOyyh18 | main / short standalone |
| Daniel Davis / Deep Dive | `J5VXlbRHMjs` | BEATING IRAN is SIMPLE - DON'T BELIEVE IT /Lt Col Daniel Davis | 989s | https://www.youtube.com/watch?v=J5VXlbRHMjs | main / short standalone |
| Alex Mercouris / The Duran | `QVURQCEMKUI` | China Deploys Spy Ships; US Says Pulling Back; Iran Israel Continue Strikes; Kiev Israel Run Short | 5047s | https://www.youtube.com/watch?v=QVURQCEMKUI | main; captured via operator paste |

## Suspected Clips / Highlights

None confidently separated from the trusted set. The Daniel Davis items are short standalone uploads rather than obvious clipped highlights based on local index metadata.

## Date-Ambiguous / Unresolved

- Glenn Diesen: no trusted `2025-06-20` YouTube watch URL recovered from local cached indexes, RSS, or the timed-out live audit.
- Dialogue Works: no trusted `2025-06-20` YouTube watch URL recovered from local cached indexes, RSS, or the timed-out live audit.
- Judging Freedom / Judge Napolitano: no trusted `2025-06-20` YouTube watch URL recovered from local cached indexes, RSS, or the timed-out live audit.

## Manual-Fetch Queue

Captured:

- https://www.youtube.com/watch?v=QVURQCEMKUI
- https://www.youtube.com/watch?v=ksStl8ytXzk

Remaining:

- https://www.youtube.com/watch?v=91LFeY6sOHk
- https://www.youtube.com/watch?v=t9BYlOyyh18
- https://www.youtube.com/watch?v=J5VXlbRHMjs

## Operator-Paste Repair

- `QVURQCEMKUI` captured to `codex/years/2026/raw-input/2025-06-20/youtube-alex-mercouris-china-deploys-spy-ships-us-says-pulling-back-iran-israel-continue-strikes-kiev-israel-run-short-2025-06-20.md`
- Receipt: `runtime/artifacts/cognition-streams/check-streams-2025-06-20-local/operator-paste-receipt-QVURQCEMKUI.md`
- Source/body verification: `sourceChars=55788; bodyChars=55791; exactMatch=True before normalized proper-noun repair`
- Quality: `transcript-bearing`; word count `9763`; residual noise `none`
- `ksStl8ytXzk` partially captured to `codex/years/2026/raw-input/2025-06-20/youtube-daniel-davis-lt-col-daniel-davis-iran-israel-war-dont-enter-into-it-2025-06-20.md`
- Receipt: `runtime/artifacts/cognition-streams/check-streams-2025-06-20-local/operator-paste-receipt-ksStl8ytXzk.md`
- Source/body verification: `sourceChars=16011; bodyChars=16011; exactMatch=True against local Codex session operator paste`
- Quality: `transcript-bearing`; word count `2979`; residual noise `none`; capture status `partial-operator-paste`

## Notes

One transcript/raw-input file was materialized for this date in this pass. If the operator pastes transcripts for the remaining watch URLs above, capture each as `youtube_transcript_operator_paste` and write a matching operator-paste receipt.
