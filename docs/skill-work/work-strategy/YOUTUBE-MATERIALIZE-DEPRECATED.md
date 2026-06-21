# YouTube materialize workflow — DEPRECATED (2026-06-20)

WORK only; not Record.

**Status:** The **`youtube-raw-input-transcript`** skill and **`python scripts/materialize_youtube_raw_input.py --apply`** path are **deprecated** for new strategy-codex capture. Do not route new lands through the materializer or treat `youtube-*` / `transcript-*` archive filenames as canonical.

## What replaced it

| Old | Use instead |
|-----|-------------|
| **`youtube-raw-input-transcript`** skill (`youtube transcript`) | **[`statecraft-source-intake`](../../../.cursor/skills/statecraft-source-intake/SKILL.md)** — say **`source-intake`**; land verbatim body to `source-archive/statecraft/YYYY-MM-DD/source-<slug>.md` |
| **`materialize_youtube_raw_input.py --apply`** (writes non-`source-*` names into archive) | **`source-intake`** sidecar land: `land_statecraft_source_body.py` + post-land day index / intake queue |
| Operator paste after fetch failure | Same thread → **`source-intake`** (chunked land on Windows) |
| Daily roster capture closeout | **`check sources`** (or **`check sources watchlist`**) for discovery + selection → transcript body (operator paste or bounded fetch) → **`source-intake`** |

## What is **not** deprecated

- **`check sources`** — roster-scoped discovery (`channel-index.json` SSOT), clip filter, list-first approval (hand off to **source-intake**)
- Legacy **`check streams`** — accepted alias; routes to **check-sources**
- **`cognition_streams_audit.py`** — advisory coverage receipts (reads discovery config + raw-input index when configured)
- **`backfill_*_youtube_raw_input.py`** — optional staging into `strategy-notebook/raw-input/` only (not canonical archive)
- **`statecraft_youtube_discovery.json`** + **`channel-index.md`** / **`channel-index.json`** — channel listing and check-sources roster SSOT
- **`materialize_youtube_raw_input.py`** (script) — **legacy / archaeology only**; dry-run receipts or `--raw-input` appearance routing on old paths until removed; **no new `--apply` archive writes**

## Migration notes for agents

- **Canonical archive filename:** always `source-<topic-slug>-YYYY-MM-DD.md` — [source-archive/statecraft/README.md](../../../source-archive/statecraft/README.md) (filename law).
- **Queue `file_prefix` vs archive:** [youtube-transcript-queue.md § Filename surfaces](../../../statecraft/sheets/source-archive-control/youtube-transcript-queue.md#filename-surfaces-file_prefix-vs-source-) — raw-input prefixes must not be copied into source-archive lands.
- **Known watch URL + full transcript in chat:** `source-intake` directly.
- **Known watch URL, need captions:** resolve metadata in the **`check sources`** thread or a one-off fetch step, then **`source-intake`** — do not close on materializer `--apply`.
- **Appearance / host-shelf quality artifacts** formerly emitted by `--with-appearances`: not automatic on source-intake today; treat as optional downstream maintenance until a post-land hook exists.

## Legacy pointers

- Deprecated skill stub: [`skills/youtube-raw-input-transcript/SKILL.md`](../../../skills/youtube-raw-input-transcript/SKILL.md)
- Script (legacy): [`scripts/materialize_youtube_raw_input.py`](../../../scripts/materialize_youtube_raw_input.py)
