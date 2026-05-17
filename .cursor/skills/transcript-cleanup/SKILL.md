---
name: transcript-cleanup
preferred_activation: transcript cleanup
description: Clean verified transcript-bearing raw-input into study-ready derivative transcripts with a visible cleaned-80 rubric, conservative proper-noun normalization, preserved source provenance, and cleanup receipts.
portable: true
version: 0.1.0
tags:
- transcript
- raw-input
- quality
- cleanup
portable_source: skills-portable/transcript-cleanup/SKILL.md
synced_by: sync_portable_skills.py
---
# Transcript cleanup

**Preferred activation:** say **`transcript cleanup`** or ask to bring transcript quality to cleaned-80.

Use this skill after raw-input capture has succeeded and the transcript body is verified non-stub, but the subtitle text still needs study-grade cleanup.

## Contract

- Preserve the source raw-input file unchanged.
- Write cleaned derivatives beside the source file using `*.cleaned.md`.
- Treat `cleaned-transcript-80` as study-ready, not human-verified verbatim.
- Do not compare against audio/video in v1.
- Use known-glossary-only proper-noun corrections; do not invent names or silently rewrite uncertain terms.

## Workflow

1. **Select verified sources**
   - Start from exact raw-input paths or a raw-input list.
   - Confirm each source has `source_url`, `pub_date`, `title`, transcript type, provenance note, and a non-stub body.
   - Reject placeholder shells and index-only files.

2. **Run the cleaner**
   - Single file:
     - `python scripts/clean_raw_input_transcript.py --raw-input <path> --apply`
   - Batch:
     - `python scripts/clean_raw_input_transcript.py --raw-input-list <file> --apply --batch-label <label>`
   - Dry-run is the default. Use `--apply` only when the operator wants derivative files and receipts written.

3. **Clean conservatively**
   - Remove caption wrapper artifacts such as `Kind: captions`, `Language: en`, timestamps, and VTT markers.
   - Collapse repeated consecutive fragments.
   - Reflow subtitle line breaks into study-readable paragraphs.
   - Apply only known glossary corrections from the script.
   - Treat declared guest names from frontmatter/title as required narrow glossary checks. If a known guest name is still misspelled in the body, the transcript must not receive a perfect score.
   - Preserve speaker-turn markers when already present; add no forced labels when unclear.

4. **Score visibly**
   - Use the weighted 0-100 rubric from the receipt:
     - frontmatter integrity
     - provenance integrity
     - caption artifact removal
     - repeated-fragment collapse
     - paragraph reflow
     - proper-noun normalization
     - speaker turns where clear
     - residual-noise scan
   - Score `>= 80` becomes `cleanup_grade: cleaned-transcript-80`.
   - Score `< 80` remains `cleanup_grade: transcript-grade-cleaned-draft`.

5. **Preserve provenance**
   - Cleaned frontmatter must include:
     - `source_raw_input`
     - `source_url`
     - `pub_date`
     - `title`
     - `cleanup_score`
     - `cleanup_grade`
     - `cleanup_receipt`
     - `cleanup_method: machine-assisted-caption-cleanup`
     - `human_review: spot-check`
     - `audio_verified: false`
     - `proper_noun_policy: known-glossary-only`
   - Use `evidence_grade: cleaned-transcript` only when the cleanup grade is `cleaned-transcript-80`.

## Closeout

Always report:

- cleaned derivatives written
- cleanup score and grade per file
- receipt paths
- high-confidence corrections made
- residual noise left in place
- whether source raw-input files were unchanged

## Guardrails

- Never overwrite the source raw-input.
- Never mark a cleaned derivative as human-verified.
- Never use broad model judgment for names in v1.
- Never give a perfect score while a declared speaker/guest name remains misspelled in the cleaned body.
- Never give a perfect score when source metadata has a known provenance conflict, such as `caption_kind` disagreeing with `source_note` or `guest` merely repeating the host name.
- Never treat cleaned-80 as quotation-ready without separate verification.
- Never edit Record surfaces from this workflow.


## Cursor / grace-mar instance

_(appendix missing: .cursor/skills/transcript-cleanup/CURSOR_APPENDIX.md)_
