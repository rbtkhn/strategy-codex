WORK only; not Record.

# Speaker-Shelf Vocabulary

Purpose: give the speaker system one compact grammar for naming a surface, describing its job, and describing what it contains.

Use this note when a shelf, template, audit, or routing surface starts drifting into overloaded nouns.

## Three-Part Surface Grammar

Every named shelf surface should answer three different questions cleanly:

1. **Surface name**: what is this file called?
2. **Surface role**: what job does it perform?
3. **Surface interior**: what kind of material does it contain?

Do not let one noun do all three jobs when a sharper split is available.

## Core Table

| Surface family | Surface name | Surface role | Surface interior |
|---|---|---|---|
| Source routing | `source-index` | `source bench` | accepted transcript-bearing or source-bearing route entries |
| Evidence emphasis | not usually a file class | `provenance bench` | evidentiary breadth, lower-interpretation source coverage |
| Recurring continuity | `thread atlas` | recurring continuity map | `arc-threads` that cross hosts, months, or bounded runs |
| Bounded continuity | `arc` / `host-local arc` / `cross-host arc` | bounded interpretive routing | braid of `arc-threads` inside one bounded surface |
| Cross-host comparison | `helix` | compare host transformations without flattening them | differences, reinforcements, tensions across arcs |
| Maturity explanation | `support spine` | explain why a shelf is mature, light, or unfinished | receipts, structure, next-step law, limits |

## Default Naming Rules

- Name the source route surface `source-index`.
- Describe the ordinary retrieval job of that surface as the `source bench`.
- Reserve `provenance bench` for prose that is specifically stressing evidence breadth or archive-facing truth.
- Name the recurring continuity surface `thread atlas`.
- Use `arc-threads` for the strands named inside an atlas or braided inside an arc.
- Use `arc` for bounded motion, not for every recurring theme map.
- Use `helix` only when multiple host-local or equivalent arcs are being compared.

## Drift Tests

If a shelf note feels muddy, ask:

1. Is the file name being confused with the job it performs?
2. Is the job being confused with the material it contains?
3. Is an internal strand grammar being used as the surface class itself?

Common repair moves:

- rename the surface in prose, even if the compatibility filename stays old
- add one sentence separating the surface name from the surface role
- add one sentence naming the interior structure explicitly

## Compatibility Rule

Legacy filenames may persist for stability.

When they do:

- keep the old path if necessary
- name the canonical surface class in prose
- state explicitly when the filename is compatibility residue rather than current doctrine

The file path may stay old. The system's thinking should not.

## Archive inventory vs voice source bench

Use **different surface classes** on opposite sides of the archive ↔ synthesis membrane. Do not call both a **source index**.

| Layer | Surface class | Surface name | Surface role | Interior grain |
| --- | --- | --- | --- | --- |
| Archive | Day inventory | `YYYY-MM-DD/README.md` | day archive inventory | stats, rollups, file list |
| Archive | Ingest register | `## Ingest register` (day README section) | ingest register | one row per land; YouTube |
| Archive | Month rollup | `YYYY-MM.md` | month archive rollup | one row per **day** |
| Archive | Thread rollup | `thread-index.md` | thread rollup | one row per `thread` slug |
| Synthesis | Source bench | `{speaker}-source-index.md` | voice source bench | curated archive anchors |

Navigation chain in prose:

`month rollup → day inventory → ingest register → source-*.md` → (promotion) → `voice source bench`

Rebuild SSOT after lands: `python3 scripts/refresh_statecraft_archive_indices.py` (day + month + year + thread + stale audit).
