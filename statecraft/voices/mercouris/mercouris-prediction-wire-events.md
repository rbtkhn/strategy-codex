# Mercouris prediction pilot — wire events

Operator index for the **two-event Mercouris prediction pilot** (registry stub): falsifiable questions, wire-resolution stubs, and rebuild paths. Stance arcs live on [mercouris-predictions.md](mercouris-predictions.md); this page is for **closure, wire-verify, and registry hygiene**.

**Doctrine:** [event-system.md](../../../docs/statecraft/event-system.md) · **Registry SSOT:** [event-registry.json](../../data/event-registry.json) · **Thesis map:** [mercouris-prediction-thesis-map.json](../../data/mercouris-prediction-thesis-map.json)

## Event map (pilot order)

| event_id | Status | Wire resolution stub | Shelf |
| --- | --- | --- | --- |
| `ukraine_escalation_russian_capitulation` | resolved · **no** | [prediction-resolution-ukraine-escalation-russian-capitulation.md](../../notes/wire/prediction-resolution-ukraine-escalation-russian-capitulation.md) | [§ ukraine](mercouris-predictions.md#ukraine_escalation_russian_capitulation) |
| `us_israel_iran_war_preparation_2025` | open | [prediction-resolution-us-israel-iran-war-preparation-2025.md](../../notes/wire/prediction-resolution-us-israel-iran-war-preparation-2025.md) | [§ iran prep](mercouris-predictions.md#us_israel_iran_war_preparation_2025) |

## Public record chain

Curated rows in [mercouris-prediction-capture-map.json](../../data/mercouris-prediction-capture-map.json) → generic voice builder → shelf JSON/MD.

```bash
python3 scripts/bootstrap_voice_capture_map.py --speaker mercouris --check
python3 scripts/build_voice_predictions.py --speaker mercouris
python3 scripts/build_voice_predictions.py --speaker mercouris --check
python3 scripts/check_voice_predictions.py --speaker mercouris
python3 -m pytest tests/test_voice_predictions.py -q
```

## Stub checklist (operator)

- [ ] Expand pilot beyond two shared registry events when Mercouris capture map is curated
- [ ] Add auto-file config only after manual gold rows exist
- [ ] Enroll `generated-manifest.yaml` when capture map stabilizes
