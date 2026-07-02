# Karajan Close - Transcript Cleanup And Deferred Families

non-authoritative. Not Record. Artifact-first conductor close.

## Object

Transcript-cleanup sequence, Jan 1/Jan 2 cleaned-80 derivatives, the provenance-score refinement, and the remaining May capture worktree.

## What Moved

Two narrow commits shipped the durable transcript-cleanup line:

- `0694e3f4 Add transcript cleanup skill`
- `7c9ec1c0 Penalize transcript cleanup provenance conflicts`

The arc held because the work separated **body cleanup quality** from **source provenance quality**. The Martyanov miss turned declared guest names into a cleanup obligation. The Davis falsifier then exposed a second scoring seam: readable, well-reflowed text should still lose perfect-score status when source metadata conflicts, such as `caption_kind` disagreeing with `source_note` or a host-only `guest` inference.

## Falsify / Next Test

A future transcript-cleanup run should fail to score `100` if source metadata has a known provenance conflict, even when the cleaned body is readable and well reflowed.

## Abundance / Scarcity

Abundance helped with generation, cleanup, and rapid regression design. Scarcity was genuinely binding at evaluation time: a high score was not trustworthy until the receipt made clear what the score covered and what it did not.

## Deferred Families

- **May capture cluster:** final target verdict plus matching May 16 raw-inputs and exact speaker receipts may become a narrow commit after one staging pass.
- **Substack raw-input cluster:** Pape/Crooke May 13/14 raw-inputs are a separate capture story.
- **Benchmark cluster:** composition benchmark artifacts for May 16/17 are work-layer calibration, separate from transcript capture.
- **Runtime / memory / cadence churn:** leave out of capture commits unless explicitly scoped.
- **Cici notebook cluster:** separate lane; do not mix with strategy-codex transcript work.

## Escalation

`[watch]` May capture cluster remains uncommitted. Commit only a final target-day slice after excluding superseded audit dirs, broad host-quality churn, memory/dream/cadence residue, Substack raw-inputs, benchmarks, and Cici notebook files.

## Rule Candidate

`transcript-cleanup` should keep treating provenance as part of study usability, not as an upstream afterthought. Future cleaner scores need visible components for both text-body cleanup and source-metadata trust.

## Next Narrow Move

Stage the May 16 target-day capture slice from final artifacts and verify the staged diff tells one story.
