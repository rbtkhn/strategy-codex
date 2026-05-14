---
name: youtube-raw-input-transcript
preferred_activation: youtube transcript
description: Extract YouTube metadata and captions, then materialize a canonical raw-input transcript with conservative provenance, speaker normalization, and date-safe frontmatter.
portable: true
version: 0.1.0
tags:
- operator
- raw-input
- youtube
- transcript
portable_source: skills-portable/youtube-raw-input-transcript/SKILL.md
synced_by: sync_portable_skills.py
---
# YouTube raw-input transcript

**Preferred activation (operator):** say **`youtube transcript`**.

Use this skill when a YouTube episode should become a canonical transcript artifact, especially when there is no human-cleaned transcript yet and the best available source is YouTube captions.

## Layering rule

- Use **`youtube transcript`** when the operator already has a specific URL or episode in hand.
- Do **not** use this as the first move for the four-stream daily roster check.
- When the task is "what did Diesen, Davis, Mercouris, and Dialogue Works upload today?", start with **`cognition streams`** and let it pass approved URLs down to this workflow.

## When to run

- A user provides a YouTube URL and wants a transcript saved into canonical raw-input.
- You need to confirm title, publication date, and channel before naming the file.
- The available source is auto-captions or subtitles rather than an operator-pasted cleaned transcript.
- A prior transcript exists but needs provenance-safe normalization or re-materialization.

## Workflow

1. **Resolve metadata first**
   - Extract video id, title, upload date, and channel before writing any file.
   - Treat the user-provided date as authoritative if they explicitly give one; otherwise use video metadata.
   - Do not infer dates from similar past episodes or title motifs.
   - Decide ownership before naming the file:
     - if the upload belongs to a designated cognition stream such as Diesen, Davis, Mercouris, or Dialogue Works, use the host stream as the owning lane
     - if the upload is on an outside channel and the recurring guest already has a real notebook lane such as `pape` or `ritter`, use the guest lane as the owning lane
   - The filename should teach that ownership rule. Keep the outside host visible, but do not let an incidental channel displace the notebook owner.
   - If the URL appears to be a same-day companion clip cut from a longer same-channel upload, do **not** materialize it by default. Prefer the longer parent interview or episode unless the operator explicitly asks for the companion clip anyway.

2. **Acquire the best subtitle source available**
   - Prefer the original-language subtitle track if available (for example `en-orig` before fallback `en`).
   - When using `yt-dlp`, prefer a wildcard language request such as `en.*` so the extractor can recover `en-orig` and related English variants instead of failing on a too-literal language list.
   - If `yt-dlp` is not on `PATH`, try the Python module path.
   - Save subtitle artifacts locally so the extraction path is auditable.
   - If the repo's normal transcript path reports errors such as `no vtt subtitle file produced` or a language-specific fetch failure even though `--list-subs` shows English auto-captions, retry with a direct `yt-dlp` subtitle pull before giving up.

3. **Use tranche mode when the operator has a vetted batch**
   - If the operator already has an approved set of exact watch URLs, treat the task as a targeted tranche rather than a channel crawl.
   - Resolve metadata per URL, pull subtitles per URL, and then materialize the resulting batch into canonical date folders.
   - Do not fall back to broad channel slicing when the real task is "capture these exact episodes."

4. **Choose the right transcript class**
   - Use `cleaned_transcript` only when the user supplies cleaned dialogue or a human-cleaned source.
   - Use `auto_subtitles_vtt` when you materialize raw captions with minimal intervention.
   - Use `speaker_normalized_from_auto_subtitles` when you perform best-effort turn assignment and sentence cleanup from captions.

5. **Materialize the canonical raw-input file**
   - Write the file into the canonical date folder using the published date.
   - Include frontmatter with `ingest_date`, `pub_date`, `thread`, `title`, `source_url`, `source_type`, `transcript_type`, and a plain-language `editorial_note`.
   - Make the note explicit about whether the transcript is operator-pasted, auto-extracted, or best-effort normalized.
   - Keep `show`, `host`, `guest`, and `channel_slug` explicit when present so host context is preserved even when the expert lane owns the filename.

6. **Normalize conservatively**
   - Remove timing markup, duplicate carryover lines, and obvious caption artifacts.
   - Remove extraction headers such as `Kind:` / `Language:` when they are not part of the episode itself.
   - Collapse repeated consecutive caption triplets or other obvious auto-caption duplication.
   - Normalize obvious HTML entities or transcript wrapper artifacts without pretending the result is human-cleaned.
   - Reflow fragments into readable paragraphs.
   - Assign speaker labels only where confidence is reasonable from interview structure.
   - Normalize recurring guest names conservatively when the lane identity is already established, for example keeping `Seyed M. Marandi` stable instead of preserving every caption-side variant.
   - Preserve uncertainty rather than inventing fluent but unsupported dialogue.

7. **Verify before declaring success**
   - Check the top metadata block, opening lines, and closing lines.
   - Make sure title, date, guest, and transcript type all agree with the extraction path.
   - If the output still has substantial caption noise, say so clearly.

## Guardrails

- Never present auto-captions as human-verified verbatim text.
- Never silently upgrade `auto_subtitles_vtt` into `cleaned_transcript`.
- Never infer a date from thematic similarity to another episode when metadata or user instruction is available.
- Never let an outside host channel silently take ownership from a recurring expert lane when the notebook clearly treats the guest as the real owner of the capture.
- Never record an obvious same-day companion clip when a longer same-channel parent episode exists, unless the operator explicitly overrides that default.
- Keep provenance explicit enough that a later operator can distinguish:
  - operator-pasted cleaned transcript
  - raw subtitle extraction
  - best-effort speaker normalization
- Prefer conservative speaker labeling over false precision.

## Output classes

- **Minimal capture:** canonical raw-input with metadata plus raw or lightly deduped caption text.
- **Speaker-normalized:** readable interview turns from auto-captions with explicit best-effort provenance.
- **Cleaned transcript:** only when a human-cleaned transcript is supplied.

## Command pattern (host-agnostic)

```bash
# Metadata
python -m yt_dlp --skip-download --print "%(id)s\n%(title)s\n%(upload_date)s\n%(channel)s" "<youtube-url>"

# Subtitle extraction
python -m yt_dlp --skip-download --write-auto-sub --sub-langs "en.*" --sub-format vtt -o "<temp-dir>/%(id)s.%(ext)s" "<youtube-url>"

# Direct fallback when the normal pipeline misses visible English auto-captions
python -m yt_dlp --skip-download --write-auto-subs --sub-langs "en.*,en,en-US,en-orig" --sub-format vtt -o "<temp-dir>/%(id)s.%(ext)s" "<youtube-url>"
```

## Success condition

The result is a date-correct, provenance-safe raw-input transcript file that future ingest or analysis can trust without confusing subtitle extraction for a human-cleaned source.


## Cursor / grace-mar instance

Grace-mar paths and commands for this repository (from `.cursor/skills/youtube-raw-input-transcript/`).

| Topic | Path |
|--------|------|
| Canonical raw-input tree | [codex/](../../codex/) |
| Date-bucket target pattern | `codex/YYYY/raw-input/YYYY-MM-DD/` |
| Existing Diesen examples | [codex/2026/raw-input/2026-04-19/](../../codex/2026/raw-input/2026-04-19/) · [codex/2026/raw-input/2026-05-11/](../../codex/2026/raw-input/2026-05-11/) |
| Temp subtitle cache | [\.codex-tmp/yt-dlp/](../../.codex-tmp/yt-dlp/) |
| Portable skill manifest | [skills-portable/manifest.yaml](../../../skills-portable/manifest.yaml) |
| Sync script | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |
| Skill validator | [scripts/validate_skills.py](../../../scripts/validate_skills.py) |

**Repo notes**

- In this repo, `thread` is usually the host lane such as `diesen`, `mercouris`, or `davis`.
- Prefer `python -m yt_dlp` if `yt-dlp` is not on `PATH`.
- Preserve explicit `editorial_note` language:
  - `Operator-pasted cleaned transcript.`
  - `Auto-captions extracted with yt_dlp from YouTube VTT (en-orig).`
  - `Best-effort speaker normalization and sentence polishing from YouTube auto-captions extracted with yt_dlp (en-orig). Not human-verified verbatim.`

**Common local command pattern**

```powershell
python -m yt_dlp --skip-download --print "%(id)s`n%(title)s`n%(upload_date)s`n%(channel)s" "<youtube-url>"

python -m yt_dlp --skip-download --write-auto-sub --sub-langs "en.*" --sub-format vtt -o "C:\dev\strategy-codex\.codex-tmp\yt-dlp\%(id)s.%(ext)s" "<youtube-url>"
```
