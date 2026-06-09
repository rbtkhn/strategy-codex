# Weekly rhythm â€” operator checklist

Run **once per week** (e.g. same calendar slot). Tick what you did; skip lanes that were dormant.

| # | Lane | Action | Done |
|---|------|--------|------|
| 1 | **Record** | Open `recursion-gate.md` â€” pending count 0 or explicit decisions (approve / reject / defer) | â˜ |
| 2 | **Record** | If companion had Voice milestones: stage or note **doc-only this week** (README WPC rhythm idea) | â˜ |
| 3 | **WPC** | Refresh [brief-source-registry](../skill-work/work-politics/brief-source-registry.md); run brief generator + **Â§0 recency** live pass | â˜ |
| 4 | **WPC** | One line in head: **doc-only** vs **one work-politics candidate staged** | â˜ |
| 5 | **Civ-mem** | If active: one retrieval or index sanity check; no ship without human approval | â˜ |
| 6 | **Operator** | Skim [operator-cognition.md](operator-cognition.md) north star â€” still true? | â˜ |
| 7 | **Repo** | `python3 scripts/harness_warmup.py -u strategy-codex --compact` pasted or run (`-u grace-mar` only on explicit **fork revive**) | â˜ |

**Time box:** 30â€“90 min total; WPC brief can be the long pole.

**Integrity (when Record or prompt changed this week):**

```bash
python3 scripts/validate-integrity.py --user grace-mar
python3 scripts/export_manifest.py -u grace-mar -o 
python3 scripts/fork_checksum.py -u grace-mar --manifest
```

(Or run full merge postflight if you processed the gate.)

