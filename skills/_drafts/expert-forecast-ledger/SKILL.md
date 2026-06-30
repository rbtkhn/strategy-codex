---
name: expert-forecast-ledger
description: Draft workflow for building a WORK-only longitudinal expert forecast ledger from a bounded local source corpus, preserving source-class discipline, falsifiers, revisit triggers, and unresolved tensions.
preferred_activation: forecast ledger for <expert>
portable: true
version: 0.1.0-draft
category: domain-pack
status: draft
tags:
  - draft
  - work-strategy
  - forecast
  - source-discipline
---
# Expert forecast ledger

Use this draft skill when the operator asks for a longitudinal ledger such as:

- `forecast ledger for <expert>`
- `longitudinal ledger`
- `expert forecast ledger`
- `same for <expert>` after another expert ledger run

The goal is not to make a generic summary. The goal is to preserve forecast discipline: dated claims, mechanisms, falsifiers, revisit triggers, source boundaries, and unresolved contradictions.

## Core rule

Default to the narrowest defensible primary source set.

Do not mix authored essays, interviews, social bundles, transcripts, host-owned appearances, generated artifacts, and chat summaries into one smooth "expert said" surface unless the operator explicitly chooses that boundary. Source-class discipline is the value of this workflow.

## Source-boundary choices

Before drafting the ledger, discover the local corpus and choose one boundary:

- **Substack-only:** use `substack-<expert>-*.md` captures only. Best when the expert's Substack is the clean authored spine.
- **Authored:** use Substack plus other authored publications such as Responsible Statecraft or personal-site essays. Best when the lane doctrine treats those as primary expert-owned material.
- **All appearances:** include interviews, YouTube transcripts, X bundles, and host-owned appearances. Use only when explicitly requested, and label source classes visibly.

If the operator has not chosen and the lane has a clear consolidation note, follow that note. Otherwise ask a concise source-boundary question before writing.

## Discovery workflow

1. Inspect the target expert lane and raw-input corpus.
   - Look for `continuity/<year>/<expert>/README.md`.
   - Look for lane consolidation notes such as `<expert>-lane-consolidation-*.md`.
   - Search `raw-input` for source files matching the candidate boundary.
2. Record the exact source count.
3. Identify whether the active layout is `continuity/<year>/...` or `continuity/years/<year>/...`.
4. Choose the target path:
   - single-year ledger: `<expert>-forecast-ledger-<year>.md`
   - cross-year authored ledger: `<expert>-forecast-ledger-<start-year>-<end-year>.md`
5. Preserve WORK-only boundary language in the file header.

## Ledger shape

Create one Markdown hub with these sections:

1. **Source Set**
   - Table ordered by publication date.
   - Include date, title, raw-input link, phase label, and source class when more than one class is included.
   - Link every row to raw-input, not chat summaries, memory, generated artifacts, or refined pages.
2. **Phase Spine**
   - Compact longitudinal arc.
   - Use the expert's native pattern, not a borrowed template from another expert.
3. **Forecast / Mechanism / Warning / Diplomacy Ledger**
   - Choose the heading that fits the lane.
   - Minimum columns: `id`, `date`, `essay`, `claim_type`, `forecast_or_mechanism`, `mechanism`, `falsifier`, `revisit`, `status`, `notes`.
   - Add `source_class` when the source boundary includes more than one class.
4. **Contradictions / Tensions**
   - Preserve unresolved internal tensions.
   - Do not flatten them into a false synthesis.
5. **Verification Notes**
   - State the exact source count and included patterns.
   - State excluded source classes.
   - Note whether a future secondary corroboration layer is deferred.

## IDs and statuses

Use stable IDs:

- Forecast rows: `<EXPERT>-<YEAR>-F001`, or `<EXPERT>-<YEAR>-F###`.
- Cross-year rows may use the row's source year, for example `PARSI-2025-F001` and `PARSI-2026-F001`.
- Tension rows: `<EXPERT>-<YEAR>-T001`.

Use conservative statuses:

- `open`: horizon has not arrived, or outside verification is still needed.
- `held`: later source-corpus items explicitly reuse or confirm the mechanism.
- `weakened`: later items shift the center of gravity enough to reduce the original framing.
- `contradiction`: later items preserve an unresolved internal tension.

Never mark a row `held` from model judgment alone. It must be held inside the chosen source corpus, or externally verified in a separately labeled pass.

## Verification workflow

After drafting:

1. Count source files matching the chosen boundary.
2. Check every included filename appears in the ledger at least once.
3. Spot-check five to seven anchor rows against source text.
4. Check excluded source-path patterns do not appear as links.
5. Run Markdown/diff hygiene checks when working in a repo.
6. Confirm no Record surfaces were edited.

## Shelf link

If the expert lane has a README shelf, add one discoverability link to the new ledger. Do not update unrelated lane docs unless asked.

## Portable theory extraction

Use this optional step when the ledger produces a reusable theory rather than only a list of forecasts.

Trigger signs:

- the expert repeats a named claim across multiple dates or hosts;
- the claim changes the metric for judging a crisis;
- a rival frame must be preserved instead of silently displaced;
- the claim can be falsified with observable indicators;
- the claim would be useful outside the expert lane as a statecraft, strategy, or policy lens.

Create a compact **theory cluster** with:

1. **Theory name.** Use plain language, for example `Fourth-Center Power Thesis`.
2. **Metric.** Define what is being measured, for example coercive system leverage vs comprehensive national power.
3. **Source chain.** Link raw-input anchors and label source class: authored spine, interview transmission, X signal, host corroboration.
4. **Rival frame.** Preserve the competing interpretation rather than overwriting it.
5. **Falsifiers.** Name concrete indicators that would weaken the theory.
6. **Reusable bridge.** If useful, add or link a WORK-only statecraft / strategy sheet that turns the theory into a repeatable question.

Keep source boundaries explicit. If the ledger is Substack-only, do not count interview or transcript links as part of the Source Set; label them as secondary transmission or corroboration.

Good output shape:

- speaker compact-state note: what the theory says and what it does not say;
- forecast-ledger rows: dated predictions, mechanisms, falsifiers, revisit triggers;
- consolidation note: short metric guard for future readers;
- optional statecraft sheet: reusable question or decision test.

Anti-pattern:

- Do not turn a memorable phrase into doctrine without a metric and falsifiers.
- Do not let a new theory erase an older frame that may still be true under a different metric.
- Do not promote host phrasing as authored expert doctrine unless the source chain supports it.

## Anti-patterns

- Do not let source discovery become implementation of unrelated ingest work.
- Do not broaden the source boundary just because more material exists.
- Do not treat interviews as authored essays without explicit source-class labels.
- Do not turn moral intensity or rhetorical confidence into forecast validation.
- Do not edit Record surfaces.
