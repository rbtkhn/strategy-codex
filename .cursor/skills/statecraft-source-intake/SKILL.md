---
name: "statecraft-source-intake"
preferred_activation: "statecraft source intake"
description: "Capture operator-supplied transcript-bearing source objects into the canonical statecraft source archive with the correct family pattern, truthful provenance, and no summary-or-stub drift."
portable: true
version: "0.1.4"
tags:
  - "operator"
  - "statecraft"
  - "source-archive"
  - "transcript"
portable_source: "skills-portable/statecraft-source-intake/SKILL.md"
synced_by: "sync_portable_skills.py"
---
# Statecraft source intake

**Preferred activation (operator):** say **`statecraft source intake`**.

Use this skill when the operator already has a transcript-bearing source object in hand, usually a pasted YouTube transcript, and wants it landed into the canonical statecraft source archive with the right family pattern.

This skill is for **archive intake**, not for helix drafting, speaker synthesis, or transcript cleanup. Its job is to create the correct full-source object honestly and consistently.

## Use this skill when

- the operator pasted a full transcript into chat
- a source capture should be filed under the statecraft archive immediately
- the main uncertainty is **which family / filename / frontmatter pattern** to use
- the source is transcript-bearing and should become a real archive object, not a stub

## Do not use this skill when

- the task is to fetch captions or metadata directly from YouTube tooling first
- the task is to clean a captured transcript into study-grade derivative form
- the task is to route, summarize, interpret, or synthesize the source in `statecraft/`
- the source belongs to another archive namespace rather than the statecraft archive

## Core law

- `source-archive` holds the full source object
- `civilization_memory` is the evidence layer for longer civilizational/source-memory arguments
- `civ-emp` is the operator-facing source base for statecraft interpretation
- lane and transaction surfaces are the downstream drafting layer
- `statecraft/` holds routing, continuity, synthesis, drafting, and control
- this workflow must not leak summaries, stubs, or control notes into the archive

## Layer boundary

This skill is for archive intake only.

- It does **not** draft CIV-EMP doctrine.
- It does **not** let source-archive captures silently become operator truth.
- It does **not** collapse archive intake into lane synthesis or civilization-state argument.

If the operator's next move is interpretation, route from the landed archive object into `civ-emp` or the relevant lane-local surfaces rather than continuing to treat the archive file as the working doctrine surface.

## Workflow

1. **Confirm the object is source-bearing**
   - Make sure the operator supplied a real transcript body, not just a title, URL, or excerpt.
   - If the source is partial, say so clearly and avoid pretending the capture is complete.

2. **Resolve the archive family before writing**
   - Identify the host / show / guest / recurring thread ownership.
   - Reuse the existing family pattern rather than inventing a fresh one.
   - Typical family questions:
     - Is this `Dialogue Works / Nima`?
     - Is this `Judging Freedom / Napolitano`?
     - Is this `Glenn Diesen`?
     - Is this a **solo Mercouris channel upload**?
     - Is this `The Duran / Mercouris`?
     - Is this a recurring guest-owned lane on an outside host?

3. **Choose the correct canonical object shape**
   - Preserve the full transcript-bearing body.
   - Use honest provenance such as:
     - operator-pasted transcript
     - cleaned transcript pasted by operator
     - transcript-bearing source capture
   - Do not silently promote a rough paste into human-verified verbatim.

4. **Place it in the canonical archive**
   - Use the published date as the archive date unless the operator explicitly gives a different authoritative date.
   - Write into the canonical statecraft archive day folder.
   - Keep filenames and frontmatter aligned with neighboring family examples.

5. **Normalize lightly**
   - Fix obvious spacing, formatting, and title/date typos when confidence is high.
   - Reflow into readable paragraphs or turns when the family pattern expects that.
   - Preserve full transcript body for solo `Alexander Mercouris` captures unless the operator explicitly asks for trimming.
   - For `Judging Freedom / Napolitano` archive captures, strip clearly separable ideological cold opens or canned sponsor/promotional reads at the opening and routine lineup/schedule promos at the close.
   - Do not over-clean, summarize, or rewrite the substance.

6. **Verify the result**
   - Check frontmatter or metadata block against the family pattern.
   - Check opening lines and archive placement.
   - Confirm the file is a real transcript-bearing object, not a shell.

7. **Close out conservatively**
   - Report the landed file path.
   - State the family shape used.
   - State whether tests were run.
   - State whether the intake batch remains uncommitted if that is still true.

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
- For Napolitano captures, remove cold-open or promo scaffolding only when the ideological, sponsor, or schedule boundary is unambiguous; if it is entangled with noisy ASR or substantive exchange, leave it and flag the file for later manual review.

## Success condition

The source ends as a **real full-source archive object** in the canonical statecraft source archive, filed under the right family, with honest provenance and no archive/control-plane drift.


## Cursor / grace-mar instance

**strategy-codex instance notes**

- Canonical archive root for this skill: [source-archive/statecraft](/C:/dev/strategy-codex/source-archive/statecraft)
- Deprecated compatibility surfaces that must **not** receive new captures:
  - [codex/years/2026/raw-input](/C:/dev/strategy-codex/codex/years/2026/raw-input)
  - [codex/years/2026/provenance](/C:/dev/strategy-codex/codex/years/2026/provenance)
- Primary neighboring families this skill should check before writing:
  - `Dialogue Works / Nima`
  - `Judging Freedom / Napolitano`
  - `Glenn Diesen`
  - `The Duran / Mercouris`

**Current live examples**

- Nima / Dialogue Works:
  - [source-archive/statecraft/2026-05-26/transcript-alkorshid-marandi-iran-opens-fire-on-american-fighter-jets-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/transcript-alkorshid-marandi-iran-opens-fire-on-american-fighter-jets-2026-05-26.md)
- Napolitano / Judging Freedom:
  - [source-archive/statecraft/2026-05-26/transcript-napolitano-freeman-israel-humiliates-itself-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/transcript-napolitano-freeman-israel-humiliates-itself-2026-05-26.md)
  - [source-archive/statecraft/2026-05-26/transcript-napolitano-mearsheimer-neocons-want-more-war-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/transcript-napolitano-mearsheimer-neocons-want-more-war-2026-05-26.md)
  - [source-archive/statecraft/2026-05-26/transcript-napolitano-crooke-fear-as-a-deterrent-to-war-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/transcript-napolitano-crooke-fear-as-a-deterrent-to-war-2026-05-26.md)
- Glenn Diesen:
  - [source-archive/statecraft/2026-05-26/youtube-glenn-diesen-lawrence-wilkerson-failing-to-adjust-to-a-multipolar-world-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/youtube-glenn-diesen-lawrence-wilkerson-failing-to-adjust-to-a-multipolar-world-2026-05-26.md)
- The Duran / Mercouris:
  - [source-archive/statecraft/2026-05-26/transcript-duran-mercouris-pressure-to-walk-away-from-a-good-iran-deal-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/transcript-duran-mercouris-pressure-to-walk-away-from-a-good-iran-deal-2026-05-26.md)

**Repo notes**

- `statecraft/` is downstream interpretation and control, not archive storage.
- For manual file creation or edits, use `apply_patch`.
- Prefer the closest same-family recent file as the pattern authority.
- When a transcript is already supplied in chat, this skill can proceed without YouTube fetching.

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill statecraft-source-intake
python scripts/sync_portable_skills.py --verify --skill statecraft-source-intake
python scripts/validate_skills.py
```
