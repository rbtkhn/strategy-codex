---
name: predictive-history-chapter-spine
description: Materialize or extend Predictive History chapter spines from a transfer authority into the canonical repo. Use when creating new chapter batches, importing transcripts, wiring corpus entries, commentary placeholders, PH-CIV entries, manifests, and public navigation for predictive-history.
---

# Predictive History Chapter Spine

Use this skill when adding or extending chapter batches in
`rbtkhn/predictive-history`, especially from
`strategy-codex/codex/predictive-history` transfer material.

## Core rule

Create routing infrastructure before analysis. The spine pass should make
chapters navigable and traceable without pretending commentary is complete.

## Default workflow

1. Discover the source-of-truth transfer material.
   - Prefer strategy-codex lecture files and metadata already named by the
     repo.
   - Do not fetch directly from YouTube unless explicitly asked.
2. For each source unit, create or verify:
   - corpus source entry
   - Part I transcript file
   - Part II commentary file or placeholder
   - PH-CIV placement entry when the corpus requires it
   - manifest row and public index rows
3. Preserve standard metadata:
   - `representation_not_endorsement: true`
   - `rights_review: required_before_long_excerpt`
   - `transcript_status: curated_transcript_pending_rights_review`
   - `transcript_fidelity: exact_body_match` when copied exactly
4. Mark analysis honestly.
   - Use `draft_pending_analysis` for newly materialized placeholders.
   - Use `in-review` / `source_reviewed` only after source-backed commentary
     exists.
5. Update public status docs so readers can distinguish calibrated, in-review,
   and draft material.

## Route and bridge follow-on

When a newly materialized chapter batch stabilizes a public route or
cross-volume crossing, ask whether the repo now needs a lattice companion in
addition to the route explainer.

Typical triggers:

- a corridor now has a fixed canonical spine plus support-ring material
- a bridge now has a named hinge source plus widened application prose
- readers could plausibly confuse route prose, source floor, support notes, and
  interpretation

In those cases, create or refine a companion retrieval note using:

```text
doorway -> primary source floor -> secondary support -> widened interpretation
```

The spine pass still comes first. The lattice companion is a follow-on
clarifier, not a replacement for chapter materialization.

## Validation

Run the relevant repo validators after any spine pass:

```powershell
.\scripts\validate-civilization-spine.ps1
.\scripts\validate-ph-civ.ps1
```

Also scan for stale placeholders and forbidden internal terminology when
PH-CIV is involved.

## Failure modes

Avoid:

- adding manifest rows without files
- creating commentary that claims review before source-backed extraction
- losing source/commentary/PH-CIV traceability
- mixing public reader navigation with internal transfer-scaffold language
