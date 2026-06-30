# Statecraft Artifact Registry


This is the minimal registry law for new or touched statecraft outputs. It does not try to catalog the entire backfile in v1. Its purpose is to give every new or revised artifact a canonical metadata shape so compiled views, audits, and comparison surfaces can exist later without reinterpreting each note from scratch.

## Required Metadata

Every new or materially revised statecraft artifact should be classifiable by:

- `lane`: `america`, `china`, `persia`, `russia`, `comparison`, `cross-lane`, or `shared`
- `output_class`: `commentary`, `braid`, `lane-note`, `memo`, `objection-matrix`, `comparison`, `router-candidate`, `transaction-use-brief`, `lane-draft`, `full-transaction`, or `recursive-update-candidate`
- `prose_class`: `none`, `note-class`, or `essay-class`
- `maturity`: `orientation`, `draftable`, `reusable`, or `review-only`
- `source_family`: `civ-state`, `speaker-state`, `verified-live-event`, `lane-local`, or `mixed`
- `bridge_usage`: `none`, `marandi`, `parsi`, or `other-adapter`
- `transaction_relevance`: `none`, `fit-check`, `existing-transaction`, or `new-candidate`

## Canonical Block

Use this block near the top of a new or touched artifact when practical, or keep the same fields explicit in equivalent prose:

```markdown
**Statecraft Registry**
- Lane:
- Output class:
- Prose class:
- Maturity:
- Source family:
- Bridge usage:
- Transaction relevance:
```

## Classification Rules

- Use the **narrowest honest output class**.
- `prose_class` is for discoverability across prose shelves:
  - use `note-class` for bounded mechanisms, route seams, threshold distinctions, audit objects, or comparison seams
  - use `essay-class` for stand-alone arguments that should travel outside the original routing context
  - use `none` when the artifact is not really a prose-shelf object
- `maturity` measures what the artifact can currently support, not what the operator hopes it will become.
- `source_family` should name the real dominant feed, not every citation in the document. Use `verified-live-event` when the artifact is primarily driven by a bounded live-event read or packet rather than deep source shelves alone.
- `bridge_usage` is only for retrieval conditioning, not for ordinary speaker citation.
- `transaction_relevance` should say whether the artifact is outside the transaction plateau, checking fit, spending an existing bundle, or proposing a genuinely new candidate.

## Boundary

- This registry does not replace [statecraft.md](statecraft.md); it implements the kernel’s output law.
- This registry does not auto-promote artifacts.
- This registry does not backfill old statecraft notes in v1 unless they are being actively touched.
