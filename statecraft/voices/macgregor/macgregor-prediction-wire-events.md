# Macgregor prediction pilot — wire events

Operator index for the **eight-event Macgregor prediction pilot**: falsifiable questions, registry links, and rebuild paths. Stance arcs live on [macgregor-predictions.md](macgregor-predictions.md).

**Doctrine:** [event-system.md](../../../docs/statecraft/event-system.md) · **Registry SSOT:** [event-registry.json](../../data/event-registry.json) · **Skill:** [voice-prediction-record](../../../.cursor/skills/voice-prediction-record/SKILL.md)

## Event map (pilot order)

| event_id | Status | Notes | Shelf |
| --- | --- | --- | --- |
| `ukraine_escalation_russian_capitulation` | open | Shared with Freeman/Mercouris | [§ ukraine](macgregor-predictions.md#ukraine_escalation_russian_capitulation) |
| `ukraine_western_aid_prolongs_war` | open | Macgregor seed | [§ aid](macgregor-predictions.md#ukraine_western_aid_prolongs_war) |
| `nato_strategic_exposure_ukraine` | open | Macgregor seed | [§ nato](macgregor-predictions.md#nato_strategic_exposure_ukraine) |
| `iran_airpower_cannot_force_submission` | open | Macgregor seed | [§ airpower](macgregor-predictions.md#iran_airpower_cannot_force_submission) |
| `us_israel_iran_war_preparation_2025` | open | Shared registry event | [§ iran prep](macgregor-predictions.md#us_israel_iran_war_preparation_2025) |
| `israel_sabotages_exit_ramps` | open | Macgregor seed | [§ exit ramps](macgregor-predictions.md#israel_sabotages_exit_ramps) |
| `gulf_crisis_macro_shock` | open | Macgregor seed | [§ gulf macro](macgregor-predictions.md#gulf_crisis_macro_shock) |
| `us_forward_presence_obsolete` | open | Macgregor seed | [§ presence](macgregor-predictions.md#us_forward_presence_obsolete) |

**Rebuild chain:** `bootstrap_voice_capture_map.py --speaker macgregor --check` → `build_voice_predictions.py --speaker macgregor` → `check_voice_predictions.py --speaker macgregor`.

## Israel trajectory dimensions (Freeman registry v4)

Parent `israel_self_destruction_trajectory` carries six preset **dimensions** on the parent row in [event-registry.json](../../data/event-registry.json). Freeman capture rows use optional `dimension` for notes-lane hooks.
