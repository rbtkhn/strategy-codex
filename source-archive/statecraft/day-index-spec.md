# Day-index — per-day archive inventory spec

_Short SSOT for derived **`day-index.md`** under `source-archive/statecraft/YYYY-MM-DD/`. Parallel to global [channel-index.md](./channel-index.md) and [writer-index.md](./writer-index.md)._

**Pilot (2026-06):** June 2026 captured days use `day-index.md`; older months may still use legacy full README until regen.

---

## Purpose

| Surface | Granularity | Job |
|---------|-------------|-----|
| **day-index.md** | One calendar day | Partition that day's lands into **channel**, **writer**, and **other** buckets |
| **README.md** (day folder) | Stub only | Pointer to `day-index.md` for link compatibility |
| **channel-index** | Global YouTube roster | check-sources aggregate |
| **writer-index** | Global prose roster | check-written aggregate |

Navigation chain:

`YYYY-MM.md` → `YYYY-MM-DD/day-index.md` → `source-*.md`

---

## Sections (per day)

| Section | Rule |
|---------|------|
| **Stats** | Counts including channel / writer / other partition |
| **Channel sources** | `is_youtube_capture(meta)` — same gate as channel-index |
| **Writer sources** | Not YouTube + matches configured writer roster ([writer-index-spec](./writer-index-spec.md)) |
| **Other sources** | Remaining `source-*.md` (unrostered prose, institutional, edge cases) |
| **Files** | Full filename list |

**Membrane:** At most one bucket per file. YouTube gate prevents channel/writer double-count.

---

## Builder

- `classify_day_captures()` — [statecraft_day_archive.py](../../scripts/statecraft_day_archive.py)
- `build_day_index()` / `build_day_readme_stub()`
- CLI: `python scripts/build_statecraft_day_indices.py --day YYYY-MM-DD` or `--month YYYY-MM`
- Reader: `python scripts/statecraft_day_source_index.py --day YYYY-MM-DD`

---

## Return

- Global YouTube roster: [channel-index.md](./channel-index.md)
- Global writer roster: [writer-index.md](./writer-index.md)
- Writer membrane: [writer-index-spec.md](./writer-index-spec.md)
- Root archive: [README.md](./README.md)
