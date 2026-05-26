---
name: statecraft-source-intake
preferred_activation: statecraft source intake
description: "Capture operator-supplied transcript-bearing source objects into the canonical statecraft source archive with the correct family pattern, truthful provenance, and no summary-or-stub drift."
portable: true
version: 0.1.1
tags:
  - operator
  - statecraft
  - source-archive
  - transcript
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
- `statecraft/` holds routing, continuity, synthesis, drafting, and control
- this workflow must not leak summaries, stubs, or control notes into the archive

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
   - For `Judging Freedom / Napolitano` archive captures, strip clearly separable canned sponsor/promotional reads at the opening and routine lineup/schedule promos at the close.
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

## Guardrails

- Never put routing notes, summaries, or scaffolds in the archive.
- Never create a transcript stub and call it landed.
- Never let deprecated names such as `raw-input` or `provenance` quietly reassert canonical ownership.
- Never convert a transcript-bearing source into a summary-grade note just because the transcript is messy.
- Never hide uncertainty about whether a transcript is verbatim, operator-pasted, or lightly normalized.
- For Napolitano captures, remove promo scaffolding only when the sponsor or schedule boundary is unambiguous; if ad copy is entangled with noisy ASR or substantive exchange, leave it and flag the file for later manual review.

## Success condition

The source ends as a **real full-source archive object** in the canonical statecraft source archive, filed under the right family, with honest provenance and no archive/control-plane drift.
