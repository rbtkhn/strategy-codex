# Prediction metrics

## Registry generation

`python3 scripts/build_prediction_registry.py` scans [`statecraft/notes/predictions/`](../statecraft/notes/predictions/) and joins each note to [`statecraft/data/event-registry.json`](../statecraft/data/event-registry.json).

Output: [`runtime/artifacts/prediction-registry.json`](../../runtime/artifacts/prediction-registry.json) (generated; do not hand-edit).

Each registry row includes:

- note fields: `file`, `speaker`, `event_id`, `stance`, `confidence`, `date_made`, `source`
- joined event fields: `event_status`, `event_outcome`, `prediction_status`

## Event joining

- Unknown `event_id` → build fails hard
- `prediction_status`:
  - `pending` when event is `open`
  - `resolved` / `void` / `deprecated` when event status matches

## Resolved vs unresolved events

Metrics only score predictions whose event has `status: resolved` and a definite `outcome` (`yes` or `no`).

Open, void, and deprecated events contribute to `total` but not to accuracy denominators.

## Scorable vs unscored stances

| Stance | Scored in v1? |
| --- | --- |
| `yes` | yes |
| `no` | yes |
| `conditional` | no (`unscored`) |
| `uncertain` | no (`unscored`) |

## Accuracy formula

```text
accuracy = correct / scorable
```

Where:

- `correct` = scorable predictions whose stance matches resolved event outcome
- `incorrect` = scorable predictions that do not match
- `scorable` = resolved predictions with `yes` or `no` stance
- `accuracy` is `null` when `scorable == 0`

Invariants checked by `check_prediction_metrics.py`:

- `correct + incorrect == scorable`
- `resolved >= scorable`

## Commands

```bash
python3 scripts/build_prediction_registry.py
python3 scripts/check_prediction_registry.py
python3 scripts/build_prediction_metrics.py
python3 scripts/check_prediction_metrics.py
```

## v1 limitations

Not supported in v1:

- probabilistic scoring
- Brier scores
- horizon weighting
- automatic event creation
- automatic resolution
- visual dashboards

See [event-system.md](event-system.md) and [prediction-analysis.md](prediction-analysis.md).
