---
note_id: scaffold-receipt-parity-recursive-learning
note_type: synthesis
authority_level: review-needed
source_basis: mixed
essay_candidate: false
created_at: 2026-06-18
updated_at: 2026-06-28
---
## Scaffold Receipt Parity — Recursive Learning Entry

WORK only; not Record.

**Statecraft Registry**
- Lane: shared
- Output class: memo
- Prose class: note-class
- Maturity: reusable
- Source family: lane-local
- Bridge usage: none
- Transaction relevance: none

**Return paths:** [recursive-learning-journal-executive-synthesis.md](./recursive-learning-journal-executive-synthesis.md) · [three-layers essay](../../essays/three-layers-of-recursive-learning-in-statecraft.md)

## Phase

Phase Three — learning from instruction / pipeline drift (June 2026 statecraft archive scaffold work).

## Pressure

Live June 2026 normalization exposed a false-confidence pattern:

- frontmatter flags claimed close promo was trimmed (`mercouris_close_promo_trim_applied: true`)
- transcript bodies still contained platform outros
- default dry-runs reported **0 would-change** because idempotency keyed on flags, not body parity
- post-land batch omitted Davis, Redacted, and Breaking Points closes

## Law (receipt parity)

```text
A scaffold normalize receipt is valid only when the transcript body agrees with it.
Flags are hints; body tail is proof.
```

Operational corollaries:

1. **Completeness before trim** — never strip close promo on `truncated_tail`; re-ingest first.
2. **Primary at land** — `post_land_statecraft_batch.py` runs caption wrapper + family normalize on intake.
3. **Dream backstop** — `dream_scaffold_catchup.py` audits since-previous-dream days; apply is opt-in and capped.
4. **Stale-flag repair** — Mercouris `--force-close` when flag set but promo anchor still in tail window.
5. **Family asymmetry** — opening normalizer ≠ close normalizer (Nawfal host close may need manual or future close lane).

## Adaptive reuse (not decorative copying)

Channel scripts share tail-bounded anchors and frontmatter-safe key patching; they do **not** share one anchor table. Mercouris solo close grammar ≠ Nawfal multi-guest outro ≠ Davis travel close.

Shared router: `scripts/post_land_statecraft_family.py`.

## Guardrails

- Do not treat dream catch-up as primary ETL — latency and false receipts return if intake skips post-land.
- Filter caption wrapper **metadata-only** dry-runs from catch-up debt signals.
- Windows month sweeps need explicit `--day` / `--month` — bare glob roots false-negative.

## Falsifiers

- `would_trim > 0` on days that ran post-land at intake → router or detector bug.
- `stale_*_close_flag` after force-close repair → anchor gap or wrong cut plane.
- Operators defer intake normalize because “dream will fix it” → synthesis reads noisy SSOT same day.

## Promotion (2026-06-17)

| Artifact | Role |
|----------|------|
| `post_land_statecraft_family.py` | SSOT family router |
| `dream_scaffold_catchup.py` | Report + opt-in apply backstop |
| `auto_dream.py` hook | Nightly debt visibility in handoff |
| Mercouris ASR-tolerant anchors | `I you can find`, `intend to finish`, `have to finish` |

## Accept / defer

**Accept:** hybrid intake + dream report; receipt parity as invariant.

**Defer:** Nawfal close normalizer lane; month audit script; `--month` on all normalizer CLIs.
