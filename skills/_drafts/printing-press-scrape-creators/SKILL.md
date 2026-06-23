---
name: printing-press-scrape-creators
description: Govern public YouTube transcript acquisition through Printing Press scrape-creators, preserving receipts and WORK-only routing.
portable: true
version: 0.1.0
category: domain-pack
status: draft
tags:
  - operator
  - work-strategy
  - transcript-ingest
  - printing-press
---
# Printing Press scrape-creators intake

Use this draft skill when the operator wants to acquire public YouTube transcript or video metadata through Printing Press `scrape-creators` for cognition-stream work.

## Workflow

1. Confirm the target is public YouTube content.
2. Refuse v1 requests for comments, replies, DMs, cookies, credentials, sessions, or cross-platform creator graph harvesting.
3. Capture or fetch the transcript payload with a receipt.
4. Convert it into the host repo's existing YouTube channel transcript layout.
5. Route downstream as WORK-layer source material for transcript analysis, Perceiver, LEARN MODE, or strategy notebook work.

## Guardrails

- Treat transcript material as interpretation, argument, or actor claim unless independently verified.
- Do not merge anything into Record surfaces.
- Do not treat scraped text as Voice knowledge.
- Keep raw acquisition reversible and clearly sourced.
- Prefer one small pilot before channel-scale ingestion.

## Output

End with:

- source URL
- fetched date
- output paths
- receipt path
- whether the payload passed or failed admission
- next safe downstream route
