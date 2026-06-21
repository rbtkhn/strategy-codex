# Cognition streams watchlist — DEPRECATED (2026-06)

WORK only; not Record.

**Status:** [`cognition-streams-watchlist.json`](cognition-streams-watchlist.json) is **deprecated** for new work. Do not add channels there or treat it as the listing SSOT.

## What replaced it

| Old | Use instead |
|---|---|
| **`cognition-streams-watchlist.json`** (flat five-channel JSON) | **[`source-archive/statecraft/channel-index.md`](../../../source-archive/statecraft/channel-index.md)** — derived **YouTube-only** channel registry (slug, counts, first/last day, URLs). Rebuild: `python scripts/refresh_statecraft_archive_indices.py` |
| Machine-readable discovery metadata (`channel_id`, playlist IDs, `handle_url`, `file_prefix`) | **[`platform/config/statecraft_youtube_discovery.json`](../../../platform/config/statecraft_youtube_discovery.json)** — daily watchlist flag + YouTube discovery fields for automation |
| Human rollout / backfill channel list | **[`statecraft/sheets/source-archive-control/youtube-transcript-queue.md`](../../../statecraft/sheets/source-archive-control/youtube-transcript-queue.md)** |

## What is **not** deprecated

- **`check streams`** daily quintet (Davis, Diesen, Dialogue Works, Napolitano, Mercouris) — behavior unchanged; config now lives in `statecraft_youtube_discovery.json` (`daily_watchlist: true`)
- **[`cognition-streams-watchset.md`](cognition-streams-watchset.md)** — prose rationale for the five-stream daily aperture
- **`python scripts/cognition_streams_audit.py`** — still valid; roster from `channel-index.json` via `load_check_sources_roster()` (main or `--roster watchlist`); reconciles against `source-archive/statecraft` by default (`--capture-surface archive`)

## Migration notes for agents

- **Listing question** (“what YouTube channels have we used?”) → **`channel-index.md`** (YouTube captures only), not the old JSON.
- **Discovery / audit** → **`statecraft_youtube_discovery.json`** via `scripts/statecraft_youtube_discovery.py`.
- **Archive land** → **`source-intake`** — not `materialize_youtube_raw_input.py --apply` ([YOUTUBE-MATERIALIZE-DEPRECATED.md](YOUTUBE-MATERIALIZE-DEPRECATED.md)).
- Legacy path [`cognition-streams-watchlist.json`](cognition-streams-watchlist.json) is a **stub redirect only**; scripts should not rely on it containing `channels`.
