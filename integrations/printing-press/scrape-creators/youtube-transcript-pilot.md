# YouTube transcript pilot

Goal: prove that Printing Press `scrape-creators` can safely feed the existing cognition stream without replacing the repo's current YouTube transcript tooling.

## Pilot object

- One public YouTube video or one small public channel slice.
- No comments.
- No cookies or logged-in account context.
- Output accepted only if it contains video id, title, URL, transcript text, and fetched timestamp.

## Flow

1. Install and inspect `scrape-creators` outside the repo change.
2. Capture one public YouTube transcript JSON payload.
3. Run the adapter in dry-run mode:

```bash
python scripts/printing_press_scrape_creators_youtube.py \
  --input-json artifacts/printing-press/scrape-creators/sample-youtube.json \
  --channel-slug pilot-channel
```

4. Review planned paths.
5. Run with `--apply` only after the payload passes admission.
6. Use existing work-strategy transcript routes for analysis.

## Acceptance

- `index.json` and `transcript_manifest.json` use the existing YouTube channel layout.
- `transcripts/*.txt` includes source URL, video id, fetched time, source tier, and pipeline version headers.
- A receipt is written under `artifacts/printing-press/scrape-creators/`.
- The adapter rejects comments and credential indicators.
- No Record surface is touched.

## Manual smoke command

The CLI command shape must be verified against the installed Printing Press binary. If the default command is wrong, set:

```bash
set SCRAPE_CREATORS_COMMAND_TEMPLATE={bin} youtube transcript --url {url} --json
```

Then run:

```bash
python scripts/printing_press_scrape_creators_youtube.py \
  --fetch-url "https://www.youtube.com/watch?v=<id>" \
  --channel-slug pilot-channel
```
