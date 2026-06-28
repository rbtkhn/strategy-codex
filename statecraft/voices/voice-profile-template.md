WORK only; not Record.

# Voice profile template

Purpose: single **shape contract** for `statecraft/voices/<speaker>/<speaker>-profile.md` and `statecraft/channels/<host>/<host>-profile.md` after migration. Placement law lives in [README.md § Speaker profile law](README.md#speaker-profile-law). Upstream minimal scaffold: [strategy-codex-template-profile.md](../../codex/strategy-codex-template-profile.md).

**Exemplars:**

- **Full (Tier A linguistic):** [barnes/barnes-profile.md](barnes/barnes-profile.md) · [mercouris/mercouris-profile.md](mercouris/mercouris-profile.md) · [mearsheimer/mearsheimer-profile.md](mearsheimer/mearsheimer-profile.md)
- **Seed:** [weichert/weichert-profile.md](weichert/weichert-profile.md) · [pape/pape-profile.md](pape/pape-profile.md)

**Host profiles** reuse the same spine; swap shelf pointers and role framing for host-law / guest-transformation jobs. Exemplar (host also has voice shelf): [davis/davis-profile.md](davis/davis-profile.md).

---

## What a profile is (and is not)

A voice profile is the **identity-and-voice hub**:

- expert_id, role, pairing tags, voice tier (compact + detailed when Tier A)
- **structured linguistic style fingerprint** (detailed tables when Tier A; stub when Tier B)
- convergence/tension stubs, signature mechanisms, failure modes (when mature)
- public **Links** hub and ingest routing notes

It is **not**:

- transcript provenance (→ `*-source-index.md`, archive)
- arc motion (→ `*-arc.md`)
- task routing (→ `*-routing.md`)
- load-bearing synthesis (→ `statecraft/notes/`, daily, essays)
- **`strategy-expert-<id>-mind.md`** as structured register SSOT — **compatibility quote bank only** ([VOICES-SUPERSEDE-MINDS.md](../../docs/skill-work/work-strategy/VOICES-SUPERSEDE-MINDS.md))

---

## Required sections (all migrated profiles)

| Section | Required | Notes |
|---|---|---|
| Title + `expert_id` | yes | `# Strategy expert — <Name> (\`<expert_id>\`)` |
| Fence | yes | `WORK only; not Record.` |
| Canonical pointers | yes | **Canonical profile**, **Canonical shelf**, **Canonical index** (commentator-threads row when applicable) |
| `## Introduction` | yes | Short orienting paragraph — who, what lane, why reused |
| `## Identity` | yes | Table: Name, expert_id, Role, Default grep tags, Typical pairings, Notebook-use tags |
| `## Voice fingerprint (compact)` | yes | Tier + last-reviewed; anchor `id="voice-fingerprint-compact"` |
| `## Linguistic style fingerprint (detailed)` | yes | Tier **B** → one-line stub; Tier **A** → 8-family tables (anchor `id="linguistic-style-fingerprint-detailed"`) |
| `## Convergence fingerprint` | yes | Full prose or explicit seed stub |
| `## Tension fingerprint` | yes | Full prose or explicit seed stub |
| `## Links` | yes | `### Social media`, `### Substack`, `### Other links` |

---

## Recommended sections (mature or seed-stubbed)

| Section | When |
|---|---|
| `## Signature mechanisms` | Always stub or fill — mechanism vocabulary is load-bearing |
| `## Failure modes / overreads` | When analyst-tier claims need verify discipline |
| `## Active weave cues` | When same-week pairings are routine |
| `## Ingest note` | When intake family is non-obvious (Nawfal, Substack mix, etc.) |
| `## Statecraft / AI` or bounded notes table | When thematic notes live under `statecraft/notes/` |
| `## Seed` | When automation mirrors commentator index rows |
| Mind pointer block | When `strategy-expert-<id>-mind.md` or CIV-MIND exists — quote bank + role/contrast; **not** duplicate of detailed tables |
| Orthogonality notes | When triad/pair contrast is load-bearing — prefer shared SSOT under `_scratch/`; profiles link, Family 8 stubs only |
| Intake receipt links (footer) | When Nawfal/archive captures are the profile's anchor set |

**Seed maturity:** mark thin sections with `*Seed profile — operator extends when upgraded.*` or `*Seed — extend when Tier A.*` rather than omitting the heading.

---

## File scaffold (copy and replace)

```md
# Strategy expert — <Full name> (`<expert_id>`)
<!-- word_count: <n> -->

WORK only; not Record.

**Canonical profile:** this file.
**Canonical shelf:** [README.md](README.md) · [index.md](index.md)
**Canonical index:** [strategy-commentator-threads.md](../../codex/strategy-commentator-threads.md) — **`<expert_id>`** lane.

---

## Introduction

<One short paragraph: who this speaker is, what translation job they perform, primary recurring surface(s).>

## Identity

| Field | Value |
|-------|-------|
| **Name** | <Name> (`@handle` when stable) |
| **expert_id** | `<expert_id>` |
| **Role** | <One-line lane job> |
| **Default grep tags** | `<tags>` |
| **Typical pairings** | × `<expert>`, … |
| **Notebook-use tags** | `validate`, `orient`, … |

<a id="voice-fingerprint-compact"></a>

## Voice fingerprint (compact) — Tier B

| Field | Value |
|-------|-------|
| **Voice tier** | `B` |
| **Voice fingerprint — last reviewed** | `YYYY-MM` |

Promotion and refresh defaults: [voice-profile-template.md § Voice fingerprint (compact)](voice-profile-template.md#voice-fingerprint-compact).

<a id="linguistic-style-fingerprint-detailed"></a>

## Linguistic style fingerprint (detailed)

*Seed — extend when Tier A. See [voice-profile-template.md § Linguistic style fingerprint (detailed)](voice-profile-template.md#linguistic-style-fingerprint-detailed).*

## Convergence fingerprint

*Seed profile — operator extends when upgraded.*

## Tension fingerprint

*Seed profile — operator extends when upgraded.*

## Signature mechanisms

- **<mechanism label>:** <one-line definition>
- …

## Failure modes / overreads

- <claim class that needs wire verify or abstention>

## Active weave cues

- Pair **<speaker>** × **<speaker>** when <condition>.

## Ingest note

- Primary intake family: `<source-archive pattern>`
- Standalone X/Substack: `thread:<expert_id>` — verify operational claims.

## Links

### Social media

- <URL or `- None currently tracked.`>

### Substack

- <URL or `- None currently tracked.`>

### Other links

- <institution / site / archive URLs>
```

Optional footer when captures anchor the profile:

```md
---

**Intake receipts:** [capture slug](<archive-path>) · …
```

---

<a id="voice-fingerprint-compact"></a>

## Voice fingerprint (compact) — template law

- **Tier `B`** is the default for migrated voice profiles until families **1–5 + 8** of the detailed section are operator-reviewed.
- **Tier `A`** = compact table shows `A` **and** `## Linguistic style fingerprint (detailed)` contains filled 8-family rows with example lines.
- **Last reviewed** = month of last operator or assistant pass on compact table **and** detailed linguistic tables (when Tier A).
- **Structured register SSOT** = profile `#linguistic-style-fingerprint-detailed` when Tier A; mind file = extended quote bank + role/contrast until rows migrate.
- Do not merge wire-grade operational claims into voice fingerprint; keep those in failure modes or ingest notes.
- **`tri-mind` choreography deprecated** — [TRI-MIND-DEPRECATED.md](../../docs/skill-work/work-strategy/TRI-MIND-DEPRECATED.md).

---

<a id="linguistic-style-fingerprint-detailed"></a>

## Linguistic style fingerprint (detailed) — template law

**Tier gate**

| Tier | Detailed section |
|---|---|
| **B** | Heading + one stub line (`*Seed — extend when Tier A.*`) |
| **A** | Eight-family table(s) with **pattern**, **example lines**, **anti-pattern** per row |

**Table columns (all voices):**

| Column | Content |
|---|---|
| **Family** | 1–8 family name (see below) |
| **Sub-dimension** | Row topic within the family |
| **Pattern** | Stable habit or move — one line |
| **Example lines** | 1–3 transcript-derived phrases (quoted) |
| **Anti-pattern** | Generic analyst voice or wrong-register habit |

**Extended examples:** link to `strategy-expert-<id>-mind.md` § IV (or equivalent) for quote bank until all rows are migrated.

### Family 1 — Macro rhythm and architecture

| Sub-dimension | Capture |
|---|---|
| Tempo | Sequential vs recursive; constraint-mapping cadence |
| Unit of thought | Person/liability vs state vs civilization |
| Opening grammar | Triad enumerators, short-answer frames, constraint-first |
| Closure grammar | Terminal emphasis, consequence projection |
| Enumeration style | One-two-three vs narrative chain vs case-list |

### Family 2 — Register and sociolinguistic color

**Regional flavor ≠ dialectology.** Family 2 captures **transcript-visible sociolinguistic markers** for in-voice emulation (oral color, regional grounding in lexicon and idiom, formality band). It is **not**:

- phonetic / accent identification or ASR accent classification
- a dialect taxonomy (e.g. Appalachian vs General American isogloss work)
- biographical truth about where a speaker grew up — only **speech-pattern evidence** with archive slug or `mind-legacy` label

When regional grounding matters, split rows: **regional grounding** (where the voice anchors itself) vs **oral colloquial** (how it sounds) vs **geographic-historical lexicon** (Family 4 — political memory vocabulary). Do not infer dialect from host intro alone unless the guest adopts that frame in their own speech.

| Sub-dimension | Capture |
|---|---|
| Regional / cultural grounding | Oral-register markers tied to stated or repeated regional identity — **not** phonology |
| Oral colloquial color | Intensifiers, domestic analogy, folksy idiom (quoted lines) |
| Formality band | Oral argument vs podcast vs written |
| Colloquial bridges | Fillers, incredulity markers |
| Epithets and nicknames | Sardonic labels, mnemonic sobriquets |
| Profanity / bluntness band | Where hedging is refused |

### Family 3 — Sentence-level syntax and punctuation

| Sub-dimension | Capture |
|---|---|
| Sentence length mix | Hammer sentences vs extended enumeration |
| Question types | Rhetorical exposure vs genuine inquiry |
| Modal and probability grammar | Odds, percentages, minimal hedge |
| Punctuation as rhetoric | Terminal periods, dashes |
| Parallelism | Same-rule-across-contexts syntax |

### Family 4 — Lexical signature and recurring metaphors

| Sub-dimension | Capture |
|---|---|
| Load-bearing nouns | jurisdiction, liability, exposure, … |
| Institutional lexicon | DOJ, confirmation, appropriations, … |
| Metaphor families | Recurring image sets |
| Pop/literary borrowings | Film, novel, TV shortcuts |
| Geographic-historical lexicon | Regional political memory vocabulary |

### Family 5 — Epistemic stance (linguistic)

| Sub-dimension | Capture |
|---|---|
| Hedge density | vs other mapped voices |
| Forbidden softeners | hope-based reasoning; institutional self-description |
| Assertive markers | “There’s no question,” blunt verdicts |
| Hypothesis labeling | When claims stay tier-D in speech |
| Wire boundary language | How operational claims are fenced |

### Family 6 — Rhetorical moves (reasoning-in-voice)

| Sub-dimension | Capture |
|---|---|
| Constraint-first opening | Jurisdiction before merits |
| Signature hypotheticals | Badge-stripping, projection filter, … |
| Theater vs substance split | Performative policy language |
| Doctrine archaeology | Cases/statutes with genesis |
| Contrarian consistency test | Same standard across factions |
| Competence verdict | Personnel blunt assessment |

### Family 7 — Audience and format modulation

| Sub-dimension | Capture |
|---|---|
| Co-host dyad | Banter vs solo |
| Podcast vs clip vs X | Density, citation habits |
| Domain mode | Trial-lawyer vs commentator vs host |
| Public copy boundary | skill-write / Locals — **not** in-voice mind default |

### Family 8 — Contrast, forbidden, and emulation QA

| Sub-dimension | Capture |
|---|---|
| Tri-lens contrast row | Cadence, hedge, unit, tone vs mapped voices |
| Forbidden linguistic behaviors | Register mistakes to avoid |
| LLM failure modes | Neutral précis; “X would say…” |
| Authenticity spot-checks | Sounds-like / not-like pairs |

**Panel QA (optional):** After Tier A promotion, run solo smoke or sequential panel per skill [`voice-profile-panel`](../../skills-portable/voice-profile-panel/SKILL.md); anti-AI tells in [triad §8](_scratch/triad-voice-orthogonality-june-2026.md#8-anti-ai-panel-checklist-llm-roundtable-qa).

---

## Migration checklist

When promoting `codex/profiles/<speaker>-profile.md` → `statecraft/voices/<speaker>/<speaker>-profile.md`:

1. Copy corpus to voices SSOT; replace codex path with a **redirect stub** only.
2. Normalize header pointers (**Canonical profile / shelf / index**).
3. Ensure required sections exist (stub acceptable); include **Linguistic style fingerprint (detailed)** stub at Tier B.
4. List profile first in shelf `README.md` **Open first** and `index.md`.
5. Add row to [codex/profiles/README.md](../../README.md) migrated table.
6. Add speaker to **Current migrated profiles** in [README.md § Speaker profile law](README.md#speaker-profile-law).
7. When `*-source-index.md` exists: register in [voice-index.md](voice-index.md) and [repo-map.yaml](../../repo-map.yaml).

---

## Boundary

- One SSOT profile per speaker shelf — no duplicate full copies under `codex/profiles/`.
- Profile shape compliance is operator-maintained until a validator is added; this file is the contract reference.
- Legacy filename: [voices-profile-template.md](voices-profile-template.md) redirects here.
