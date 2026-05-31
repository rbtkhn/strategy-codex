# Primary-Text Architecture

WORK only; not Record.

This note defines the CIV-STATE primary-text architecture that sits beneath bibliography source doors and above any future large-scale archival program.

Its purpose is to convert a curated bibliography into a deeper working source substrate without turning the main repo into a bulk text dump.

The governing law is:

`identify the source -> classify rights -> locate the best lawful witness -> lock one canonical witness and one working translation -> acquire verbatim text lawfully -> validate -> store by class`

## Why Full-Text Availability Matters

Full-text availability is not an archival luxury. It is a strategic amplifier for CIV-STATE quality.

It improves:

- retrieval depth
- excerpt construction
- quotation discipline
- counterweight discovery
- translation and edition awareness
- cross-civilizational comparison
- downstream drafting speed once the substrate exists

Without full text, a bibliography remains a map. With lawful full-text availability, the shelf becomes a working memory surface.

## Three-Layer Source Law

The primary-text layer has three storage depths:

1. **Source record**
   - canonical source identity
   - witness, translation, rights, and provenance metadata
2. **Bounded excerpt**
   - short, load-bearing passages tied to `source_id`
   - rights-safe and edition-aware
3. **Sidecar full text**
   - lawful verbatim body keyed by `source_id`
   - used only for `public_domain`, `official_government_text`, `operator_authored_transcription`, or similarly safe classes

These layers support three storage outcomes:

- `metadata_only`
- `excerpt_only`
- `full_text_sidecar`

## Human-Facing Hierarchy

This architecture does not replace the current CIV-STATE reading apparatus.

- `README` = volume front door
- `shelf-reader` = traversal guide
- `bibliography` = era index plus bounded supports
- `primary-sources` = curated source doors
- `source records / excerpts / sidecar full text` = deeper evidence substrate

Bibliography files should remain readable. They should point toward deeper text support rather than absorb it.

## Acquisition Bias

Default acquisition posture:

- **rights-first**
- **witness-first**
- **manual-first**
- **founding-language first**
- **state-form and legitimacy first**
- **one canonical working translation, alternates noted**

This means:

- do not store text before rights are classified
- do not accept an arbitrary web copy as a text witness
- do not merge multiple translations into one silent composite
- do not optimize first for backfill speed if that weakens witness quality

## Search Order

When acquiring verbatim text, search in this order:

1. official state, legal, treaty, ecclesial, or institutional archive
2. canonical public-domain text library
3. trusted academic or foundation-hosted edition
4. stable public transcription source
5. rights-safe scan suitable for OCR
6. manual transcription only for short bounded passages or operator-owned material

The system is looking for a lawful **text witness**, not merely any available text.

## Excerpt Rule

When the source base supports it, the excerpt layer should prefer a **balanced pair**:

- one legal / doctrinal / legitimacy-bearing passage
- one narrative / chronicle / literary carrier

This keeps law and memory in tension rather than flattening the shelf into one genre.

## Sidecar Rule

The sidecar archive is keyed by `source_id`.

It should:

- keep full texts outside bibliography and volume files
- remain file-backed and deterministic
- preserve provenance and validation state
- support later passage search and excerpt regeneration

Do not overengineer a database in the first pass.

## Companion Surfaces

- [Hybrid References](hybrid-references.md)
- [Source Retrieval Matrix](indexes/source-retrieval-matrix.md)
- [CIV-STATE Volumes](volumes/README.md)
- [Source Records README](source-records/README.md)
- [Source Excerpts README](source-excerpts/README.md)
- [Source Sidecar README](source-sidecar/README.md)
