---
name: statecraft-source-intake
preferred_activation: statecraft source intake
description: "Capture an operator-supplied transcript-bearing source object into the canonical statecraft source archive with the correct family pattern, truthful provenance, and no summary-or-stub drift. Supports single-source intake and repeated same-day batch intake, including the operator phrases `statecraft daily intake` and `statecraft daily intake / source-archive first`. Do not use for direct YouTube metadata/caption fetch, month inventory work, or downstream synthesis."
portable: true
version: 0.3.0
tags:
  - operator
  - statecraft
  - source-archive
  - transcript
---

# Statecraft source intake

**Preferred activation (operator):** say **`statecraft source intake`**.

Also support the source-first batch phrases:

- **`statecraft daily intake`**
- **`statecraft daily intake / source-archive first`**

Use this skill when the operator already has a transcript-bearing source object in hand, usually a pasted YouTube transcript, and wants it landed into the canonical statecraft source archive with the right family pattern.

This skill is for **source-truth intake**, not for helix drafting, speaker synthesis, transcript cleanup, or broad month auditing. Its job is to create the correct full-source object honestly and consistently.

## Use this skill when

- the operator pasted a full transcript into chat
- the operator is uploading several same-day transcripts as a batch
- a source capture should be filed under the statecraft source archive immediately
- the main uncertainty is **which family / filename / frontmatter pattern** to use
- the source is transcript-bearing and should become a real archive object, not a stub

## Do not use this skill when

- the task is to fetch captions or metadata directly from YouTube tooling first
- the task is to clean a captured transcript into study-grade derivative form
- the task is to route, summarize, interpret, or synthesize the source in `statecraft/`
- the source belongs to another source-archive namespace rather than the statecraft source archive

If the operator wants a daily report after the archive batch is real, stop this skill and route to `statecraft daily synthesis`.

## Core law

- root `archive/` is for preserved legacy or frozen holdings; it is not the live intake lane
- `source-archive/` holds the full source object
- `/codex` holds chronology and continuity beneath statecraft
- `civilization_memory` is the evidence layer for longer civilizational/source-memory arguments
- `civ-state` is the operator-facing source base for statecraft interpretation
- lane and transaction surfaces are the downstream drafting layer
- `statecraft/` holds routing, notes, essays, synthesis, drafting, and control
- this workflow must not leak summaries, stubs, or control notes into `source-archive/`

## Layer boundary

This skill is for source-truth intake only.

- It does **not** draft CIV-STATE doctrine.
- It does **not** let `source-archive/` captures silently become operator truth.
- It does **not** collapse source intake into lane synthesis or civilization-state argument.

If the operator's next move is interpretation, route from the landed source object into `/codex`, `civ-state`, or the relevant lane-local `statecraft/` surfaces rather than continuing to treat the source file as the working doctrine surface.

## Batch law

When the operator is doing same-day transcript intake, treat the workflow as a **bounded source-archive batch**:

- keep each transcript as its own canonical source object
- reuse the same touched day folder
- choose explicitly between immediate rebuild and deferred rebuild
- refresh the smallest still-live archive indices after each landed file or at the end of the same bounded batch
- keep synthesis downstream; do not write the daily report into `source-archive/`

### Operating modes

Use one of these two modes on purpose rather than drifting between them.

#### 1. Single-source safe mode

Use when:

- the operator supplied one source and did not imply throughput pressure
- the archive surfaces should stay live after each intake
- the operator wants the usual full closeout for one object

In this mode:

- land the file
- rebuild the smallest touched archive surfaces immediately
- verify the landed file plus touched rollups
- close with the refreshed-surface summary

Short rule:

`land -> rebuild -> verify -> close`

#### 2. Batch-throughput mode

Use when:

- the operator is clearly sending a same-day batch
- multiple transcript URLs or transcript pastes are arriving in sequence
- rebuild-after-every-file would create avoidable overhead
- the operator explicitly asks for higher-efficiency or batch behavior

In this mode:

- land each file immediately
- do a lightweight per-file verification only
- defer day/month/navigation rebuilds until a batch checkpoint
- run one bounded rebuild and verification pass for the whole still-live batch

Short rule:

`land -> header-check -> queue for checkpoint`

#### Batch checkpoint triggers

In batch-throughput mode, rebuild when one of these becomes true:

- the operator explicitly asks for a checkpoint, rebuild, verify, or closeout
- the batch appears to pause or end
- enough same-day files have accumulated that continuing without a rebuild becomes awkward
- you need the day/month/navigation surfaces live before the next step

## Workflow

1. **Confirm the object is source-bearing**
   - Make sure the operator supplied a real transcript body, not just a title, URL, or excerpt.
   - If the source is partial, say so clearly and avoid pretending the capture is complete.
   - In batch mode, keep the current day folder and already-landed sibling captures in mind before naming the new object.

2. **Resolve the archive family before writing**
   - Identify the host / show / guest / recurring thread ownership.
   - Reuse the existing family pattern rather than inventing a fresh one.
   - Distinguish **full interview / parent episode** from **highlight clip / companion clip** before naming anything.
   - Typical family questions:
     - Is this `Dialogue Works / Nima`?
     - Is this `Judging Freedom / Napolitano`?
     - Is this `Glenn Diesen`?
     - Is this a **solo Mercouris channel upload**?
     - Is this `The Duran / Mercouris`?
     - Is this a recurring guest-owned lane on an outside host?
     - Is this a real full-source Tucker / Carlson interview, or only a clipped excerpt from one?

3. **Choose the correct canonical object shape**
   - Preserve the full transcript-bearing body.
   - Use honest provenance such as:
     - operator-pasted transcript
     - cleaned transcript pasted by operator
     - transcript-bearing source capture
   - Do not silently promote a rough paste into human-verified verbatim.
   - Keep **front-door completeness** separate from **transcript reality**:
     - a real full transcript may still have an unresolved direct watch surface
     - if so, preserve that seam explicitly in `source_note` rather than flattening it away

4. **Place it in the canonical archive**
   - Use the published date as the archive date unless the operator explicitly gives a different authoritative date.
   - Write into the canonical statecraft archive day folder.
   - Keep filenames and frontmatter aligned with neighboring family examples.
   - When publication date comes from a trustworthy secondary surface because the direct watch URL is still missing, use that date but say so plainly in `source_note`.
   - For Duran podcast-style Mercouris objects whose transcript body does not carry a spoken date, prefer a trustworthy external podcast mirror date over guesswork and preserve that dating seam explicitly in `source_note`.

5. **Normalize lightly**
   - Fix obvious spacing, formatting, and title/date typos when confidence is high.
   - Strip obvious pasted wrapper residue such as leading `Transcripts:` lines or duplicated title wrappers when the boundary is unmistakable.
   - Reflow into readable paragraphs or turns when the family pattern expects that.
   - Preserve full transcript body for solo `Alexander Mercouris` captures unless the operator explicitly asks for trimming.
   - For `Judging Freedom / Napolitano` archive captures, strip clearly separable ideological cold opens or canned sponsor/promotional reads at the opening and routine lineup/schedule promos at the close.
   - Do not over-clean, summarize, or rewrite the substance.

6. **Verify the result at the right depth**
   - Always check frontmatter or metadata block against the family pattern.
   - Always check opening lines and archive placement.
   - Always confirm the file is a real transcript-bearing object, not a shell.
   - In `single-source safe mode`, also verify the rebuilt archive surfaces.
   - In `batch-throughput mode`, stop after the lightweight per-file verification and queue the rollup verification for the checkpoint pass.

7. **Close out conservatively**
   - Report the landed file path.
   - State the family shape used.
   - State whether tests were run.
   - In `batch-throughput mode`, say plainly that rebuild and verification of day/month/navigation surfaces is deferred to the next checkpoint.
   - State whether the intake batch remains uncommitted if that is still true.

8. **Refresh the smallest still-live archive surfaces**
   - In `single-source safe mode`, refresh the touched day-folder `README.md` immediately.
   - In `single-source safe mode`, refresh the touched month index and archive navigation when the new source changes those rollups.
   - In `batch-throughput mode`, defer these refreshes until the batch checkpoint.
   - Keep the rebuild bounded to the touched day/month/navigation surfaces rather than drifting into downstream synthesis.

9. **Clean transient residue**
   - Remove obvious scratch residue created by intake work, such as temporary transcript body files, before final verification.
   - Do not leave `.tmpbody` or similar helper artifacts in the canonical archive tree.

## Verification and closeout

Use a simple Windows-safe verification sequence matched to the active mode.

- Prefer small single-target `rg` checks over large multi-path quoted PowerShell commands.
- Prefer verifying one surface at a time when using PowerShell.
- `Per-file verification`:
  - confirm the new archive file exists and contains `source_url` or `youtube_id`
  - confirm the header/frontmatter matches the chosen family pattern
  - confirm the file is not a shell or partial write
- `Checkpoint verification`:
  - confirm the target day `README.md` includes the filename after rebuild
  - confirm the touched month/year/navigation surfaces reflect the new file when those surfaces were part of the rebuild
  - confirm the required host bench and/or speaker bench entry exists when that lane expects one
- Archive intake is not complete until the required downstream routing surfaces are updated when the lane calls for them.

Default closeout law:

- report the landed archive file
- state the family pattern used
- state which archive indices were refreshed
- in batch-throughput mode, state that the current file is queued inside the still-open batch checkpoint
- do not silently drift into lane or civ-lens synthesis

## Partial front-door doctrine

When the operator provides a full transcript but the exact direct watch URL is still missing, the archive may still accept the object if identity is well anchored.

Minimum anchor set:

- full transcript body
- stable host/show identity
- stable episode title
- trustworthy publication date from direct metadata or a trustworthy secondary listing

In that situation:

- land the archive object
- keep provenance explicit
- preserve the unresolved front-door seam in `source_note`
- do not guess or synthesize a `youtube.com/watch?v=` URL

Preferred metadata rule:

- if the object is clearly a known YouTube host-family episode and only the exact watch URL is missing, it is acceptable to keep the host-family context while stating that the direct watch URL was not recovered
- if the only actually confirmed source surface is a podcast or mirror page, prefer the truthful confirmed `source_url` over an inferred YouTube front door

Short rule:

`real transcript + anchored identity + unresolved direct URL -> archive yes, fiction no`

## Clip discipline

Do not let a clipped object quietly replace the real interview.

- If the supplied object is clearly a short highlight clip, excerpt, or same-day companion segment cut from a longer parent episode, do **not** file it as the canonical archive object by default.
- Prefer the full parent interview or full parent monologue when it exists or is clearly the true source event.
- If only the clip is currently recoverable, keep it outside canonical statecraft archive intake unless the operator explicitly asks to preserve that clip as its own object.
- If uncertainty remains, say so plainly and avoid pretending the clip is the whole interview.

Short rule:

`parent interview first, clip only by explicit operator override`

## Family-resolution heuristics

- Prefer the **existing neighboring file family** over abstract perfection.
- If the same host family already exists for the same month or day, match it.
- Keep host/show context explicit even when the recurring expert thread owns the capture.
- If there are multiple near-families, choose the one that best matches how the archive is already being used now, not how an older deprecated path used to behave.

## Family disambiguation

### Mercouris split

- Use `youtube-alex-mercouris-*` for **solo Alexander Mercouris channel monologues** published on the Mercouris YouTube channel.
- Use `transcript-duran-mercouris-*` for **The Duran discussion/interview format** where the archive already treats the object as a Duran-side transcript family.
- If both families exist nearby, let the **channel/show identity** decide:
  - solo channel voiceover / monologue -> `youtube-alex-mercouris-*`
  - Duran conversational frame -> `transcript-duran-mercouris-*`
- If the title looks like a Duran podcast episode and the transcript opens with Christoforou prompting Mercouris, do not file it under the solo Mercouris family even when the operator discovered it during a Mercouris month pass.
- For Duran podcast dating, if the transcript body has no spoken date:
  - use a trustworthy external episode listing such as Apple Podcasts, Podchaser, Goodpods, or another stable podcast mirror
  - preserve that provenance explicitly in `source_note`
  - do not imply the date came from the spoken transcript itself

### Napolitano / Judging Freedom

- Keep the substantive interview transcript.
- Strip the recurring ideological cold open when it is a clearly separable pre-interview boilerplate block.
- Strip canned sponsor reads at the opening only when the boundary is unmistakable.
- Strip routine schedule tails such as "coming up later today" or "if you're watching us live" only when clearly separable.
- If ad copy or show promo is entangled with noisy ASR or substantive exchange, leave it in place and flag it for later manual review.

### Nima / Dialogue Works

- Prefer the existing `transcript-alkorshid-*` family when the object belongs to Nima Alkorshid / Dialogue Works.
- Resolve by host/show identity first, not by guest fame or topic overlap.

### Glenn Diesen

- Preserve the Diesen-side naming cues that often include the guest surname set in the filename.
- When multiple major guests appear, prefer the established neighboring Diesen naming pattern instead of inventing a new compact scheme.
- If a Glenn Diesen transcript is real but the direct YouTube watch URL is still missing, do not block archive intake on that basis alone. Use the best trustworthy dated surface available, keep `show`/`host`/`thread` stable, and make the unresolved watch-surface seam explicit in `source_note`.

### Tucker Carlson / outside-host support lanes

- Treat Tucker captures as real archive objects when the operator has supplied a full transcript-bearing interview or a clearly anchored full-source mirror.
- Keep the host/show context explicit:
  - `show: Tucker Carlson`
  - `host: Tucker Carlson`
  - recurring guest ownership can still appear in filename or downstream shelf routing when the repo already uses that pattern
- If the direct watch URL is unresolved but a trustworthy transcript mirror and publication date are available, land the object honestly rather than over-claiming a recovered watch surface.
- Do not confuse a Tucker clip, teaser, or excerpt with the full interview; if the object is clipped, fall back to the clip-discipline rule above.

### Daniel Davis Deep Dive

- Use `youtube-daniel-davis-deep-dive-*` for standard Daniel Davis Deep Dive YouTube captures unless a different neighboring family clearly governs the object.
- Default metadata for this lane:
  - `show: Daniel Davis Deep Dive`
  - `host: Daniel Davis`
  - `thread: davis`
- Preserve the full transcript body by default.
- Do not assume the guest field is globally standardized across the whole Daniel Davis lane; verify against neighboring files before normalizing titles, rank prefixes, or first-name variants.
- Strip only clearly separable routine closing promos such as "coming up next" or "just a few minutes from now" when they are non-substantive show-lineup tails.
- If the closing setup contains substantive transition context or is entangled with the interview close, leave it in place.

### Guest normalization

- Normalize unstable ASR guest spellings to the established archive form when confidence is high.
- Keep guest normalization narrow and evidence-backed; do not promote a lane-wide normalization rule from one fresh example.
- For Seyed Marandi appearances in the Daniel Davis lane, prefer `guest: Seyed M. Marandi` even when the pasted transcript varies across forms such as `say Mandi`, `Seyed Marandi`, or `Seyed Morandi`.

## Guardrails

- Never put routing notes, summaries, or scaffolds in the archive.
- Never create a transcript stub and call it landed.
- Never let deprecated names such as `raw-input` or `provenance` quietly reassert canonical ownership.
- Never convert a transcript-bearing source into a summary-grade note just because the transcript is messy.
- Never hide uncertainty about whether a transcript is verbatim, operator-pasted, or lightly normalized.
- Never treat a highlight clip as the canonical full interview unless the operator explicitly wants the clip preserved as its own object.
- Never write the daily synthesis report into `source-archive/statecraft/`; that belongs in `statecraft/`.
- For Napolitano captures, remove cold-open or promo scaffolding only when the ideological, sponsor, or schedule boundary is unambiguous; if it is entangled with noisy ASR or substantive exchange, leave it and flag the file for later manual review.

## Success condition

The source ends as a **real full-source archive object** in the canonical statecraft source archive, filed under the right family, with honest provenance and no archive/control-plane drift.
