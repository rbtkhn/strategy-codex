# Living files


A **living file** is durable repo material that humans and agents can load as context, instruction, evidence, synthesis, or reusable work product.

Agent work compounds when useful outputs are promoted into **governed paths** instead of staying in chat, terminal scrollback, or untracked scratch. This doc names that habit; it does not replace the SSOT surfaces below.

---

## What makes a file living

A file is **living** when it is:

- human-readable
- agent-readable
- located in a **governed repo path**
- **routable** ([LLM-ROUTING.md](../LLM-ROUTING.md) → [repo-map.yaml](../repo-map.yaml))
- **reviewable** (git history, operator review, or documented generator)
- **reusable** as future context

---

## Living ≠ authoritative

A living file is **not** authoritative merely because it exists on disk.

**Category** (what kind of truth it is) — see [AGENTS.md](../AGENTS.md) § Authority categories:

| Category | Meaning |
|----------|---------|
| **source** | Primary or canonical source material |
| **work** | Active operator-authored surfaces |
| **generated** | Rebuildable derived outputs |
| **archive** | Frozen historical or compatibility material |

**Authority class** (what an agent may do to a surface) — see [authority-map.md](authority-map.md) (`read_only`, `draftable`, `review_required`, …). Use `python3 scripts/check-authority.py --surface <key>` when scope is unclear.

**Policy lines:**

```text
Agent-visible does not mean agent-editable.
Agent-readable does not mean authoritative.
Generated does not mean source.
Archive does not mean active doctrine.
```

---

## Load the smallest slice

Route before you bulk-read. Default load order for **instructions**: [layer-architecture.md](layer-architecture.md) (Core → Instance → Lane → Mode).

For **volume** after you know what to open: [runtime/context-budgeting.md](runtime/context-budgeting.md).

---

## When chat becomes a living file

Not every session turn needs a file. Promote when work crosses the work membrane — reusable, auditable, or citeable — per [replacement-capture-habits.md](replacement-capture-habits.md).

**Authority and freshness:** [runtime-vs-record.md](runtime-vs-record.md) · **Promotion ladder:** [start-here.md](start-here.md) § Promotion ladder.

---

## See also

- [harness-architecture-map.md](harness-architecture-map.md) — harness topology hub
- [complexity-budget.md](complexity-budget.md) — product kernel and anti-sprawl targets
