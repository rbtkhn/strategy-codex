# Writer-index — inclusion spec

_Short SSOT for derived **`writer-index.md`** / **`writer-index.json`** under `source-archive/statecraft/`. Parallel to **[channel-index.md](./channel-index.md)** (YouTube / check-sources). **v1 built** — roster from [statecraft_writer_discovery.json](../../platform/config/statecraft_writer_discovery.json)._

**Inventory baseline (2026-06-21):** ~320 non-YouTube archive files vs ~1,432 YouTube. Unfiltered slug rollups **over-count** video recovery (e.g. `davis`, `napolitano`, `sachs` transcript paste). This spec defines filters so the builder stays prose-first.

---

## Purpose

| Index | Discovery unit | Operator skill (future) |
|-------|----------------|-------------------------|
| **channel-index** | YouTube channel (`channel_slug`) | **check sources** |
| **writer-index** | Recurring written outlet (`writer_slug`) | **check written** (TBD) |
| **thread-index** | Speaker / commentator thread (cross-modal) | lookup only |

**writer-index** answers: *“Which Substack feeds, essay series, and institutional prose outlets do we track, and how much is in archive?”*

It does **not** replace **thread-index** for guest-on-video or cross-host appearances.

---

## Hard excludes (never writer-index)

Apply **before** inclusion rules. A capture is **out of scope** when any of the following is true:

1. **`_is_youtube_capture(meta)`** — same helper as [build_statecraft_archive_navigation.py](../../scripts/build_statecraft_archive_navigation.py): `source_type: youtube`, non-empty `youtube_id`, or YouTube host in `source_url`.
2. **`source_form`** ∈ `{solo, interview, panel, livestream}` **and** `kind` ∈ `{transcript, operator-transcript, cleaned-transcript}` — video-shaped speech capture even if `source_type` was mistyped.
3. **Operator transcript recovery** whose primary identity is a **watch URL** or host-stream episode (route to **channel-index** + **thread-index** instead).

Rationale: ~89 transcript-shaped rows and ~25 mistyped `source_type: youtube` rows in the non-YouTube bucket are intake noise for writer-index.

---

## Inclusion rules (any match → eligible)

A capture **passes** when not hard-excluded **and** any inclusion signal matches:

### A — `source_type` whitelist

`substack`, `substack-post`, `article`, `rss-item`, `web-page`, `institutional-primary`, `paste-bundle`, `mixed`, `x-post-text`, `x-post-bundle`, `verbatim-sidecar`

### B — `kind` whitelist

`substack-post`, `rss-item`, `paste-bundle`, `article`, `mixed`, `x-post-text`, `x-post-bundle`, `verbatim-sidecar`

### C — `source_form` prose signals

`newsletter`, `essay`, `article`, `institutional-statement`, `op-ed`, `wire`

### D — Explicit config row

Future **`statecraft_writer_discovery.json`** (or `writers[]` in a shared discovery config) lists `writer_slug` with `feed_url` / outlet metadata — **force-include** even when legacy frontmatter is thin.

### E — Explicit frontmatter

Non-empty **`writer_slug`** or **`publication_slug`** on the capture (operator or intake sets when landing).

**Tie-break:** If both prose signals (A/B/C) and video-shaped signals (hard exclude #2) appear, **hard exclude wins** unless `source_form` is clearly prose (`newsletter`, `essay`, …).

---

## `writer_slug` resolution (registry key)

Same precedence order for aggregation:

1. YAML **`writer_slug`**
2. YAML **`publication_slug`**
3. YAML **`thread`** (when capture is prose-eligible — aligns with commentator lanes: `crooke`, `pape`, `parsi`, `simplicius`)
4. YAML **`author`** → slugify
5. YAML **`publication`** → slugify
6. Filename prefix `source-<token>-…-YYYY-MM-DD` → first token **only if** capture already passed inclusion rules

Apply **`writer_slug_aliases`** from discovery config (mirror `slug_aliases` on channel-index): e.g. merge duplicate Simplicius keys, normalize outlet spellings.

**Do not** use `channel_slug` as writer-index key — that field is YouTube roster vocabulary.

---

## Main vs misc partition

| Tier | Rule | Expected scale (2026-06-21, filtered) |
|------|------|--------------------------------------|
| **writer-index.md** (main) | ≥ **3** prose-eligible files **or** listed in discovery config **`check_written: true`** | ~5–8 rows: `simplicius`, `pape`, `crooke`, `parsi`, `jiang`, `vatican`, … |
| **writer-index-misc.md** | 1–2 prose-eligible files, not in config main list | Long tail, one-off essays, X-posts |
| **Excluded entirely** | Fails hard exclude or no inclusion signal | Transcript recovery, video mis-types |

Misc slugs live in config as **`writer_index_misc_slugs`** (parallel to `channel_index_misc_slugs`).

---

## Row shape (future JSON sketch)

```json
{
  "writer_slug": "crooke",
  "label": "Alastair Crooke / Conflicts Forum",
  "source_types": ["substack", "substack-post", "paste-bundle"],
  "thread": "crooke",
  "feed_url": "https://conflictsforum.substack.com",
  "file_count": 29,
  "first_day": "2026-01-08",
  "last_day": "2026-06-18",
  "check_written": true,
  "discoverable": false
}
```

No `channel_id`. **`discoverable`** becomes true only when RSS/Substack polling is wired (future).

---

## Relationship to other surfaces

- **channel-index** — video only; do not merge writer rows.
- **thread-index** — speaker-centric across video + prose; use for “how much Freeman?” not “which Substack feed?”
- **Day README ingest register** — authoritative per-day list regardless of index.
- **CAPTURE-TYPES** — [Essay §](../../statecraft/sheets/source-archive-control/CAPTURE-TYPES.md#essay) defines intake **`kind:`** / **`thread:`**; writer-index is derived inventory, not intake law.

---

## Builder hook (future)

Extend **`refresh_statecraft_archive_indices.py`** / **`build_statecraft_archive_navigation.py`**:

- `collect_writer_stats(root)` — apply hard excludes + inclusion rules above
- emit `writer-index.md`, `writer-index-misc.md`, optional `writer-index.json`
- rebuild alongside channel-index; never mix rosters in one JSON file

---

## Open questions (defer)

- Unified operator command **check written** vs manual ingest-only for low-volume feeds
- RSS discovery config location (`statecraft_writer_discovery.json` vs section in existing config)
- Whether **`paste-bundle`** Crooke captures without `source_type: substack` stay included (current spec: **yes** via whitelist)

---

## Return

- YouTube roster: [channel-index.md](./channel-index.md)
- Cross-modal speakers: [thread-index.md](./thread-index.md)
- Capture typing: [CAPTURE-TYPES.md](../../statecraft/sheets/source-archive-control/CAPTURE-TYPES.md)
