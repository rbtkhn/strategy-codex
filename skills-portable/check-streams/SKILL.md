---
name: check-streams
preferred_activation: check streams
description: "Check the daily tracked YouTube stream roster for Davis, Diesen, Alkorshid/Dialogue Works, Napolitano/Judging Freedom, and Mercouris: discover today's uploads, filter suspected clips, list main uploads first, materialize only the operator-approved subset into canonical raw-input, and suggest speaker-folder routing hints."
portable: true
version: 0.2.0
tags:
  - operator
  - strategy
  - raw-input
  - youtube
  - daily
---

# Check streams

**Preferred activation (operator):** say **`check streams`**.

Use this skill for the **daily stream check / daily ingest routine** across the fixed main-stream watchlist. It discovers today's Davis, Diesen, Alkorshid/Dialogue Works, Napolitano/Judging Freedom, and Mercouris uploads, filters likely highlight clips and same-day companion clips, presents a list-first view, materializes only the operator-approved subset into canonical `raw-input`, and then suggests speaker-folder routing hints.

Use the single-URL YouTube transcript workflow for one-off URLs. Use this skill when the operator wants the **daily roster**.

**Legacy activation:** `cognition streams` remains accepted as a compatibility alias. Treat `check streams` as canonical in new docs, Coffee C routing, and operator-facing prose.

For the higher-level notebook meaning of this routine, see [cognition-streams-daily-aperture.md](../../docs/skill-work/work-strategy/cognition-streams-daily-aperture.md).

## Durable routing model

Treat `check streams` as the intake gate, not the durable interpretation layer.

- **`check streams`** = daily discovery, clip filtering, and operator selection
- **`youtube transcript`** = subtitle/materialization layer for approved URLs
- **appearance** = one normalized host/speaker/date/source event derived from verified `raw-input`
- **speaker folders** = durable accumulation layer for speaker objects, speaker arcs, helixes, and cross-year notes
- **lattice / cognition-streams surfaces** = secondary lookup and analysis views over accumulated speaker material

After materialization, prefer asking **which appearance was created and which route stack it strengthens** before updating lattice surfaces. Do not create or update speaker objects automatically from the daily check unless the operator explicitly asks.

## Layering rule

- Start with **`check streams`** when the task is "what went up today across the tracked streams?"
- Start with **`youtube transcript`** when the task is "turn this specific YouTube URL into canonical raw-input."
- If the daily roster check produces approved URLs, hand each selected item down to the lower-layer YouTube transcript workflow for the actual materialization step.
- After materialization, produce speaker-folder routing hints when the transcript clearly names a recurring speaker, guest lane, or existing `codex/<year>/speakers/<speaker>/` folder; treat the verified capture as an appearance before making interpretation claims.
- If the operator approves a guest-and-host backlog such as `Glenn x Marandi`, treat that as a valid batched handoff shape and pass the exact approved URLs down as one tranche.

## When to run

- The operator asks to check **today's uploads** across tracked main streams.
- The operator wants a **daily list-first ingest pass** rather than a one-off YouTube transcript.
- The operator asks what Daniel Davis, Glenn Diesen, Nima Alkhorshid/Dialogue Works, Judge Napolitano/Judging Freedom, and Alexander Mercouris uploaded today.
- The operator asks to materialize today's uploads from the tracked main streams after reviewing the list.

## When not to run

- A single YouTube URL is provided without daily-list intent.
- The task is one-off transcript cleanup or speaker normalization.
- The operator wants to ingest one channel item directly.

In those cases, use the lower-layer single-URL YouTube transcript workflow instead.

## Default watchlist

Track these five streams in v1:

- Daniel Davis
- Glenn Diesen
- Dialogue Works
- Judge Napolitano / Judging Freedom
- Alexander Mercouris

If a stream has no upload on the target day, say so explicitly.

## Daily workflow

1. **Discover today's uploads**
   - Query the tracked channels for the operator's local day.
   - Prefer the channel's **uploads playlist / channel-id feed** over a handle-based `/videos` page.
   - Treat a handle page as a fallback only; some channels can undercount, mis-order, or hide same-day uploads there.
   - Normalize each result into:
     - stream / channel
     - title
     - URL
     - exact `pub_date`
     - duration
   - Keep the discovery pass separate from materialization.
   - Preserve a local **discovery receipt** for the day so later audits can compare what the channel exposed against what was materialized.

2. **Run the highlight-clip filter**
   - Classify items into:
     - **Main uploads**
     - **Suspected clips / highlights**
     - **Upcoming / not-yet-aired**
   - Use a **conservative keep** bias for borderline material, but treat obvious same-day companion clips as a default no-ingest class.

3. **Present a list-first view**
   - Show the **Main uploads** first.
   - Add one short line if clips were hidden:
     - `N suspected clips hidden; show if wanted`
   - Do not materialize anything yet.

4. **Wait for operator selection**
   - Support selections such as `all`, `all except X`, channel-specific subsets, and explicit clip inclusion.

5. **Materialize the approved subset**
   - Use the atomic materializer as the default command path for approved YouTube URLs:
     - single URL: `python scripts/materialize_youtube_raw_input.py --url "<youtube-url>" --apply --with-appearances --purpose daily`
     - approved batch: `python scripts/materialize_youtube_raw_input.py --input <approved-urls.jsonl> --apply --with-appearances --purpose daily`
     - dry-run/probe: `python scripts/materialize_youtube_raw_input.py --url "<youtube-url>" --no-apply --run-id <label>`
   - For each approved URL:
     - resolve metadata first
     - fetch the best subtitle source available
     - preserve extraction receipts locally
     - write canonical date-folder raw-input
     - verify the written raw-input has a non-stub transcript body before reporting success
   - Review `.codex-tmp/youtube-raw-input/<run-id>/materialization-summary.md` and `capture-summary.md` before claiming capture.
   - For apply-mode runs with `--with-appearances`, expect the materializer to refresh `artifacts/host-shelf-quality/<year>/<host>/<YYYY-MM>/quality-summary.md/json` unless `--no-quality-report` was explicitly used.
   - Close materialization/densification claims with the mandatory quality line from the capture summary: `Structure: <delta> | Purity: <delta/%> | Unresolved: <count> | Git: on-disk/verified/not-committed/not-pushed`.
   - Do not treat new routeable appearances as textual purity gains unless the quality report shows transcript-grade, cleaned-transcript, or transcript-bearing improvement.
   - When the approved subset is really a guest-host tranche rather than "today's whole roster," preserve that exact tranche shape instead of reopening discovery or broad channel slicing.
   - If materialization returns `failed-fetch` or `failed-verification`, report the failure and stop before speaker routing, lattice updates, or completion claims.
   - For `failed-fetch` cases where a human will paste the transcript later, use the materializer's receipt-side `manual-transcript-scaffolds/` output. Keep the scaffold outside canonical raw-input until the paste marker is replaced and verification passes.

6. **Default transcript class**
   - Default to `auto_subtitles_vtt`.
   - Use explicit provenance stating subtitle-derived, lightly deduped, and not human-verified verbatim.
   - Upgrade to stronger normalization only when the operator explicitly asks.

7. **Suggest speaker-folder routing**
   - After approved items are materialized and verified as non-stub raw-input, inspect metadata, title, host, guest, and obvious `thread:` identity.
   - Treat each verified capture as an **appearance**: one host/speaker/date/source event derived from raw-input, not a durable interpretation by itself.
   - The atomic materializer now emits the first durable appearance packet for approved items when run with `--with-appearances`: `appearance-ledger.jsonl`, speaker-routing queue, speaker-memory action queue, and capture summary.
   - Treat the host-shelf quality summary as the benchmark surface for structural gain, transcript-purity gain, unresolved speaker count, and scoped git state.
   - Suggest the route stack: primary route first, then any speaker object, stream-local speaker arc, helix, or cross-host note the same appearance also strengthens.
   - For a durable advisory queue, run `python scripts/build_speaker_routing_queue.py --start YYYY-MM-DD --end YYYY-MM-DD` and review `artifacts/speaker-routing/<start>_to_<end>/speaker-routing-queue.md` plus `appearance-ledger.jsonl`.
   - When the operator wants concrete follow-up proposals, run `python scripts/build_speaker_memory_actions.py --start YYYY-MM-DD --end YYYY-MM-DD` and review `artifacts/speaker-memory-actions/<start>_to_<end>/memory-action-queue.md`.
   - Prefer existing host-local speaker arcs as the primary route when host + guest match; list matching speaker objects or helix/cross-host notes as additional strengthened surfaces.
   - If no clear speaker route exists, say so and stop at raw-input.
   - Treat lattice rows as lookup pointers; update them only after the speaker object or arc path is clear and the operator asks for that follow-up.

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
- the item appears to be a same-day companion clip cut from a longer upload on the same channel

Classify as **upcoming / not-yet-aired** when:

- the YouTube object is a scheduled live event or premiere
- the extractor reports that the live event has not begun yet
- the object has no stable aired runtime and should not yet be treated as part of the day's ingestable corpus

### Soft suspicion signals

Mark as **suspected clip** when multiple weaker signals stack:

- very short duration
- title is a reactive fragment rather than normal house style
- title is all-caps hook language with no guest/topic structure
- duplicate same-day subject with a longer same-channel upload
- description links to a separate full episode as the parent object

### Companion-clip rule

Treat a shorter same-day upload as a **companion clip** when all or nearly all of the following are true:

- the same channel has a longer upload with the same guest or same substantive topic on the same day
- the shorter item's title reads like a narrowed thesis, punchier hook, or extracted sub-claim from the longer upload
- the runtime is materially shorter than the longer same-day upload
- the shorter item does not look like an independent house-style episode in its own right

Default policy:

- **do not record companion clips**
- show them only in the hidden `Suspected clips / highlights` bucket
- materialize them only if the operator explicitly overrides that default

For recurring cases like `Davis x Crooke`, assume the longer same-day interview is the canonical daily object unless there is strong evidence the shorter file is a genuinely separate episode.

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
- **Alkorshid / Dialogue Works:** titles may be dramatic, and some legitimate interviews can still be relatively short; title sensationalism or a 10-15 minute runtime alone is not enough
- **Napolitano / Judging Freedom:** high-volume interview cadence is normal; use guest/title structure and live/upcoming status before duration-only exclusion
- **Mercouris:** usually long monologues; short uploads are more suspicious

### Discovery-source discipline

Use this priority order:

1. **Channel uploads playlist / channel-id feed**
2. **Channel RSS feed** when the latest window is enough
3. **Handle-based `/videos` page** only as fallback
4. **Local inventory / prior receipts** only as audit aid, not as the primary truth source

Rationale:

- handle pages can undercount or reorder uploads on some channels
- high-volume channels can mix shorts, clips, livestream placeholders, and main uploads in unstable ways
- a preserved daily receipt lets you distinguish "not ingested yet" from "not actually published" later

### Audit discipline

When checking whether a day is complete:

- reconcile by **`source_url` / YouTube id**, not by filename alone
- use frontmatter identity (`show`, `channel_slug`, `source_url`) before filename heuristics
- treat outside-channel collabs as separate from the four-stream watchlist even if the guest/host overlaps
- never claim a day is "complete" unless the discovery receipt and the local materialized set have both been checked
- when you need a computed score, repair queue, and durable receipts, run `python scripts/cognition_streams_audit.py --start YYYY-MM-DD --end YYYY-MM-DD --recent-start YYYY-MM-DD` against the active `/codex/<year>` notebook root
- when you need a derived speaker-routing queue after materialization, run `python scripts/build_speaker_routing_queue.py --start YYYY-MM-DD --end YYYY-MM-DD`; this emits advisory queue and appearance-ledger artifacts only and does not edit speaker folders
- when you need concrete speaker-memory follow-up proposals, run `python scripts/build_speaker_memory_actions.py --start YYYY-MM-DD --end YYYY-MM-DD`; this emits advisory action artifacts only and does not edit speaker folders

## Output shape

Use this shape by default:

```markdown
# Today's Stream Check

## Main uploads
- <channel> — <title> — <date> — <url>

N suspected clips hidden; show if wanted.
```

If the operator asks to see clips:

```markdown
## Suspected clips / highlights
- <channel> — <title> — <why flagged> — <url>
```

After operator selection, report only the approved items being materialized and the resulting raw-input outcome. When materialization succeeds and a speaker route is clear, add:

```markdown
## Speaker routing hints
- <raw-input file> -> <primary speaker route> — <next action> — <why>
- also strengthens: <speaker object / speaker arc / helix / cross-host note paths, if any>
- action queue: <memory-action-queue.md path, when generated>
```

Use "candidate" when the target does not exist yet or would require a new speaker object / speaker arc decision.

## Guardrails

- Never silently discard borderline items.
- Do not record same-day companion clips by default.
- Never auto-materialize everything by default.
- Never treat clip suspicion as certainty.
- Never silently promote subtitle-derived outputs into stronger transcript classes.
- Never claim a stream item is captured when the raw-input file is header-only, index-only, placeholder text, or otherwise fails non-stub body verification.
- Never create or update speaker folders, speaker objects, speaker arcs, helixes, or lattice rows from the daily check unless the operator explicitly asks.
- Do not let the lattice become the first durable destination. Raw-input comes first; speaker-folder routing comes next; lattice updates are secondary pointers.

## Success condition

The operator gets a clean daily upload list for the tracked main streams, with obvious clips filtered into a secondary bucket, only the approved subset materialized into provenance-safe canonical `raw-input` that passes non-stub body verification, and clear speaker-folder routing hints for any material that strengthens an existing or candidate speaker object.
