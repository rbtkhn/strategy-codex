---
name: civ-state-primary-text-acquisition
description: Acquire, classify, and stage CIV-STATE primary-source text through a rights-first, witness-first workflow. Use when the operator wants source records, excerpt collections, lawful full-text sidecars, or witness-locking discipline for civilization-state primary sources.
portable: true
version: 0.1.0
tags:
- operator
- statecraft
- civ-state
- primary-sources
- acquisition
portable_source: skills/civ-state-primary-text-acquisition/SKILL.md
synced_by: sync_portable_skills.py
---
# CIV-STATE Primary-Text Acquisition

Use this skill to acquire, classify, and stage CIV-STATE primary-source text without collapsing bibliography work into a bulk archive scrape.

This is a narrow **operator workflow** skill. Its job is to turn CIV-STATE source doors into:

- structured source records
- bounded excerpt collections
- lawful sidecar full-text payloads

It is not a general bibliography skill and not a bulk crawler.

## Use this skill when

- a CIV-STATE bibliography source needs a stable `source_id`
- the operator wants a source record or excerpt file
- the operator wants lawful full-text sidecar storage for a primary source
- multiple witnesses or translations exist and one canonical working witness must be locked
- the operator wants to prove retrieval depth with real text rather than title-only bibliography entries

## Do not use this skill when

- the task is PH-CIV public-manuscript authoring
- the task is broad academic bibliography building without text acquisition
- the task is bulk scraping or mass ingestion of unclear-rights texts
- the task is statecraft archive intake into `source-archive/statecraft`

## Core law

`identify the source -> classify rights -> locate the best lawful witness -> lock one canonical witness and one working translation -> acquire verbatim text lawfully -> validate -> store by class`

This skill is governed by six biases:

- rights-first
- witness-first
- manual-first
- founding-language first
- state-form and legitimacy first
- one canonical working translation, alternates noted

## Storage classes

Every source must be placed into one storage class:

- `metadata_only`
- `excerpt_only`
- `full_text_sidecar`

Default behavior:

- if rights are unclear, narrow
- if the translation is modern and restricted, narrow
- if the text is lawful and strategically useful, store it in sidecar rather than in bibliography files

## Search order

Search for a lawful text witness in this order:

1. official state, legal, treaty, ecclesial, or institutional archive
2. canonical public-domain text library
3. trusted academic or foundation-hosted edition
4. stable public transcription source
5. rights-safe scan suitable for OCR
6. manual transcription only for short bounded passages or operator-owned material

Do not settle for an arbitrary web copy when a better witness exists.

## Witness and translation rule

- Prefer the closest original-language or earliest authoritative witness when lawful and usable.
- Choose the witness that best illuminates sovereignty, law, legitimacy, continuity, rupture, and restoration.
- Lock one canonical working translation when the operator needs a target-language surface.
- Record alternate translations as metadata, not as coequal defaults.

## Excerpt rule

When the source base supports it, prefer a balanced pair:

- one legal / doctrinal / legitimacy-bearing passage
- one narrative / chronicle / literary carrier

Excerpts should be:

- short
- source-linked
- edition-aware
- rights-safe

## Workflow

1. **Fix the source identity.**
   Name the civilization, era, branch, title, author or body, and source type before any acquisition work.

2. **Create or refine the source record.**
   Give the source a stable `source_id` and fill rights, witness, and storage metadata before storing text.

3. **Classify rights early.**
   Use:
   - `public_domain`
   - `official_government_text`
   - `operator_authored_transcription`
   - `modern_translation_restricted`
   - `unclear`

4. **Search for witnesses in order.**
   Look for the strongest lawful witness rather than the fastest available copy.

5. **Lock one canonical witness.**
   Record the exact witness and, when needed, one canonical working translation.

6. **Choose storage depth.**
   - record only
   - excerpt only
   - sidecar full text

7. **Acquire conservatively.**
   Normalize encoding and obvious OCR noise only when certainty is high. Do not silently rewrite the text.

8. **Capture provenance.**
   Record witness locator, acquisition method, validation status, and any translation or rights caveat.

9. **Validate the result.**
   Check:
   - unique `source_id`
   - required fields
   - lawful storage state
   - excerpt references
   - sidecar locator integrity

## Guardrails

- Do not mirror unclear-rights modern translations by default.
- Do not blend multiple translations into one silent composite.
- Do not put bulk text into bibliography files or volume READMEs.
- Do not widen this workflow into a general archive-ingest engine.
- Do not let witness quality collapse for the sake of throughput.

## Success condition

The operator ends with a trustworthy CIV-STATE text object:

- source identity is stable
- rights status is explicit
- witness choice is explainable
- excerpting is disciplined
- full text, if stored, is lawful and linked
- the result improves retrieval rather than merely adding files


## Cursor / strategy-codex instance

**strategy-codex instance notes**

- Canonical doctrine note for this skill: [statecraft/states/primary-text-architecture.md](/C:/dev/strategy-codex/statecraft/states/primary-text-architecture.md)
- Canonical structured layers:
  - [source-records](/C:/dev/strategy-codex/statecraft/states/source-records/README.md)
  - [source-excerpts](/C:/dev/strategy-codex/statecraft/states/source-excerpts/README.md)
  - [source-sidecar](/C:/dev/strategy-codex/statecraft/states/source-sidecar/README.md)
- Current pilot records live under:
  - [statecraft/states/source-records/pilot](/C:/dev/strategy-codex/statecraft/states/source-records/pilot)

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill civ-state-primary-text-acquisition
python scripts/sync_portable_skills.py --verify --skill civ-state-primary-text-acquisition
python scripts/validate_skills.py
```
