---
name: youtube-raw-input-transcript
preferred_activation: youtube transcript
description: "Extract metadata and captions for a specific YouTube episode, then materialize a canonical transcript-bearing raw-input file with conservative provenance, speaker normalization, and date-safe frontmatter. Use when the operator already has a specific watch URL or exact episode in hand and wants transcript materialization or re-materialization. Do not use for archive family resolution, month-slice inventory work, or post-capture cleanup passes."
portable: true
version: 0.1.2
tags:
  - operator
  - raw-input
  - youtube
  - transcript
---

# YouTube raw-input transcript

**Preferred activation (operator):** say **`youtube transcript`**.

Use this skill when a YouTube episode should become a canonical transcript artifact, especially when there is no human-cleaned transcript yet and the best available source is YouTube captions.

In strategy-codex, this skill is also the shared **transcript + appearance materialization** layer for daily ingest, one-off captures, and bounded densification tranches. Prefer the one-shot capture path unless the operator explicitly asks for transcript-only output.

## Layering rule

- Use **`youtube transcript`** when the operator already has a specific URL or episode in hand.
- Do **not** use this as the first move for the five-stream daily roster check.
- When the task is "what did Davis, Diesen, Alkhorshid/Dialogue Works, Napolitano/Judging Freedom, and Mercouris upload today?", start with **`check streams`** and let it pass approved URLs down to this workflow. `cognition streams` remains a legacy alias for the same daily roster pass.

## When to run

- A user provides a YouTube URL and wants a transcript saved into canonical raw-input.
- You need to confirm title, publication date, and channel before naming the file.
- The available source is auto-captions or subtitles rather than an operator-pasted cleaned transcript.
- YouTube fetch failed or was blocked, but the operator pasted a full transcript in the Codex thread for a known episode.
- A prior transcript exists but needs provenance-safe normalization or re-materialization.

## Workflow

1. **Resolve metadata first**
   - Extract video id, title, upload date, and channel before writing any file.
   - Treat the user-provided date as authoritative if they explicitly give one; otherwise use video metadata.
   - Do not infer dates from similar past episodes or title motifs.
   - If YouTube metadata fetch fails but the operator supplied title, publication date, and lane/file ownership metadata, do not stop immediately. Use the video id from the URL and attempt subtitle extraction with operator-supplied metadata as the capture authority.
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
   - Distinguish subtitle source plainly: `manual` means manually provided YouTube subtitles, while `auto` means auto-generated YouTube subtitles. Do not call all subtitle-derived material "auto-captions."
   - If the repo's normal transcript path reports errors such as `no vtt subtitle file produced` or a language-specific fetch failure even though `--list-subs` shows English auto-captions, retry with a direct `yt-dlp` subtitle pull before giving up.
   - Treat metadata-bypass success as transcript-grade only when subtitle fetch and non-stub verification still pass. Treat metadata-bypass caption failure as a normal failed-fetch with manual scaffold output.

3. **Use operator-paste fallback when the transcript is in chat**
   - If the operator pasted a full YouTube transcript in the current Codex thread, treat it as transcript-bearing source material even when YouTube metadata, bot-check, or subtitle fetch failed.
   - Prefer mechanical extraction from the local Codex session log over hand-copying or summarizing long chat text. Look under `$CODEX_HOME/sessions/<YYYY>/<MM>/<DD>/` or `~/.codex/sessions/<YYYY>/<MM>/<DD>/` for the rollout JSONL that contains the distinctive title plus `Transcripts:`.
   - Extract the `event_msg` whose payload type is `user_message`, then split the message body on `Transcripts:\r?\n`. The text after that marker is the transcript source.
   - Write canonical raw-input with explicit provenance. Prefer repo-native transcript language such as:
     - `source_type: youtube`
     - `transcript_type: operator_pasted_transcript`
     - `source_note: transcript pasted manually by operator` or `mechanically extracted from local Codex session log after operator pasted full transcript`
   - If the direct watch URL is still unresolved, this workflow should usually hand off to the archive intake layer rather than pretending the front door is complete. Preserve the unresolved seam explicitly in `source_note`.
   - Verify exact correspondence between the extracted transcript source and the file body after `## Transcript`. Report `sourceChars`, `bodyChars`, and `exactMatch=True` before claiming capture.
   - Use `partial-chat-capture` only if the session source cannot be found, the operator clearly supplied an excerpt rather than a full transcript, or exact-match verification fails. Partial captures remain repair-queue items with `full-transcript-import-needed`.
   - Operator-paste fallback is not the same as auto subtitles or a human-cleaned transcript. It is a useful transcript-bearing capture with honest provenance unless separately cleaned or independently verified.

## Front-door completeness rule

This skill is strongest when a **specific YouTube episode URL** is already in hand.

- If a trustworthy direct YouTube watch URL exists, proceed normally.
- If subtitle or metadata fetch fails but the watch URL still exists, operator-paste fallback can still finish the capture.
- If the direct watch URL itself is still missing and the item is anchored only by a secondary listing plus transcript paste, do **not** invent or guess a YouTube front door here.

In that last case:

- preserve the transcript as real
- preserve the unresolved watch-surface seam explicitly
- prefer handing the item to `statecraft source intake` if the operator's real task is canonical archive filing rather than URL-grade YouTube capture

Short rule:

`known watch URL -> youtube transcript`

`unknown watch URL but full transcript + anchored identity -> archive intake with explicit provenance`

4. **Use tranche mode when the operator has a vetted batch**
   - If the operator already has an approved set of exact watch URLs, treat the task as a targeted tranche rather than a channel crawl.
   - Resolve metadata per URL, pull subtitles per URL, and then materialize the resulting batch into canonical date folders.
   - Do not fall back to broad channel slicing when the real task is "capture these exact episodes."
   - For densification work, name the bounded tranche with `--purpose densification --tranche-label <label>` and keep the approved URL set or raw-input list as the tranche authority.
   - For already-materialized transcript files, use `--raw-input <path>` or `--raw-input-list <file>` with `--with-appearances` to produce appearance, routing, and action artifacts without refetching or rewriting transcripts.

5. **Choose the right transcript class**
   - Use `cleaned_transcript` only when the user supplies cleaned dialogue or a human-cleaned source.
   - Use `auto_subtitles_vtt` when you materialize raw captions with minimal intervention.
   - Use `speaker_normalized_from_auto_subtitles` when you perform best-effort turn assignment and sentence cleanup from captions.
   - Use `operator_pasted_youtube_transcript` when a full transcript is supplied through chat or a session log and exact-match verification passes.
   - Use `partial-chat-capture` only as an explicit incomplete repair state, not as a convenience label for long but complete pastes.

6. **Materialize the canonical raw-input file**
   - Write the file into the canonical date folder using the published date.
   - Include frontmatter with `ingest_date`, `pub_date`, `thread`, `title`, `source_url`, `source_type`, `transcript_type`, and a plain-language `editorial_note`.
   - Include verification frontmatter when available: `body_word_count`, `body_chars`, `verification_ok`, `verification_reason`, and `evidence_grade`.
   - Make the note explicit about whether the transcript is operator-pasted, auto-extracted, or best-effort normalized.
   - Keep `show`, `host`, `guest`, and `channel_slug` explicit when present so host context is preserved even when the expert lane owns the filename.
   - If the title only identifies the host, do not write the host as `guest`. Prefer blank guest with a host-only inference note such as `guest_inference: host-only-title-match`.

7. **Normalize conservatively**
   - Remove timing markup, duplicate carryover lines, and obvious caption artifacts.
   - Remove extraction headers such as `Kind:` / `Language:` when they are not part of the episode itself.
   - Collapse repeated consecutive caption triplets or other obvious auto-caption duplication.
   - Normalize obvious HTML entities or transcript wrapper artifacts without pretending the result is human-cleaned.
   - Reflow fragments into readable paragraphs.
   - Assign speaker labels only where confidence is reasonable from interview structure.
   - Normalize recurring guest names conservatively when the lane identity is already established, for example keeping `Seyed M. Marandi` stable instead of preserving every caption-side variant.
   - When a transcript is already captured but proper nouns are badly mangled, invoke **`proper noun normalization`** rather than broad prose cleanup.
   - Preserve uncertainty rather than inventing fluent but unsupported dialogue.

8. **Verify before declaring success**
   - Check the top metadata block, opening lines, and closing lines.
   - Make sure title, date, guest, and transcript type all agree with the extraction path.
   - Verify the canonical raw-input is not a header-only shell: it must have frontmatter with `source_url`, `pub_date`, `title`, provenance note, source/transcript type, and a real transcript body after frontmatter.
   - Treat bodies below roughly 75 words or 400 non-frontmatter characters as failed embodiment unless the operator explicitly asked for a minimal metadata-only capture.
   - Reject placeholder phrases such as `transcript pending`, `index-only`, or `listed_only` as successful transcript bodies.
   - If the output still has substantial caption noise, say so clearly.
   - If YouTube blocks metadata or captions, do not create a canonical stub. Use the receipt-side manual transcript scaffold instead, then wait for a human-filled body before routing appearances.
   - For operator-paste fallback, do not report success unless the canonical body is non-stub and exact-match verification against the extracted paste source passes.

9. **Emit the appearance packet**
   - For strategy-codex captures, prefer `--with-appearances` so successful raw-input files immediately produce:
     - `appearance-ledger.jsonl`
     - `speaker-routing-queue.md/jsonl`
     - `memory-action-queue.md/jsonl`
     - `artifacts/host-shelf-quality/<year>/<host>/<YYYY-MM>/quality-summary.md/json`
     - `codex/years/2026/raw-input/raw-input-master-index.md/json`
     - `codex/years/2026/raw-input/raw-input-index-audit.md/json`
     - `.codex-tmp/youtube-raw-input/<run-id>/capture-summary.md`
   - Route only files from the approved run or densification tranche; do not sweep every file in the same date folder.
   - For `--apply --with-appearances`, keep the host-shelf quality report enabled unless the operator explicitly uses `--no-quality-report`.
   - Any `--apply` run should leave the raw-input master index refreshed; treat that index as a maintained route map, not as stronger authority than the dated raw-input folders themselves.
   - The companion raw-input index audit is advisory only. Use it to spot index sprawl or plausible missing benches, but do not let it outrank the dated tree or turn ordinary capture into a hard failure.
   - Close every densification pass with the quality contract line: `Structure: <delta> | Purity: <delta/%> | Unresolved: <count> | Git: on-disk/verified/not-committed/not-pushed`.
   - For ordinary one-off or daily captures, close with raw-input path, `youtube_id`, `caption_kind`, `caption_language`, `body_word_count`, `evidence_grade`, and verification reason.
   - Treat materializer quality reports as `full-host-month` receipts; if a single-file run differs from the monthly shelf baseline, name the scope explicitly instead of implying shelf regression.
   - Distinguish topological progress from text-quality progress: route count and shelf coverage are not the same as transcript-grade or cleaned-transcript purity.
   - Stop at advisory artifacts unless the operator separately asks to edit speaker objects, arcs, helixes, lattice rows, or other interpretation surfaces.
   - If a speaker is touched during ingest or routing, resolve it through one of these paths and say which one applies when useful:
     - existing speaker raw-input index
     - existing host / core lane
     - existing arc / object / routing surface
     - explicit note that no new index is justified
   - Do not create an arc-specific index by default. Arc files stay interpretive unless the doctrine threshold is clearly met: the parent arc is no longer a practical front door, the indexed items form a distinct retrieval domain, and the new surface answers a different operator question than the neighboring bench or arc.

## Guardrails

- Never present auto-captions as human-verified verbatim text.
- Never silently upgrade `auto_subtitles_vtt` into `cleaned_transcript`.
- Never report a YouTube transcript as materialized when only discovery metadata, a filename, or a stub body exists on disk.
- Never infer a date from thematic similarity to another episode when metadata or user instruction is available.
- Never let an outside host channel silently take ownership from a recurring expert lane when the notebook clearly treats the guest as the real owner of the capture.
- Never record an obvious same-day companion clip when a longer same-channel parent episode exists, unless the operator explicitly overrides that default.
- Never downgrade a full operator-pasted transcript to partial because the paste is long, YouTube is blocked, or `apply_patch` is awkward. Use session-log extraction when available and verify exact match.
- Never mark operator-paste repairs captured unless the written raw-input body matches the extracted source and the receipt records that match.
- Keep provenance explicit enough that a later operator can distinguish:
  - operator-pasted cleaned transcript
  - operator-pasted raw YouTube transcript
  - manual YouTube subtitles extracted by tooling
  - raw subtitle extraction
  - best-effort speaker normalization
- Prefer conservative speaker labeling over false precision.

## Output classes

- **Minimal capture:** canonical raw-input with metadata plus raw or lightly deduped caption text.
- **Speaker-normalized:** readable interview turns from auto-captions with explicit best-effort provenance.
- **Cleaned transcript:** only when a human-cleaned transcript is supplied.
- **Operator-pasted transcript:** valid fallback after fetch failure or bot-check. Use `full-operator-paste` when mechanically extracted and exact-match verified; use `partial-chat-capture` only for incomplete or unverified chat excerpts.

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

The result is a date-correct, provenance-safe raw-input transcript file with a verified non-stub body that future ingest or analysis can trust without confusing subtitle extraction for a human-cleaned source. For approved YouTube URLs in strategy-codex, prefer `python scripts/materialize_youtube_raw_input.py --url "<youtube-url>" --apply` so success is computed before downstream claims.

Default strategy-codex command:

```bash
python scripts/materialize_youtube_raw_input.py --url "<youtube-url>" --apply --with-appearances --purpose one-off
```

Manual fallback after bot-check/auth failure:

```bash
python scripts/materialize_youtube_raw_input.py --url "<youtube-url>" --apply --with-appearances --purpose one-off --title "<title>" --pub-date YYYY-MM-DD --host "<host>" --show "<show>" --thread "<thread>" --channel-slug "<slug>" --file-prefix "<prefix>" --guest "<guest>"
```

When title, date, channel slug, and file prefix are supplied, this command can bypass a YouTube metadata-fetch failure and still try caption extraction by video id. This is the preferred repair path before manual transcript paste.

If the fetch fails, use `.codex-tmp/youtube-raw-input/<run-id>/manual-curation-queue.md` plus `manual-transcript-scaffolds/`. The queue is the human inbox. Each scaffold row includes a receipt-only `.draft.md`, `.paste-body.txt` buffer, target canonical path, paste marker, curator notes, and verification helper. It must not be treated as captured raw-input until a human replaces the marker with a real transcript body and the verifier accepts it.

Densification tranche examples:

```bash
python scripts/materialize_youtube_raw_input.py --input approved-urls.jsonl --apply --with-appearances --purpose densification --tranche-label napolitano-core-six
python scripts/materialize_youtube_raw_input.py --raw-input-list existing-raw-inputs.txt --apply --with-appearances --purpose densification --tranche-label diesen-marandi-backfill
```
