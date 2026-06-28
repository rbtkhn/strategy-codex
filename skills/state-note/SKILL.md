---
name: state-note
description: Promote one bounded statecraft argument from chat, daily synthesis, multi-lens comparison, or archive intake into a reusable statecraft/notes/ object without overpromoting into daily shelf or essay. Use when the operator says state-note, promote to statecraft note, statecraft note, or when a comparison seam or mechanism should survive outside chat with source-archive anchors and citation splits.
portable: true
version: 0.1.1
category: truth-pipeline
status: active
scope_class: repo-governed
tags:
  - operator
  - statecraft
  - notes
  - promotion
  - synthesis
---
# State Note

Use this skill when one statecraft argument has become **reusable enough to stand alone as a note**, but not yet broad or settled enough for repo-root essay or the full daily shelf.

**Sibling:** `singularity-note-promotion` — same promotion discipline, **`statecraft/notes/`** shelf instead of `singularity/notes/`. **`civ-state-note`** when CIV-STATE retrieve pre-pass is load-bearing (parallel to **`civ-state-essay`**).

## Boundary

- WORK only; not Record.
- Promote **one bounded argument**, not the whole day or month.
- Keep the note **argument-shaped**, not archive-shaped (no verbatim transcript mirrors).
- Default to **shelf-native** under `statecraft/notes/`; do not duplicate full prose on speaker shelves.
- Do not use note promotion to smuggle in doctrine that still belongs in daily synthesis, monthly synthesis, or a multi-lens pass.

## When to use

Use when **all** of the following are true:

- the claim is **method-bearing** (mechanism, route, comparison seam, audit, citation split, threshold distinction)
- the claim can travel **beyond one chat turn** while staying bounded
- source-archive paths (or a parent synthesis/daily) can anchor it without restating the archive

**Do not use** when:

- the job is still **source intake** only
- the object is the **whole day** — use `state-synthesis` first, then promote one wedge
- multiple competing claims are unsettled — stay in synthesis or use **`state-synthesis`** mechanism-comparison subroutine first (`statecraft-multi-lens` archived)
- the object is a **stand-alone thesis** that no longer needs parent context — route toward repo-root essay via `docs/prose-index.md`

## When not to confuse with adjacent skills

| Skill | Job |
|---|---|
| **state-note** (this) | One bounded note under `statecraft/notes/` |
| **civ-state-note** | Same shelf; **mandatory CIV-STATE retrieve pre-pass** when civilizational shelf is load-bearing — parallel to **`civ-state-essay`** |
| **state-synthesis** | Operator daily surface for a full archive day |
| **statecraft-multi-lens** | **Archived** — use **`state-synthesis`** comparison subroutine or **`primary-overhearing-analysis`**; may **hand off** here when method-bearing |
| **statecraft-intelligence-essay** | Synthetic essay-class object, not a bounded note |
| **singularity-note-promotion** | Same promotion shape; **singularity** shelf only |

## Workflow

### 1. Pick exactly one promotable object

Choose **one** such as:

- a **mechanism** (one causal seam)
- a **route question** (where to cite next)
- a **speaker-function** or **speaker-pair citation split**
- a **threshold** or sequencing distinction
- a **bounded audit** or postmortem
- a **comparison seam** that must not collapse into one blended voice

If you are drafting "the whole MOU day" or "the whole month," **narrow further**.

### 2. Confirm note-class (prose-index gate)

Before writing, pass the local test:

- removing surrounding machine context would **break** the piece → usually still a **note**
- the piece carries a thesis that should travel **without** parent day/month context → probably **essay**, not this skill

When uncertain, read host prose-class chooser (see appendix).

### 3. Use the bounded-note shape

A strong statecraft note usually includes some subset of:

- `Purpose`
- `Core claim` or `Shared object`
- `Why this matters` / `Best use`
- per-carrier **`X owns here`** blocks (for comparisons)
- `Citation hygiene` or `Source anchors` (exact `source-archive/` paths)
- `Falsifiers` (when claims are tierable)
- `Next use` / return paths to parent day or synthesis

Do **not** bloat into a pseudo-essay. Tables are fine when they preserve **disproportion** (who carries what).

**Filename:** kebab-case, date or topic slug, unique on shelf — e.g. `june-18-2026-mou-guest-pair-citation-split.md`.

**Header fence:** first line `WORK only; not Record.`

### 4. Preserve source anchors

Name exact archive captures or parent surfaces:

- `source-archive/statecraft/<day>/source-*.md`
- day README when useful
- parent daily or multi-lens memo if promotion is downstream

Prefer **a small number of checkpoints** over widening the source base for authority.

Do **not** paste full transcripts into the note.

### 5. Wire the shelf (required)

After the note exists:

1. Add entry to **`statecraft/notes/README.md`** (Live Mechanism / comparison cluster when appropriate)
2. Mark **`shelf-native`** in README classification when the note is canonical prose authority
3. If promoted from daily or multi-lens, add **return link** in parent surface when that parent exists

Bidirectional provenance when a parent exists: note → parent; parent → note.

### 6. Guard against overpromotion

Before finalizing, ask:

1. Is this still **one** argument?
2. Could this live in `statecraft/notes/` rather than `essays/`?
3. Does the note still need the parent day/month beside it?
4. Did promotion make **citation routing** clearer than chat alone?

If (2) is no → essay work. If (3) is yes → not mature enough; stay in synthesis.

## Comparison-note pattern (common)

When promoting speaker-function or same-day pair splits:

- state the **shared object** once
- assign **distinctive load** per voice (`Guest owns here`)
- include **Best use** (when to reach for which capture)
- keep **internal tensions** visible (same-day contradictions are signal)
- one-line weave rule optional

Template reference: host appendix example `barnes-johnson-aguilar-kent-on-section-224.md`.

## Success condition

The new note is a **reusable statecraft argument** with clear archive anchors and clear return paths; chat synthesis does not remain the only SSOT for citation splits or mechanism seams.

## Verification / Proof Standard

Do not call this complete unless:

- the input source, file, paste, URL, or archive path is named
- the output surface is named
- skipped steps are explicitly marked with a reason
- uncertainty, missing evidence, or unresolved source defects are stated
- note class and source floor must be named
- **note contract fields** are populated for Tier A notes (`note_type`, `authority_level`, `source_basis`, optional `archive_links` / `nodes`)
- `python3 scripts/check_statecraft_notes.py --verify` passes for the promoted note path before marking **shelf-native**

Evidence to report:

- files touched or produced
- scripts or commands run
- source URLs, archive paths, or transcript identifiers used
- `check_statecraft_notes.py --verify` exit code when promoting shelf-native
- confidence downgrade, if any

If verification cannot be completed:

- state what was not verified
- stop before archive land, synthesis, publication, or promotion
- return a bounded partial result for operator review

## Preferred maintenance after skill edits

Run host sync and validation (see appendix).
