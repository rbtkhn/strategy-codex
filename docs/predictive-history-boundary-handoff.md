# Predictive History boundary handoff

This note summarizes the Predictive History boundary shift for operators, future assistants, and any public-facing explanation that needs a compact "what changed and why" block.

## Status

The boundary is landed in two commits on `main`:

- `3e339445` `Freeze Predictive History as external-only boundary`
- `40e0d395` `Align Predictive History boundary follow-up docs`

## Canonical ownership

The canonical writable Predictive History repo is:

- [`rbtkhn/ph-workshop`](https://github.com/rbtkhn/ph-workshop)

Inside `strategy-codex`, Predictive History is now an **external observed project**, not a local production lane.

## What changed

`strategy-codex` now treats these local trees as frozen migration residue / historical reference only:

- `codex/predictive-history/`
- `research/external/youtube-channels/predictive-history/`

The repo now includes:

- doctrine declaring external canonical ownership
- a validator and CI guardrail blocking normal edits to frozen PH paths
- deprecation of the old local `work_jiang` rebuild path
- operator docs and skill docs updated to stop advertising local PH production as the normal route

## What is now forbidden here

Inside `strategy-codex`, do **not**:

- create new canonical Predictive History lecture, chapter, registry, queue, or manuscript content
- regenerate PH corpus/manuscript artifacts as if this repo still owns them
- refresh the local PH transcript tree as an active ingest lane
- treat `codex/predictive-history/` as a live work surface

## What still belongs here

Allowed Predictive History work in `strategy-codex` now looks like:

- review packets
- pasted diffs or excerpts from the external repo
- editorial critique
- structure feedback
- source-discipline review
- strategy-notebook commentary on externally supplied PH material
- boundary doctrine or migration-maintenance updates

## Review packet flow

The standard flow is:

1. Do canonical writing and curation in [`rbtkhn/ph-workshop`](https://github.com/rbtkhn/ph-workshop).
2. Bring a bounded packet into `strategy-codex`.
3. Ask for one or more of:
   - editorial critique
   - structure feedback
   - source-discipline review
   - strategy resonance / notebook commentary
4. Keep resulting feedback in `strategy-codex` as critique or strategy context, not as a silent patch path back into PH.

Good packet shapes:

- one PR diff plus a few review questions
- one file snapshot plus a source-discipline check
- one chapter outline plus structure critique
- one prediction-tracking artifact plus strategy commentary

## One-line public/internal summary

`strategy-codex` is no longer the place where Predictive History gets written; it is now the place where Predictive History can be observed, reviewed, and critiqued without blurring canonical ownership.
