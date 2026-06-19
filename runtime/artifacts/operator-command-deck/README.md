# Operator Command Deck (derived dashboard)

Non-canonical **runtime / derived** repo-wide cockpit: posture, recommended next moves, queues, and health summary. Aggregates Repo Surgeon and Statecraft War Room when available.

**Phase 0 alignment:** [docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md](../../../docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md)

**Registry:** [docs/operator-surface-registry.md](../../../docs/operator-surface-registry.md) · `surface_id`: `operator-command-deck`

## Layout

```text
runtime/artifacts/operator-command-deck/latest.md
runtime/artifacts/operator-command-deck/latest.json
runtime/artifacts/operator-command-deck/YYYY-MM-DD.md   # optional snapshot
```

**Default:** `latest.*` and dated snapshots are **gitignored**. Regenerate on demand.

## Authority

> **Mode:** runtime / derived  
> **Authority:** advisory only — not a substitute for thread-start paste

**Does not replace:** [`harness_warmup.py`](../../../scripts/harness_warmup.py), [`operator_reentry_stack.py`](../../../scripts/operator_reentry_stack.py), [`recursion-gate.md`](../../../recursion-gate.md), or lane-specific dashboards (`library-index`, `lane-dashboards`, `review-dashboard`).

## Rebuild

```bash
python3 scripts/operator_command_deck.py \
  --out runtime/artifacts/operator-command-deck/latest.md \
  --json-out runtime/artifacts/operator-command-deck/latest.json \
  --max-next-actions 5
```

**Flags:**

- `--full-surgeon` — run layout/path/skill subprocess checks (slower structural triage)
- `--include-gate` — fork-revive territory only; surfaces pending gate candidates without merge authority
- `--no-git` — skip git working-tree snapshot
- `--snapshot` — optional dated `.md` copy

## SSOT return paths

- [docs/harness-architecture-map.md](../../../docs/harness-architecture-map.md)
- [docs/intelligence-harness.md](../../../docs/intelligence-harness.md)
- [docs/statecraft-intake-queue.md](../../../docs/statecraft-intake-queue.md)
- [docs/runtime/context-budgeting.md](../../../docs/runtime/context-budgeting.md)
