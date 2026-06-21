# Statecraft Archive - YouTube Channel Index

_Generated inventory note. Rebuild with `python scripts/refresh_statecraft_archive_indices.py`._

Flat registry of **YouTube channels** seen in `source-*.md` captures (`source_type: youtube`,
`youtube_id`, or YouTube `source_url`). Articles, Substack, and other non-YouTube surfaces are excluded.
Primary key: YAML `channel_slug` when present; otherwise derived from `channel_name` / `show`,
or configured `host`, YAML `series`, or filename prefix when listed in discovery config.

Low-volume / occasional channels live in [channel-index-misc.md](./channel-index-misc.md).

Curated daily watchlist (subset): [statecraft_youtube_discovery.json](../../platform/config/statecraft_youtube_discovery.json) · [youtube-transcript-queue.md](../../statecraft/sheets/source-archive-control/youtube-transcript-queue.md) · Legacy: [COGNITION-STREAMS-WATCHLIST-DEPRECATED.md](../../docs/skill-work/work-strategy/COGNITION-STREAMS-WATCHLIST-DEPRECATED.md)

## Stats

- Distinct YouTube channel keys: `15`
- YouTube source files mapped: `1415`
- Rows with explicit `channel_slug`: `13`
- Watchlist channels (matched): `6`

## Channels

| Channel slug | Label | Files | Days | Watchlist | Channel URL | First day | Last day |
| --- | --- | ---: | ---: | --- | --- | --- | --- |
| `alexander-mercouris` | Alexander Mercouris | 365 | 336 | yes | [open](https://www.youtube.com/@AlexMercouris) | `2025-01-03` | `2026-06-20` |
| `dialogue-works` | Dialogue Works | 298 | 190 | yes | [open](https://www.youtube.com/@dialogueworks01) | `2025-01-04` | `2026-06-20` |
| `daniel-davis` | Daniel Davis / Deep Dive | 245 | 141 | yes | [open](https://www.youtube.com/@DanielDavisDeepDive) | `2025-01-01` | `2026-06-20` |
| `glenn-diesen` | Glenn Diesen | 209 | 171 | yes | [open](https://www.youtube.com/@GDiesen1) | `2023-01-14` | `2026-06-19` |
| `judging-freedom` | Judge Napolitano - Judging Freedom | 203 | 135 | yes | [open](https://www.youtube.com/@judgingfreedom) | `2025-01-07` | `2026-06-19` |
| `mario-nawfal` | Mario Nawfal | 46 | 27 |  | [open](https://www.youtube.com/channel/UCTWBp-39z6tvz4-LQB-Z_QA) | `2026-05-12` | `2026-06-19` |
| `predictive-history` * | Predictive History | 11 | 9 |  |  | `2026-04-14` | `2026-06-10` |
| `breaking-points` | Breaking Points | 7 | 6 |  | [open](https://www.youtube.com/c/BreakingPoints) | `2026-04-29` | `2026-06-17` |
| `neutrality-studies` | Neutrality Studies | 7 | 6 |  | [open](https://www.youtube.com/@neutralitystudies/videos) | `2025-02-06` | `2026-06-20` |
| `tucker-carlson` | Tucker Carlson | 6 | 6 |  | [open](https://www.youtube.com/@TuckerCarlson) | `2025-03-11` | `2026-06-15` |
| `reason-to-resist` | Reason to Resist | 5 | 5 |  |  | `2026-05-18` | `2026-06-18` |
| `redacted-news` | Redacted News | 5 | 4 | yes | [open](https://www.youtube.com/@RedactedNews) | `2026-04-20` | `2026-06-16` |
| `india-and-global-left` | India and Global Left | 3 | 3 |  |  | `2026-05-20` | `2026-06-11` |
| `moral-resistance` | Moral Resistance | 3 | 3 |  |  | `2026-05-31` | `2026-06-18` |
| `unknown` * | (none) | 2 | 2 |  |  | `2026-02-27` | `2026-04-20` |

_`*` = slug derived from label; no explicit `channel_slug` in frontmatter._

## Return

- Root archive: [source-archive/statecraft/README.md](./README.md)
- Thread index: [thread-index.md](./thread-index.md)
- Miscellaneous channels: [channel-index-misc.md](./channel-index-misc.md)
