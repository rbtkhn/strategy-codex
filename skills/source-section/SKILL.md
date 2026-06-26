---
name: source-section
description: Post-intake transcript section curation for solo and interview source captures — Title Case ### headings, anchor splits, speaker-boundary fixes; not first-pass land, synthesis, or wire-verify.
preferred_activation: source-section
activation: source-section
portable: true
version: 1.0.2
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
---
# Source section (`source-section`)

**Preferred activation:** **`source-section`** (or **`source section`**, **`section source`**). **Outline-only:** **`source-section outline`** (or **`section outline`**) — plan and pin the map; do not mutate body until operator approves ship.

**Scope:** Post-land **editorial structure** for long **solo** and **interview** transcript captures — not first-pass intake, not ASR tier cleanup, not synthesis.

**Pipeline position:** **`source-intake`** (land flat verbatim) → optional **`source-clean`** → **`source-section`** (outline → approve → ship) → downstream study / synthesis.

## Use this skill when

- A transcript capture is already landed with `source_form: solo` or `source_form: interview`
- Operator wants **Title Case** `### … — …` section headings for navigation and study (not lowercase slug headers)
- You have or can derive a **section map**: ~6–14 thematic headings + **anchor phrases** (N−1 anchors for N sections; last section → EOF)
- **Interview** captures need **speaker labels** restored at section splits after anchor insertion
- **Solo** monologue captures need thematic breaks only (usually no speaker repair)

## Do not use when

- Capture is not yet landed — run **`source-intake`** first
- `source_form` is `panel`, `clip`, `newsletter`, `article`, or `roundup` unless operator explicitly overrides
- Job is ASR / proper-noun cleanup only — use **`source-clean`**
- Job is wire triage — use **`wire-verify`**
- Job is interpretive synthesis, notebook weave, or lane drafting
- Operator wants summary or paraphrase instead of full transcript body

## Core law

- **Intake lands truth; sectioning organizes reading.** Do not substitute synthesis for transcript body in the archive object.
- **Verbatim substance preserved** — sectioning adds headings and light mechanical fixes only; no argument rewrite.
- **Headings are editorial** — Title Case thematic labels (`### Show Open — …`), never machine slug headers (`### iran-attrition-…`) on operator surfaces.
- **Anchors are pinned** — per-source section maps must be reproducible (script with `SECTION_TITLES` + `SECTION_ANCHORS`, or checked-in patch recipe).
- **Outline before ship** — propose and pin the section map; **do not** insert headings into the capture body until the operator approves (except trivial one-off captures where operator already supplied the full map).
- **Mark curation honestly** — set `transcript_curation: curated_sectioned` and/or append a dated receipt to `editorial_note` / `source_note` **on ship only**, not on outline-only passes.

## Eligibility (`source_form`)

| `source_form` | Default |
| --- | --- |
| `solo` | **In scope** — thematic sections; rare speaker repair |
| `interview` | **In scope** — sections + speaker-boundary fixes at splits |
| `panel` | Out of scope unless operator names a host–guest spine to section |
| `clip` | Out of scope — section a full parent capture instead |

Confirm `source_form` from frontmatter after land. If missing, infer from body (one dominant speaker vs turn-taking) and state the assumption.

## Outline phase (plan — required before ship)

**Stop here** when activation is **`source-section outline`** or operator says **`outline only`** / **`plan map`**.

1. **Confirm landed capture** — real transcript body under a standard marker (`## Transcript` or host-equivalent). Not a shell or excerpt-only stub.
2. **Read once** — bounded read of the flat body (after optional **`source-clean`** when ASR would block anchor choice).
3. **Propose section map in chat** — numbered list (~6–14 rows). Each row:
   - **Title** — Title Case, `Topic — Subtopic` (becomes `### …` on ship)
   - **Anchor** — verbatim phrase expected in body (N−1 anchors for N sections; last section → EOF)
   - **Interview only** — optional speaker label if the anchor splits mid-turn (`Host`, `Guest`, or named labels matching the capture)
4. **Operator gate** — wait for approve, revise, or reject. Do not call outline complete if anchors were not checked against the body.
5. **Pin the map** — write or update `scripts/patch_<slug>_sections.py` (or equivalent) holding `SECTION_TITLES`, `SECTION_ANCHORS`, and interview `speaker_cleanup` tuples. Map must survive chat; chat-only maps are not durable.

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
3. **Speaker repair (interview)** — prepend `**Speaker:**` at section opens when anchors split mid-turn; strip duplicate speaker lines before `###` headings.
4. **Frontmatter receipt** — `transcript_curation: curated_sectioned` + dated note tail.
5. **Verify** — section count, anchor uniqueness, no truncated final section, word count stable ± light ASR deltas only.

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
| **Anchor insert** | Flat body, approved map | `insert_sections` + speaker fixes |
| **Slug retitle** | Legacy lowercase slug headings already present | `apply_slug_to_title_headings` only |
| **Re-section** | Operator explicitly requests new map | outline phase again; new anchors on flat export or manual unsection first |

Default **reject** if body already starts with `### Title Case` unless operator says re-section.

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

**Ship:** additionally report speaker-fix scope, word count before/after, `transcript_curation` receipt, git durability.

Report:

- capture path and `source_form`
- phase completed: outline | ship | both
- section count and heading list (titles only)
- anchors used (count matches N−1)
- speaker-fix passes applied (interview) or skipped (solo) — ship only
- word count before/after (substance must not shrink) — ship only
- frontmatter receipt field updated — ship only
- git durability: on disk / not committed / not pushed unless EXECUTE lane

Do not call **outline** complete unless the numbered map is in the reply and anchors were checked (or misses are named).

Do not call **ship** complete unless:

- the input capture path is named
- eligibility (`solo` / `interview`) is confirmed
- skipped steps are marked with reason
- uncertainty or anchor miss is stated explicitly

If verification cannot be completed:

- state what was not verified
- leave capture unsectioned rather than shipping a broken map
