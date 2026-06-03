---
name: ph-civ-orientation-harden
description: Create or harden PH-CIV public orientation entries in Predictive History. Use when updating corpus/ph-civ entries, preserving reader-facing placement, limits, return paths, and internal-scaffold-free public navigation.
---

# PH-CIV Orientation Harden

Use this skill when creating or refining `corpus/ph-civ/` entries, route
guidance, or bridge guidance for Predictive History.

## Core rule

PH-CIV is reader orientation, not duplicate commentary. It should tell the
reader where a chapter sits, how to read it, what pressures matter, what limits
apply, and how to return to the source.

When the object is a route or bridge rather than a single chapter, preserve the
same discipline: orientation first, source floor second, support only when
difficulty appears, widened interpretation after that.

## Source-lattice rule

When PH-CIV prose is doing retrieval work rather than only local description,
ask whether the object needs a source-lattice companion.

Use a source-lattice when the reader needs a lawful order of operations across
multiple surfaces such as:

- corridor explainer
- routed cards or chapters
- support ring or bridge notes
- widened cross-volume or interpretive claims

The compact formula is:

```text
doorway -> primary source floor -> secondary support -> widened interpretation
```

For route and bridge work:

- keep the `doorway` reader-facing
- keep the `primary source floor` tied to the routed units or hinge sources
- use `secondary support` only when the route or bridge becomes unstable
- do not let the widened layer pretend to be the same thing as the source floor

## Required public sections

Every PH-CIV entry should keep:

- `Where This Sits`
- `Reading Posture`
- `Historical Pressure Points`
- `Limits of the Frame`
- `Return Path`

## Frontmatter expectations

Preserve existing fields and path traceability:

- `source_id`
- `title`
- `source_series`
- `publication_date`
- `source_corpus_path`
- `source_chapter_path`
- `commentary_path`
- `derived_corpus: ph-civ`
- `placement_weight`
- `review_status`

## Writing posture

- Keep entries compact and public-facing.
- Preserve `placement_weight`; do not inflate medium or light chapters.
- Surface limits in plain language.
- Use the companion commentary for detailed claims, not the PH-CIV entry.
- Keep internal scaffold terminology out of public PH-CIV files.

## When hardening

Strengthen:

- contested evidence boundaries
- analogy guardrails
- transcript cutoff caveats
- source-layer distinctions
- return paths into transcript and commentary
- route and bridge retrieval order when prose begins to span multiple layers

Avoid:

- turning PH-CIV into a second commentary
- adding unsupported new claims
- making the orientation more rhetorically weighty than the chapter fit allows
- exposing internal derivation terminology
- letting corridor or bridge prose silently replace the source floor

## Validation

Run:

```powershell
.\scripts\validate-ph-civ.ps1
```

Then scan changed PH-CIV entries for stale draft language and forbidden
internal terminology.
