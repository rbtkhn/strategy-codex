# MEMORY template — strategy-codex continuity

**File:** `memory.md` at repo root  
**Status:** ACTIVE (WORK continuity; not museum Record)

---

## Purpose

`memory.md` holds **session continuity** at three horizons — short, medium, and long. It primes assistants and operators; it does **not** override governed surfaces or museum Record.

**Horizon ≠ authority.** Long-term here means **how you run sessions** (pointers, habits, rotation policy), not durable identity or facts.

## Horizons

| Horizon | Use for | Avoid |
|---------|---------|--------|
| **Short-term** | Tone, immediate thread, calibrations | Facts that belong in statecraft synthesis or museum archive |
| **Medium-term** | Open loops, sprint notes, labeled hypotheses | Copying durable doctrine |
| **Long-term** | Rotation habits, pointers to canonical WORK paths | Knowledge claims, identity claims |

## Hierarchy

When `memory.md` conflicts with active WORK doctrine (`statecraft/`, `continuity/`, skills), follow the WORK surface.

If a line survives weeks and sounds like museum Record content, **do not** upgrade it in `memory.md` — use explicit **`fork revive`** archaeology only.

## Lifespan and decay

When the file grows past budget, run:

```bash
python3 scripts/prune_memory.py -u strategy-codex --dry-run
python3 scripts/prune_memory.py -u strategy-codex --apply
```

Pruned excerpts land under `runtime/artifacts/memory-prune/`.

**Dream** (`auto_dream.py`) may normalize horizons during end-of-day maintenance; see `.cursor/skills/dream/SKILL.md`.

## Related

- Museum Record: [`docs/archive/grace-mar-record-museum.md`](archive/grace-mar-record-museum.md)
- Path resolution: `scripts/repo_io.py` → `resolve_memory_path()`
- Statecraft **memory skill** (CIV-MEM / arc-lens): `.cursor/skills/memory/SKILL.md` — different object family
