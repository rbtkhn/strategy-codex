---
name: statecraft-transcript-section-balance
description: "Statecraft archive transcript section ladder — section map, quantify receipt, flatten/re-anchor balance, thematic retitle. Triggers: section balance pass, quantify section nav, transcript section ladder."
category: truth-pipeline
status: draft
scope_class: repo-governed
---
# statecraft-transcript-section-balance (draft)

**Preferred activation:** **`section balance pass`** · **`quantify section nav`** · **`transcript section ladder`**

**Edit surface:** `source-archive/statecraft/YYYY-MM-DD/source-*.md` with `transcript_curation: curated_sectioned` (or nudge from flat).

**Not this skill:** PH public interviews → [`ph-interview-transcript-curation`](../../ph-interview-transcript-curation/SKILL.md); first land / verbatim intake → [`statecraft-source-intake`](../../statecraft-source-intake/SKILL.md).

## Ladder (default order)

1. **Initial section pass** — anchor map at transcript pivots; set `transcript_curation: curated_sectioned`.
2. **Receipt** — `python scripts/quantify_section_nav.py --day YYYY-MM-DD` (or in-process `analyze` on named paths). Fail on: flat ≥4000w, bootstrap slug titles, section &lt;100w or &gt;1500w.
3. **Balance pass** — flatten existing `###` headings → validate anchor order follows **transcript chronology** → `insert_sections` with merged stubs and split monoliths. Copy pattern from `scripts/patch_reason_resist_may_balance.py`.
4. **Thematic retitle** (optional) — replace `Segment N —` / `Show Open — Introduction` slugs only; body unchanged. Pattern: `scripts/patch_reason_resist_jun_retitle.py` + `write_slug_retitle_capture`.
5. **Corpus receipt** — re-run quantify on batch; target zero warnings before commit.

## Host-only channel law (when applicable)

Show host routing → `statecraft/channels/{slug}/{slug}-channel-index.md`; compat stub on legacy `{host}-index.md`. **No** `statecraft/voices/{host}/` unless operator promotes guest mechanism depth.

## Exemplar

Reason to Resist (`channel_slug: reason-resist`): 6 captures May 18 → Jun 25; May trio balance + Jun 13/18 retitle; **6/6** section-nav clean.

| Commit | Scope |
|--------|-------|
| `ebacef942` | May section + balance; channel index; routing |
| `e2fa70ae1` | RLJ law extract |
| `888c7ab28` | Jun thematic retitle |

RLJ: [`statecraft/recursive-learning-journal.md` § 2026-06-26](../../../statecraft/recursive-learning-journal.md#2026-06-26---reason-to-resist-host-only-shelf--transcript-section-balance-ladder)

## Windows harness

One Shell per turn; no parallel `StrReplace` on same capture. Balance = flatten then single re-insert — do not stack section passes on stale headings.

## Promote when

Pattern repeats on another channel batch (Duran solo rails, Dialogue Works, etc.) or operator asks for portable SKILL + manifest sync.
