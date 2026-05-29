---
name: "check-streams"
preferred_activation: "check streams"
description: "Check the daily tracked YouTube stream roster for Davis, Diesen, Alkorshid/Dialogue Works, Napolitano/Judging Freedom, and Mercouris: discover today's uploads with YouTube-first tooling, filter suspected clips, list main uploads first, materialize only the operator-approved subset into canonical raw-input, and suggest speaker-folder routing hints."
portable: true
version: "0.2.8"
tags:
  - "operator"
  - "strategy"
  - "raw-input"
  - "youtube"
  - "daily"
portable_source: "skills-portable/check-streams/SKILL.md"
synced_by: "sync_portable_skills.py"
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

When routing friction becomes a **speaker shelf** problem rather than an ingest problem, hand off to [`speaker-shelf-hygiene`](../speaker-shelf-hygiene/SKILL.md) instead of improvising shelf doctrine inside the daily check.

## Answer-first stopping rule

When the operator asks for a **bounded retrieval object** inside the check-streams domain, return that object **immediately** and stop unless broader workflow was explicitly requested.

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

- repo-local raw-input counts
- prior receipts
- secondary mirrors
- web snippets

when a direct YouTube-first recovery path is available and has not yet been tried.

Short rule:

`episode object requested -> yt-dlp / YouTube-first discovery first -> answer with titles + direct URLs -> stop`

## Meaning of "check streams"

Default interpretation:

- **source discovery first**
- **repo reconciliation second**
- **materialization third**

If the operator says `check-streams` or `check streams` without narrowing it to `repo-only`, assume they want you to check the live source surfaces first, especially YouTube, and only then compare that result against local `raw-input`, receipts, and inventories.

Do not silently collapse `check streams` into a repo-only audit unless the operator explicitly asks for a local-only check.

If the operator asks for **episode objects**, **missing episode recovery**, or **show URLs**, a repo-only audit is not enough. Treat receipts and local inventories as secondary until the YouTube-first path has been attempted or has clearly failed.

## Mode split

Explicitly distinguish these three modes in your own reasoning and in operator-facing results when useful:

- **YouTube discovery** = what appears to exist on the live source side for the requested day, month, stream, or speaker
- **Repo audit** = what is already present locally in `raw-input`, receipts, inventories, and adjacent artifacts
- **Repair / materialization** = taking an approved or operator-pasted item and turning it into canonical `raw-input`

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

Do not blur these states together in prose. In particular:

- `already captured` means a local `raw-input` artifact already exists
- `found externally, missing locally` means the item is evidenced outside the repo but not yet present in local `raw-input`
- `materialized from operator paste` means the operator supplied the transcript body and you used that to create or strengthen the local artifact
- `discovered but unresolved` means the title/date/source shape appears real, but transcript-grade or canonical-source conditions are not yet satisfied
- `missing direct watch URL` means exactly that: you found external evidence, but not a trustworthy direct YouTube watch URL

## URL confidence rule

- If you have a **direct YouTube watch URL**, show it first.
- If you have only a **secondary listing URL** such as a podcast mirror, transcript mirror, Apple Podcasts, Art19, Podbay, Podchaser, or similar, say so plainly.
- Do **not** synthesize, infer, or guess a `youtube.com/watch?v=` URL from partial evidence.
- When a direct watch URL is missing, keep the item labeled `missing direct watch URL` until it is actually recovered.
- When `yt-dlp` or an equivalent YouTube retrieval path is available, try that direct-source recovery before closing with only secondary URLs, unless the operator explicitly asked for a repo-local or web-only answer.

## Inventory staleness rule

Treat repo inventories, `needs capture` labels, and prior receipts as useful but non-authoritative hints.

- A row marked `needs capture` may already exist in `raw-input`
- A row marked `mirrored` may still be weak, stale, or incomplete
- A missing inventory row does not prove the item never existed

Before reporting an item as missing locally, check the actual date folders and likely filename variants in `raw-input`.

Short rule:

`inventory is a hint, raw-input tree is the authority`

The maintained helper surface for quick repo-wide lookup is `codex/years/2026/raw-input/raw-input-master-index.md` with `raw-input-master-index.json` as the machine-readable companion. Use it as a fast route map, but if the index and the tree ever disagree, the dated raw-input folders win.

The companion audit surfaces are `codex/years/2026/raw-input/raw-input-index-audit.md/json`. They are heuristic architecture checks, not authority and not a hard gate.

## Index hierarchy and routing choice

After materialization, treat the routing stack this way:

- the raw-input master index is the maintained corpus-wide route map
- a speaker raw-input index is added only when it functions as a real `non-core appearance bench`
- arc files remain interpretive surfaces by default

Do not split an arc into a dedicated index surface unless the speaker-map threshold is met: the arc is no longer a practical front door, the items form a distinct retrieval domain, and the new surface would answer a different operator question than the neighboring bench or arc.

If a speaker is touched during ingest or routing, choose one of these outcomes explicitly:

- existing speaker raw-input index
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

If the operator pastes a full transcript body for a discovered item, that is sufficient to perform **local raw-input recovery** even when the direct YouTube watch URL remains unresolved.

In that situation:

- create the canonical raw-input file
- mark `transcript_type: operator_pasted_transcript`
- keep `source_type: youtube` if the appearance is clearly a YouTube stream item
- state in `source_note` that the transcript was operator-pasted and the direct watch URL is not yet recovered
- report the item as **materialized from operator paste**
- keep any unresolved YouTube URL issue separately labeled as **missing direct watch URL**

Do **not** block local transcript recovery merely because the direct watch URL is still missing, as long as the appearance identity is otherwise well anchored.

## Source-archive closeout rule

When a check-stream or one-off recovery **adds or strengthens canonical `source-archive/statecraft/` raw-input**, close the ingest loop at every still-live index layer touched by that capture.

Minimum required follow-ons:

- refresh the touched day folder `README.md`
- verify whether the capture belongs to an existing live `statecraft/civ-lens/civ-lens-<speaker>/` shelf with a `*-raw-input-index.md` provenance bench
- if such a shelf exists and the new capture is route-relevant for that speaker, update the speaker raw-input bench in the same pass before closing

Short rule:

`source-archive upload -> day index refresh -> touched speaker raw-input bench refresh -> close`

Do not assume day-index regeneration is enough. If the live speaker shelf owns a provenance bench, that bench is part of canonical ingest completion.

If the new capture materially changes the continuity story rather than only extending the bench, also tighten the minimally affected live shelf surfaces, usually:

- `*-arc.md`
- `*-routing.md`

Do this narrowly. Do not widen a simple ingest into full shelf redesign unless the operator asks.

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
- **found externally, missing locally** means the appearance is evidenced but not yet recovered in `raw-input`
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

For this skill, **transcript-bearing stream capture means YouTube-first provenance**.

- A stream item should be treated as a real transcript candidate only when you have a **direct YouTube watch URL** (`https://www.youtube.com/watch?v=...` or equivalent canonical YouTube watch link).
- Podcast mirrors, Apple/Podbay/Art19/Podscan listings, transcript mirrors, and other secondary directories may help discovery, but they do **not** by themselves qualify an item as transcript-ready.
- If only secondary episode listings are available, treat the item as **discovered but unresolved**:
  - you may report it in the check result,
  - you may create a clearly marked **scaffold/discovery placeholder**,
  - but you must **not** describe it as a completed transcript capture or canonical transcript source.
- When the operator asks for URLs, prefer the **direct YouTube watch URLs** first. Only fall back to secondary listing URLs if YouTube could not yet be recovered, and say that explicitly.

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

5. **Materialize the approved subset**
   - Use the atomic materializer as the default command path for approved YouTube URLs:
     - single URL: `python scripts/materialize_youtube_raw_input.py --url "<youtube-url>" --apply --with-appearances --purpose daily`
     - approved batch: `python scripts/materialize_youtube_raw_input.py --input <approved-urls.jsonl> --apply --with-appearances --purpose daily`
     - dry-run/probe: `python scripts/materialize_youtube_raw_input.py --url "<youtube-url>" --no-apply --run-id <label>`
   - **Do not materialize from podcast-directory URLs or transcript-mirror URLs.** For transcript-grade or transcript-bearing raw-input, the approved source must be the direct YouTube watch URL.
   - For each approved URL:
     - resolve metadata first
     - if metadata fetch fails but the operator supplied title, publication date, and lane/file metadata, let the materializer bypass metadata and try subtitle extraction from the URL's video id
     - fetch the best subtitle source available
     - preserve extraction receipts locally
     - write canonical date-folder raw-input
     - verify the written raw-input has a non-stub transcript body before reporting success
   - Review `.codex-tmp/youtube-raw-input/<run-id>/materialization-summary.md` and `capture-summary.md` before claiming capture.
   - For apply-mode runs with `--with-appearances`, expect the materializer to refresh `artifacts/host-shelf-quality/<year>/<host>/<YYYY-MM>/quality-summary.md/json` unless `--no-quality-report` was explicitly used.
   - For all apply-mode materialization runs, expect the materializer to refresh `codex/years/2026/raw-input/raw-input-master-index.md` and `raw-input-master-index.json`.
   - Close materialization/densification claims with the mandatory quality line from the capture summary: `Structure: <delta> | Purity: <delta/%> | Unresolved: <count> | Git: on-disk/verified/not-committed/not-pushed`.
   - Preserve the receipt scope: materializer host-quality closeouts are `full-host-month`, even when the capture run started from one transcript.
   - Do not treat new routeable appearances as textual purity gains unless the quality report shows transcript-grade, cleaned-transcript, or transcript-bearing improvement.
   - After every successful transcript raw-input completion, include an **item-level transcript quality receipt** in the operator-facing result. Prefer `python scripts/report_raw_input_quality.py --path <raw-input-file>`; if that helper is unavailable, use the host-shelf quality artifact or run a dry-run host-month report such as `python scripts/host_shelf_quality.py --host <host> --year <YYYY> --month <YYYY-MM>` and quote the matching artifact row. The receipt must include: raw-input path, evidence grade (`transcript-grade`, `cleaned-transcript`, `transcript-bearing`, `summary-grade`, or `legacy-appearance-only`), word count, routeable yes/no, unresolved speaker yes/no, residual noise terms, quality/provenance note, and the host-month `Structure | Purity | Unresolved | Git` closeout line.
   - Residual-noise repair loop: if the item-level receipt reports residual noise terms, inspect each occurrence before closing. Automatically patch obvious speech-to-text/proper-noun artefacts when the local context makes the intended correction clear (for example known analyst names, public figures, or recurring transcript noise such as `Zalinski` -> `Zelensky` and `Mandi` in a professor/guest context -> `Marandi`). Rerun `python scripts/report_raw_input_quality.py --path <raw-input-file>` after the patch. Close with `residual noise: none` only after the rerun confirms it; if a term is ambiguous, leave it unchanged and list it as unresolved in the receipt.
   - If a transcript body is present but metadata causes the quality classifier to return `legacy-appearance-only`, say that explicitly and do not call it transcript-valid until the metadata is normalized.
   - Legacy transcript normalization rule: when an existing raw-input file has a real transcript body plus enough provenance to identify host, title, date, and source URL, normalize metadata before closeout unless the operator asked for read-only inspection. Add `source_type`, `transcript_type`, quality/provenance notes, and an explicit transcript marker while preserving the transcript body; then rerun `report_raw_input_quality.py --path <raw-input-file>` and close with the updated receipt.
   - When the approved subset is really a guest-host tranche rather than "today's whole roster," preserve that exact tranche shape instead of reopening discovery or broad channel slicing.
   - If materialization returns `failed-fetch` or `failed-verification`, report the failure and stop before speaker routing, lattice updates, or completion claims.
   - For `failed-fetch` cases where a human will paste the transcript later, use the materializer's receipt-side `manual-curation-queue.md` and `manual-transcript-scaffolds/` outputs. Keep those scaffold files outside canonical raw-input until the paste marker is replaced and verification passes.
   - If YouTube discovery fails but secondary listings strongly suggest a same-day upload exists, report it as **missing-watch-url / unresolved**, not as transcript-captured. Recover the YouTube watch URL before claiming transcript completion.
   - If the operator has already pasted the full transcript in the current Codex thread, treat that paste as a valid transcript source and hand the item down to the YouTube transcript workflow's **operator-paste fallback**. Prefer mechanical extraction from the local Codex session log over hand-copying long chat text. Do not call the result `partial-chat-capture` merely because the paste is long or awkward to patch.
   - For full operator-paste repairs, require an exact-match receipt before closing the item: `sourceChars`, `bodyChars`, and `exactMatch=True` between the extracted session transcript and the body written after `## Transcript`.
   - After exact-match verification passes, update the check-stream receipts as captured with `capture_status: full-operator-paste`; move the item out of the open repair queue. Use `partial-chat-capture` only when the source is truly incomplete or exact extraction cannot be verified, and leave that item queued as `full-transcript-import-needed`.
   - After any successful apply-mode or operator-paste materialization into `source-archive/statecraft/`, refresh the touched day `README.md` and then refresh any already-existing live speaker `*-raw-input-index.md` bench that the new capture clearly strengthens.
   - If the bench refresh changes the shelf's practical first-open logic or current-motion story, patch the narrowest relevant live shelf files, usually `*-arc.md` and `*-routing.md`, in the same pass.

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
   - Distinguish the surface type: use **host-local arc** for one host x guest braid, **thread atlas** for recurring strands across months or hosts, and **speaker helix** for cross-host comparison of multiple host-local arcs.
   - If no clear speaker route exists, say so and stop at raw-input.
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
- when you need a computed score, repair queue, and durable receipts, run `python scripts/cognition_streams_audit.py --start YYYY-MM-DD --end YYYY-MM-DD --recent-start YYYY-MM-DD` against the active `/codex/<year>` notebook root
- when you need a derived speaker-routing queue after materialization, run `python scripts/build_speaker_routing_queue.py --start YYYY-MM-DD --end YYYY-MM-DD`; this emits advisory queue and appearance-ledger artifacts only and does not edit speaker folders
- when you need concrete speaker-memory follow-up proposals, run `python scripts/build_speaker_memory_actions.py --start YYYY-MM-DD --end YYYY-MM-DD`; this emits advisory action artifacts only and does not edit speaker folders

### Capture mode diagnosis

When the capture path is noisy, distinguish the failure layer plainly:

- **Online discovery failed:** the channel or YouTube surface was blocked, timed out, or undercounted.
- **Cached/offline audit worked:** local discovery receipts were sufficient to identify missing videos and repair queue state.
- **Exact-URL materialization worked:** a specific approved watch URL produced verified raw-input even if broad discovery was brittle.
- **Metadata-bypass materialization worked:** YouTube metadata fetch failed, but the operator-provided title/date/lane metadata let the exact URL proceed to subtitle extraction and verification.
- **Operator-paste materialization worked:** YouTube fetch or patch ergonomics failed, but a full operator-pasted transcript was mechanically extracted from the local session log, written to canonical raw-input, and exact-match verified.

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

After operator selection, report only the approved items being materialized and the resulting raw-input outcome. When materialization succeeds and a speaker route is clear, add:

```markdown
## Capture closeout
- target: <date or item> - <target_date_status or target_window_status> - <captured>/<main_total> captured - must-capture remaining: <N>
- raw-input: <path(s)>
- audit artifact: <summary/repair queue path>
- backlog: <overall_backlog_status>; probably-capture backlog remains: <yes/no>
- capture mode: <online discovery / cached offline audit / exact-URL materialization / metadata-bypass materialization / operator-paste materialization>

## Transcript quality
- raw-input: <path>
- evidence grade: <transcript-grade / cleaned-transcript / transcript-bearing / summary-grade / legacy-appearance-only>
- word count: <N>
- routeable: <yes/no>; unresolved speaker: <yes/no>
- residual noise: <none or terms>
- quality note: <source_note/editorial_note/quality_note>
- host-month closeout: Structure: <delta> routeable | Purity: <delta> transcript-valid / <pct>% (<delta pp>) | Unresolved: <N> | Git: <state>

## Speaker routing hints
- <raw-input file> -> <primary speaker route> - <next action> - <why>
- also strengthens: <speaker object / speaker arc / helix / cross-host note paths, if any>
- action queue: <memory-action-queue.md path, when generated>
```

## Steward closeout

When a check-stream repair becomes a commit candidate, keep the ship slice narrow:

- stage only raw-input files, check-stream audit artifacts, speaker-routing/action receipts, and cadence lines
- leave runtime observability, memory, handoff, host-quality background churn, and unrelated benchmark artifacts untouched unless explicitly scoped
- before suggesting push safety, report branch ahead count and any remaining untracked capture artifacts

Use "candidate" when the target does not exist yet or would require a new speaker object / speaker arc decision.

## Guardrails

- Never silently discard borderline items.
- Do not record same-day companion clips by default.
- Never auto-materialize everything by default.
- Never treat clip suspicion as certainty.
- Never silently promote subtitle-derived outputs into stronger transcript classes.
- Never claim a stream item is captured when the raw-input file is header-only, index-only, placeholder text, or otherwise fails non-stub body verification.
- Never downgrade a full operator-pasted transcript to partial just because it was supplied in chat, too long for a comfortable patch, or unavailable from YouTube. Extract it mechanically from the local session log when available, then verify exact body match.
- Never remove an item from the repair queue on operator-paste evidence unless the canonical raw-input body is non-stub and exact-match verification has passed.
- Never create or update speaker folders, speaker objects, speaker arcs, helixes, or lattice rows from the daily check unless the operator explicitly asks.
- Do not let the lattice become the first durable destination. Raw-input comes first; speaker-folder routing comes next; lattice updates are secondary pointers.
- Never continue into repair, capture, dependency, or routing work after a bounded retrieval ask has already been satisfied, unless the operator explicitly asks for the next step.

## Success condition

The operator gets a clean daily upload list for the tracked main streams, with obvious clips filtered into a secondary bucket, only the approved subset materialized into provenance-safe canonical `raw-input` that passes non-stub body verification, and clear speaker-folder routing hints for any material that strengthens an existing or candidate speaker object.


## Cursor / grace-mar instance

Grace-mar paths and commands for this repository (from `.cursor/skills/check-streams/`).

| Topic | Path |
|--------|------|
| Canonical raw-input tree | [codex/](../../codex/) |
| Date-bucket target pattern | `codex/YYYY/raw-input/YYYY-MM-DD/` |
| Existing lower-layer ingest skill | [skills-portable/youtube-raw-input-transcript/SKILL.md](../../../skills-portable/youtube-raw-input-transcript/SKILL.md) |
| Generated lower-layer Cursor skill | [\.cursor/skills/youtube-raw-input-transcript/SKILL.md](../youtube-raw-input-transcript/SKILL.md) |
| Speaker folder shelf | [codex/speakers/](../../../codex/speakers/) |
| Speaker arc boundary | [docs/skill-work/work-strategy/speaker-arc-thread-lattice-boundaries.md](../../../docs/skill-work/work-strategy/speaker-arc-thread-lattice-boundaries.md) |
| Raw-input vs speaker arc boundary | [docs/skill-work/work-strategy/raw-input-ownership-vs-speaker-arc.md](../../../docs/skill-work/work-strategy/raw-input-ownership-vs-speaker-arc.md) |
| Philosophical gloss | [docs/skill-work/work-strategy/cognition-streams-daily-aperture.md](../../../docs/skill-work/work-strategy/cognition-streams-daily-aperture.md) |
| Temp daily discovery cache | [\.codex-tmp/](../../.codex-tmp/) |
| Temp subtitle cache | [\.codex-tmp/yt-dlp/](../../.codex-tmp/yt-dlp/) |
| Portable skill manifest | [skills-portable/manifest.yaml](../../../skills-portable/manifest.yaml) |
| Sync script | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |
| Skill validator | [scripts/validate_skills.py](../../../scripts/validate_skills.py) |

**Repo notes**

- This skill is the **daily wrapper** over the single-URL YouTube transcript workflow.
- `check streams` is the canonical activation; `cognition streams` remains a legacy compatibility alias.
- After raw-input materialization, speaker folders are the durable routing layer. Lattice/cognition-streams surfaces are secondary lookup views, not the first update target.
- In v1, the fixed default watchlist is:
  - Glenn Diesen
  - Daniel Davis
  - Alexander Mercouris
  - Dialogue Works
- The operator-facing rule is:
  - `check streams` for daily roster checks
  - `cognition streams` as a legacy alias
  - `youtube transcript` for one-off URLs
- Default output class should remain conservative:
  - `auto_subtitles_vtt`
- When the operator asks for stronger cleanup later, follow the lower-layer transcript skill rather than inventing a second transcript doctrine here.

**Common local command pattern**

```powershell
python scripts/sync_portable_skills.py --skill check-streams
python scripts/sync_portable_skills.py --verify --skill check-streams
python scripts/build_speaker_routing_queue.py --start YYYY-MM-DD --end YYYY-MM-DD
python scripts/validate_skills.py
```
