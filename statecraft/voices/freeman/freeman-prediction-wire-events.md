# Freeman prediction pilot — wire events

Operator index for the **seven-event Freeman prediction pilot**: falsifiable questions, wire-resolution stubs, register bridges, and rebuild paths. Stance arcs live on [freeman-predictions.md](freeman-predictions.md); this page is for **closure, wire-verify, and registry hygiene**.

**Doctrine:** [event-system.md](../../../docs/statecraft/event-system.md) · **Registry SSOT:** [event-registry.json](../../data/event-registry.json) · **Thesis map:** [freeman-prediction-thesis-map.json](../../data/freeman-prediction-thesis-map.json) · **Auto-file config:** [freeman-prediction-auto-file.json](../../data/freeman-prediction-auto-file.json) · **Skill:** [voice-prediction-record](../../../.cursor/skills/voice-prediction-record/SKILL.md)

## Public shelf v3 (capture map → generated MD)

Curated rows live in [freeman-prediction-capture-map.json](../../data/freeman-prediction-capture-map.json) (`freeman-predictions-v3`). Each row carries **verbatim audit** + **display** + **speaker attribution**:

| Field | Role |
| --- | --- |
| `public_excerpt_raw` | Verbatim capture substring — audit SSOT |
| `public_excerpt` | Rendered quote (may differ when `asr_repair` documents repair) |
| `asr_repair` / `asr_repair_notes` | Repair tier + notes when display ≠ raw |
| `quote_speaker` | `freeman` · `mixed` · `host` · `operator_summary` |
| `host_setup` / `context_note` | Required for **`mixed`** rows |
| `public_display` | `false` → JSON audit only; omitted from public source trail |

**Rebuild chain:** `bootstrap_voice_capture_map.py --check` → `build_voice_predictions.py` → `check_voice_predictions.py` → pytest. Do **not** hand-edit [freeman-predictions.md](freeman-predictions.md).

### Source trail (public-facing)

Each event on the shelf exposes one collapsible **Source trail** table. Required header (checker fails on legacy `Appearance | Exact words`):

```md
| Date | Channel | Episode | Stance | Speech act | Excerpt |
| --- | --- | --- | --- | --- | --- |
```

| Column | Source |
| --- | --- |
| **Date** | `appearance.date` (or row `appearance_date`) |
| **Channel** | `citation.channel` |
| **Episode** | `[citation.title](youtube_url)` when URL present; plain title otherwise |
| **Stance** | row `stance` |
| **Speech act** | row `speech_act` |
| **Excerpt** | `public_excerpt` (+ host setup / context for **`mixed`**) |

YouTube links are optional when the archive capture has no watch URL. Anchor blockquotes on the shelf use the same speaker-aware shapes as the excerpt column.

## Event map (pilot order)

| event_id | Status | Horizon / closure | Wire resolution stub | Register / bridge | Shelf |
| --- | --- | --- | --- | --- | --- |
| `israel_self_destruction_trajectory` | open | Ongoing trajectory (Jan 7) | [prediction-resolution-israel-self-destruction-trajectory.md](../../notes/wire/prediction-resolution-israel-self-destruction-trajectory.md) | [Israel trajectory register](../../notes/2025-freeman-israel-trajectory-register.md) | [§ israel](freeman-predictions.md#israel_self_destruction_trajectory) |
| `ukraine_escalation_russian_capitulation` | resolved · **no** | Kellogg negation (Jan 10) | [prediction-resolution-ukraine-escalation-russian-capitulation.md](../../notes/wire/prediction-resolution-ukraine-escalation-russian-capitulation.md) | — | [§ ukraine](freeman-predictions.md#ukraine_escalation_russian_capitulation) |
| `gaza_hostage_deal_jan_2025` | resolved · **yes** | Deal reached (wire Jan 21) | [prediction-resolution-gaza-hostage-deal-jan-2025.md](../../notes/wire/prediction-resolution-gaza-hostage-deal-jan-2025.md) | — | [§ hostage](freeman-predictions.md#gaza_hostage_deal_jan_2025) |
| `gaza_ceasefire_holds_2025` | resolved · **no** | Pause-not-ceasefire; resume Oct 2025 | [prediction-resolution-gaza-ceasefire-holds-2025.md](../../notes/wire/prediction-resolution-gaza-ceasefire-holds-2025.md) | [IGL Gaza ceasefire register](../../notes/2025-freeman-igl-gaza-ceasefire-register.md) | [§ ceasefire](freeman-predictions.md#gaza_ceasefire_holds_2025) |
| `us_israel_iran_war_preparation_2025` | open | Active prep (Jan 21) | [prediction-resolution-us-israel-iran-war-preparation-2025.md](../../notes/wire/prediction-resolution-us-israel-iran-war-preparation-2025.md) | [IGL Iran war push register](../../notes/2025-freeman-igl-iran-war-push-register.md) | [§ iran prep](freeman-predictions.md#us_israel_iran_war_preparation_2025) |
| `iran_great_power_direct_war_entry` | open | No direct entry (Mar 28) | [prediction-resolution-iran-great-power-direct-war-entry.md](../../notes/wire/prediction-resolution-iran-great-power-direct-war-entry.md) | — · related: `us_israel_iran_war_preparation_2025` | [§ great-power](freeman-predictions.md#iran_great_power_direct_war_entry) |
| `china_tariff_capitulation_2025` | open | No capitulation (Apr 22) | [prediction-resolution-china-tariff-capitulation-2025.md](../../notes/wire/prediction-resolution-china-tariff-capitulation-2025.md) | — | [§ china tariff](freeman-predictions.md#china_tariff_capitulation_2025) |

**Related pairs (thesis map):** Iran war prep ↔ great-power direct entry — score lanes separately; use `title_conflict_patterns` and register strictness so bridge captures do not bleed.

### Israel trajectory dimensions (registry v4)

Parent `israel_self_destruction_trajectory` carries six preset **dimensions** on the parent row in [event-registry.json](../../data/event-registry.json). Freeman capture rows may carry optional `dimension` (non-registry pointer) for notes-lane hooks; the public shelf keeps the parent umbrella.

| dimension | Label |
| --- | --- |
| `israel_moral_pariah_status` | Western / global moral pariah treatment |
| `israel_regional_isolation` | Regional diplomatic isolation |
| `israel_us_support_erosion` | U.S. political / public support erosion |
| `israel_military_overextension` | Military overextension / blowback |
| `israel_economic_emigration_pressure` | Economic strain + emigration |
| `israel_internal_political_fragmentation` | Domestic political fragmentation |

## Wire closure workflow

1. Open the **wire resolution stub** for the event (table above).
2. Grade **closure hooks** with [news-verify](../../../.cursor/skills/news-verify/SKILL.md) / [wire-verify](../../../.cursor/skills/wire-verify/SKILL.md); paste verdict + cite into the stub table.
3. Fill **Resolution decision (operator)** on the stub; set `resolution_source` text for registry paste.
4. Update [event-registry.json](../../data/event-registry.json) (`status`, `outcome`, `resolved_date`, `resolution_source`) when closing.
5. Rebuild generated surfaces (below) so [freeman-predictions.md](freeman-predictions.md) source-trail tables and [prediction-registry.json](../../../runtime/artifacts/prediction-registry.json) reflect closure and capture-map v3.

## Auto-file and calibration

Hooks and thresholds per event live in [freeman-prediction-auto-file.json](../../data/freeman-prediction-auto-file.json). Manual gold for calibration = prediction notes **without** `auto_file: true` ([calibrate_auto_file.py](../../../scripts/calibrate_auto_file.py) `manual_only` default).

**Capture map + shelf (every recuration or rebuild):**

```bash
python3 scripts/bootstrap_voice_capture_map.py --speaker freeman --check
python3 scripts/build_voice_predictions.py --speaker freeman
python3 scripts/build_voice_predictions.py --speaker freeman --check
python3 scripts/check_voice_predictions.py --speaker freeman
python3 -m pytest tests/test_freeman_predictions.py tests/test_voice_predictions.py -q
```

**Full closure / auto-file chain** (when hooks, registry, or auto-file config change):

```bash
python3 scripts/auto_materialize_freeman_predictions.py --prune
python3 scripts/build_prediction_registry.py
python3 scripts/build_prediction_timeline.py
python3 scripts/build_voice_predictions.py --speaker freeman
python3 scripts/calibrate_auto_file.py --all-events
python3 scripts/check_voice_predictions.py --speaker freeman
```

Freeman-named wrappers (`build_freeman_predictions.py`, `check_freeman_predictions.py`) delegate to the same `--speaker freeman` builders.

**Calibration artifact:** [freeman-prediction-auto-file-calibration-all.json](../../../runtime/artifacts/freeman-prediction-auto-file-calibration-all.json)

## Generated artifacts

| Artifact | Role |
| --- | --- |
| [prediction-registry.json](../../../runtime/artifacts/prediction-registry.json) | Event + note join for pipeline |
| [prediction-timeline.json](../../../runtime/artifacts/prediction-timeline.json) | Chronological touchpoints |
| [freeman-prediction-crawl.json](../../../runtime/artifacts/freeman-prediction-crawl.json) | Crawl manifest (audit queue) |

## Stub checklist (operator)

- [ ] Open events graded at Freeman **closure trigger** with wire receipts in stub hooks
- [ ] Registry rows updated after each resolution decision
- [ ] Capture map passes `bootstrap_voice_capture_map.py --check` before shelf rebuild
- [ ] Auto-file calibration re-run after hook/config changes
