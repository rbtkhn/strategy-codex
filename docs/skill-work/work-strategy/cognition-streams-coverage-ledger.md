# Cognition streams coverage ledger

Use this file as the **machine-shaped audit contract** for month or date-window completeness across the five tracked cognition streams.

Its purpose is not to replace the daily skill. It exists so later scripts and operators can answer:

- what was published
- what was captured
- what was intentionally hidden
- whether the evidence base is rich enough yet

## Scope

Default tracked channels:

- Glenn Diesen
- Daniel Davis / Deep Dive
- Dialogue Works
- Judge Napolitano / Judging Freedom
- Alexander Mercouris

Default unit:

- one row per **published YouTube object**

Default audit window:

- a bounded date range such as `2026-05-01` through `2026-05-13`

## Source-of-truth order

Use this order when populating the ledger:

1. channel uploads playlist / channel-id feed
2. channel RSS feed when the latest window is enough
3. handle-based `/videos` page as fallback only
4. local inventory / prior receipts as audit aid only
5. local `raw-input/` as the capture truth

The ledger is only as good as its discovery surface. If discovery is wrong, coverage math is wrong.

## Row schema

Use these columns for CSV, TSV, JSONL, or Markdown-table export.

Required fields:

- `date`
- `channel_key`
- `channel_name`
- `youtube_id`
- `title`
- `url`
- `duration_seconds`
- `discovery_source`
- `classification`
- `captured`
- `raw_input_path`
- `notes`

Recommended optional fields:

- `guest`
- `same_day_parent_id`
- `receipt_path`
- `audit_window`
- `captured_at`

## Allowed values

### `channel_key`

- `glenn-diesen`
- `daniel-davis-deep-dive`
- `dialogue-works`
- `napolitano`
- `alex-mercouris`

### `discovery_source`

- `uploads_playlist`
- `channel_feed`
- `videos_page`
- `inventory_appendix`
- `manual_url`

### `classification`

- `captured-main`
- `uncaptured-main`
- `hidden-companion`
- `hidden-short`
- `upcoming`
- `deferred`
- `outside-watchlist`

### `captured`

- `1`
- `0`

Rules:

- `captured-main` must have `captured=1`
- `uncaptured-main` must have `captured=0`
- `hidden-companion`, `hidden-short`, `upcoming`, and `outside-watchlist` must not count toward main-upload coverage
- `deferred` is allowed only when the item is still considered a real main upload but was intentionally left undone

## Coverage denominator rule

Only count these rows in the **main-upload denominator**:

- `captured-main`
- `uncaptured-main`
- `deferred`

Do **not** count:

- `hidden-companion`
- `hidden-short`
- `upcoming`
- `outside-watchlist`

This keeps the metric aligned with cognition value rather than raw upload volume.

## Core formulas

Let:

- `main_total = count(classification in {captured-main, uncaptured-main, deferred})`
- `captured_main = count(classification = captured-main)`
- `recent_main_total = same formula on the recent sub-window`
- `recent_captured_main = same formula on the recent sub-window`

Then:

- `overall_pct = captured_main / main_total`
- `recent_pct = recent_captured_main / recent_main_total`
- `must_capture_remaining = count(priority = must-capture and captured = 0)`

If using integer display:

- `overall_pct_display = round(100 * overall_pct)`
- `recent_pct_display = round(100 * recent_pct)`

## Benchmarks

Use this default benchmark for May-like backfill windows:

- `overall_pct >= 0.70`
- `recent_pct >= 0.90`
- `must_capture_remaining = 0`

Interpretation:

- `70%` overall means the month is cognition-rich enough for strategy work
- `90%` recent means live operational confidence is high
- `0` must-capture misses means the remaining gaps are mostly marginal

## Priority field

If using a second table or queue overlay, use:

- `must-capture`
- `probably-capture`
- `hide-default`

That queue is operational. The coverage ledger remains the canonical measurement layer.

## Minimal CSV header

```text
date,channel_key,channel_name,youtube_id,title,url,duration_seconds,discovery_source,classification,captured,raw_input_path,notes
```

## Minimal JSONL shape

```json
{"date":"2026-05-12","channel_key":"dialogue-works","channel_name":"Dialogue Works","youtube_id":"vmCvNogL8PU","title":"Col. Larry Wilkerson: Iran WIPES OUT Trump's Proposal & INSISTS on Its Own Terms (It's Over)","url":"https://www.youtube.com/watch?v=vmCvNogL8PU","duration_seconds":3569,"discovery_source":"uploads_playlist","classification":"uncaptured-main","captured":0,"raw_input_path":"","notes":"High-value missed main during May 12 audit."}
{"date":"2026-05-12","channel_key":"daniel-davis-deep-dive","channel_name":"Daniel Davis / Deep Dive","youtube_id":"S3bPrYf1w40","title":"Trump & American's Pocketbooks (Iran War)","url":"https://www.youtube.com/watch?v=S3bPrYf1w40","duration_seconds":27,"discovery_source":"uploads_playlist","classification":"hidden-short","captured":0,"raw_input_path":"","notes":"Do not count toward main coverage."}
{"date":"2026-05-13","channel_key":"daniel-davis-deep-dive","channel_name":"Daniel Davis / Deep Dive","youtube_id":"QCUzMPfGuZY","title":"Prof John Mearsheimer LIVE TODAY 2:00p et","url":"https://www.youtube.com/watch?v=QCUzMPfGuZY","duration_seconds":0,"discovery_source":"channel_feed","classification":"upcoming","captured":0,"raw_input_path":"","notes":"Scheduled live event; exclude from aired-upload denominator."}
```

## Automation notes

Scripts should:

- derive discovery rows from uploads playlist or feed first
- derive capture truth from `raw-input/` frontmatter by `source_url` / `youtube_id`
- avoid filename-only matching
- emit both row-level ledger and summary metrics

Recommended summary outputs:

- `main_total`
- `captured_main`
- `overall_pct`
- `recent_main_total`
- `recent_captured_main`
- `recent_pct`
- `must_capture_remaining`
- per-date breakdown
- per-channel breakdown

## Completion claim rule

Do not say a date or month is complete unless:

- every discovered item has a classification
- every main upload is either captured or explicitly deferred
- the summary metrics have been recomputed from the row set

That is the point of the ledger: completion becomes computed, not felt.
