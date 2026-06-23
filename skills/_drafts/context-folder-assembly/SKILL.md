---
name: context-folder-assembly
description: Assemble a bounded working folder from NL source discovery, questions-as-spec PLAN, and task-shape seal — then fresh-thread EXECUTE; WORK-only, not bridge or harvest.
preferred_activation: context folder
portable: true
version: 0.1.0
category: domain-pack
status: draft
tags:
  - operator
  - work-dev
  - context
  - plan
---
# Context Folder Assembly

**Preferred activation (operator):** say **`context folder`**. **Aliases:** **`assemble working folder`**, **`assemble context`**, **`clean context window`**.

Use when heavy multi-file or long-document work needs a **bounded on-disk folder** before **EXECUTE** in a **fresh thread** — after PLAN has clarified success as meaningful questions.

## Governance

- WORK-only prepared context; **not** Record, **not** EVIDENCE, **not** gate merge authority.
- **Copy** sources into the folder; canonical paths remain SSOT until EXECUTE commits elsewhere.
- Do not substitute for **bridge** (session seal), **harvest** (midstream paste packet), or **dream** (maintenance).

## When to use

Use when **all three** apply:

1. Multi-file or long-output task (synthesis, cross-month weave, large doc/refactor set).
2. You want a **fresh EXECUTE thread** (current chat noisy or switching model).
3. PLAN needs **questions-as-spec** plus a bounded file set before agentic churn.

**Skip when:** one-file fix; **harvest**; **bridge** alone; lane-only orient (**compress_active_lane**).

## Procedure (shape-then-execute)

1. **Discover** — Operator describes sources in natural language (topic, era, lane, “when I wrote X”). Search the host repo; propose candidate paths with one-line rationale. Operator confirms or narrows.
2. **Assemble** — Copy (never move) confirmed files into `<working-root>/<slug>/sources/`. Write `sources-index.md` (original path → copy path, copy date).
3. **Questions pass (PLAN)** — Write `questions.md` using the host questions-as-spec template. Refine task shape; **no EXECUTE** until operator approves.
4. **Seal shape** — Write `task-shape.md` (deliverable, in/out, link to `questions.md`, `Ready to EXECUTE: yes`).
5. **Hand off** — Operator opens a **fresh thread**: read only `<working-root>/<slug>/`; execute `task-shape.md`. Then **EXECUTE**.

## Folder contract

| File | Role |
|------|------|
| `README.md` | Purpose, slug, created date, inspection-only |
| `questions.md` | Standards as questions (pre-execute) |
| `task-shape.md` | Agreed scope after PLAN |
| `sources-index.md` | Provenance map |
| `sources/` | Copied inputs only |
| `EXECUTE.md` | Optional detailed instructions or transcript snippet |
| `lane-orientation.md` | Optional lane compression memo |

## Operator workflow integration

Optional wedge **between PLAN and EXECUTE**. Does **not** replace coffee, conductor, bridge, or dream.

```text
coffee / conductor → PLAN (questions-as-spec) → [optional] context folder → fresh thread EXECUTE → bridge / dream
```

| Phase | Behavior |
|-------|----------|
| **Morning — coffee** | A/B/C/D as usual. No folder unless you already know it is a big-compose day. |
| **Midday — WORK** | Single-file fix, notebook pass, gate review → current thread, no folder. |
| **Conductor** | Closeout on disk as usual. Folder when **next** step is long EXECUTE in a clean thread. |
| **Evening — dream + bridge** | Bridge packet + seal. Active slug may appear under **Open loops** if the task continues. |

**Example flows**

- **Statecraft synthesis:** Coffee C → PLAN → `context folder` → new thread → EXECUTE → bridge notes slug if unfinished.
- **Conductor follow-up:** Copy closeout paths into folder → fresh thread executes without re-litigating conductor chat.
- **Multi-thread incubation:** One slug per idea; sequential EXECUTE threads.

**Decision rule:** If the task fits one chat and one path, skip the folder. If you would say “new chat, but first gather everything about X,” use the folder.

## Guardrails

- Abstain if discover returns ambiguous duplicates — list forks; ask once.
- No trailing **`coffee`** line, no Session Bridge title, no harvest closing line.
- Do not stage WORK methodology to any Record gate.

## Agent behavior norms

- **Human authority** — Operator approves shape before EXECUTE.
- **Abstention** — Say when sources are thin or copies would duplicate canonical truth.
- **No silent overwrite** — Copies only; do not edit canonical sources during assembly unless explicitly scoped.

## Related skills

- **bridge** — session end; may reference active slug in Open loops.
- **harvest** — midstream paste; not on-disk folder.
- **packet-before-synthesis** — packet discipline before folder on mixed seams.
- **compress_active_lane** — optional `lane-orientation.md` input.

## Provenance

Pattern inspired by Nate Jones “My AI Workflow Has Changed” (NL discover → working folder → new chat). **Host-agnostic** — not tied to one vendor or IDE.
