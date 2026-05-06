# Parallel macro-actions (non-interfering agent work)

**Purpose:** When multiple agent sessions (or humans) work in parallel on **different** slices of the repo, reduce **merge collisions** and keep **gate law** clear: each slice can use a **dedicated branch**; **merge order** is explicit; **Record merges** still only via `process_approved_candidates.py`.

**Not:** A new pipeline, OpenClaw feature, or automatic merge. **Local / operator discipline only.**

---

## Checklist (before starting)

1. **Split paths** â€” Assign non-overlapping path prefixes (e.g. `bot/` vs `docs/skill-work/work-dev/` vs `skills.md` only).
2. **Name branches** â€” Use a shared prefix so reviews are obvious, e.g. `macro/<session>-agent-1`, `macro/<session>-agent-2`.
3. **Merge order** â€” If agent-2 depends on agent-1â€™s work, merge **1 â†’ 2 â†’ main** (or rebase 2 onto 1 before final merge).
4. **Gate** â€” Staging to RECURSION-GATE can happen on any branch; **apply** merges only after companion approval, from a clean operator run (usually `main`).
5. **Receipts** â€” Keep PRs small; one concern per branch where possible.

---

## Generate branch names + merge order

Stateless helper (no repo writes):

```bash
python scripts/integration_macro_actions.py branches --session my-feature --slots 3
python scripts/integration_macro_actions.py checklist --session my-feature --slots 3
```

Copy the printed branch names into your git workflow. Adjust `--prefix` if `macro/` collides with your naming.

---

## When *not* to parallelize

- Same file edited by two agents without coordination.
- Anything that touches **gated files** (`self.md`, `self-evidence.md`, `recursion-gate.md`, `bot/prompt.py`) â€” **one** actor or sequential edits; merges still **only** via the approved pipeline script.

---

## Cross-references

- [INTEGRATION-PROGRAM.md](INTEGRATION-PROGRAM.md) â€” full read / export / stage / merge loop.
- [openclaw-integration.md](../../openclaw-integration.md) â€” full integration guide.

