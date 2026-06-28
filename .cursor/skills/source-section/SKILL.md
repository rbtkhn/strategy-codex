---
name: source-section
description: Post-intake transcript section curation for YouTube channel solo and interview captures — Title Case
preferred_activation: source-section
activation: source-section
portable: true
version: 1.2.0
category: truth-pipeline
status: active
scope_class: public-portable
requires:
- statecraft-source-intake
tags:
- operator
- source-archive
- transcript
- curation
outputs:
- sectioned source capture with curated_sectioned receipt
portable_source: skills/source-section/SKILL.md
synced_by: sync_portable_skills.py
---
# Source section (`source-section`)

**Preferred activation:** **`source-section`** (or **`source section`**, **`section source`**). **Outline-only:** **`source-section outline`** (or **`section outline`**) — plan and pin the map; do not mutate body until operator approves ship.

**Scope:** Post-land **editorial structure** for long **YouTube channel** **solo** and **interview** transcript captures — not authored essays, not first-pass intake, not ASR tier cleanup, not synthesis.

**Channel vs authored (hard boundary):**

| In scope | Out of scope |
| --- | --- |
| YouTube **guest** interviews (`source_form: interview`, `source_type: youtube`, or `channel_slug`) | **Authored** Substack / newsletter / essay (`kind: substack-post`, `paste-bundle`, `source_form: newsletter`) |
| YouTube **solo** monologues on a channel shelf | Wire clips, panels, roundups (unless operator names a host spine) |
| Operator-paste **transcript** bodies with turn-taking under `## Transcript` | Short confirmation posts, X posts, authored briefing prose |

**Do not** offer **`source-section`** on land for authored Pape essays — even when long or flat. Authored work uses essay structure / synthesis links, not transcript section maps.

**SSOT helper:** `scripts/transcript_section_curation.is_source_section_eligible()`

**Pipeline position:** **`source-intake`** (land flat verbatim) → optional **`source-clean`** → **`source-section`** (outline → approve → ship) → downstream study / synthesis.

## Why section (operator value)

Sectioning **does not** summarize, clean ASR, or verify wire hooks. It turns one long transcript into a **table of contents with named doors**:

- **Jump, don't scroll** — skim ~6–14 headings, open the seam you need (~700–1,100 words) instead of linear search through 6k–12k words.
- **Stable link targets** — synthesis, wire-verify receipts, and notebook weave can cite `### Topic — Subtopic` anchors.
- **Lower cognitive load** — hold one movement at a time instead of the whole interview arc.
- **In-section scan** — paragraph reflow breaks each section into ~80–120 word blocks (markdown `\n\n` only) so a hop is readable, not a wall of text.

Intake lands truth; sectioning organizes reading. Do not substitute synthesis for transcript body in the archive object.

## Post-land nudge (mandatory agent behavior)

After **`source-intake`** land (+ optional **`source-clean`**) on a **YouTube channel** capture with **`source_form: solo`** or **`source_form: interview`**, **say explicitly** (not only as a buried menu fork) when **any** of:

| Trigger | Recommend |
| --- | --- |
| Transcript body is **flat** (no `###` headings under the body marker) and **≥ ~4,000 words** | **`source-section outline`** before daily synthesis |
| Body has **bootstrap slug** headings (`Segment N — …`, `Show Open — Introduction` only) | **`source-section`** slug **retitle** to thematic Title Case |
| **`check_statecraft_intake_daily_sync.py`** shows **DESYNC** and archive captures are unsectioned or slug-only | Section the archive batch **before** `state synthesis` |

**One-line nudge template (adapt):**

> Recommend **`source-section outline`** before synthesis — ~N thematic jump targets vs one monolith; expect roughly **~90% less scan** per random topic (uniform hop model).

Do **not** auto-section on land — operator approves map on large captures. **Do** surface the payoff when triggers match. **Never** nudge **`source-section`** on **`source_form: newsletter`**, **`kind: substack-post`**, or other **authored** captures.

## Use this skill when

- A **YouTube channel** transcript capture is already landed with `source_form: solo` or `source_form: interview` (confirm `source_type: youtube`, `channel_slug`, or YouTube `source_url`)
- Operator wants **Title Case** `### … — …` section headings for navigation and study (not lowercase slug headers)
- You have or can derive a **section map**: ~6–14 thematic headings + **anchor phrases** (N−1 anchors for N sections; last section → EOF)
- **Interview** captures need **speaker labels** restored at section splits after anchor insertion
- **Solo** monologue captures need thematic breaks only (usually no speaker repair)

## Do not use when

- Capture is not yet landed — run **`source-intake`** first
- **Authored text** — Substack essays, newsletters, articles, paste-bundle opinion posts (`kind: substack-post`, `source_form: newsletter`, etc.) — **never** **`source-section`**
- `source_form` is `panel`, `clip`, `newsletter`, `article`, or `roundup` unless operator explicitly overrides with a YouTube transcript spine
- Job is ASR / proper-noun cleanup only — use **`source-clean`**
- Job is wire triage — use **`wire-verify`**
- Job is interpretive synthesis, notebook weave, or lane drafting
- Operator wants summary or paraphrase instead of full transcript body

## Core law

- **Intake lands truth; sectioning organizes reading.** Do not substitute synthesis for transcript body in the archive object.
- **Verbatim substance preserved** — sectioning adds headings and light mechanical fixes only; no argument rewrite.
- **Paragraph reflow is whitespace-only** — `reflow_section_paragraphs` inserts `\n\n` between rational blocks; no paraphrase; speaker turns and `>>` markers preserved.
- **Headings are editorial** — Title Case thematic labels (`### Show Open — …`), never machine slug headers (`### iran-attrition-…`) on operator surfaces.
- **Anchors are pinned** — per-source section maps must be reproducible (script with `SECTION_TITLES` + `SECTION_ANCHORS`, or checked-in patch recipe).
- **Outline before ship** — propose and pin the section map; **do not** insert headings into the capture body until the operator approves (except trivial one-off captures where operator already supplied the full map).
- **Mark curation honestly** — set `transcript_curation: curated_sectioned` and/or append a dated receipt to `editorial_note` / `source_note` **on ship only**, not on outline-only passes.

## Eligibility (`source_form` + channel)

| Surface | Default |
| --- | --- |
| YouTube **`interview`** (guest on channel) | **In scope** — sections + speaker-boundary fixes |
| YouTube **`solo`** monologue | **In scope** — thematic sections |
| **`substack-post`** / **`newsletter`** / authored essay | **Out of scope** — not YouTube channel content |
| `panel` | Out of scope unless operator names a host–guest spine to section |
| `clip` | Out of scope — section a full parent capture instead |

Confirm `source_form`, `kind`, and YouTube signals (`source_type`, `channel_slug`, `source_url`) from frontmatter after land. If missing, infer from body (turn-taking transcript vs authored prose) and state the assumption. When in doubt on authored vs channel, **abstain**.

## Transcript body markers

`detect_body_marker()` in `scripts/transcript_section_curation.py` (`BODY_MARKERS`) accepts:

| Marker | Typical surface |
| --- | --- |
| `## Transcript\n` | Default statecraft solo/interview lands |
| `## Part I: Full transcript\n` | Long-form provenance packets in sibling repos |
| `## Cleaned Transcript\n` | Post-**`source-clean`** / ASR-normalized captures (e.g. Dialogue Works clean wrapper) |

**Do not** rename `## Cleaned Transcript` → `## Transcript` before sectioning for tooling compatibility — detection handles both; **ship preserves** whichever marker was present (`write_sectioned_capture` rewrites using the detected marker).

Pass `--body-marker` only when auto-detect is ambiguous.

## Outline phase (plan — required before ship)

**Stop here** when activation is **`source-section outline`** or operator says **`outline only`** / **`plan map`**.

1. **Confirm landed capture** — real transcript body under a standard marker (`## Transcript`, `## Cleaned Transcript`, or `## Part I: Full transcript`). Not a shell or excerpt-only stub.
2. **Read once** — bounded read of the flat body (after optional **`source-clean`** when ASR would block anchor choice).
3. **Propose section map in chat** — numbered list (~6–14 rows). Each row:
   - **Title** — Title Case, `Topic — Subtopic` (becomes `### …` on ship)
   - **Anchor** — verbatim phrase expected in body (N−1 anchors for N sections; last section → EOF)
   - **Interview only** — optional speaker label if the anchor splits mid-turn (`Host`, `Guest`, or named labels matching the capture)
4. **Operator gate** — wait for approve, revise, or reject. Do not call outline complete if anchors were not checked against the body.
5. **Pin the map** — write or update `scripts/patch_<slug>_sections.py` **or** a day batch such as `scripts/patch_YYYY_MM_DD_day_sections.py` when the operator is curating a compose day. Each entry holds `titles`, `anchors`, and optional interview `speaker_cleanup` tuples. Map must survive chat; chat-only maps are not durable.

**Outline deliverable (report even when stopping):**

```text
capture: <path>
source_form: solo | interview
sections: N
1. Title — anchor: "<phrase>" [speaker: Host if interview]
…
pinned: scripts/patch_<slug>_sections.py | not yet pinned
body mutated: no
```

## Ship phase (after operator approval)

Run only when the outline is approved or operator supplied a complete map up front.

1. **Optional light ASR** — duplicate-word / obvious name fixes only when they do not change argument; defer heavy tiers to **`source-clean`** (run **before** sectioning when ASR is load-bearing).
2. **Insert sections** — `insert_sections(body, SECTION_TITLES, SECTION_ANCHORS)`; last section runs to EOF.
3. **Paragraph reflow** — `reflow_section_paragraphs(body)` (default on in `write_sectioned_capture`; skip when operator says **`no paragraph reflow`**).
4. **Speaker repair (interview)** — prepend `**Speaker:**` at section opens when anchors split mid-turn; strip duplicate speaker lines before `###` headings.
5. **Frontmatter receipt** — `transcript_curation: curated_sectioned` + dated note tail.
6. **Verify** — section count, anchor uniqueness, no truncated final section, word count stable ± light ASR deltas only.
7. **Navigation receipt** — report section chunk stats **and** paragraph stats; flag quality warnings (ship phase):

```text
navigation: sections=N  min=…w  med=…w  max=…w  chunk_cv=…%
paras: total=…  min=…w  med=…w  max=…w
warnings: [section <100w | section >1500w | section N single-paragraph megablock >200w | section N para M >150w | slug titles remain] | none
```

Optional CLI for a landed day batch:

```bash
python scripts/quantify_section_nav.py --day YYYY-MM-DD
```

**Chunk quality targets (editorial, not hard fail):** prefer sections **~400–1,200 words**; flag any **< 100 w** (micro-sliver) or **> ~1,500 w** (mega-hop). Prefer **3–8 paragraphs per ~700w section**; flag any paragraph **> ~150 w** or a **single-paragraph section > ~200 w**. Even chunking may require re-section with new anchors — outline phase again; do not silent-ship uneven maps without naming warnings.

**One-turn shortcut:** When operator passes a pre-approved map and says **ship**, skip re-proposing the outline but still name titles + anchor count in the receipt.

## Section map rules

- **N sections → N−1 anchors** (unless documented `anchor_slice` when section 1 naturally starts at document open and anchor 0 would duplicate).
- Anchors must be **unique** in the body after cleanup pass applied.
- Prefer anchors at **speaker turn starts** or unmistakable topic pivots.
- **Title pattern:** `### {Topic} — {Subtopic}` (em dash); stable across re-runs.

## Modes

| Mode | When | Action |
| --- | --- | --- |
| **Outline only** | `source-section outline` / `outline only` | Propose map + pin script; **no body edit** |
| **Anchor insert** | Flat body, approved map | `insert_sections` / `write_sectioned_capture` + speaker fixes |
| **Slug retitle** | Body already has bootstrap `Segment N — …` or auto-slug headings under `###` | **`write_slug_retitle_capture`** — old heading → thematic Title Case pairs; **no body re-cut** |
| **Thematic retitle** | Title Case headings present but topic labels wrong | Same as slug retitle with old→new title map |
| **Re-section** | Operator explicitly requests new map or chunk quality failed | outline phase again; new anchors on flat export or manual unsection first |
| **Paragraph reflow only** | Body already `curated_sectioned`; operator wants readability fix without new section map | **`write_paragraph_reflow_capture`** — reflow within existing `###` blocks only |

Default **reject** full re-section if body already has **thematic** Title Case `### Topic — Subtopic` unless operator says re-section. If headings are **bootstrap slugs**, default next step is **retitle**, not re-section from flat.

## Relationship to sibling skills

| Skill | Role |
| --- | --- |
| [`statecraft-source-intake`](../statecraft-source-intake/SKILL.md) | Land flat capture; family / filename / provenance |
| [`source-clean`](../source-clean/SKILL.md) | ASR tiers, scaffold, entity pass — usually **before** sectioning |
| [`wire-verify`](../wire-verify/SKILL.md) | Desk-hook receipts — independent |

**Do not** fold this skill into source-intake default land — intake stays verbatim-first; sectioning is an explicit follow-on for solo/interview study surfaces.

## Agent behavior norms

- **Human authority** — Section titles are editorial judgment; operator approves map before ship on large captures.
- **No silent overwrite** — If `transcript_curation: curated_sectioned` already set, stop or ask before re-sectioning.
- **Abstention** — If anchors fail or body is too fragmentary, report failure; do not invent filler text.

## Verification / Proof Standard

**Outline-only:** report capture path, `source_form`, numbered titles + anchors, pin path, `body mutated: no`. Word-count and frontmatter receipt fields are **N/A**.

**Ship:** additionally report speaker-fix scope, word count before/after, `transcript_curation` receipt, **navigation receipt** (min/med/max section words, warnings), git durability.

Report:

- capture path and `source_form`
- phase completed: outline | ship | both
- section count and heading list (titles only)
- anchors used (count matches N−1)
- speaker-fix passes applied (interview) or skipped (solo) — ship only
- word count before/after (substance must not shrink) — ship only
- **navigation receipt** — section word min / median / max; chunk CV; **paragraph** min / median / max; quality warnings — ship only
- frontmatter receipt field updated — ship only
- git durability: on disk / not committed / not pushed unless EXECUTE lane

Do not call **outline** complete unless the numbered map is in the reply and anchors were checked (or misses are named).

Do not call **ship** complete unless:

- the input capture path is named
- eligibility (YouTube channel transcript; not authored) is confirmed
- skipped steps are marked with reason
- uncertainty or anchor miss is stated explicitly

If verification cannot be completed:

- state what was not verified
- leave capture unsectioned rather than shipping a broken map


## Cursor / strategy-codex instance

# Cursor appendix — `source-section`

Host-specific paths for **strategy-codex**. Portable core: [`skills/source-section/SKILL.md`](../../skills/source-section/SKILL.md).

## Shared library

```text
scripts/transcript_section_curation.py
```

Import (Windows-safe — in-process for batch):

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path("scripts").resolve()))
from transcript_section_curation import (
    insert_sections,
    reflow_section_paragraphs,
    write_sectioned_capture,
    write_paragraph_reflow_capture,
    write_slug_retitle_capture,
    common_asr_cleanup,
    prepend_speaker_at_section_opens,
    strip_speakers_before_section_headings,
)
```

## Body markers (statecraft archive)

| Marker | Typical surface |
| --- | --- |
| `## Transcript\n` | Default `source-archive/statecraft/**/source-*.md` |
| `## Part I: Full transcript\n` | Long-form provenance packets in sibling repos |
| `## Cleaned Transcript\n` | Post-**`source-clean`** / ASR-normalized captures (Dialogue Works clean wrapper, etc.) |

Auto-detect via `detect_body_marker()` unless `--body-marker` is passed. **Do not** rename `## Cleaned Transcript` → `## Transcript` before sectioning — detection handles both; ship preserves the marker in use.

## Per-source patch scripts

Pin section maps under `scripts/patch_<slug>_sections.py` (pattern from truth-pipeline curation). **Day-batch pins** are OK when curating a compose day — e.g. `scripts/patch_2026_06_25_day_sections.py` holding multiple capture entries.

Each script entry should only hold:

- `titles` / `anchors` (or `SECTION_TITLES` / `SECTION_ANCHORS`)
- optional `asr_cleanup` overrides
- interview `speaker_cleanup` fixes

Call `write_sectioned_capture()` from `main()` for flat bodies; use `write_slug_retitle_capture()` for bootstrap slug → thematic retitle only.

## Navigation quant receipt

After ship or before daily synthesis on a multi-capture day:

```bash
python scripts/quantify_section_nav.py --day YYYY-MM-DD
```

Reports per-capture chunk min/med/max, flat vs sectioned, slug-title warnings, and day-level scan reduction estimate. Wire into **`source-section`** ship receipt when operator asks for metrics.

## Default CLI-shaped one-liner

After map is pinned in a patch script:

```bash
python scripts/patch_<slug>_sections.py
```

No repo-wide batch sectioner — maps stay per capture.

## Pipeline hook (source-intake step 5)

After land (+ optional **`source-clean`**) on a **YouTube channel** capture with **`source_form: solo`** or **`source_form: interview`**, apply **`source-section` § Post-land nudge** when body is flat (≥ ~4k words) or slug-only — state the one-line payoff explicitly; offer **`source-section outline`** first; ship only after map approval. **Not** for authored Substack/newsletter lands. Not automatic on every intake.

## Related docs

- [`source-archive/statecraft/README.md`](../../../statecraft/README.md)
- [`skills/source-clean/SKILL.md`](../../skills/source-clean/SKILL.md)
- [`skills/statecraft-source-intake/SKILL.md`](../../skills/statecraft-source-intake/SKILL.md)
