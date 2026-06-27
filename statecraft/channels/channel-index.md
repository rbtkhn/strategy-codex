# Statecraft Channels — YouTube Channel Index

_Generated inventory note. Rebuild with `python scripts/refresh_statecraft_archive_indices.py`._

SSOT for the main **check-sources** roster lives under `statecraft/channels/` (one shelf folder per `channel_slug`).

Flat registry of **YouTube channels** seen in `source-*.md` captures (`source_type: youtube`,
`youtube_id`, or YouTube `source_url`). Articles, Substack, and other non-YouTube surfaces are excluded.
Primary key: YAML `channel_slug` when present; otherwise derived from `channel_name` / `show`,
or configured `host`, YAML `series`, or filename prefix when listed in discovery config.

Low-volume / occasional channels live in [channel-index-misc.md](./channel-index-misc.md).

Curated daily watchlist (subset): [statecraft_youtube_discovery.json](../../platform/config/statecraft_youtube_discovery.json) · [youtube-transcript-queue.md](../../statecraft/sheets/source-archive-control/youtube-transcript-queue.md) · Legacy: [COGNITION-STREAMS-WATCHLIST-DEPRECATED.md](../../docs/skill-work/work-strategy/COGNITION-STREAMS-WATCHLIST-DEPRECATED.md)

## Stats

- Distinct YouTube channel keys: `15`
- YouTube source files mapped: `1489`
- Rows with explicit `channel_slug`: `15`
- Watchlist channels (matched): `7`
- Check-sources roster (main, misc excluded): `15` — [channel-index.json](./channel-index.json)
- Discoverable on roster: `15` (YouTube URL or discovery `channel_id` / `handle_url`)

## Channels

| Channel slug | Label | Files | Days | Watchlist | Channel URL | First day | Last day |
| --- | --- | ---: | ---: | --- | --- | --- | --- |
| `alexander-mercouris` | Alexander Mercouris | 332 | 330 | yes | [open](https://www.youtube.com/@AlexMercouris) | `2025-01-03` | `2026-06-26` |
| `dialogue-works` | Dialogue Works | 309 | 197 | yes | [open](https://www.youtube.com/@dialogueworks01) | `2025-01-04` | `2026-06-26` |
| `daniel-davis` | Daniel Davis / Deep Dive | 260 | 153 | yes | [open](https://www.youtube.com/@DanielDavisDeepDive) | `2025-01-01` | `2026-06-26` |
| `judging-freedom` | Judge Napolitano - Judging Freedom | 216 | 140 | yes | [open](https://www.youtube.com/@judgingfreedom) | `2025-01-07` | `2026-06-26` |
| `glenn-diesen` | Glenn Diesen | 214 | 175 | yes | [open](https://www.youtube.com/@GDiesen1) | `2023-01-14` | `2026-06-25` |
| `mario-nawfal` | Mario Nawfal | 52 | 31 |  | [open](https://www.youtube.com/channel/UCTWBp-39z6tvz4-LQB-Z_QA) | `2026-05-12` | `2026-06-26` |
| `the-duran` | The Duran | 31 | 31 | yes | [open](https://www.youtube.com/@TheDuran) | `2025-02-07` | `2026-06-23` |
| `india-global-left` | India and Global Left | 21 | 21 |  | [open](https://www.youtube.com/@IndiaGlobalLeft) | `2025-02-22` | `2026-06-11` |
| `neutrality-studies` | Neutrality Studies | 11 | 9 |  | [open](https://www.youtube.com/@neutralitystudies) | `2025-02-06` | `2026-06-22` |
| `predictive-history` | Predictive History | 11 | 9 |  | [open](https://www.youtube.com/@PredictiveHistory) | `2026-04-14` | `2026-06-10` |
| `breaking-points` | Breaking Points | 9 | 7 |  | [open](https://www.youtube.com/@BreakingPoints) | `2026-04-29` | `2026-06-23` |
| `tucker-carlson` | Tucker Carlson | 7 | 7 |  | [open](https://www.youtube.com/@TuckerCarlson) | `2025-03-11` | `2026-06-24` |
| `reason-resist` | Reason to Resist | 6 | 6 |  | [open](https://www.youtube.com/@reason2resist) | `2026-05-18` | `2026-06-25` |
| `moral-resistance` | Moral Resistance | 5 | 5 |  | [open](https://www.youtube.com/@MoralResistance) | `2026-05-31` | `2026-06-26` |
| `redacted-news` | Redacted News | 5 | 4 | yes | [open](https://www.youtube.com/@RedactedNews) | `2026-04-20` | `2026-06-16` |

_`*` = slug derived from label; no explicit `channel_slug` in frontmatter._

## Return

- Channels layer: [statecraft/channels/README.md](./README.md)
- Source archive: [source-archive/statecraft/README.md](../../source-archive/statecraft/README.md)
- Thread index: [thread-index.md](../../source-archive/statecraft/thread-index.md)
- Miscellaneous channels: [channel-index-misc.md](./channel-index-misc.md)
