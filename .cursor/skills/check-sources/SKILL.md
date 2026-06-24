---
name: check-sources
description: Check the main channel-index YouTube roster (channel-index.json SSOT; misc excluded) for live discovery, repo reconciliation, clip filtering, and handoff to source-intake. Use check sources watchlist for the six daily_watchlist channels. Legacy check streams and cognition streams remain compatibility aliases.
preferred_activation: check sources
activation: check sources
portable: true
version: 1.0.1
category: truth-pipeline
status: active
scope_class: repo-governed
tags:
- operator
- strategy
- source-archive
- youtube
- daily
- source-archive
portable_source: skills/check-sources/SKILL.md
synced_by: sync_portable_skills.py
---
# Check sources

**Preferred activation (operator):** say **`check sources`**.

Use this skill for **YouTube source discovery and daily ingest** across the **main channel-index roster**. It discovers live uploads, filters likely highlight clips and same-day companion clips, presents a list-first view, reconciles against local archive captures, and hands off only the operator-approved subset to **`source-intake`** for canonical archive land (`source-*` under `source-archive/statecraft/`).

Do **not** use the deprecated **`youtube-raw-input-transcript`** / **`materialize_youtube_raw_input.py --apply`** path. See [YOUTUBE-MATERIALIZE-DEPRECATED.md](../../docs/skill-work/work-strategy/YOUTUBE-MATERIALIZE-DEPRECATED.md).

For a single URL with transcript already in hand, use **`source-intake`** directly. Use this skill when the operator wants **roster-scoped discovery** (full main index or watchlist-fast pass).

**Legacy activation:** **`check streams`** and **`cognition streams`** remain accepted compatibility aliases. Treat **`check sources`** as canonical in new docs, Coffee C routing, and operator-facing prose.

## Roster SSOT (channel-index)

The check-sources roster is **not** a hard-coded channel list in this skill.

| Surface | Role |
|---------|------|
| [`channel-index.json`](../../source-archive/statecraft/channel-index.json) | Machine roster — **main index only**; each row has `check_sources: true` |
| [`channel-index.md`](../../source-archive/statecraft/channel-index.md) | Human inventory + stats (regenerated together) |
| [`channel-index-misc.md`](../../source-archive/statecraft/channel-index-misc.md) | **Excluded** from check-sources |
| [`statecraft_youtube_discovery.json`](../../platform/config/statecraft_youtube_discovery.json) | Discovery metadata (`channel_id`, `handle_url`, routing rules) |

**Loader (Python):** `load_check_sources_roster()` in [`scripts/statecraft_youtube_discovery.py`](../../scripts/statecraft_youtube_discovery.py) — reads `channel-index.json` or rebuilds live via `build_channel_index_json()`.

**Scope modes:**

- **`check sources`** (default) — all **main-index** channels where `discoverable: true` in JSON (YouTube URL or discovery `channel_id` / `handle_url`). Non-discoverable main rows may still appear in repo audit when asked.
- **`check sources watchlist`** — subset with `watchlist: true` (six `daily_watchlist` channels: Mercouris, Dialogue Works, Davis, Diesen, Judging Freedom, Redacted). Fast daily pass; same clip filter and source-intake closeout.
- **`check sources repo-only`** — local archive / intake reconciliation without live YouTube discovery (operator must say repo-only or equivalent).

Regenerate roster after archive routing changes: `python scripts/refresh_statecraft_archive_indices.py`.

For the higher-level notebook meaning of this routine, see [cognition-streams-daily-aperture.md](../../docs/skill-work/work-strategy/cognition-streams-daily-aperture.md).

## Clip law

Treat highlight clips, teaser cuts, and same-day companion excerpts as discovery noise unless the operator explicitly asks to preserve them.

- Main uploads come first.
- Clips are secondary and should usually be listed separately or suppressed.
- Do not materialize a clip into canonical archive merely because it is easier to recover than the parent interview.
- If the parent interview is not yet recovered, keep the clip as a clue, not as a substitute.

Short rule:

`discover clips if useful -> prefer parent episode -> archive clips only by explicit operator override`

## Durable routing model

Treat **`check sources`** as the intake gate, not the durable interpretation layer.

- **`check sources`** = roster-scoped discovery, clip filtering, operator selection, archive reconciliation
- **`youtube transcript`** = subtitle/materialization layer for approved URLs
- **appearance** = one normalized host/speaker/date/source event derived from a verified **source archive** capture
- **speaker folders** = durable accumulation layer for speaker objects, speaker arcs, helixes, and cross-year notes
- **lattice / cognition-streams surfaces** = secondary lookup and analysis views over accumulated speaker material

After materialization, prefer asking **which appearance was created and which route stack it strengthens** before updating lattice surfaces. Do not create or update speaker objects automatically from the daily check unless the operator explicitly asks.

## Answer-first stopping rule

When the operator asks for a **bounded retrieval object** inside the check-sources domain, return that object **immediately** and stop unless broader workflow was explicitly requested.

Examples:

- if the operator asks for **URLs**, return the URLs first
- if the operator asks for a **priority order**, return the priority order first
- if the operator asks for **which items are missing**, return the missing set first

Do **not** expand a bounded retrieval ask into discovery repair, dependency installation, transcript materialization, routing updates, or rubric analysis unless the operator explicitly asks for that next layer after receiving the requested object.

Short rule:

`requested object in hand -> answer -> stop`

The daily ingest workflow exists to support operator intent, not to outrank it.

## Episode-object retrieval rule

When the requested object is an **actual episode object** rather than a repo summary, discovery must start with the strongest available **YouTube-first** retrieval path.

Examples:

- `show me the episode titles and urls`
- `find more mearsheimer, feb 2025`
- `which Mearsheimer episodes are missing that month`

Default behavior:

- use the host's YouTube discovery tooling first
- if `yt-dlp` is available in the host, treat it as the default direct-episode recovery path
- return direct watch URLs and canonical episode titles first when they can be recovered

Do **not** satisfy an episode-object request with only:

- repo-local source archive capture counts
- prior receipts
- secondary mirrors
- web snippets

when a direct YouTube-first recovery path is available and has not yet been tried.

Short rule:

`episode object requested -> yt-dlp / YouTube-first discovery first -> answer with titles + direct URLs -> stop`

## Meaning of "check sources"

Default interpretation:

- **load roster from channel-index.json** (main only; misc excluded)
- **source discovery first** (unless `repo-only`)
- **repo reconciliation second** (archive captures under `source-archive/statecraft/`)
- **source-intake third** (approved URLs / operator paste)

If the operator says `check-sources`, `check sources`, or legacy `check streams` without narrowing it to `repo-only`, assume they want live YouTube discovery for the active roster scope, then compare against local archive captures and receipts.

Do not silently collapse **`check sources`** into a repo-only audit unless the operator explicitly asks for a local-only check.

If the operator asks for **episode objects**, **missing episode recovery**, or **show URLs**, a repo-only audit is not enough. Treat receipts and local inventories as secondary until the YouTube-first path has been attempted or has clearly failed.

## Mode split

Explicitly distinguish these three modes in your own reasoning and in operator-facing results when useful:

- **YouTube discovery** = what appears to exist on the live source side for the requested day, month, stream, or speaker
- **Repo audit** = what is already present locally in **`source-archive/statecraft/`**, receipts, inventories, and adjacent artifacts
- **Repair / materialization** = taking an approved or operator-pasted item and landing it via **`source-intake`** into a canonical **`source-*`** archive capture

Short rule:

`discover -> compare -> repair only if asked or clearly supplied`

For bounded retrieval asks such as `find more Freeman`, `missing days list`, or `show URLs`, discovery should lead unless the operator explicitly says `repo-local`, `already on disk`, or similar.

For those bounded retrieval asks, **discovery** means **direct-source discovery**, not merely searching local notes about prior discovery. If the host exposes `yt-dlp` or an equivalent YouTube retrieval tool, use that path before falling back to receipts, mirrors, or secondary web search.

## Status labels

When returning results, label each item or group with one of these statuses whenever feasible:

- **already captured**
- **found externally, missing locally**
- **materialized from operator paste**
- **discovered but unresolved**
- **missing direct watch URL**
- **clip only, parent unresolved**

Do not blur these states together in prose. In particular:

- `already captured` means a local **`source-*`** archive capture already exists under **`source-archive/statecraft/`**
- `found externally, missing locally` means the item is evidenced outside the repo but not yet present in the source archive
- `materialized from operator paste` means the operator supplied the transcript body and you used that to create or strengthen the local artifact
- `discovered but unresolved` means the title/date/source shape appears real, but transcript-grade or canonical-source conditions are not yet satisfied
- `missing direct watch URL` means exactly that: you found external evidence, but not a trustworthy direct YouTube watch URL
- `clip only, parent unresolved` means the only thing currently recovered is a highlight or companion clip and the full parent episode is still not materially recovered

## URL confidence rule

- If you have a **direct YouTube watch URL**, show it first.
- If you have only a **secondary listing URL** such as a podcast mirror, transcript mirror, Apple Podcasts, Art19, Podbay, Podchaser, or similar, say so plainly.
- Do **not** synthesize, infer, or guess a `youtube.com/watch?v=` URL from partial evidence.
- When a direct watch URL is missing, keep the item labeled `missing direct watch URL` until it is actually recovered.
- When `yt-dlp` or an equivalent YouTube retrieval path is available, try that direct-source recovery before closing with only secondary URLs, unless the operator explicitly asked for a repo-local or web-only answer.

## Inventory staleness rule

Treat repo inventories, `needs capture` labels, and prior receipts as useful but non-authoritative hints.

- A row marked `needs capture` may already exist in **`source-archive/statecraft/`**
- A row marked `mirrored` may still be weak, stale, or incomplete
- A missing inventory row does not prove the item never existed

Before reporting an item as missing locally, check the actual date folders and likely **`source-*`** filename variants under **`source-archive/statecraft/`**.

Short rule:

`inventory is a hint, source-archive tree is the authority`

**Legacy (archaeology only):** `codex/years/2026/raw-input/raw-input-master-index.md` and companion audit JSON may still help locate pre-migration captures. If the legacy index and **`source-archive/statecraft/`** disagree, the **source archive** wins for new work.

## Index hierarchy and routing choice

After materialization, treat the routing stack this way:

- the **source archive** day-index and thread-index surfaces are the maintained corpus-wide route maps
- a speaker **source bench** (`*-raw-input-index.md` legacy filename) is updated only when it functions as a real `non-core appearance bench`
- arc files remain interpretive surfaces by default

Do not split an arc into a dedicated index surface unless the speaker-map threshold is met: the arc is no longer a practical front door, the items form a distinct retrieval domain, and the new surface would answer a different operator question than the neighboring bench or arc.

If a speaker is touched during ingest or routing, choose one of these outcomes explicitly:

- existing speaker source bench (legacy `*-raw-input-index.md` when present)
- existing host / core lane
- existing arc / object / routing surface
- explicit note that no new index is justified

## Month-ledger closeout

When the operator is working a month, a speaker batch, or another bounded calendar slice, prefer ending with a compact ledger:

- **captured**
- **found externally, missing locally**
- **repaired this pass**
- **still missing direct watch URL**

This helps distinguish discovery completeness from transcript/materialization completeness.

When the operator is driving transcript recovery by paste, prefer the stronger four-line closeout vocabulary used in the Freeman month passes:

- **already captured**
- **materialized from operator paste**
- **found externally, missing locally**
- **still missing direct watch URL**

Use the exact labels when possible so month-closeout replies remain comparable across runs.

## Date-conflict rule

When a stream item has a **recording/opening date** that conflicts with an earlier **publication/discovery date**, do not flatten the conflict away.

Short rule:

`pick one canonical pub_date for the file -> preserve the conflicting date explicitly in source_note`

Preferred precedence:

1. direct source publication evidence
2. trustworthy secondary publication listing
3. spoken/opening date inside the transcript

Typical cases:

- transcript says `Friday, June 20` but the episode was published `June 22`
- transcript says `Tuesday, June 17` but the episode surfaced externally as `June 18`
- transcript says the wrong month entirely due to transcript noise

In those cases:

- materialize under the most defensible **publication date**
- keep the conflict explicit in `source_note`
- mention the ambiguity in the operator-facing closeout

Do **not** silently rewrite or ignore date tensions.

## Operator-paste recovery rule

If the operator pastes a full transcript body for a discovered item, that is sufficient to perform **local source archive recovery** even when the direct YouTube watch URL remains unresolved.

In that situation:

- land the canonical **`source-*`** capture via **`source-intake`**
- mark `transcript_type: operator_pasted_transcript`
- keep `source_type: youtube` if the appearance is clearly a YouTube stream item
- state in `source_note` that the transcript was operator-pasted and the direct watch URL is not yet recovered
- report the item as **materialized from operator paste**
- keep any unresolved YouTube URL issue separately labeled as **missing direct watch URL**

Do **not** block local transcript recovery merely because the direct watch URL is still missing, as long as the appearance identity is otherwise well anchored.

## Partial front-door rule

Keep **local transcript recovery** separate from **front-door completeness**.

- If a direct YouTube watch URL is recovered, use it and treat the item as a normal YouTube-first capture.
- If the direct watch URL is still missing but the episode identity is otherwise well anchored by:
  - a full operator-pasted transcript
  - a trustworthy title
  - a trustworthy publication date
  - a stable host/show identity
  then local archive materialization may still proceed.
- In that case, preserve the unresolved front-door seam explicitly:
  - keep the operator-facing status `materialized from operator paste`
  - also keep the unresolved status `missing direct watch URL`
  - say plainly which secondary surface anchored the date or title

Do **not** pretend that unresolved front-door recovery means the episode is fake.

Short rule:

`real transcript + anchored identity + missing watch URL -> materialize honestly -> keep front-door unresolved`

If the only recovered external surface is a podcast or directory listing and a trustworthy YouTube watch URL was not recovered, do **not** invent one. Either:

- keep `source_type: youtube` when the stream identity is clearly a known YouTube host-family object and the unresolved watch URL is explicitly preserved, or
- use the more truthful secondary source surface in the archive metadata when the direct YouTube front door is not actually confirmed

The archive must preserve the strongest truthful provenance, not the most flattering one.

## Source-archive closeout rule

When a check-stream or one-off recovery **adds or strengthens a canonical `source-archive/statecraft/` capture**, close the ingest loop at every still-live index layer touched by that capture.

Minimum required follow-ons:

- refresh the touched day folder `README.md`
- verify whether the capture belongs to an existing live `statecraft/<speaker>/` shelf with a `*-raw-input-index.md` provenance bench
- if such a shelf exists and the new capture is route-relevant for that speaker, update the speaker source bench in the same pass before closing

Short rule:

`source-archive upload -> day index refresh -> touched speaker source bench refresh -> close`

Do not assume day-index regeneration is enough. If the live speaker shelf owns a provenance bench, that bench is part of canonical ingest completion.

If the new capture materially changes the continuity story rather than only extending the bench, also tighten the minimally affected live shelf surfaces, usually:

- `*-arc.md`
- `*-routing.md`
- one bounded `*-support-spine*.md` note when the new source changes reinforcement-vs-primary reading

Do this narrowly. Do not widen a simple ingest into full shelf redesign unless the operator asks.

Short shelf-closeout heuristic:

`bench always -> routing when opener meaning changes -> support spine when lane role changes`

## Multi-guest naming rule

For guest-heavy stream appearances, preserve a stable canonical shape in both filename and frontmatter.

- filenames should include the visible principal guests in title order, normalized to slug-safe text
- frontmatter should keep:
  - `thread` for the primary speaker of the current recovery tranche
  - `thread_2`, `thread_3`, etc. for additional principal guests when useful
  - `guest`, `guest_2`, `guest_3`, etc. in spoken/title order

Examples:

- `freeman` + `wilkerson`
- `freeman` + `wilkerson` + `parsi`

The goal is not perfect ontology. The goal is stable month-ledger accounting and later speaker-route discoverability.

## Direct-URL absence is not transcript absence

Keep this distinction sharp:

- **missing direct watch URL** does **not** mean the appearance is fake
- **found externally, missing locally** means the appearance is evidenced but not yet recovered in the **source archive**
- **materialized from operator paste** means local transcript presence is now solved even if URL provenance is not fully solved

Do not let URL incompleteness erase transcript completeness.

## Fullness-before-closure rule

Do not treat a successful daily run as complete merely because discovery and materialization succeeded.

Before closure, ask:

- did the run produce a trustworthy discovery receipt, rather than only a plausible list?
- did each approved item become a verified appearance, rather than just a stored transcript?
- did the routing hint name the correct next surface, rather than merely mentioning a speaker?
- did any lattice or stream-facing suggestion avoid substituting for a fuller speaker route that should exist elsewhere?

Short rule:

`discovered` is not enough
`captured` is not enough
`complete` means the run leaves behind trustworthy provenance, clear appearance status, and the right next routing surface

## Skill closure rule

Use [skill-closure-doctrine.md](../../docs/skill-closure-doctrine.md) as the shared maturity test.

For this skill, stronger synthesis belongs only after the daily run has yielded verified appearances and the correct next route. A successful ingest run does not by itself justify speaker doctrine or shelf-level meaning.

## YouTube-first invariant

For this skill, **discovery should be YouTube-first whenever possible**.

- A stream item should be treated as a real transcript candidate only when you have a **direct YouTube watch URL** (`https://www.youtube.com/watch?v=...` or equivalent canonical YouTube watch link).
- Podcast mirrors, Apple/Podbay/Art19/Podscan listings, transcript mirrors, and other secondary directories may help discovery, but they do **not** by themselves qualify an item as transcript-ready.
- If only secondary episode listings are available, treat the item as **discovered but unresolved**:
  - you may report it in the check result,
  - you may create a clearly marked **scaffold/discovery placeholder**,
  - and you may materialize from a full operator paste only under the **partial front-door rule**
  - but you must **not** silently describe it as a fully recovered YouTube-provenance capture.
- When the operator asks for URLs, prefer the **direct YouTube watch URLs** first. Only fall back to secondary listing URLs if YouTube could not yet be recovered, and say that explicitly.

## Layering rule

- Start with **`check sources watchlist`** when the task is "what went up today across the six daily watchlist channels?"
- Start with **`check sources`** when the task is "what went up across the full main channel-index roster?"
- Start with **`source-intake`** when the task is "turn this specific YouTube URL (or pasted body) into a canonical **source archive** capture."
- If the daily roster check produces approved URLs, hand each selected item to **`source-intake`** for the actual land step.
- After materialization, produce speaker-folder routing hints when the transcript clearly names a recurring speaker, guest lane, or existing `codex/<year>/speakers/<speaker>/` folder; treat the verified capture as an appearance before making interpretation claims.
- If the operator approves a guest-and-host backlog such as `Glenn x Marandi`, treat that as a valid batched handoff shape and pass the exact approved URLs down as one tranche.

## When to run

- The operator asks to **`check sources`** or **`check sources watchlist`** for today's uploads.
- The operator wants a **list-first ingest pass** across the channel-index roster rather than a one-off URL.
- The operator asks what uploaded today across Mercouris, Dialogue Works, Davis, Diesen, Judging Freedom, Redacted, or the broader main index.
- The operator asks to land today's approved uploads via **`source-intake`** after reviewing the discovery list.

**Roster load (agent):** at session start, call `load_check_sources_roster()` or read `channel-index.json`; filter to `watchlist: true` when the operator said watchlist.

## When not to run

- A single YouTube URL is provided without daily-list intent.
- The task is one-off transcript cleanup or speaker normalization.
- The operator wants to ingest one channel item directly.

In those cases, use the lower-layer single-URL YouTube transcript workflow instead.

## Default watchlist (fast pass)

**`check sources watchlist`** tracks the six `daily_watchlist` channels from discovery config (also `watchlist: true` in `channel-index.json`):

- Alexander Mercouris
- Dialogue Works
- Daniel Davis
- Glenn Diesen
- Judge Napolitano / Judging Freedom
- Redacted News

The **full main roster** (currently 14 channels) adds Nawfal, Breaking Points, Tucker Carlson, Neutrality Studies, and other main-index slugs — use plain **`check sources`** when the operator wants breadth beyond the six.

If a channel has no upload on the target day, say so explicitly.

## Daily workflow

1. **Discover today's uploads**
   - Query the tracked channels for the operator's local day.
   - Prefer a direct-source YouTube retrieval path. When available in the host, use `yt-dlp` as the default discovery and metadata-recovery tool before falling back to weaker channel-page or web-snippet methods.
   - Prefer the channel's **uploads playlist / channel-id feed** over a handle-based `/videos` page.
   - Treat a handle page as a fallback only; some channels can undercount, mis-order, or hide same-day uploads there.
   - Preserve the **direct YouTube watch URL** for every discovered item. If discovery only surfaces a title through a secondary listing, keep that item flagged as unresolved until the watch URL is recovered or the operator explicitly accepts a scaffold.
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

5. **Land the approved subset (`source-intake`)**
   - After operator approval, obtain a **full transcript body** for each URL (operator paste in thread, session-log extraction, or bounded subtitle fetch — same provenance rules as before).
   - Land each capture with **`source-intake`**: sidecar `header.md` + body → `python scripts/land_statecraft_source_body.py` → `source-archive/statecraft/YYYY-MM-DD/source-<slug>.md`.
   - Run the source-intake post-land chain (day README, intake queue) per [statecraft-source-intake](../statecraft-source-intake/SKILL.md).
   - **Do not** call `python scripts/materialize_youtube_raw_input.py --apply` for new archive writes. That path is deprecated ([YOUTUBE-MATERIALIZE-DEPRECATED.md](../../docs/skill-work/work-strategy/YOUTUBE-MATERIALIZE-DEPRECATED.md)).
   - **Do not materialize from podcast-directory URLs or transcript-mirror URLs.** The approved source must be the direct YouTube watch URL in frontmatter.
   - For each approved URL:
     - resolve metadata first (title, `pub_date`, channel / host)
     - if subtitle fetch fails, report failure and offer operator-paste **`source-intake`** — do not invent stub archive files
     - preserve extraction receipts locally when fetch was used
     - verify the landed archive file has a non-stub transcript body before reporting success
   - If the operator has already pasted the full transcript in the current Codex thread, run **`source-intake`** with mechanical session-log extraction when available. Require exact-match verification before closing: `sourceChars`, `bodyChars`, `exactMatch=True`.
   - After exact-match verification passes, update check-stream receipts as captured with `capture_status: full-operator-paste`. Use `partial-chat-capture` only when the source is truly incomplete or exact extraction cannot be verified.
   - After successful **`source-intake`**, refresh the touched day `README.md` (included in post-land chain).
   - If materialization returns `failed-fetch` or `failed-verification`, report the failure and stop before synthesis or completion claims.
   - If YouTube discovery fails but secondary listings strongly suggest a same-day upload exists, report it as **missing-watch-url / unresolved**, not as captured.

6. **Default transcript class**
   - Default to `auto_subtitles_vtt`.
   - Use explicit provenance stating subtitle-derived, lightly deduped, and not human-verified verbatim.
   - Upgrade to stronger normalization only when the operator explicitly asks.

7. **Suggest speaker-folder routing**
   - After approved items are landed via **`source-intake`** and verified as non-stub archive captures, inspect metadata, title, host, guest, and obvious `thread:` identity.
   - Treat each verified capture as an **appearance**: one host/speaker/date/source event derived from the archive capture, not a durable interpretation by itself.
   - Appearance / routing queues are **not** auto-emitted by source-intake; run routing builders manually when the operator wants them (see below).
   - Treat the host-shelf quality summary as the benchmark surface for structural gain, transcript-purity gain, unresolved speaker count, and scoped git state.
   - Suggest the route stack: primary route first, then any speaker object, stream-local speaker arc, helix, or cross-host note the same appearance also strengthens.
   - For a durable advisory queue, run `python scripts/build_speaker_routing_queue.py --start YYYY-MM-DD --end YYYY-MM-DD` and review `runtime/artifacts/speaker-routing/<start>_to_<end>/speaker-routing-queue.md` plus `appearance-ledger.jsonl`.
   - When the operator wants concrete follow-up proposals, run `python scripts/build_speaker_memory_actions.py --start YYYY-MM-DD --end YYYY-MM-DD` and review `runtime/artifacts/speaker-memory-actions/<start>_to_<end>/memory-action-queue.md`.
   - Prefer existing host-local speaker arcs as the primary route when host + guest match; list matching speaker objects or helix/cross-host notes as additional strengthened surfaces.
   - Distinguish the surface type: use **host-local arc** for one host x guest braid, **thread atlas** for recurring strands across months or hosts, and **speaker helix** for cross-host comparison of multiple host-local arcs.
   - If no clear speaker route exists, say so and stop at archive land.
   - Treat lattice rows as lookup pointers; update them only after the speaker object or arc path is clear and the operator asks for that follow-up.
   - If the only available suggestion is a roster mention or vague lattice presence, say the route is still thin rather than implying completion.

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
- report the requested target date or item first; historical backlog is secondary context
- when `summary.json` includes `target_date_*` or `target_window_*`, use those fields for the operator-facing verdict
- treat `overall_backlog_status` as a backlog-health signal, not as the answer to a date-scoped request
- when you need a computed score, repair queue, and durable receipts, run `python scripts/cognition_streams_audit.py --start YYYY-MM-DD --end YYYY-MM-DD --recent-start YYYY-MM-DD --roster watchlist` (default reconciles `source-archive/statecraft`; use `--roster main` for full channel-index roster)
- when you need a derived speaker-routing queue after materialization, run `python scripts/build_speaker_routing_queue.py --start YYYY-MM-DD --end YYYY-MM-DD`; this emits advisory queue and appearance-ledger artifacts only and does not edit speaker folders
- when you need concrete speaker-memory follow-up proposals, run `python scripts/build_speaker_memory_actions.py --start YYYY-MM-DD --end YYYY-MM-DD`; this emits advisory action artifacts only and does not edit speaker folders

### Capture mode diagnosis

When the capture path is noisy, distinguish the failure layer plainly:

- **Online discovery failed:** the channel or YouTube surface was blocked, timed out, or undercounted.
- **Cached/offline audit worked:** local discovery receipts were sufficient to identify missing videos and repair queue state.
- **Exact-URL materialization worked:** a specific approved watch URL produced a verified **source archive** capture even if broad discovery was brittle.
- **Metadata-bypass materialization worked:** YouTube metadata fetch failed, but the operator-provided title/date/lane metadata let the exact URL proceed to subtitle extraction and verification.
- **Operator-paste materialization worked:** YouTube fetch or patch ergonomics failed, but a full operator-pasted transcript was mechanically extracted from the local session log, written to a canonical **`source-*`** capture, and exact-match verified.

Prefer exact-URL materialization for repair queue items once the operator has named or approved them.

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

After operator selection, report only the approved items being landed and the resulting archive outcome. When **`source-intake`** succeeds and a speaker route is clear, add:

```markdown
## Capture closeout
- target: <date or item> - <target_date_status or target_window_status> - <captured>/<main_total> captured - must-capture remaining: <N>
- archive: <source-archive path(s)>
- audit artifact: <summary/repair queue path>
- backlog: <overall_backlog_status>; probably-capture backlog remains: <yes/no>
- capture mode: <online discovery / cached offline audit / operator-paste source-intake / subtitle-fetch then source-intake>

## Transcript quality
- archive: <path>
- evidence grade: <transcript-grade / cleaned-transcript / transcript-bearing / summary-grade / legacy-appearance-only>
- word count: <N>
- routeable: <yes/no>; unresolved speaker: <yes/no>
- residual noise: <none or terms>
- quality note: <source_note/editorial_note/quality_note>

## Speaker routing hints
- <archive capture> -> <primary speaker route> - <next action> - <why>
- also strengthens: <speaker object / speaker arc / helix / cross-host note paths, if any>
- action queue: <memory-action-queue.md path, when generated>
```

## Steward closeout

When a check-sources repair becomes a commit candidate, keep the ship slice narrow:

- stage only source-archive captures, check-sources audit artifacts, speaker-routing/action receipts, and cadence lines
- leave runtime observability, memory, handoff, host-quality background churn, and unrelated benchmark artifacts untouched unless explicitly scoped
- before suggesting push safety, report branch ahead count and any remaining untracked capture artifacts

Use "candidate" when the target does not exist yet or would require a new speaker object / speaker arc decision.

## Guardrails

- Never silently discard borderline items.
- Do not record same-day companion clips by default.
- Never auto-materialize everything by default.
- Never treat clip suspicion as certainty.
- Never silently promote subtitle-derived outputs into stronger transcript classes.
- Never claim a stream item is captured when the archive file is header-only, index-only, placeholder text, or otherwise fails non-stub body verification.
- Never downgrade a full operator-pasted transcript to partial just because it was supplied in chat, too long for a comfortable patch, or unavailable from YouTube. Extract it mechanically from the local session log when available, then verify exact body match.
- Never remove an item from the repair queue on operator-paste evidence unless the canonical archive body is non-stub and exact-match verification has passed.
- Never create or update speaker folders, speaker objects, speaker arcs, helixes, or lattice rows from the daily check unless the operator explicitly asks.
- Do not let the lattice become the first durable destination. Archive land comes first; speaker-folder routing comes next; lattice updates are secondary pointers.
- Never continue into repair, capture, dependency, or routing work after a bounded retrieval ask has already been satisfied, unless the operator explicitly asks for the next step.

## Success condition

The operator gets a clean upload list for the active roster scope (watchlist or full main index), with obvious clips filtered into a secondary bucket, only the approved subset landed via **`source-intake`** into provenance-safe canonical **`source-*`** archive captures that pass non-stub body verification, and clear speaker-folder routing hints for any material that strengthens an existing or candidate speaker object.

## Verification / Proof Standard

Do not call this complete unless:

- the input source, file, paste, URL, or archive path is named
- the output surface is named
- skipped steps are explicitly marked with a reason
- uncertainty, missing evidence, or unresolved source defects are stated
- watchlist/roster source and selected candidates must be named

Evidence to report:

- files touched or produced
- scripts or commands run
- source URLs, archive paths, or transcript identifiers used
- confidence downgrade, if any

If verification cannot be completed:

- state what was not verified
- stop before archive land, synthesis, publication, or promotion
- return a bounded partial result for operator review


## Cursor / strategy-codex instance

Grace-mar paths and commands for this repository (from `.cursor/skills/check-sources/`).

| Topic | Path |
|--------|------|
| Canonical source archive | [source-archive/statecraft/](../../source-archive/statecraft/) |
| Check-sources roster (machine) | [channel-index.json](../../source-archive/statecraft/channel-index.json) |
| Check-sources roster (human) | [channel-index.md](../../source-archive/statecraft/channel-index.md) |
| Roster loader | [statecraft_youtube_discovery.py](../../scripts/statecraft_youtube_discovery.py) (`load_check_sources_roster`) |
| Archive land skill | [statecraft-source-intake/SKILL.md](../statecraft-source-intake/SKILL.md) |
| Deprecated materialize path | [YOUTUBE-MATERIALIZE-DEPRECATED.md](../../../docs/skill-work/work-strategy/YOUTUBE-MATERIALIZE-DEPRECATED.md) |
| Legacy check-streams stub | [check-streams/SKILL.md](../check-streams/SKILL.md) |
| Deprecated raw-input (archaeology) | [RAW-INPUT-DEPRECATED.md](../../../docs/skill-work/work-strategy/RAW-INPUT-DEPRECATED.md) · [codex/raw-input/README.md](../../../codex/raw-input/README.md) |
| Speaker folder shelf | [codex/speakers/](../../../codex/speakers/) |
| Philosophical gloss | [docs/skill-work/work-strategy/cognition-streams-daily-aperture.md](../../../docs/skill-work/work-strategy/cognition-streams-daily-aperture.md) |
| Temp daily discovery cache | [\.codex-tmp/](../../.codex-tmp/) |
| Portable skill manifest | [skills/manifest.yaml](../../../skills/manifest.yaml) |
| Sync script | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |

**Repo notes**

- **`check sources`** is canonical; **`check streams`** and **`cognition streams`** are legacy aliases.
- Roster SSOT: **`channel-index.json`** (main only; misc excluded). Watchlist fast pass = six `daily_watchlist` channels.
- Approved captures close with **`source-intake`**, not `materialize_youtube_raw_input.py --apply`.

**Common local command pattern**

```powershell
python scripts/sync_portable_skills.py --skill check-sources
python scripts/sync_portable_skills.py --verify --skill check-sources
python -c "from pathlib import Path; import sys; sys.path.insert(0,'scripts'); from statecraft_youtube_discovery import load_check_sources_roster; print(len(load_check_sources_roster()))"
python scripts/refresh_statecraft_archive_indices.py
python scripts/build_speaker_routing_queue.py --start YYYY-MM-DD --end YYYY-MM-DD
python scripts/validate_skills.py
```
