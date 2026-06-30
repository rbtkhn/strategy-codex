# Freeman prediction pilot — wire events

WORK only; not Record.

Operator index for the **seven-event Freeman prediction pilot**: falsifiable questions, wire-resolution stubs, register bridges, and rebuild paths. Stance arcs live on [freeman-predictions.md](freeman-predictions.md); this page is for **closure, wire-verify, and registry hygiene**.

**Doctrine:** [event-system.md](../../../docs/statecraft/event-system.md) · **Registry SSOT:** [event-registry.json](../../data/event-registry.json) · **Thesis map:** [freeman-prediction-thesis-map.json](../../data/freeman-prediction-thesis-map.json) · **Auto-file config:** [freeman-prediction-auto-file.json](../../data/freeman-prediction-auto-file.json)

## Event map (pilot order)

| event_id | Status | Close | Wire resolution stub | Register / bridge | Shelf |
| --- | --- | --- | --- | --- | --- |
| `israel_self_destruction_trajectory` | open | 2025-12-31 | [prediction-resolution-israel-self-destruction-trajectory.md](../../notes/wire/prediction-resolution-israel-self-destruction-trajectory.md) | [Israel trajectory register](../../notes/2025-freeman-israel-trajectory-register.md) | [§ israel](freeman-predictions.md#israel_self_destruction_trajectory) |
| `ukraine_escalation_russian_capitulation` | resolved · **no** | 2025-12-31 | [prediction-resolution-ukraine-escalation-russian-capitulation.md](../../notes/wire/prediction-resolution-ukraine-escalation-russian-capitulation.md) | — | [§ ukraine](freeman-predictions.md#ukraine_escalation_russian_capitulation) |
| `gaza_hostage_deal_jan_2025` | resolved · **yes** | 2025-01-31 | [prediction-resolution-gaza-hostage-deal-jan-2025.md](../../notes/wire/prediction-resolution-gaza-hostage-deal-jan-2025.md) | — | [§ hostage](freeman-predictions.md#gaza_hostage_deal_jan_2025) |
| `gaza_ceasefire_holds_2025` | open | 2025-12-31 | [prediction-resolution-gaza-ceasefire-holds-2025.md](../../notes/wire/prediction-resolution-gaza-ceasefire-holds-2025.md) | [IGL Gaza ceasefire register](../../notes/2025-freeman-igl-gaza-ceasefire-register.md) | [§ ceasefire](freeman-predictions.md#gaza_ceasefire_holds_2025) |
| `us_israel_iran_war_preparation_2025` | open | 2025-06-30 | [prediction-resolution-us-israel-iran-war-preparation-2025.md](../../notes/wire/prediction-resolution-us-israel-iran-war-preparation-2025.md) | [IGL Iran war push register](../../notes/2025-freeman-igl-iran-war-push-register.md) | [§ iran prep](freeman-predictions.md#us_israel_iran_war_preparation_2025) |
| `iran_great_power_direct_war_entry` | open | 2025-12-31 | [prediction-resolution-iran-great-power-direct-war-entry.md](../../notes/wire/prediction-resolution-iran-great-power-direct-war-entry.md) | — · related: `us_israel_iran_war_preparation_2025` | [§ great-power](freeman-predictions.md#iran_great_power_direct_war_entry) |
| `china_tariff_capitulation_2025` | open | 2025-12-31 | [prediction-resolution-china-tariff-capitulation-2025.md](../../notes/wire/prediction-resolution-china-tariff-capitulation-2025.md) | — | [§ china tariff](freeman-predictions.md#china_tariff_capitulation_2025) |

**Related pairs (thesis map):** Iran war prep ↔ great-power direct entry — score lanes separately; use `title_conflict_patterns` and register strictness so bridge captures do not bleed.

## Wire closure workflow

1. Open the **wire resolution stub** for the event (table above).
2. Grade **closure hooks** with [news-verify](../../../.cursor/skills/news-verify/SKILL.md) / [wire-verify](../../../.cursor/skills/wire-verify/SKILL.md); paste verdict + cite into the stub table.
3. Fill **Resolution decision (operator)** on the stub; set `resolution_source` text for registry paste.
4. Update [event-registry.json](../../data/event-registry.json) (`status`, `outcome`, `resolved_date`, `resolution_source`) when closing.
5. Rebuild generated surfaces (below) so [freeman-predictions.md](freeman-predictions.md) and [prediction-registry.json](../../../runtime/artifacts/prediction-registry.json) reflect closure.

## Auto-file and calibration

Hooks and thresholds per event live in [freeman-prediction-auto-file.json](../../data/freeman-prediction-auto-file.json). Manual gold for calibration = prediction notes **without** `auto_file: true` ([calibrate_auto_file.py](../../../scripts/calibrate_auto_file.py) `manual_only` default).

```bash
python3 scripts/auto_materialize_freeman_predictions.py --prune
python3 scripts/build_prediction_registry.py
python3 scripts/build_prediction_timeline.py
python3 scripts/build_freeman_predictions.py
python3 scripts/calibrate_auto_file.py --all-events
python3 scripts/check_freeman_predictions.py
```

**Calibration artifact:** [freeman-prediction-auto-file-calibration-all.json](../../../runtime/artifacts/freeman-prediction-auto-file-calibration-all.json)

## Generated artifacts

| Artifact | Role |
| --- | --- |
| [prediction-registry.json](../../../runtime/artifacts/prediction-registry.json) | Event + note join for pipeline |
| [prediction-timeline.json](../../../runtime/artifacts/prediction-timeline.json) | Chronological touchpoints |
| [freeman-prediction-crawl.json](../../../runtime/artifacts/freeman-prediction-crawl.json) | Crawl manifest (audit queue) |

## Stub checklist (operator)

- [ ] Open events graded at `close_date` with wire receipts in stub hooks
- [ ] Registry rows updated after each resolution decision
- [ ] Auto-file calibration re-run after hook/config changes
