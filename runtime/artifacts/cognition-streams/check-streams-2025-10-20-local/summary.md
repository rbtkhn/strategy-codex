# check-streams 2025-10-20 local summary

Run date: 2026-05-20

Scope: `check-streams oct 20 2025`

## Discovery Status

- Live audit attempted with `py scripts/cognition_streams_audit.py --start 2025-10-20 --end 2025-10-20 --recent-start 2025-10-20`.
- The live audit timed out after repeated YouTube bot-check failures and did not leave a trusted day receipt.
- Trusted entries below come from local cached channel indexes with exact `2025-10-20` date ties and direct YouTube watch URLs.
- Narrow web search corroborated the Mercouris candidate through The Duran Telegram repost, but the trusted date tie comes from the local cached index.
- PreserveTube showed Judging Freedom month-bucket entries only and did not provide a trusted `2025-10-20` date tie.

## Aired / Trusted Set

| Channel | Video ID | Title | Duration | URL | Classification |
| --- | --- | --- | ---: | --- | --- |
| Daniel Davis / Deep Dive | `CYcmm9KmMO4` | IRAN's NUCLEAR DILEMMA /Trita Parsi & Lt Col Daniel Davis | 1346s | https://www.youtube.com/watch?v=CYcmm9KmMO4 | main |
| Daniel Davis / Deep Dive | `Jc8t8SBhmCo` | Russia: All About DEMILITARIZING NATO /Andrei Martynaov & Lt Col Daniel Davis | 1684s | https://www.youtube.com/watch?v=Jc8t8SBhmCo | main |
| Glenn Diesen | `_HembJRfcFQ` | Alex Krainer: Europe's Militarism & Economic Decline | 3818s | https://www.youtube.com/watch?v=_HembJRfcFQ | main |
| Alex Mercouris / The Duran | `hGqf1_KeRXk` | Trump Zelensky Furious Row; US Tells Kiev Accept Moscow's Terms Or Be Destroyed; Pokrovsk Falls Fast | 5031s | https://www.youtube.com/watch?v=hGqf1_KeRXk | main |

## Suspected Clips / Highlights

None confidently separated from the trusted set.

## Date-Ambiguous / Unresolved

- Dialogue Works: no trusted `2025-10-20` YouTube watch URL recovered from local cached indexes, live audit, or web search in this pass.
- Judging Freedom / Judge Napolitano: no trusted `2025-10-20` YouTube watch URL recovered. PreserveTube's channel page listed October items in a broad month bucket, but not with a safe exact date tie.

## Manual-Fetch Queue

Trusted date-tied URLs:

- https://www.youtube.com/watch?v=CYcmm9KmMO4
- https://www.youtube.com/watch?v=Jc8t8SBhmCo
- https://www.youtube.com/watch?v=_HembJRfcFQ
- https://www.youtube.com/watch?v=hGqf1_KeRXk

## Notes

Captured transcripts materialized after operator paste:

- Daniel Davis / Deep Dive `CYcmm9KmMO4`: `codex/years/2026/raw-input/2025-10-20/youtube-daniel-davis-irans-nuclear-dilemma-trita-parsi-lt-col-daniel-davis-2025-10-20.md`
  - receipt: `runtime/artifacts/cognition-streams/check-streams-2025-10-20-local/operator-paste-receipt-CYcmm9KmMO4.md`
  - capture_status: `partial-operator-paste`
  - evidence_grade: `transcript-bearing`
  - exact-match verified; residual noise none; routeable speaker metadata present.
  - note: pasted transcript ends mid-sentence, so full-transcript import remains needed for this item.

- Daniel Davis / Deep Dive `Jc8t8SBhmCo`: `codex/years/2026/raw-input/2025-10-20/youtube-daniel-davis-russia-all-about-demilitarizing-nato-andrei-martynaov-lt-col-daniel-davis-2025-10-20.md`
  - receipt: `runtime/artifacts/cognition-streams/check-streams-2025-10-20-local/operator-paste-receipt-Jc8t8SBhmCo.md`
  - capture_status: `full-operator-paste`
  - evidence_grade: `transcript-bearing`
  - exact-match verified before normalized proper-name repairs; ASR variants normalized to `Martyanov` and `Kaja Kallas`.

- Glenn Diesen `_HembJRfcFQ`: `codex/years/2026/raw-input/2025-10-20/youtube-glenn-diesen-alex-krainer-europes-militarism-economic-decline-2025-10-20.md`
  - receipt: `runtime/artifacts/cognition-streams/check-streams-2025-10-20-local/operator-paste-receipt-_HembJRfcFQ.md`
  - capture_status: `full-operator-paste`
  - evidence_grade: `transcript-bearing`
  - exact-match verified before normalized proper-name repairs; ASR variant normalized to `Zelensky`.

- Alex Mercouris / The Duran `hGqf1_KeRXk`: `codex/years/2026/raw-input/2025-10-20/youtube-alex-mercouris-trump-zelensky-furious-row-us-tells-kiev-accept-moscows-terms-or-be-destroyed-pokrovsk-falls-fast-2025-10-20.md`
  - receipt: `runtime/artifacts/cognition-streams/check-streams-2025-10-20-local/operator-paste-receipt-hGqf1_KeRXk.md`
  - capture_status: `full-operator-paste`
  - evidence_grade: `transcript-bearing`
  - exact-match verified before normalized proper-name repairs; ASR variants normalized to `Zelensky`.

## Trusted-set capture status

- Captured: 4 / 4 trusted date-tied URLs.
- Full captures: 3 / 4.
- Partial captures: 1 / 4 (`CYcmm9KmMO4`, pasted transcript ended mid-sentence).
- Remaining trusted manual-fetch queue: full-transcript import needed only for `CYcmm9KmMO4`; no untouched trusted URLs remain.
- Unresolved channels remain unresolved only because no trusted date-tied URL was recovered for Dialogue Works or Judging Freedom in this pass.
