strategy-codex host wiring for **tufte-data-viz** (from portable core).

| Topic | Path |
|--------|------|
| Portable core | [skills/tufte-data-viz/SKILL.md](../../../skills/tufte-data-viz/SKILL.md) |
| Cadence pressure JSON | `runtime/artifacts/work-cadence/cadence-pressure-report.json` |
| Workflow observability | `runtime/artifacts/workflow-observability/` (regenerate via scripts below) |
| Compute ledger | `platform/users/<profile>/compute-ledger.jsonl` (token columns often zero) |
| Gate board MD | `runtime/artifacts/gate-board.md` via `scripts/build_gate_board.py` |

## Data preflight

```bash
python3 scripts/audit_cadence_rhythm.py -u strategy-codex --days 14 --pressure-report
python3 scripts/emit_workflow_event.py --repo-root .
python3 scripts/build_workflow_observability.py --repo-root .
python3 scripts/build_context_efficiency_report.py --repo-root .
python3 scripts/build_gate_board.py
```

**User id:** Use `strategy-codex` for cadence events in this repo (`cadence-events.md` tags). `grace-mar` may return `NO_DATA`.

## Canvas inline extract

```bash
python3 -c "import json; print(json.dumps(json.load(open('runtime/artifacts/work-cadence/cadence-pressure-report.json')), indent=2))"
```

## Token burn

Defer until `total_tokens > 0` in ledger or operator supplies external usage. Env: `GRACE_MAR_INTEGRATION_*_TOKENS` on [emit_compute_ledger.py](../../../scripts/emit_compute_ledger.py).

## Docs

- [workflow-observability.md](../../../docs/workflow-observability.md)
- [context-efficiency.md](../../../docs/context-efficiency.md)
- [cadence-governance-bridge.md](../../../continuity/cadence/cadence-governance-bridge.md)
- [operator-dashboards.md](../../../docs/operator-dashboards.md)
