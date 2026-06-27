# Coming from OB1? Start here

> **Record frozen (2026):** Growing the Grace-Mar interpretive machine is **not** a `strategy-codex` objective. Default onboarding: [start-here.md](start-here.md) (interpretive machine). This page maps **legacy** OB1 → Grace-Mar gate surfaces for **`fork revive`** only. See [grace-mar-instance-boundary.md](grace-mar-instance-boundary.md).

Plain-language bridge for people who know **Open Brain (OB1)**-style systems. Precise legacy doctrine: [glossary.md](glossary.md), [conceptual-framework.md](conceptual-framework.md).

---

## Translation table

| If you think inâ€¦ | In Grace-Mar |
|------------------|--------------|
| **Library** | **removed operator-books symlink** â€” display label **Library** ([scripts/surface_aliases.py](../scripts/surface_aliases.py)) |
| **Skills** (executable packs) | Two layers: **SKILLS** (Record capability in `self-skills.md`) vs **portable skills** (`skills/`). See [skills-explained.md](skills-explained.md). |
| **Evidence / activity log** | **EVIDENCE** â€” canonical body on `self-archive.md` |
| **Pending approvals / review queue** | **Approval Inbox** â€” user-facing name for pending candidates in [`recursion-gate.md`](../archive/grace-mar-instance/recursion-gate.md) (canonical file name: **recursion-gate**). **Boundary Review** (classification hints) is related but not the whole inbox; see [boundary-review-queue.md](boundary-review-queue.md). |
| **Workflows / recipes** | `docs/skill-work/**`, scripts, bridges â€” [workflow-catalog.md](workflow-catalog.md) |
| **Imports / capture** | [imports-and-capture.md](imports-and-capture.md) |
| **Dashboard** | [observability.md](observability.md), `runtime/observability/`, family hub / miniapp: [simple-user-interface.md](simple-user-interface.md) |

---

## What will feel familiar

- **Observable state** â€” pipeline, observability feeds, session tooling ([observability.md](observability.md), [session-observability.md](session-observability.md)).
- **Skills culture** â€” Cursor **skills**, portable operator assets, plus **SKILLS** as Record capability ([skills-explained.md](skills-explained.md)).
- **Integrations and bridges** â€” OpenClaw, exports, prepared context ([openclaw-integration.md](openclaw-integration.md), [prepared-context-layer.md](prepared-context-layer.md) in [state-model.md](state-model.md)).
- **A queue before durable memory** â€” candidates land in the **Approval Inbox** (`recursion-gate.md`); nothing becomes lasting Record truth without companion approval ([AGENTS.md](../AGENTS.md) Â§ Gated Pipeline).

---

## What is different

- **Four Record surfaces** â€” SELF, removed operator-books symlink, SKILLS, EVIDENCE â€” not a single undifferentiated DB ([README.md](../README.md) Concept).
- **No silent merge into the Record** â€” staging is not adoption; merge runs only after approval (`process_approved_candidates.py`).
- **Identity vs library** â€” museum knowledge (who she is) vs removed operator-books symlink (reference corpora) â€” [archive/boundary-self-knowledge-self-library.md](archive/boundary-self-knowledge-self-library.md).
- **Template state model** â€” evidence vs prepared context vs governed state complements the four surfaces ([state-model.md](state-model.md)).

---

## Where to start first

1. Skim [README.md](../README.md) â€” Concept + Gated Pipeline.
2. Open [docs/start-here.md](start-here.md) â€” **Choose your path** (operator = **C** is the usual OB1-adjacent role).
3. Peek at pending work: [`recursion-gate.md`](../archive/grace-mar-instance/recursion-gate.md) (**Approval Inbox**).
4. Optional: run a short observability or session script ([observability.md](observability.md)) to see â€œdashboard-ishâ€ output locally.

---

## How imports and memory work here

Bridges and hooks **ingest**; imports **do not** write directly to durable Record. Typical path: material â†’ **EVIDENCE** / prepared context / transcripts â†’ **candidates** in the Approval Inbox â†’ merge after approval. Full narrative: [imports-and-capture.md](imports-and-capture.md).

---

## What the Approval Inbox does

1. **Signal detection** (bot, operator, tests) proposes structured candidates.  
2. Candidates sit in `recursion-gate.md` until **approved**, **rejected**, or **edited**.  
3. **Merge** runs only on approved rows â€” Sovereign Merge Rule.

Deeper review semantics (tiers, quick-merge eligibility): [recursion-gate-three-tier.md](recursion-gate-three-tier.md).

---

## See also

- [start-here.md](start-here.md) â€” audience doors (Aâ€“F)
- [gate-vs-change-review.md](gate-vs-change-review.md) â€” when to escalate beyond the gate
- [feedback-loops.md](feedback-loops.md) â€” low-friction approval, merge feedback

