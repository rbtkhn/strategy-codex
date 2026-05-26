# Raw-input index architecture audit

Generated: `2026-05-24T17:07:51Z`

WORK only; not Record. This is a heuristic audit over raw-input and speaker routing surfaces.

## Summary

- corpus-wide master indexes expected: `markdown=1`, `json=1`
- corpus-wide master indexes found: `markdown=1`, `json=1`
- speaker raw-input indexes present: `16`
- candidate arc index surfaces: `6`
- weak justification signals: `6`
- plausible missing benches: `11`

## Speaker raw-input indexes

- `blumenthal` -> [blumenthal-raw-input-index.md](codex/speakers/blumenthal/blumenthal-raw-input-index.md)
- `crooke` -> [crooke-raw-input-index.md](codex/speakers/crooke/crooke-raw-input-index.md)
- `davis` -> [davis-raw-input-index.md](codex/speakers/davis/davis-raw-input-index.md)
- `diesen` -> [diesen-raw-input-index.md](codex/speakers/diesen/diesen-raw-input-index.md)
- `freeman` -> [freeman-raw-input-index.md](codex/speakers/freeman/freeman-raw-input-index.md)
- `johnson` -> [johnson-raw-input-index.md](codex/speakers/johnson/johnson-raw-input-index.md)
- `macgregor` -> [macgregor-raw-input-index.md](codex/speakers/macgregor/macgregor-raw-input-index.md)
- `marandi` -> [marandi-raw-input-index.md](codex/speakers/marandi/marandi-raw-input-index.md)
- `mearsheimer` -> [mearsheimer-raw-input-index.md](codex/speakers/mearsheimer/mearsheimer-raw-input-index.md)
- `mercouris` -> [mercouris-raw-input-index.md](codex/speakers/mercouris/mercouris-raw-input-index.md)
- `napolitano` -> [napolitano-raw-input-index.md](codex/speakers/napolitano/napolitano-raw-input-index.md)
- `nima` -> [nima-raw-input-index.md](codex/speakers/nima/nima-raw-input-index.md)
- `pape` -> [pape-raw-input-index.md](codex/speakers/pape/pape-raw-input-index.md)
- `parsi` -> [parsi-raw-input-index.md](codex/speakers/parsi/parsi-raw-input-index.md)
- `ritter` -> [ritter-raw-input-index.md](codex/speakers/ritter/ritter-raw-input-index.md)
- `wilkerson` -> [wilkerson-raw-input-index.md](codex/speakers/wilkerson/wilkerson-raw-input-index.md)

## Candidate arc index surfaces

- `crooke` -> [crooke-march-may-2026-interview-arc-threads.md](codex/speakers/crooke/stream/crooke-march-may-2026-interview-arc-threads.md)
- `freeman` -> [freeman-dec-2025-may-2026-arc-threads.md](codex/speakers/freeman/stream/freeman-dec-2025-may-2026-arc-threads.md)
- `johnson` -> [johnson-april-may-2026-arc-threads.md](codex/speakers/johnson/stream/johnson-april-may-2026-arc-threads.md)
- `marandi` -> [marandi-2025-present-arc-threads.md](codex/speakers/marandi/stream/marandi-2025-present-arc-threads.md)
- `mercouris` -> [mercouris-arc-threads.md](codex/speakers/mercouris/stream/mercouris-arc-threads.md)
- `parsi` -> [parsi-2025-present-arc-threads.md](codex/speakers/parsi/stream/parsi-2025-present-arc-threads.md)

## Weak justification signals

- `crooke` -> [crooke-march-may-2026-interview-arc-threads.md](codex/speakers/crooke/stream/crooke-march-may-2026-interview-arc-threads.md) | index-like arc support surface exists alongside a speaker bench; verify it remains interpretive rather than becoming a duplicate retrieval surface.
- `freeman` -> [freeman-dec-2025-may-2026-arc-threads.md](codex/speakers/freeman/stream/freeman-dec-2025-may-2026-arc-threads.md) | index-like arc support surface exists alongside a speaker bench; verify it remains interpretive rather than becoming a duplicate retrieval surface.
- `johnson` -> [johnson-april-may-2026-arc-threads.md](codex/speakers/johnson/stream/johnson-april-may-2026-arc-threads.md) | index-like arc support surface exists alongside a speaker bench; verify it remains interpretive rather than becoming a duplicate retrieval surface.
- `marandi` -> [marandi-2025-present-arc-threads.md](codex/speakers/marandi/stream/marandi-2025-present-arc-threads.md) | index-like arc support surface exists alongside a speaker bench; verify it remains interpretive rather than becoming a duplicate retrieval surface.
- `mercouris` -> [mercouris-arc-threads.md](codex/speakers/mercouris/stream/mercouris-arc-threads.md) | index-like arc support surface exists alongside a speaker bench; verify it remains interpretive rather than becoming a duplicate retrieval surface.
- `parsi` -> [parsi-2025-present-arc-threads.md](codex/speakers/parsi/stream/parsi-2025-present-arc-threads.md) | index-like arc support surface exists alongside a speaker bench; verify it remains interpretive rather than becoming a duplicate retrieval surface.

## Missing bench candidates

- `aguilar` | transcript mentions=3; speaker markdown=2
- `armstrong` | transcript mentions=11; speaker markdown=8
- `barnes` | transcript mentions=13; speaker markdown=9
- `baud` | transcript mentions=31; speaker markdown=11
- `jiang` | transcript mentions=5; speaker markdown=9
- `kent` | transcript mentions=6; stream markdown=2; speaker markdown=5
- `krainer` | transcript mentions=6; speaker markdown=2
- `martyanov` | transcript mentions=14; speaker markdown=2
- `mcgovern` | transcript mentions=10; speaker markdown=2
- `postol` | transcript mentions=3; speaker markdown=2
- `sachs` | transcript mentions=11; speaker markdown=8

## Signal counts

| speaker | transcript mentions | stream markdown | speaker markdown |
|---|---:|---:|---:|
| `aguilar` | 3 | 0 | 2 |
| `alkorshid` | 20 | 0 | 1 |
| `armstrong` | 11 | 0 | 8 |
| `barnes` | 13 | 0 | 9 |
| `baud` | 31 | 0 | 11 |
| `beebe` | 0 | 0 | 4 |
| `berletic` | 2 | 0 | 8 |
| `blumenthal` | 5 | 0 | 9 |
| `carlson` | 3 | 0 | 0 |
| `crooke` | 13 | 33 | 10 |
| `davis` | 201 | 25 | 6 |
| `diesen` | 90 | 37 | 6 |
| `freeman` | 115 | 4 | 16 |
| `greenwald` | 0 | 0 | 0 |
| `jermy` | 0 | 0 | 9 |
| `jiang` | 5 | 0 | 9 |
| `johnson` | 47 | 3 | 14 |
| `karaganov` | 0 | 0 | 2 |
| `kent` | 6 | 2 | 5 |
| `krainer` | 6 | 0 | 2 |
| `macgregor` | 25 | 0 | 12 |
| `marandi` | 42 | 3 | 16 |
| `martyanov` | 14 | 0 | 2 |
| `mate` | 2 | 0 | 6 |
| `matlock` | 0 | 0 | 2 |
| `mcgovern` | 10 | 0 | 2 |
| `mearsheimer` | 21 | 0 | 30 |
| `mercouris` | 230 | 25 | 7 |
| `napolitano` | 56 | 16 | 5 |
| `nawfal` | 6 | 0 | 0 |
| `nima` | 126 | 18 | 3 |
| `pape` | 13 | 38 | 8 |
| `parsi` | 15 | 13 | 12 |
| `postol` | 3 | 0 | 2 |
| `ritter` | 43 | 35 | 10 |
| `sachs` | 11 | 0 | 8 |
| `wilkerson` | 24 | 0 | 8 |
