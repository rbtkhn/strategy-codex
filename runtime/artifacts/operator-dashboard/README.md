# Operator Dashboard (umbrella index)

Non-canonical **runtime / derived** stitched index over the three Phase 1–3 aggregators (Repo Surgeon, Statecraft War Room, Operator Command Deck).

**Phase 0 alignment:** [docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md](../../../docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md)

**Registry:** [docs/operator-surface-registry.md](../../../docs/operator-surface-registry.md) · `surface_id`: `operator-dashboard`

## Layout

```text
runtime/artifacts/operator-dashboard/latest.md
runtime/artifacts/operator-dashboard/latest.json
runtime/artifacts/operator-dashboard/YYYY-MM-DD.md   # optional snapshot
```

**Default:** `latest.*` and dated snapshots are **gitignored**. Regenerate on demand.

## Authority

> **Mode:** runtime / derived  
> **Authority:** advisory only — stitched index, not a fourth SSOT brain

**Does not replace:** child bucket reports, [`harness_warmup.py`](../../../scripts/harness_warmup.py), [`operator_reentry_stack.py`](../../../scripts/operator_reentry_stack.py), or [`coffee` Dashboard nudge](../../../docs/operator-dashboard-when-to-use.md).

## Rebuild

Full regen (all three producers in-process, then compose umbrella):

```bash
python3 scripts/operator_dashboard.py
```

Compose umbrella only from existing child `latest.json` files:

```bash
python3 scripts/operator_dashboard.py --compose-only
```

**Pass-through flags:** `--surgeon-scope`, `--full-surgeon`, `--verify-portable-skills`, `--fail-on-blocking`, `--war-room-latest-days`, `--war-room-max-objects`, `--max-next-actions`, `--include-gate`, `--no-git`, `--snapshot`

**Note:** Default run executes Surgeon + War Room for their buckets, then Command Deck (which recomputes Surgeon + War Room in-process). Acceptable for occasional full regen; use individual producers for single-surface refresh.

**When to use:** [docs/operator-dashboard-when-to-use.md](../../../docs/operator-dashboard-when-to-use.md) — **Full regen (all dashboards)** row; not the default `coffee` nudge.

## Child dashboards

| Bucket | Question |
|--------|----------|
| [repo-surgeon](../repo-surgeon/README.md) | What is structurally broken? |
| [statecraft-war-room](../statecraft-war-room/README.md) | Which statecraft objects are live? |
| [operator-command-deck](../operator-command-deck/README.md) | What should I do next? |

## SSOT return paths

- [docs/operator-dashboard-when-to-use.md](../../../docs/operator-dashboard-when-to-use.md)
- [docs/operator-dashboards.md](../../../docs/operator-dashboards.md)
- [docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md](../../../docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md)
