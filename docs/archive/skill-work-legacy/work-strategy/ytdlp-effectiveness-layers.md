# yt-dlp effectiveness layers

This note separates three different questions that are often blurred together after a YouTube ingest:

- did **`yt-dlp`** itself work?
- did the **ingest wrapper** turn that receipt into a usable raw-input correctly?
- did the **inventory / discovery layer** reflect reality afterward?

Those are not the same success condition.

## 1. Tool success

`yt-dlp` succeeds when it does the narrow extractor job:

- resolves the target video
- downloads the best available subtitle track
- leaves a usable local receipt such as `en-orig.vtt` or fallback `en.vtt`

If the `.vtt` receipt exists and is readable, the extractor layer probably worked even if later notebook surfaces are incomplete.

This is the most mechanical layer.

## 2. Wrapper success

The wrapper succeeds when it converts the extractor receipt into a notebook-usable raw-input with the right provenance.

Minimum tests:

- correct `source_url`
- correct `pub_date`
- correct `thread`
- correct host or show ownership
- correct `transcript_type`
- conservative editorial note matching the real intervention level

This is where naming doctrine, lane ownership, and transcript-class honesty matter.

The wrapper can fail even when `yt-dlp` worked perfectly.

## 3. Inventory failure

The inventory or discovery layer fails when the notebook's index underreports, misclassifies, or forgets captures that already exist.

Typical symptoms:

- a raw-input exists on disk but the inventory still says `needs capture`
- a serial guest run is much larger than the mirrored subset suggests
- a daily channel list omits uploads that the extractor could have handled

This is not a subtitle-extraction failure.
It is a discovery, sync, or maintenance failure.

## 4. Why the distinction matters

If these layers are not separated, the notebook can learn the wrong lesson.

Bad diagnosis:

- "yt-dlp missed the lane"

More truthful diagnosis:

- `yt-dlp` may have succeeded at subtitle extraction
- the wrapper may have succeeded at raw-input creation
- the inventory may still have failed to represent the resulting corpus honestly

That distinction matters because the repair path changes:

- extractor failure -> retry, fallback, or alternate subtitle method
- wrapper failure -> fix provenance, naming, ownership, or transcript class
- inventory failure -> reconcile ledgers, backfill indexes, or widen discovery

## 5. Current audit lesson

The May 12 cognition-stream ingest is a good example of strong extractor performance.

What worked:

- local `.vtt` receipts were produced for the selected uploads
- raw-input files were written with consistent `auto_subtitles_vtt` provenance
- host or expert ownership remained legible

What did not automatically follow:

- historical lane completeness
- inventory synchronization
- full-year visibility for serial guest runs such as `Dialogue Works × Baud`

So the right conclusion is:

- **tool success** was high
- **wrapper success** was high
- **inventory completeness** remained partial

## 6. Operator rule

After any meaningful `yt-dlp` action, ask three separate questions:

1. did the extractor leave real receipts?
2. did the wrapper write honest raw-input?
3. does the inventory now describe what the repo actually holds?

Only when all three answers are yes should the ingest be treated as fully complete.
