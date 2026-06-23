# YouTube transcript queue
<!-- word_count: ~780 -->

WORK only; not Record.

## Purpose

These are the canonical input channels for strategy-notebook. The queue is a rollout list for YouTube transcript automation and metadata capture, not a taxonomy of different roles.

## Canonical input channels

- Dialogue Works
- Daniel Davis Deep Dive
- Glenn Diesen
- Alex Mercouris
- The Duran / Mercouris
- Judging Freedom / Judge Napolitano
- Redacted News

## Additional channels

Other channels can be added when useful, but they are not part of the canonical daily watchlist above.

- The Grayzone
- Breaking Points

## Resource estimate

The transcript pipeline is efficient as long as the common path stays caption-first:

| Tier | What it uses | Expected cost |
|---|---|---|
| Tier 1 | `youtube-transcript-api` | Low CPU, low memory, mostly network-bound |
| Tier 2 | `yt-dlp` subtitle download | Still cheap; a little slower and more variable than Tier 1 |
| Tier 3 | Whisper fallback | CPU-heavy; use only when captions/subtitles fail |

Rule of thumb:
- Tier 1 and Tier 2 should make the queue feel lightweight.
- Whisper should remain the exception path, not the default path.
- Throughput is typically gated by network latency and transcript availability, not local compute, unless a channel falls back to Whisper often.

## Routing rules

- Automated capture writes `raw-input/` only.
- Pages and thread files are composed later in a separate pass.
- Keep the queue selective: substantial episodes only, not completeness-by-default.

## Filename surfaces (`file_prefix` vs `source-`)

Discovery `file_prefix` on each channel and archive land names are **different surfaces**. Do not treat `file_prefix` as the statecraft archive filename.

| Surface | Path | Prefix rule | Role |
|---------|------|-------------|------|
| **Raw-input queue** | `docs/skill-work/work-strategy/strategy-notebook/raw-input/<pub_date>/` | `file_prefix` from [`statecraft_youtube_discovery.json`](../../../platform/config/statecraft_youtube_discovery.json) — often legacy `youtube-*` or `transcript-*` | Transcript automation / backfill staging |
| **Statecraft source archive** | `source-archive/statecraft/YYYY-MM-DD/` | Always `source-<topic-slug>-YYYY-MM-DD.md` | Canonical full-source capture ([filename law](../../../source-archive/statecraft/README.md)) |

**Watchlist mapping** (queue config → archive land):

| `channel_key` | `file_prefix` (raw-input) | Archive land pattern |
|---------------|---------------------------|----------------------|
| `dialogue-works` | `transcript-dialogue-works` | `source-dialogue-works-*` or `source-alkorshid-*` |
| `daniel-davis` | `youtube-daniel-davis-deep-dive` | `source-daniel-davis-*` |
| `glenn-diesen` | `youtube-glenn-diesen` | `source-diesen-*` / `source-glenn-diesen-*` |
| `alexander-mercouris` | `youtube-alex-mercouris` | `source-mercouris-*` |
| `judging-freedom` | `transcript-napolitano` | `source-napolitano-*` |
| `redacted-news` | `source-redacted` | `source-redacted-*` |

Channel-index routing also reads legacy raw-input prefixes and explicit `source-*` rules in discovery config (`filename_prefix_index_canonical`) so thin-YAML archive captures still roll up correctly. New **source-archive** lands: use `source-*` only; keep shape in frontmatter (`kind`, `source_form`, `channel_slug`).

**Deprecated:** `youtube-raw-input-transcript` / `materialize_youtube_raw_input.py --apply` — [YOUTUBE-MATERIALIZE-DEPRECATED.md](../../../docs/skill-work/work-strategy/YOUTUBE-MATERIALIZE-DEPRECATED.md). Use **`source-intake`** after roster approval or paste.

## Runner suggestions

Use the generic helper for the majority of cases:

- `scripts/backfill_youtube_channel_raw_input.py`

Discovery config (replaces deprecated `cognition-streams-watchlist.json`): `platform/config/statecraft_youtube_discovery.json`. Channel listing: `source-archive/statecraft/channel-index.md`. See [COGNITION-STREAMS-WATCHLIST-DEPRECATED.md](../../../docs/skill-work/work-strategy/COGNITION-STREAMS-WATCHLIST-DEPRECATED.md).

Thin wrappers exist for the common rollout targets:

- `scripts/backfill_nima_youtube_raw_input.py`
- `scripts/backfill_alexmercouris_youtube_raw_input.py`
- `scripts/backfill_davis_youtube_raw_input.py`
- `scripts/backfill_diesen_youtube_raw_input.py`
- `scripts/backfill_judgingfreedom_youtube_raw_input.py`
- `scripts/backfill_the_duran_youtube_raw_input.py`
- `scripts/backfill_grayzone_youtube_raw_input.py`
- `scripts/backfill_breaking_points_youtube_raw_input.py`

## Rollout note

Roll out one channel at a time so fallback rates and transcript quality can be observed before the queue expands. The list above is the default canonical set, not a mandate to run every channel at once.
