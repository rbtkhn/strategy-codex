# Printing Press scrape-creators pilot

Status: governed pilot

Purpose: admit Printing Press `scrape-creators` as a WORK-layer acquisition adapter for public YouTube transcript and video metadata. This is for the Strategy-Codex cognition stream: transcript capture, Perceiver, LEARN MODE, current-events analysis, and optional strategy-notebook raw input. It is not Record truth, not Voice knowledge, and not a merge path.

Root bootstrap: [Printing Press integration](../README.md).

## V1 boundary

Allowed:

- public YouTube video metadata and transcripts
- operator-reviewed single video or channel pulls
- receipts under `runtime/artifacts/printing-press/scrape-creators/`
- conversion into `research/external/youtube-channels/<channel-slug>/`

Excluded:

- comments and replies
- DMs or private surfaces
- credentialed, cookie, or browser-session scraping
- cross-platform creator graph harvesting
- automatic updates to `self.md`, `self-archive.md`, `recursion-gate.md`, `session-log.md`, or `archive/grace-mar-instance/bot/prompt.py`

## Install status

Printing Press lists `scrape-creators` as covering public creator data across social platforms including YouTube transcripts:

- https://printingpress.dev/

Install and smoke test separately before using the adapter:

```bash
npx -y @mvanhorn/printing-press install scrape-creators
```

The repo adapter does not install dependencies. It only calls an already-installed CLI when `--fetch-url` is used, or maps a captured JSON payload supplied with `--input-json`.

## Adapter

```bash
python scripts/printing_press_scrape_creators_youtube.py \
  --input-json runtime/artifacts/printing-press/scrape-creators/sample-youtube.json \
  --channel-slug example-channel \
  --channel-url "https://www.youtube.com/@Example/videos" \
  --apply
```

Default dry-run prints the paths it would write. With `--apply`, output goes to:

- `research/external/youtube-channels/<channel-slug>/index.json`
- `research/external/youtube-channels/<channel-slug>/transcript_manifest.json`
- `research/external/youtube-channels/<channel-slug>/transcripts/*.txt`
- `runtime/artifacts/printing-press/scrape-creators/*.json`

## Downstream route

After acquisition, route through the existing work-strategy transcript path:

- `research/external/work-strategy/transcripts/README.md`
- `docs/archive/skill-work-legacy/work-strategy/current-events-analysis.md`
- `docs/archive/skill-work-legacy/work-strategy/LEARN_MODE_RULES.md`

Transcript material remains commentary, argument, or actor claim unless independently verified.
