# Statecraft archive index ROI


Purpose: quantify the practical gains from adding generated month, year, thread, and stale-audit indices to the canonical statecraft archive.

Scope: this note estimates operational benefit from the navigation layer now present under [source-archive/statecraft](../../source-archive/statecraft/README.md), including:

- day indices at `source-archive/statecraft/YYYY-MM-DD/README.md`
- month indices at `source-archive/statecraft/YYYY-MM.md`
- year indices at `source-archive/statecraft/YYYY.md`
- [thread-index.md](../../source-archive/statecraft/thread-index.md)
- [stale-index-audit.md](../../source-archive/statecraft/stale-index-audit.md)

## Baseline

Current archive coverage exposed by the new layer:

- `17` month indices
- `2` year indices
- `411` day folders represented in stale audit
- `55` distinct threads in the thread index
- `1302` thread-linked source files in the thread index

## Estimated benefits

### 1. Date-navigation narrowing

Before the month and year layers, archive navigation was effectively:

`root -> day`

or, at best, an implicit search through dated folders.

Now the path is:

`root -> year -> month -> day`

Estimated first-step narrowing:

- annual navigation reduced from `17` month files to `2` year files
- date targeting inside `2025` reduced from `263` captured days to `12` month buckets before opening a month page

Estimated benefit:

- annual browse overhead reduced by about `88%`
- first-step date search space reduced by about `95%+` for `2025`

### 2. Thread retrieval compression

Before [thread-index.md](../../source-archive/statecraft/thread-index.md), finding all coverage for a lane such as `mercouris`, `davis`, `kent`, or `wilkerson` required scanning many day or month pages manually.

Now one page exposes:

- `55` distinct threads
- `1302` thread-linked files
- first and last day per thread
- top channels and hosts per thread

Estimated benefit:

- lookup hops for thread-based retrieval reduced from `dozens to hundreds` of day-page scans to `1` primary index page
- practical compression on thread discovery: roughly `100x` better in hop count for large lanes

### 3. Maintenance observability

Before [stale-index-audit.md](../../source-archive/statecraft/stale-index-audit.md), stale or missing day indices were found reactively.

The audit now surfaces the full status in one pass:

- day indices: `318 ok`, `85 stale`, `8 missing`
- month indices: `17 ok`
- year indices: `2 ok`
- thread index: `ok`

Estimated benefit:

- day-index maintenance visibility improved from partial/manual to effectively `100% surfaced`
- repair work converted from open-ended scanning to a bounded queue of `93` day-index issues

### 4. Summary-speed gain

Questions like:

- "what dominated 2026?"
- "which threads are heaviest in 2025?"
- "where does Kent actually appear?"
- "which month has the densest Mercouris concentration?"

can now be answered from one year page or the thread page rather than by cross-reading many month or day files.

Estimated benefit:

- operator summary time reduced by about `5x-15x` on common archive questions

## Net estimate

Reasonable overall estimate:

- navigation friction improved by about `5x-20x`, depending on task
- thread-lane retrieval improved by about `100x` in hop count for large threads
- annual top-level browse load reduced by about `88%`
- first-step date narrowing improved by about `95%+` on full-year targeting
- maintenance observability on archive indices improved to effectively `100%`

## Why this matters

The core gain is not just convenience. The new index layer changes archive work from:

- implicit
- memory-dependent
- reactive
- day-folder-heavy

to:

- explicit
- measurable
- auditable
- lane-aware

That makes both retrieval and upkeep more compounding over time.

## Return

- Root archive: [source-archive/statecraft/README.md](../../source-archive/statecraft/README.md)
- Thread index: [thread-index.md](../../source-archive/statecraft/thread-index.md)
- Stale audit: [stale-index-audit.md](../../source-archive/statecraft/stale-index-audit.md)
