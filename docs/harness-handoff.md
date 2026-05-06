# Harness handoff (hybrid workflows)

**Inventory:** [harness-inventory.md](harness-inventory.md) (includes **two doors, one book**). **Fresh-context paste:** `python scripts/harness_warmup.py -u grace-mar --fresh-judge`. **Pending scan:** `python scripts/generate_gate_dashboard.py -u grace-mar` â†’ open `gate-dashboard.html`.

Short guide for using **more than one AI harness** (e.g. **Cursor** + **Codex**, **Claude Code** + **ChatGPT**) on the same Grace-Mar work without losing state.

**Problem:** Each harness has its own chat context. Memory in chat **does not** live in the Record. Switching tools without a handoff resets understanding.

**Rule:** Handoff = **files in git** (+ optional warmup paste). Never **only** â€œitâ€™s in the other chat.â€

---

## Handoff checklist

1. **Land work in the repo** â€” commit or save edits under ``, `bot/`, `docs/`, etc., so the next harness sees files on disk.
2. **If the gate changed** â€” ensure `recursion-gate.md` edits are saved; companion still approves before merge.
3. **Start the next session** â€” run  
   `python3 scripts/harness_warmup.py -u grace-mar`  
   and paste into **message 1** (pending candidates, last activity, session tail).
4. **Optional** â€” one line in `session-log.md` or commit message: *Handoff: planned in [A], implementing in [B].*

---

## Example flows

| Plan in â€¦ | Implement in â€¦ | Handoff |
|-----------|----------------|--------|
| Cursor (explore, stage candidates) | Codex / cloud agent (PR-sized edits) | Committed or staged files + warmup paste in Codex thread |
| Claude Code (terminal) | Cursor (editing docs) | Same repo; open same branch; warmup in Cursor |
| OpenClaw (research) | grace-mar pipeline | `openclaw_stage.py` or â€œwe did Xâ€ + artifact path â€” still **gate**, not auto-merge |

---

## What not to do

- Rely on **copy-paste from Chat A** as the only record of decisions â€” put decisions in **markdown in repo** or session-log if they matter for merge.
- Merge from a second harness **without** companion approval â€” same Sovereign Merge Rule everywhere.

---

**See also:** [implementable-insights Â§11](implementable-insights.md#11-harness-lock-in-and-compound-workflows) Â· [openclaw-integration](openclaw-integration.md) Â· [ARCHITECTURE â€” harness](architecture.md#system-boundaries-and-harness)

