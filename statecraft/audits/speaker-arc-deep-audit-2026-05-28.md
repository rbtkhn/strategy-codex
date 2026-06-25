WORK only; not Record.

# Speaker Arc Deep Audit - 2026-05-28

Purpose: assess the live `statecraft/voices/` corpus for recursive self-improvement value across connectivity, consistency, completion, format, shelf-law clarity, and machine-auditability.

Scope:

- canonical speaker shelves under `statecraft/voices/`
- top-level speaker shelf doctrine in [statecraft/voices/README.md](/C:/dev/strategy-codex/statecraft/voices/README.md)
- top-level shelf surfaces (`README.md`, `index.md`, `*-arc.md`, `*-routing.md`, `*-source-index.md`, `*-support-spine*.md`, `*-helix.md`)
- speaker-owned `stream/` and `themes/` surfaces where present

Explicit carveout:

- the embedded Jiang mirror at [public/predictive-history/](/C:/dev/strategy-codex/public/predictive-history/README.md) was treated as a special mirror surface, not judged by ordinary shelf-link expectations

## Executive View

The speaker corpus is stronger than it looks at first glance. Shelf-class design is mostly coherent, the normalized month-ladder speakers are complete at the structural level, and most lighter shelves are tidy and retrieval-ready.

The real weakness is not missing architecture. It is migration drift:

- mature shelves still point into legacy `years/.../provenance` and `codex/years/.../provenance` paths
- some cross-host references still point at absent host-arc files
- Mercouris carries a second layer of internal stream dead-ends
- Jiang and Hoh now function as real exceptions, but the top-level doctrine does not yet name those exception classes cleanly

That means the highest-value next work is not broad redesign. It is targeted link-law repair plus a small amount of doctrinal normalization.

## Corpus Map

Observed speaker folders:

1. `barnes`
2. `crooke`
3. `freeman`
4. `hoh`
5. `jiang`
6. `johnson`
7. `macgregor`
8. `marandi`
9. `martyanov`
10. `mcgovern`
11. `mercouris`
12. `pape`
13. `parsi`
14. `postol`
15. `ritter`
16. `sachs`

Practical class map:

- Normalized month-ladder shelves: `crooke`, `freeman`, `johnson`, `macgregor`, `mercouris`, `ritter`
- Cross-context exception shelves: `pape`, `parsi`
- Lighter first-pass canonical shelves: `barnes`, `marandi`, `martyanov`, `mcgovern`, `postol`, `sachs`
- Starter exception shelf: `hoh`
- Embedded mirror exception shelf: `jiang`

## What Is Working

### 1. Shelf-law is mostly real, not decorative

The top-level doctrine in [statecraft/voices/README.md](/C:/dev/strategy-codex/statecraft/voices/README.md) broadly matches the actual corpus:

- all six normalized shelves have `README.md`, `index.md`, arc, routing, provenance bench, support spine, `stream/`, and `themes/`
- all six normalized shelves have a full bounded `2026-01` through `2026-05` monthly ladder
- lighter shelves are compact and consistent rather than pretending to be mature ladders
- cross-context shelves use a different internal law instead of being forced into fake month symmetry

### 2. Most shelves are connectivity-clean

Top-level shelf-plus-stream/theme link audit, excluding the Jiang mirror, shows zero broken local links for:

- `barnes`
- `freeman`
- `hoh`
- `jiang` top-level shelf surfaces
- `johnson`
- `marandi`
- `martyanov`
- `mcgovern`
- `pape`
- `parsi`
- `postol`

This is a strong baseline. The corpus is not broadly decaying everywhere.

### 3. Normalized month ladders are structurally complete

All normalized shelves expose:

- `*-shelf-2026-01.md`
- `*-shelf-2026-02.md`
- `*-shelf-2026-03.md`
- `*-shelf-2026-04.md`
- `*-shelf-2026-05.md`

Verified for:

- [crooke/stream](../speakers/crooke/stream/README.md)
- [freeman/stream](../speakers/freeman/stream/README.md)
- [johnson/stream](../speakers/johnson/stream/README.md)
- [macgregor/stream](../speakers/macgregor/stream/README.md)
- [mercouris/stream](../speakers/mercouris/stream/README.md)
- [ritter/stream](../speakers/ritter/stream/README.md)

This is valuable because it means the structural grammar is already reusable once link-law is repaired.

## Findings

### [P1] Connectivity debt is concentrated, deep, and migration-shaped

This is the dominant weakness in the corpus.

Broken-link concentration by speaker shelf, excluding the Jiang mirror:

- `crooke`: 180 broken local links across 15 files
- `mercouris`: 136 broken local links across 15 files
- `macgregor`: 10 broken local links across 2 files
- `ritter`: 6 broken local links across 1 file
- `sachs`: 3 broken local links across 3 files

Healthy shelves with zero broken links should be treated as the norm. The five shelves above are the real repair queue.

Representative files:

- [statecraft/voices/crooke/crooke-source-index.md](/C:/dev/strategy-codex/statecraft/voices/crooke/crooke-source-index.md)
- [statecraft/voices/crooke/crooke-interview-appearances-2025-2026.md](/C:/dev/strategy-codex/statecraft/voices/crooke/crooke-interview-appearances-2025-2026.md)
- [statecraft/voices/mercouris/stream/mercouris-arc-threads.md](/C:/dev/strategy-codex/statecraft/voices/mercouris/stream/mercouris-arc-threads.md)
- [statecraft/voices/mercouris/stream/mercouris-shelf-2026-01.md](/C:/dev/strategy-codex/statecraft/voices/mercouris/stream/mercouris-shelf-2026-01.md)
- [statecraft/voices/macgregor/macgregor-source-index.md](/C:/dev/strategy-codex/statecraft/voices/macgregor/macgregor-source-index.md)
- [statecraft/voices/ritter/ritter-source-index.md](/C:/dev/strategy-codex/statecraft/voices/ritter/ritter-source-index.md)
- [statecraft/voices/sachs/sachs-routing.md](/C:/dev/strategy-codex/statecraft/voices/sachs/sachs-routing.md)

Why this matters:

- retrieval trust falls when front-door surfaces do not resolve
- recursive audit tools start producing noise instead of guidance
- shelf maturity becomes overstated because the grammar looks complete but the routes are dead

### [P1] The broken-link pattern is systematic, not random

Broken local links cluster into six failure families:

1. Legacy `years/.../provenance` links: 213
2. Legacy `codex/years/.../provenance` links: 49
3. Missing internal Mercouris stream pages: 24
4. `academy/statecraft/...` pre-statecraft links: 18
5. Missing cross-host speaker arcs: 15
6. Other local missing targets: 16

This is good news operationally because a small number of deterministic rewrite rules should clear most of the debt.

Representative failure patterns:

- `../../years/2026/provenance/...`
- `/C:/dev/strategy-codex/codex/years/2026/provenance/...`
- `mercouris-thread.md`
- `mercouris-page-2026-04-05.md`
- `../diesen/stream/diesen-crooke-speaker-arc.md`
- `../../academy/statecraft/states/...`

### [P1] Top-level doctrine is missing two real shelf classes that now exist on disk

The constitutional shelf taxonomy in [statecraft/voices/README.md](/C:/dev/strategy-codex/statecraft/voices/README.md) covers normalized, cross-context, lighter first-pass, and host-led exception shelves well, but two actual classes are under-described:

- `hoh` is a real starter exception shelf with routing and provenance but without full canonical shelf status
- `jiang` is a mirror-bearing exception shelf whose primary value is an embedded public corpus mirror, not ordinary speaker shelf symmetry

Symptoms:

- [statecraft/voices/hoh/README.md](/C:/dev/strategy-codex/statecraft/voices/hoh/README.md) openly says it is "not yet a full canonical speaker shelf"
- [statecraft/voices/jiang/README.md](/C:/dev/strategy-codex/statecraft/voices/jiang/README.md) defines a mirror-first rule that does not fit the standard shelf classes

Why this matters:

- doctrine currently overfits the main speaker families
- future audits will keep mis-scoring Hoh and Jiang unless their exception law is made explicit

### [P2] Format grammar is strong at the README layer but weaker below it

README front doors are generally disciplined:

- almost all shelves start with the `WORK only; not Record.` fence
- almost all use `Open First`, `Canonical Structure`, and `Boundary`
- compatibility and boundary language is usually explicit

But the lower shelf surfaces vary sharply:

- some canonical files keep the `WORK only; not Record.` fence
- many equally canonical files omit it
- some canonical files use shared section grammar consistently
- others are prose-only or sparse

This is not a correctness bug by itself, but it lowers machine-auditability and makes shelf law harder to infer automatically.

Examples of especially tidy front doors:

- [statecraft/voices/parsi/README.md](/C:/dev/strategy-codex/statecraft/voices/parsi/README.md)
- [statecraft/voices/pape/README.md](/C:/dev/strategy-codex/statecraft/voices/pape/README.md)
- [statecraft/voices/sachs/README.md](/C:/dev/strategy-codex/statecraft/voices/sachs/README.md)

Examples of format irregularity:

- [statecraft/voices/hoh/README.md](/C:/dev/strategy-codex/statecraft/voices/hoh/README.md) places the H1 before the `WORK only; not Record.` fence and uses `Open first:` / `Boundary:` prose instead of the standard `##` sections
- several top-level non-README canonical surfaces omit the work fence entirely even within the same mature shelves, for example [statecraft/voices/crooke/crooke-arc.md](/C:/dev/strategy-codex/statecraft/voices/crooke/crooke-arc.md) and [statecraft/voices/mercouris/mercouris-routing.md](/C:/dev/strategy-codex/statecraft/voices/mercouris/mercouris-routing.md)

### [P2] Cross-host connectivity is under-owned

Some mature shelves still advertise host-lane openings that no longer exist at the named paths.

Clear cases:

- [statecraft/voices/crooke/README.md](/C:/dev/strategy-codex/statecraft/voices/crooke/README.md) points to absent Diesen, Davis, and Nima speaker arcs
- [statecraft/voices/sachs/README.md](/C:/dev/strategy-codex/statecraft/voices/sachs/README.md), [sachs-routing.md](/C:/dev/strategy-codex/statecraft/voices/sachs/sachs-routing.md), and [sachs-source-index.md](/C:/dev/strategy-codex/statecraft/voices/sachs/sachs-source-index.md) all point to a missing `diesen-sachs-speaker-arc.md`

Why this matters:

- routing notes are supposed to answer "what do I open first?"
- broken host-lane references are more damaging than deep provenance misses because they corrupt the first retrieval step

### [P2] Indexes are valuable, but there is no explicit machine-readable shelf manifest

`README.md` and `index.md` are not duplicates, which is good. The index files often function as richer route maps.

Example:

- [statecraft/voices/freeman/index.md](/C:/dev/strategy-codex/statecraft/voices/freeman/index.md) is a denser operational route surface than [freeman/README.md](/C:/dev/strategy-codex/statecraft/voices/freeman/README.md)

But the repo has no per-speaker manifest declaring:

- shelf class
- canonical first-open surfaces
- canonical support surfaces
- month ownership rule
- mirror / starter / exception flags

That means audits must infer law from prose instead of reading a compact SSOT.

### [P3] Jiang mirror depth creates avoidable audit noise

The embedded Jiang mirror contains a very large internal corpus:

- 756 markdown files
- 124 YAML files

It is structurally healthy as a mirror-led exception surface, but generic shelf audits will overcount it unless they deliberately carve it out.

Why this matters:

- a generic `statecraft/voices/**/*.md` audit produces too much mirror noise
- recursive self-improvement loops need mirror-aware tooling, not only speaker-aware tooling

## Completion Assessment

### High completion

- `freeman`
- `johnson`
- `parsi`
- `pape`
- `barnes`
- `marandi`
- `martyanov`
- `mcgovern`
- `postol`

These are structurally coherent and connectivity-clean.

### Structurally complete but repair-constrained

- `crooke`
- `mercouris`
- `macgregor`
- `ritter`
- `sachs`

These shelves largely know what they are, but route integrity has decayed.

### Intentionally partial

- `hoh`
- `jiang`

These should not be treated as failures, but their exception law needs clearer top-level doctrinal support.

## Recursive Self-Improvement Value

The highest-value recursive gains are:

1. Repair link-law on the five unhealthy shelves
2. Make shelf class explicit and machine-readable
3. Separate mirror audits from ordinary shelf audits
4. Normalize starter and mirror exception doctrine so future shelves are judged correctly

These are force-multipliers because they improve:

- retrieval reliability
- audit signal quality
- migration safety
- automation friendliness
- onboarding clarity for future assistants

## Recommended Repair Order

### Phase 1 - Connectivity sweep

Target shelves:

1. `crooke`
2. `mercouris`
3. `macgregor`
4. `ritter`
5. `sachs`

Repair rules:

- rewrite `years/.../provenance` links to `source-archive/statecraft/...`
- rewrite `codex/years/.../provenance` links to live `source-archive/statecraft/...` targets
- either materialize or remove stale Mercouris internal placeholders like `mercouris-thread.md`
- repair or replace missing cross-host arc references with real current openings
- rewrite stale `academy/statecraft/...` links to current `statecraft/...` or `statecraft/states/...` paths

### Phase 2 - Shelf manifest pass

For each speaker shelf, create a small machine-readable manifest, for example `speaker-shelf.yaml`, containing:

- `shelf_class`
- `open_first`
- `core_surfaces`
- `support_surfaces`
- `month_rule`
- `mirror_exception`
- `starter_exception`

This would remove a lot of audit ambiguity now encoded only in prose.

### Phase 3 - Doctrine normalization

Update [statecraft/voices/README.md](/C:/dev/strategy-codex/statecraft/voices/README.md) to add:

- starter exception shelves
- mirror-bearing exception shelves

Suggested live examples:

- `Hoh` as starter exception shelf
- `Jiang` as mirror-bearing exception shelf

### Phase 4 - Automated shelf health check

Add a repo script that scores each speaker shelf on:

- required files by shelf class
- broken local links
- month ladder completeness where applicable
- README section grammar
- unresolved legacy path patterns

That should become the standing recursive audit surface for this corpus.

## Bottom Line

The speaker-arc system is not suffering from conceptual failure. It is suffering from uneven migration completion.

The architecture is already good enough to scale. The next real leap comes from:

- making the shelf classes machine-legible
- restoring route integrity on the five unhealthy shelves
- treating Jiang and Hoh as first-class exceptions instead of silent anomalies

That is the highest-value path for recursive self-improvement because it improves both human trust and machine reuse without redesigning the corpus from scratch.
