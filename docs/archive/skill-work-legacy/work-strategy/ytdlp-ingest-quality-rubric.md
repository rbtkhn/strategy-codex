# yt-dlp ingest quality rubric

This rubric scores a `yt-dlp` ingest as four separate layers rather than one undifferentiated success or failure.

Use it when the operator wants a quick judgment on whether an ingest pass was:

- merely extracted
- notebook-usable
- discoverable afterward
- fully closed as a maintained corpus object

## Scoring dimensions

Score each dimension from `0` to `3`.

### 1. Discovery

How well did the action find the right target set?

- `0` — missed the relevant upload or searched the wrong scope
- `1` — partial discovery, obvious omissions, or unstable filtering
- `2` — correct operator-selected set found, but historical or adjacent completeness still uncertain
- `3` — correct set found and any known surrounding inventory implications were checked

### 2. Subtitle extraction

Did `yt-dlp` actually leave usable receipts?

- `0` — no usable subtitle receipt
- `1` — receipt exists but is damaged, empty, or clearly wrong-track
- `2` — usable fallback receipt exists
- `3` — preferred receipt exists cleanly, usually `en-orig` with fallback present when available

### 3. Provenance wrapper

Did the raw-input write path preserve notebook truth correctly?

- `0` — raw-input missing or materially wrong
- `1` — raw-input exists but ownership, date, URL, or transcript class is suspect
- `2` — raw-input is usable and mostly correct, but some provenance or naming ambiguity remains
- `3` — raw-input is cleanly owned, correctly dated, correctly sourced, and honestly labeled

### 4. Index sync

Did the relevant inventory or ledger reflect the new reality afterward?

- `0` — inventory now materially misstates what the repo holds
- `1` — inventory drift is visible but not yet reconciled
- `2` — primary inventory updated, but adjacent ledgers or serial-lane views may still lag
- `3` — inventories and discovery surfaces now reflect the ingest outcome accurately

## Reading the result

Do not collapse the four scores into one vague mood.

Instead read the profile:

- strong **discovery** + weak **subtitle extraction** = targeting was right, extractor failed
- strong **subtitle extraction** + weak **provenance wrapper** = tool worked, notebook write path failed
- strong **wrapper** + weak **index sync** = ingest exists, but the corpus still teaches the wrong picture

## Quick labels

Use these shorthand labels when helpful:

- **mechanical success** = subtitle extraction `2-3`
- **notebook success** = provenance wrapper `2-3`
- **maintenance success** = index sync `2-3`
- **fully closed ingest** = all four dimensions at `2+`, with no `0`

## Current lesson

The May 12 cognition-stream pass is the model case for why the split matters:

- discovery was good for the operator-selected set
- subtitle extraction was strong
- provenance wrapper was strong
- index sync was only partial until the Baud / Dialogue Works inventory was reconciled

So the pass was a **good ingest** before it was a **fully closed ingest**.
