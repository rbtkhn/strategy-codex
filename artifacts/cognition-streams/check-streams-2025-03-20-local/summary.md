# check-streams 2025-03-20 local receipt

Run date: 2026-05-20

## Status

Live `cognition_streams_audit.py` discovery for 2025-03-20 timed out after repeated YouTube bot-check and upcoming-live responses. The date-tied trusted set below comes from local cached channel indexes plus the partial discovery receipts written by the live audit.

The live audit wrote partial discovery receipts for Daniel Davis, Glenn Diesen, Dialogue Works, and Judge Napolitano / Judging Freedom under `.codex-tmp/cognition-streams/2025-03-20_to_2025-03-20/`. Daniel Davis and Glenn Diesen returned empty uploads-playlist result sets, which conflicts with date-tied local index hits. Dialogue Works and Napolitano each returned one unresolved scheduled/live item without a trusted date, so both are excluded from the trusted set.

Three canonical raw-input files now exist under `codex/years/2026/raw-input/2025-03-20/`: `BWbDO4UJ0wg`, `Z2j4d9brMPc`, and `F2Uy1kGrVKQ`, all captured from operator-pasted transcript text and normalized for repeated speaker-name artifacts where needed.

## Sources Checked

- `.codex-tmp/cognition-streams/2025-03-20_to_2025-03-20/*.discovery.json`
- `.codex-tmp/davis-january/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/diesen-january/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/youtube-alex-mercouris-index/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/**/CHANNEL-VIDEO-INDEX.md` local index scan for `2025-03-20`
- `codex/years/2026/raw-input/2025-03-20/*.md`

## Aired / Trusted Set

| channel | youtube_id | class | duration | local status | title |
|---|---:|---|---:|---|---|
| daniel-davis-deep-dive | `Z_fULp_oam0` | main | 1179 | not captured | John Mearsheimer: Can Big-Stick Diplomacy Work on Iran? |
| daniel-davis-deep-dive | `BWbDO4UJ0wg` | main | 2498 | captured / transcript-bearing / full-operator-paste | John Mearsheimer "There'll be NO Meaningfulf CeaseFire" in Ukraine Russia War |
| daniel-davis-deep-dive | `V4d8F4g6TCc` | main / short standalone | 683 | not captured | The Non-Negotiables w/the Ukraine Russia War Ceasefire |
| glenn-diesen | `ni6gF3JH3cA` | main | 1934 | not captured | Gilbert Doctorow: US Control of Ukraine's Power Plants and Europe's Preparation for War |
| glenn-diesen | `Z2j4d9brMPc` | main | 2037 | captured / transcript-bearing / full-operator-paste | Seyed Marandi: Is Israel Destroying Itself? |
| glenn-diesen | `MWNsyhva87k` | main | 3420 | not captured | Lasha Kasradze: Does the EU Stabilise or Destabilise its Neighbourhood? |
| alex-mercouris | `F2Uy1kGrVKQ` | main | 5629 | captured / transcript-bearing / full-operator-paste | Trump No As Zelensky Begs Patriots; Wants Power Plants; Moscow All 4 Regions Ours, Sanctions To Stay |

## Suspected Clips / Highlights

No same-day clip/highlight candidate was trusted from local indexes in this pass.

## Date-Ambiguous / Unresolved

- Dialogue Works: live audit returned `FeTkzRHdYBQ` / `Matthew Hoh: The Pentagon's Biggest Lie About Iran`, but with no trusted publication date and an upcoming-live extractor error. It is not treated as a 2025-03-20 aired upload.
- Judge Napolitano / Judging Freedom: live audit returned `LBLqfUhUBc8` / `Israel, Gaza, and the Weaponization of Sexual Violence w/ Aaron Mate`, but with no trusted publication date and an upcoming-live extractor error. It is not treated as a 2025-03-20 aired upload.

## Operator-Paste Repair

- `BWbDO4UJ0wg` - raw input: `codex/years/2026/raw-input/2025-03-20/youtube-daniel-davis-deep-dive-john-mearsheimer-therell-be-no-meaningfulf-ceasefire-in-ukraine-russia-war-2025-03-20.md`; receipt: `artifacts/cognition-streams/check-streams-2025-03-20-local/operator-paste-receipt-BWbDO4UJ0wg.md`
  - sourceChars/bodyChars: `38077` / `38077`
  - exactMatch: `true` against the local Codex session operator paste before residual-noise repair
  - bodyWordCount: `6981`
  - normalization: repeated ASR spelling normalized to `Zelensky`
  - quality: `transcript-bearing`; routeable: `yes`; unresolved speaker: `no`
- `Z2j4d9brMPc` - raw input: `codex/years/2026/raw-input/2025-03-20/youtube-glenn-diesen-seyed-marandi-is-israel-destroying-itself-2025-03-20.md`; receipt: `artifacts/cognition-streams/check-streams-2025-03-20-local/operator-paste-receipt-Z2j4d9brMPc.md`
  - sourceChars/bodyChars: `27949` / `27949` before residual-noise repair; normalizedBodyChars: `27952`
  - exactMatch: `true` against the local Codex session operator paste before residual-noise repair
  - normalizedBodyWordCount: `5266`
  - normalization: two repeated ASR spellings normalized to `Marandi`
  - quality: `transcript-bearing`; routeable: `yes`; unresolved speaker: `no`
- `F2Uy1kGrVKQ` - raw input: `codex/years/2026/raw-input/2025-03-20/youtube-alex-mercouris-trump-no-as-zelensky-begs-patriots-wants-power-plants-moscow-all-4-regions-ours-sanctions-to-stay-2025-03-20.md`; receipt: `artifacts/cognition-streams/check-streams-2025-03-20-local/operator-paste-receipt-F2Uy1kGrVKQ.md`
  - sourceChars/bodyChars: `60812` / `60812` before residual-noise repair; normalizedBodyChars: `60814`
  - exactMatch: `true` against the local Codex session operator paste before residual-noise repair
  - normalizedBodyWordCount: `10717`
  - normalization: repeated ASR spellings normalized to `Zelensky`
  - quality: `transcript-bearing`; routeable: `no`; unresolved speaker: `yes`

## Manual-Fetch Queue

Highest-confidence direct YouTube URLs tied to 2025-03-20:

- `Z_fULp_oam0` - https://www.youtube.com/watch?v=Z_fULp_oam0 - John Mearsheimer: Can Big-Stick Diplomacy Work on Iran?
- `BWbDO4UJ0wg` - https://www.youtube.com/watch?v=BWbDO4UJ0wg - captured from operator paste; see Operator-Paste Repair above
- `V4d8F4g6TCc` - https://www.youtube.com/watch?v=V4d8F4g6TCc - The Non-Negotiables w/the Ukraine Russia War Ceasefire
- `ni6gF3JH3cA` - https://www.youtube.com/watch?v=ni6gF3JH3cA - Gilbert Doctorow: US Control of Ukraine's Power Plants and Europe's Preparation for War
- `Z2j4d9brMPc` - https://www.youtube.com/watch?v=Z2j4d9brMPc - captured from operator paste; see Operator-Paste Repair above
- `MWNsyhva87k` - https://www.youtube.com/watch?v=MWNsyhva87k - Lasha Kasradze: Does the EU Stabilise or Destabilise its Neighbourhood?
- `F2Uy1kGrVKQ` - https://www.youtube.com/watch?v=F2Uy1kGrVKQ - captured from operator paste; see Operator-Paste Repair above

Date-ambiguous / do not materialize as March 20 without fresh date evidence:

- `FeTkzRHdYBQ` - https://www.youtube.com/watch?v=FeTkzRHdYBQ - Matthew Hoh: The Pentagon's Biggest Lie About Iran
- `LBLqfUhUBc8` - https://www.youtube.com/watch?v=LBLqfUhUBc8 - Israel, Gaza, and the Weaponization of Sexual Violence w/ Aaron Mate
