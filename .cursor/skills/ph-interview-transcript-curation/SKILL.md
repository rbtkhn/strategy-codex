---
name: ph-interview-transcript-curation
description: 'PH interview transcript curation — section rails, host/turn speaker labeling, ASR repair, pass ladder, validate, PH-TRANSCRIPT-EDIT ship. Canonical repo: predictive-history interviews/ packets. Not statecraft source-clean.'
preferred_activation: PH transcript pass
activation: PH transcript pass
portable: true
version: 0.3.0
category: truth-pipeline
status: active
scope_class: repo-governed
tags:
- operator
- predictive-history
- transcript
- interviews
portable_source: skills/ph-interview-transcript-curation/SKILL.md
synced_by: sync_portable_skills.py
---
# PH interview transcript curation

**Preferred activation:** **`PH transcript pass`** · **`interview section pass`** · **`interview turn pass`** · **`PH-TRANSCRIPT-EDIT`**

**Canonical edit surface:** [`predictive-history`](https://github.com/rbtkhn/predictive-history) repo — `interviews/interview-YYYY-MM-DD-{host-slug}/`. Edit from strategy-codex when operator grants PH repo access; do **not** edit `public/predictive-history/` mirror by hand (refresh via `sync_predictive_history_mirror.py` after push).

## Exemplars

| Interview | Shape | Reference |
|-----------|--------|-----------|
| Tucker vi-11 | Clean promote — sections + named speaker turns in one pass | [`interview-2026-03-20-tucker-carlson`](https://github.com/rbtkhn/predictive-history/tree/main/interviews/interview-2026-03-20-tucker-carlson) · `d475974` |
| DOAC ext-doac-01 | ASR/paste dump — **incremental pass ladder**; **14/14 section rails pass C complete** (2026-06-26) | [`interview-2026-05-07-diary-of-a-ceo`](https://github.com/rbtkhn/predictive-history/tree/main/interviews/interview-2026-05-07-diary-of-a-ceo) · sections `ddeeff7`; pass 13 `a6f86e8` |

### DOAC ext-doac-01 — pass ladder (reference)

Read packet `README.md` **Transcript pass N** notes for receipts. **Pass C complete** on all 14 Part I section rails; sponsor/read blocks and Cold Open montage remain **unlabeled by design**.

| Pass | Date | Scope | Notes |
|------|------|--------|--------|
| 2 | 2026-06-25 | **A + B** | 14 Title Case rails; `>>` → **Steven Bartlett:**; light ASR |
| 3 | 2026-06-26 | **B** | Batch `>>` / cold-open tags |
| 4 | 2026-06-26 | **C** | Iran Topography, Attrition, and Hormuz (~22 exchanges) |
| 5 | 2026-06-26 | **C** | National Defense Strategy — Western Hemisphere |
| 6 | 2026-06-26 | **C** | War Phases — Ground Troops and IRGC |
| 7 | 2026-06-26 | **C** (batch) | Remaining 11 sections — mechanical; superseded by hand passes 8–13 where listed below |
| 8 | 2026-06-26 | **C** (hand) | Chess Grand Strategies — **lecture + Mhm/Okay interjections** |
| 9 | 2026-06-26 | **C** (hand) | Eight Predictions — **Q&A chain** (constitution, draft, AI surveillance) |
| 10 | 2026-06-26 | **C** (hand) | Global Chokepoints — shadow fleet, three-prong Iran, wire-read insert |
| 11 | 2026-06-26 | **C** (hand) | Interview Open + Timeline |
| 12 | 2026-06-26 | **C** (hand) | Israel · East Asia (NK game-theory) · Community · Hermetic closing |
| 13 | 2026-06-26 | **C** (hand) | Plato Cave — cave allegory, media-ownership Q&A, Spengler close |

### DOAC — section rails × pass-C status

| # | Section rail | Pass-C receipt | Pattern |
|---|----------------|----------------|---------|
| 1 | Cold Open — Predictions Teaser | Partial labels only | Montage / teaser — do not force full turns |
| 2 | Interview Open — Predictions and Petrodollar | Pass 11 | Q&A + long Jiang monologue; BRICS/petrodollar |
| 3 | Iran Topography, Attrition, and Hormuz | Pass 4 | Map lecture + clear host questions |
| 4 | National Defense Strategy — Western Hemisphere | Pass 5 | Map + NDS lecture |
| 5 | War Phases — Ground Troops and IRGC | Pass 6 | Phased war lecture + Q&A |
| 6 | Chess Grand Strategies and WWIII Players | Pass 8 | **Lecture + embedded Mhm/Right/Exactly** |
| 7 | Global Chokepoints — Russia Shadow Fleet | Pass 10 | Lecture + seizure Q&A; Steven wire read |
| 8 | Timeline — Trump Term Limits and Forever War | Pass 11 | Host timeline questions + Jiang attrition |
| 9 | Eight Predictions — Trump Third Term and AI State | Pass 9 | **Prediction box Q&A chain** |
| 10 | Israel — Greater Israel, NATO, and Odessa | Pass 12 | Prediction pivots + Odessa map |
| 11 | East Asia Flashpoints — North Korea | Pass 12 | **NK game-theory roleplay** |
| 12 | Community, Hope, and Bronze Age Collapse | Pass 12 | Average-person + Bronze Age; Steve Keen |
| 13 | Plato Cave — Reality and Financial Elite | Pass 13 | Allegory + financial-elite layers + media Q&A |
| 14 | Hermetic Philosophy, Life Advice, and Closing Tradition | Pass 12 | Advice + wife closing + outro |

**Unlabeled by design (DOAC):** Shopify / Pipedrive / DOAC Circle sponsor reads; YouTube algorithm outro; ambiguous merged lines → README unresolved (e.g. Araghchi title).

### Pass-C hand-fix patterns (DOAC)

Use when batch pass 7-style heuristics mis-attribute lecture blocks to the host.

| Pattern | When | Technique |
|---------|------|-----------|
| **Q&A chain** | Prediction box, constitution, draft | One Steven question per label; Jiang answer blocks |
| **Lecture + interjections** | Chess, Plato allegory, chokepoints | Pull standalone **Mhm**, **Okay**, **Right?**, **Exactly** to Steven; keep rhetorical pivots on Jiang when teaching |
| **Game-theory roleplay** | East Asia NK extortion | Jiang as NK voice; Steven as interlocutor |
| **Wire read** | Global Chokepoints tanker seizures | Steven reads verified facts; Jiang frames |
| **Host monologue** | Plato Sapiens / independent-media | Long Steven blocks stay under Steven |
| **Stop rule** | Low confidence | README unresolved; do not guess |


## Use this skill when

- A promoted PH **interview** transcript needs curation: **Title Case section rails**, **speaker/turn labeling**, ASR/toponym cleanup, duplicate-line removal
- Operator names an interview id (`vi-11`, `ext-doac-01`, `interview-2026-05-07-diary-of-a-ceo`) or asks to repeat Tucker or DOAC patterns
- Transcript is already public under `interviews/` with `## Part I: Full transcript` (workshop or external promote)

## Do not use when

- Source is **statecraft archive** (`source-archive/statecraft/**/source-*.md`) — use [`source-clean`](../source-clean/SKILL.md)
- Job is **first promote / external intake** (card, manifest, intake script) — separate promote slice; see CURSOR_APPENDIX § External intake sibling
- Job is commentary, essay prose, or YouTube public copy — other skills
- Operator wants **audio-verified verbatim** — this skill is **transcript-logic only** unless operator supplies audio or caption SSOT

## Scope gate

| In scope | Out of scope |
|----------|--------------|
| `{slug}.md` transcript body + YAML frontmatter | Commentary canvas rewrites |
| Packet `README.md` pass notes + unresolved entities | Card/manifest unless validate regenerates indexes |
| Section rails, host markers, turn labeling (scoped) | Full-file turn labeling when operator scoped one section only |
| Index refresh via `civ_ph validate` (auto) | `continuity/predictive-history/` frozen workshop |

## Interview shapes

| Shape | Typical source | Default ladder |
|-------|----------------|----------------|
| **Clean promote** | Workshop promotion, pre-labeled capture | Pass **A + C** together (Tucker pattern) |
| **ASR / paste dump** | External intake, `>>` markers, merged paragraphs | **A → B → C** by section or block; do not block ship on full-file turns |

## Pass ladder

Run the **lowest pass still needed**. One commit slice per pass when practical. Increment **Transcript pass N** in README each time.

| Pass | Activation stub | Work |
|------|-----------------|------|
| **A — Section rails** | `interview section pass` | `### Title Case` topic headings under `## Part I: Full transcript`; light dedup |
| **B — Host surface** | `PH transcript pass` (host cleanup) | `>>` → named host; cold open / sponsor block tags; inline host/guest splits when obvious |
| **C — Turn labeling** | `interview turn pass` | `**Host Name:**` / `**Guest Name:**` turn-by-turn within **operator-scoped section(s)**; light ASR in touched blocks |
| **D — ASR / entity** | (with B or C) | Places, names, acronyms; preserve load-bearing quotes; list **unresolved** in README |

**Stop rule:** merged host/guest paragraphs with ambiguous turn breaks → **README unresolved**; do not guess splits without transcript-logic confidence.

**Do not** require full-file turn labeling in pass A on long ASR interviews (DOAC ~900 lines). Ship readable section rails first.

## Default execution order

1. **Read first half** — note shape (clean vs ASR), existing labels, sponsor/read boundaries, which passes already landed (README pass notes).
2. **Pick pass** — A only, A+B, or C on named section(s); Tucker one-shot = A+C together when capture is already clean.
3. **Section rails (A)** — plan Title Case headings at topic pivots; count is **per interview** (Tucker = 7; DOAC = 14; not a fixed template).
4. **Host surface (B)** — when `>>` or cold-open montage remains; convert to packet host name (e.g. `**Steven Bartlett:**`).
5. **Turn labeling (C)** — scoped section only unless operator expands scope; split clear Q&A; keep Jiang monologue blocks under `**Jiang Xueqin:**` when turn breaks are uncertain → unresolved.
6. **ASR (D)** — in the same edit as B/C for touched blocks only.
7. **Dedup** — duplicate sponsor blocks or closing questions when transcript-logic shows a clear duplicate.
8. **Frontmatter** — set or update when any curation lands:
   - `transcript_curation: curated_sectioned` (after pass A or later)
   - `transcript_fidelity: curated_pass` (after any B/C/D work, or full Tucker pass)
   - `fidelity_reviewed_at: YYYY-MM-DD` (session date)
   - leave `transcript_status`, `review_status`, workshop ids unchanged unless operator directs
9. **README provenance** — **Transcript pass N (YYYY-MM-DD):** pass letter(s), section scope, turn count or exchange count, unresolved entities.
10. **Validate** — from PH repo root:
    ```bash
    PYTHONPATH=src python -m civ_ph.cli validate
    python -m pytest -q
    ```
11. **Commit + push** — prefix **`PH-TRANSCRIPT-EDIT:`** · scope pass + section in subject when pass C.
12. **Mirror (optional)** — from strategy-codex: `python scripts/sync_predictive_history_mirror.py`; commit with `[predictive-history-sync]` when operator asks **EXECUTE** on mirror.

## Section heading rules

- **Title Case** ASCII headings (Tucker: `### Iran Attrition and Global Stakes`; DOAC: `### Iran Topography, Attrition, and Hormuz`)
- Insert **under** `## Part I: Full transcript`, **above** the first line of each topic block
- Headings describe **topic pivot**, not timestamps
- Do not add sections outside Part I unless packet structure already uses other parts

## Turn labeling rules

- Use **named speakers** when known (`**Tucker Carlson:**` / `**Jiang Xueqin:**`; DOAC: `**Steven Bartlett:**` / `**Jiang Xueqin:**`) — not generic Host/Guest when packet README names the host
- One speaker label per turn; continuation paragraphs stay under the same label until a clear host question or guest answer pivot
- Blank line between speaker turns when the block is long (Tucker exemplar)
- **Sponsor/read blocks:** omit turn labels unless operator asks; may use `[Sponsor segment omitted.]` (Tucker) or leave unlabeled (DOAC)
- **Transcript-logic only** — do not claim audio verification

## ASR / entity discipline

- Infer speakers from turn-taking and host/guest names; list ambiguous names in README (Tucker: "John" at CUFI — likely Hagee, not pinned)
- When editing from strategy-codex, apply operator place-name policy in **framing** around quotes ([Kiev/Kharkov rule](../../.cursor/rules/strategy-codex-kiev-spelling.mdc)) — preserve source spelling inside load-bearing quotes when load-bearing
- Do not rewrite argument, add facts, or smooth into editorial essay prose

## Windows harness

- One **Shell** per turn; one **StrReplace/Write path** per file per turn when possible
- Bounded **Read** on known interview paths — no repo-wide grep storms
- After hang: Read/Write only until patch lands ([agent-tool-latency-discipline](../../.cursor/rules/agent-tool-latency-discipline.mdc))

## Verification / Proof Standard

Do not call a pass complete unless:

- interview **source_id** and packet path are named
- **pass letter(s)** (A/B/C/D) and **section scope** stated
- section heading list when pass A (or already present) — count + names
- for pass C: **turn/exchange count** or labeled section name
- speaker/ASR scope stated (which section or line range)
- unresolved entities listed in README or reply
- `validate` exit + card count reported
- `pytest` exit reported
- commit hash + push status (or explicit defer)
- skipped steps marked with reason

Evidence to report:

- files touched
- pass ladder step(s) completed
- section heading list (if relevant)
- turn labeling scope + approximate exchange count (if pass C)
- validate/pytest commands and exit codes
- commit message and hash
- mirror sync receipt if run

If verification cannot be completed:

- state what was not verified
- stop before push or mirror commit
- return bounded partial for operator review

## Related skills

| Task | Skill |
|------|--------|
| Statecraft archive ASR | [`source-clean`](../source-clean/SKILL.md) |
| PH external interview promote | `scripts/intake_interview_external.py` (PH repo) — sibling workflow |
| Mirror refresh | `scripts/sync_predictive_history_mirror.py` (strategy-codex) |
| Skill capture | [`extract-skill-from-session`](../extract-skill-from-session/SKILL.md) |


## Cursor / strategy-codex instance

Cursor-only paths for [ph-interview-transcript-curation/SKILL.md](../../../skills/ph-interview-transcript-curation/SKILL.md).

## Repo layout

| Surface | Path |
|---------|------|
| Canonical PH repo (edit here) | `$PREDICTIVE_HISTORY_ROOT` or operator clone of `rbtkhn/predictive-history` |
| Inbound mirror (do not hand-edit) | `public/predictive-history/` in strategy-codex |
| Frozen workshop (do not edit unless revived) | `continuity/predictive-history/` |

## Known interview packets

Catalog: `predictive-history/docs/predictive-history-index.md` · **Provenance** section.

| Packet | Role |
|--------|------|
| `interviews/interview-2026-03-20-tucker-carlson/` (vi-11, `d475974`) | One-shot exemplar — sections + named turns |
| `interviews/interview-2026-05-07-diary-of-a-ceo/` (ext-doac-01) | Pass-ladder exemplar — **14/14 section rails pass C complete** (pass 13 `a6f86e8`); see SKILL § DOAC pass ladder |

## Commands (PH repo root)

```bash
PYTHONPATH=src python -m civ_ph.cli validate
python -m pytest -q
git -c user.name="Robert Kuhne" -c user.email="rbtkhn@users.noreply.github.com" commit -m "PH-TRANSCRIPT-EDIT: …"
git push origin main
```

## Mirror (strategy-codex)

```bash
python scripts/sync_predictive_history_mirror.py
# commit message must include [predictive-history-sync]
```

## External intake sibling

Promote **new** external interviews (not pass-2) via PH `scripts/intake_interview_external.py` — separate commit slice from this skill. Exclude sidecar `_land_*` folders from commits.

## Portable plumbing

| Topic | Path |
|-------|------|
| Manifest | [skills/manifest.yaml](../../../skills/manifest.yaml) |
| Backlog | [skills/skill-candidates.md](../../../skills/skill-candidates.md) |
| Sync | `python3 scripts/sync_portable_skills.py --skill ph-interview-transcript-curation --verify` |
| Validate | `python3 scripts/validate_skills.py` |
