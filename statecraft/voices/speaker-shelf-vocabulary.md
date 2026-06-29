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

## Flat shelf (2026-06)

Speaker and channel shelf roots are **flat** — no `stream/` or `themes/` subfolders. Theme registers use `{speaker}-themes.md`; monthly shelves use `{speaker}-shelf-YYYY-MM.md` or `{speaker}-monthly-shelves.md`. Legacy nested paths are compatibility residue only.

## Archive inventory vs voice source bench

Use **different surface classes** on opposite sides of the archive ↔ synthesis membrane. Do not call both a **source index**.

| Layer | Surface class | Surface name | Surface role | Interior grain |
| --- | --- | --- | --- | --- |
| Archive | Day inventory | `YYYY-MM-DD/day-index.md` | day archive inventory | stats; channel / writer / other partitions; file list |
| Archive | Day README stub | `YYYY-MM-DD/README.md` | pointer to day-index | link compat only |
| Archive | Ingest register | _(legacy; merged into day-index)_ | — | — |
| Archive | Month rollup | `YYYY-MM.md` | month archive rollup | one row per **day** |
| Archive | Thread rollup | `thread-index.md` | thread rollup | one row per `thread` slug |
| Synthesis | Source bench | `{speaker}-source-index.md` | voice source bench | curated archive anchors |

Navigation chain in prose:

`month rollup → day-index → source-*.md` → (promotion) → `voice source bench`

Rebuild SSOT after lands: `python3 scripts/refresh_statecraft_archive_indices.py` (day + month + year + thread + stale audit).

## Author/guest voice index (`{slug}-index.md`)

**Operator term:** **voice index** (not “shelf index”). **Voices router:** [`voice-index.md`](voice-index.md). **Registry dashboard:** [`voice-index-registry.md`](voice-index-registry.md).

**Surface role:** exhaustive month-grouped route map for **authored written** + **guest interview** captures on disk for a voice shelf (parsi, pape, crooke, ritter, …).

**Not the same as:**

| Surface | Job |
| --- | --- |
| `{slug}-index.md` | **Author/guest index** — every qualifying land must appear here |
| `writer-index.md` | Prose-outlet roster (Substack counts only) |
| `{slug}-forecast-ledger*.md` / `{slug}-interview-appearances*.md` | Interpretive routing — **do not** substitute for index listing |
| `day-index.md` | Day partition / stats |

**Source-intake law:** after `build_statecraft_day_indices.py --day`, any landed capture resolving to a voice shelf must be indexed before closeout:

1. `python scripts/shelf_index_from_capture.py --path <landed-file> --apply`
2. `python scripts/audit_statecraft_archive_index.py --shelf-index <slug>`

**Jiang exception:** `jiang-index.md` = external interview appearances only (rebuild: `python scripts/build_jiang_index.py`). PH channel + essays: `source-archive/statecraft/jiang-predictive-history-index.md` — not audited by `--shelf-index jiang` parity. Sneako #15 is dual-indexed.

**Pape rebuild:** `python scripts/build_pape_index.py` (full regen). **Boundary exclusions** (date stubs, verify-*) must be named in the shelf Boundary section and honored by `--shelf-index` audit.
