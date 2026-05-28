---
name: transcript-proper-noun-normalization
preferred_activation: proper noun normalization
description: "Normalize proper nouns and obvious ASR substitutions inside an already-landed transcript-bearing raw-input while preserving provenance, uncertainty, and argument structure. Use for noisy YouTube or operator-pasted transcripts whose names, places, institutions, weapons, or recurring corpus terms are mangled but whose overall body should otherwise stay intact. Do not use for first-pass capture, broad prose cleanup, or synthesis."
portable: true
version: 0.1.0
tags:
  - transcript
  - raw-input
  - quality
  - cleanup
---

# Transcript proper-noun normalization

**Preferred activation:** say **`proper noun normalization`** or ask to clean names/proper nouns in a noisy transcript.

Use this skill when a transcript-bearing raw-input is usable for routing but too noisy for shelf/search use because names, places, institutions, weapons, or recurring terms are mangled by ASR or copy/paste artifacts.

## Contract

Normalize only what is mechanically recoverable from context:

- people, offices, institutions, countries, cities, regions
- weapons, military systems, abbreviations, organizations
- repeated corpus terms and stable host/speaker names
- obvious ASR substitutions that harm search or meaning

Do **not** rewrite the argument, summarize, improve style, smooth all grammar, remove uncertainty, or make the transcript look human-verified.

## Workflow

1. **Read provenance first**
   - Check frontmatter: `kind`, `source_type`, `transcript_type`, `source_note`, `editorial_note`, `host`, `guest`, `thread`.
   - Confirm this is a transcript cleanup task, not a Record merge or interpretive notebook edit.

2. **Build a correction set**
   - Scan for suspicious capitalized words, repeated phonetic variants, one-letter leader names, garbled acronyms, and malformed place names.
   - Prefer corrections already stable in the repo's speaker objects, host shelves, raw-input corpus, or obvious title/source context.
   - Use search for local precedent before correcting ambiguous expert names or locations.

3. **Apply conservative edits**
   - Replace high-confidence forms throughout the transcript.
   - Fix repeated ASR artifacts only when they are clearly mechanical, such as `zero someum` -> `zero-sum`.
   - Leave uncertain terms unchanged or mark them in an editorial note; do not guess silently.

4. **Update provenance**
   - If the pass materially cleans proper nouns, set `kind: cleaned-transcript` only when the file is still a full transcript body and the cleanup is documented.
   - If the transcript remains noisy, keep `kind: transcript`, set an explicit `source_type` / `transcript_type`, and add `normalization_state` or `quality_note` rather than upgrading the grade.
   - Use a transcript type such as `ai_assisted_operator_pasted_youtube_transcript` or another explicit source-specific form.
   - Add or update `source_note` / `editorial_note` to say: AI-assisted proper-noun cleanup; not human-verified verbatim; verify load-bearing claims before quotation.
   - Never upgrade to `transcript-grade` from this skill.

5. **Verify**
   - Re-scan for the known bad forms from the correction set.
   - Report any remaining high-salience residual noisy forms; leaving them visible is better than guessing.
   - Run the repository's transcript/materialization validator when available.
   - Refresh quality/appearance receipts if the transcript participates in host-shelf quality reporting.

## Quality States

- **Before:** usually `transcript-bearing but noisy`.
- **After:** may be `cleaned-transcript` if proper nouns and obvious mechanical substitutions are substantially normalized.
- **Never:** `transcript-grade`, unless a separate human/source-verbatim process proves it.

## Closeout

Always report:

- before grade -> after grade
- whether the evidence grade changed separately from whether text was corrected
- high-confidence corrections made
- unresolved or uncertain terms left in place
- whether validation/quality receipts were refreshed
- git durability state: on disk / verified / not committed / not pushed

## Starting Lexicon

Use as examples, not as an exhaustive script:

- `C`, `Cining`, `Sining`, `Cinping` -> `Xi Jinping` / `Xi`
- `Tajjikistan` -> `Tajikistan`
- `Jai Shanka` -> `Jaishankar`
- `Lavro` -> `Lavrov`
- `Shooyu` -> `Shoigu`
- `Zalinski`, `Zilinski` -> `Zelensky`
- `Yermach` -> `Yermak`
- `Naboo` -> `NABU`
- `Kaakalis` -> `Kaja Kallas`
- `Hin Matal` -> `Rheinmetall`
- `TAD` -> `THAAD`
- `tourist missiles` -> `Taurus missiles`
- `chassis missiles` -> `JASSM missiles`
- `sea of Azorov` -> `Sea of Azov`
- `Zaporosia`, `Zaporia`, `Zaporoia` -> `Zaporizhzhia`
- `Neper` -> `Dnieper`
- `Nepro` -> `Dnipro`
- `Adessa` -> `Odesa`
- `Chasufiar`, `Chasfyar`, `Chas of Yar` -> `Chasiv Yar`
- `Kataussk`, `Katausk`, `Katossk` -> `Kramatorsk`
- `Dujifka`, `Dujiffka` -> `Druzhkivka`
