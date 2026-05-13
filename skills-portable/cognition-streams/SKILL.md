---
name: cognition-streams
preferred_activation: cognition streams
description: "Run the daily four-stream cognition ingest routine: discover today's uploads, filter suspected clips, list main uploads first, and materialize only the operator-approved subset into canonical raw-input."
portable: true
version: 0.1.0
tags:
  - operator
  - strategy
  - raw-input
  - youtube
  - daily
---

# Cognition streams

**Preferred activation (operator):** say **`cognition streams`**.

Use this skill for the **daily stream check / daily ingest routine** across a fixed cognition-stream watchlist. It discovers today's uploads, filters likely highlight clips, presents a list-first view, and materializes only the operator-approved subset into canonical `raw-input`.

Use the single-URL YouTube transcript workflow for one-off URLs. Use this skill when the operator wants the **daily roster**.

For the higher-level notebook meaning of this routine, see [cognition-streams-daily-aperture.md](../../docs/skill-work/work-strategy/cognition-streams-daily-aperture.md).

## Layering rule

- Start with **`cognition streams`** when the task is "what went up today across the tracked streams?"
- Start with **`youtube transcript`** when the task is "turn this specific YouTube URL into canonical raw-input."
- If the daily roster check produces approved URLs, hand each selected item down to the lower-layer YouTube transcript workflow for the actual materialization step.

## When to run

- The operator asks to check **today's uploads** across tracked cognition streams.
- The operator wants a **daily list-first ingest pass** rather than a one-off YouTube transcript.
- The operator asks what Glenn Diesen, Daniel Davis, Alexander Mercouris, and Dialogue Works uploaded today.
- The operator asks to materialize today's uploads from the tracked cognition streams after reviewing the list.

## When not to run

- A single YouTube URL is provided without daily-list intent.
- The task is one-off transcript cleanup or speaker normalization.
- The operator wants to ingest one channel item directly.

In those cases, use the lower-layer single-URL YouTube transcript workflow instead.

## Default watchlist

Track these four streams in v1:

- Glenn Diesen
- Daniel Davis
- Alexander Mercouris
- Dialogue Works

If a stream has no upload on the target day, say so explicitly.

## Daily workflow

1. **Discover today's uploads**
   - Query the tracked channels for the operator's local day.
   - Normalize each result into:
     - stream / channel
     - title
     - URL
     - exact `pub_date`
     - duration
   - Keep the discovery pass separate from materialization.

2. **Run the highlight-clip filter**
   - Classify items into:
     - **Main uploads**
     - **Suspected clips / highlights**
   - Use a **conservative keep** bias: auto-hide only obvious clips, Shorts, teasers, and repost fragments.

3. **Present a list-first view**
   - Show the **Main uploads** first.
   - Add one short line if clips were hidden:
     - `N suspected clips hidden; show if wanted`
   - Do not materialize anything yet.

4. **Wait for operator selection**
   - Support selections such as `all`, `all except X`, channel-specific subsets, and explicit clip inclusion.

5. **Materialize the approved subset**
   - For each approved URL:
     - resolve metadata first
     - fetch the best subtitle source available
     - preserve extraction receipts locally
     - write canonical date-folder raw-input

6. **Default transcript class**
   - Default to `auto_subtitles_vtt`.
   - Use explicit provenance stating subtitle-derived, lightly deduped, and not human-verified verbatim.
   - Upgrade to stronger normalization only when the operator explicitly asks.

## Clip-filter model

Use a **layered scoring model**, not a single brittle rule.

### Hard exclude signals

Classify as **suspected clip** when any of these are true:

- the YouTube object is a **Short**
- the title contains strong clip markers such as:
  - `shorts`
  - `clip`
  - `highlights`
  - `best moments`
  - `preview`
  - `teaser`
  - `trailer`
  - `snippet`
  - `excerpt`
- the title explicitly says it is from another episode, such as `from today's show`, `from my interview with`, `full interview here`, or `watch full episode`
- description or metadata clearly identifies repost / excerpt packaging

### Soft suspicion signals

Mark as **suspected clip** when multiple weaker signals stack:

- very short duration
- title is a reactive fragment rather than normal house style
- title is all-caps hook language with no guest/topic structure
- duplicate same-day subject with a longer same-channel upload
- description links to a separate full episode as the parent object

Short duration alone is **not** enough when the item still looks like a complete house-style upload.

### Duration heuristics

Use duration as a **supporting** signal only:

- `< 3 min`: very likely clip
- `3-8 min`: likely clip unless metadata strongly indicates a complete monologue, short formal update, or normal same-channel standalone upload
- `8-15 min`: ambiguous; do not auto-hide on duration alone
- `15+ min`: generally main upload unless strong clip markers fire

### Channel-sensitive expectations

Use light priors, but do not build separate policy trees:

- **Glenn Diesen:** guest-name + thesis-title interviews are typical; short fragments are more suspicious
- **Daniel Davis:** legitimate uploads can be short topical monologues; duration alone is unreliable and should not override normal standalone title structure
- **Mercouris:** usually long monologues; short uploads are more suspicious
- **Dialogue Works:** titles may be dramatic, and some legitimate interviews can still be relatively short; title sensationalism or a 10-15 minute runtime alone is not enough

## Output shape

Use this shape by default:

```markdown
# Today's Cognition Streams

## Main uploads
- <channel> — <title> — <date> — <url>

N suspected clips hidden; show if wanted.
```

If the operator asks to see clips:

```markdown
## Suspected clips / highlights
- <channel> — <title> — <why flagged> — <url>
```

After operator selection, report only the approved items being materialized and the resulting raw-input outcome.

## Guardrails

- Never silently discard borderline items.
- Never auto-materialize everything by default.
- Never treat clip suspicion as certainty.
- Never silently promote subtitle-derived outputs into stronger transcript classes.

## Success condition

The operator gets a clean daily upload list for the tracked cognition streams, with obvious clips filtered into a secondary bucket and only the approved subset materialized into provenance-safe canonical `raw-input`.
