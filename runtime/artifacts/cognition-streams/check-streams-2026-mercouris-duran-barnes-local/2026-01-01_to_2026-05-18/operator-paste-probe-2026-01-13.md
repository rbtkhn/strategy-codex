# Operator-Paste Probe - 2026-01-13 Barnes / The Duran

**Status:** superseded by `operator-paste-receipt-2026-01-13.md`.

This probe checked a later, truncated wrapper source. A broader session-log search found the original full paste at `C:\Users\rober\.codex\sessions\2026\05\17\rollout-2026-05-17T22-44-22-019e3966-3d71-7fb2-b1e9-d835d6f0d596.jsonl` line `3732`, which exact-match verified successfully.

## Target

- Date: `2026-01-13`
- Video ID: `O3tOyjSUs0M`
- Title: `Regime change escalator w/ Robert Barnes (Live)`
- Raw-input path: `codex/years/2026/raw-input/2026-01-13/transcript-duran-mercouris-barnes-regime-change-escalator-2026-01-13.md`

## Probe

- Local session log searched: `C:\Users\rober\.codex\sessions\2026\05\18\rollout-2026-05-18T06-33-16-019e3b13-88f3-7c51-9c59-a87102bdc326.jsonl`
- Matching source line: `186`
- Matching source type: `response_item` / `message` / `role=user`
- Extracted Jan transcript chars before next user message: `7923`
- Contains truncation marker: `true`
- Contains omitted marker: `true`

## Verdict

Original probe verdict: do **not** promote from this truncated source.

The available local session source for the Jan 13 paste is transcript-bearing but truncated. Because the source itself includes truncation / omitted markers, exact-match verification cannot establish a full transcript capture. The correct state remains `partial-chat-capture` with `full-transcript-import-needed`.

## Supersession

This failed probe is retained as a cautionary receipt only. The repair was closed from the original full paste source recorded in `operator-paste-receipt-2026-01-13.md`, which satisfied:

- `sourceChars`
- `bodyChars`
- `exactMatch=True`
- no truncation / omitted markers in the extracted source
