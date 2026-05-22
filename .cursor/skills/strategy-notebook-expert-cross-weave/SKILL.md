---
name: "strategy-notebook-expert-cross-weave"
preferred_activation: "weave expert cross"
description: "Legacy alias for strategy-codex expert cross-weave: fold two expert-thread ingests into one host-equivalent daily seam (Chronicle/Reflection/References/Open), with optional batch-analysis rows and a month-level grep anchor; WORK lane only."
portable: true
version: "0.2.0"
tags:
  - "operator"
  - "work-strategy"
  - "strategy-codex"
  - "strategy-notebook-legacy"
portable_source: "skills-portable/strategy-notebook-expert-cross-weave/SKILL.md"
synced_by: "sync_portable_skills.py"
---
# Strategy-codex expert cross-weave

**Naming:** This portable skill keeps the legacy slug `strategy-notebook-expert-cross-weave` for compatibility. The active concept is **strategy-codex expert cross-weave** and the portable core should use host-equivalent notebook surfaces.

**Preferred activation (operator):** **`weave <expert-a> <expert-b>`**, **`expert cross-weave`**, **`crosses:expert-a+expert-b`**.

Use this skill when two indexed **`thread:<expert_id>`** lines in a host daily inbox should become **one explicit judgment seam** on a dated notebook page without collapsing distinct evidence chains.

## Required host equivalents

| Purpose | Portable placeholder |
|---------|----------------------|
| Commentator roster with stable expert ids | `<expert-roster>` |
| Daily inbox or ingest queue | `<daily-inbox>` |
| Calendar notebook or daily page surface | `<calendar-notebook>` |
| Month-level meta or summary surface | `<month-meta>` |
| Status or recent-work receipt surface | `<status-surface>` |

## Preconditions

1. Both experts appear in the host's commentator roster with stable **`expert_id`** values.
2. Source lines exist, or are recoverable, in the host's daily inbox - including any **`crosses:`** or **`batch-analysis`** tails you intend to preserve.
3. You know the calendar date for the target **`## YYYY-MM-DD`** section.

## Procedure

### 0) Page-shape fork (before any file write)

When the operator invokes **expert cross-weave** or **`crosses:`** without naming a single shape, present **4-6** labeled options that describe this session's thesis or page shape.

Examples:

- cross-expert seam
- continuity-only daily seam
- judgment-heavy / links-light
- verify-first open

Stub only. Do not write developed prose until the operator picks. If the operator already names both experts or says **`no menu`**, skip or shorten this fork per the host's notebook architecture.

### 1) Name the seam

- Use **`crosses:<expert-a>+<expert-b>`** with consistent expert-id ordering.
- Write one sentence each for what A answers versus what B answers.
- Keep tension visible. Do not pretend they are solving the same question if they are not.

### 2) Write the daily seam

Under the host's calendar notebook, in the correct **`## YYYY-MM-DD`** block:

1. **Signal** - one bullet naming the source objects and the before -> after move.
2. **Judgment** - one bullet naming the **`crosses:`** seam, the convergence if any, and the tension that must not be merged away.
3. **Links** - inbox pointer, transcript or episode links, profile URLs, and any verify reminders.
4. **Open** - optional explicit **`batch-analysis | YYYY-MM-DD | A x B | crosses:...`** suggestion for grep membership.

Do not add a second top-level **`##`** for the same day if that heading already exists. Append to the day's existing sections.

### 3) Optional - daily inbox update

- Add or extend a **`batch-analysis`** line when the host architecture expects it.
- Append a minimal grep stub on its own line when you want a pure search hit:

  `batch-analysis | YYYY-MM-DD | Short label | crosses:expert-a+expert-b`

### 4) Optional - month meta update

- Add one grep anchor line under the month's one-screen summary linking the exact **`batch-analysis`** stub to the daily seam anchor.

### 5) Status receipt

- Update the host's status or recent-work receipt surface when this weave closes real notebook work.

## Guardrails

- **WORK only** - not SELF, not EVIDENCE, not Voice, and not Record staging.
- Do not treat digest or transcript quantities as wire-grade without the host's verify discipline.
- Do not fold unrelated third experts into the seam without an explicit **`batch-analysis`** or operator request.
- Do not write false convergence. The seam exists to place two experts in tension or coordination, not to pretend they now say the same thing.

## See also

- The host's notebook architecture for daily composition.
- The host's expert-thread continuity surface.
- The host's stable **`expert_id`** roster and crossing rules.


## Cursor / grace-mar instance

Grace-mar paths (from `.cursor/skills/strategy-notebook-expert-cross-weave/`).

| Topic | Path |
|--------|------|
| Portable core | [skills-portable/strategy-notebook-expert-cross-weave/SKILL.md](../../../skills-portable/strategy-notebook-expert-cross-weave/SKILL.md) |
| Daily inbox (SSOT) | [docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md](../../../docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md) |
| Chapter days | [docs/skill-work/work-strategy/strategy-notebook/chapters/2026-04/days.md](../../../docs/skill-work/work-strategy/strategy-notebook/chapters/2026-04/days.md) (adjust `YYYY-MM`) |
| Chapter meta | [docs/skill-work/work-strategy/strategy-notebook/chapters/2026-04/meta.md](../../../docs/skill-work/work-strategy/strategy-notebook/chapters/2026-04/meta.md) |
| Notebook STATUS | [docs/skill-work/work-strategy/strategy-notebook/STATUS.md](../../../docs/skill-work/work-strategy/strategy-notebook/STATUS.md) |
| Commentator roster | [docs/skill-work/work-strategy/strategy-notebook/strategy-commentator-threads.md](../../../docs/skill-work/work-strategy/strategy-notebook/strategy-commentator-threads.md) |
| Notebook architecture | [docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md) |
| Parent lane skill | [.cursor/skills/skill-strategy/SKILL.md](../skill-strategy/SKILL.md) |
| Manifest / sync | [skills-portable/manifest.yaml](../../../skills-portable/manifest.yaml) · [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |

**Worked example (2026-04):** Ritter × Davis weave — `crosses:ritter+davis`; commits `c09cedcc`, `ecac8c0e`, `4fff0860` on `main`.
