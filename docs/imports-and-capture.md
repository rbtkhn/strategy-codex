# Imports and capture

**Purpose:** Clarify the **safety boundary** between bringing material *into* the repo and promoting it *into* the durable **Record**.

> Grace-Mar is not just a memory layer; it is a **governed companion record**. Imports and bridges **feed evidence and prepared context first**; **Approval Inbox** (`recursion-gate.md`) sits before merges into SELF, SKILLS, EVIDENCE, and prompt.

---

## What is true

1. **Ingestion is normal** â€” bridges, hooks, operator paste, bot conversations â€” see [openclaw-integration.md](openclaw-integration.md), [feedback-loops.md](feedback-loops.md).
2. **Imports do not auto-write the durable Record** â€” material may land in **EVIDENCE**, transcripts, prepared context, or staging files without yet being â€œcanonical identity.â€
3. **Promotion is gated** â€” structured **candidates** in [`recursion-gate.md`](../archive/grace-mar-instance/recursion-gate.md) (**Approval Inbox**); companion approval; `process_approved_candidates.py` performs the merge ([AGENTS.md](../AGENTS.md)).

---

## Typical path

```text
External material â†’ evidence / prepared context / staging â†’ candidates (Approval Inbox) â†’ approve â†’ Record + EVIDENCE + prompt (as applicable)
```

Cross-surface or high-materiality changes may use **change-review** instead of a routine gate row ([gate-vs-change-review.md](gate-vs-change-review.md)).

---

## Related docs

- [state-model.md](state-model.md) â€” three layers vs four Record surfaces
- [pipeline/](pipeline/) â€” evidence â†’ proposal â†’ review â†’ merge
- [skills-explained.md](skills-explained.md) â€” portable skills vs SKILLS capability
- [start-here-ob1-users.md](start-here-ob1-users.md) â€” OB1-oriented map

