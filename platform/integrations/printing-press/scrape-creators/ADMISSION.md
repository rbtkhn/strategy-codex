# scrape-creators admission checklist

Use this before any live Printing Press `scrape-creators` run enters Strategy-Codex artifacts.

## Required

- Source is public YouTube content.
- Operator names the channel or video URL.
- No credential, cookie, session, or logged-in browser access is used.
- Comments, replies, DMs, and social graph data are excluded.
- Tool version, command shape, source URL, fetched date, and output paths are recorded in a receipt.
- Transcript output is labeled WORK-only and is not treated as Record truth.
- Strong claims downstream are corroborated per `docs/archive/skill-work-legacy/work-strategy/brief-source-registry.md`.

## Reject

- Any payload with comments or replies.
- Any payload that indicates cookies, tokens, sessions, credentials, or authenticated mode.
- Any non-YouTube platform in v1.
- Any request to scrape private, account-specific, or relationship data.
- Any attempt to write directly to Record surfaces.

## Review note

Scraping can be legitimate operator research, but it is higher-risk than public APIs because platform behavior, terms, rate limits, and page formats can change. Keep v1 narrow, receipted, and reversible.
