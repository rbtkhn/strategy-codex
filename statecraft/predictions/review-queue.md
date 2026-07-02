# Prediction review queue

Operator backlog for registry closure, falsifiers, trajectory decomposition, and notes-lane enrollment. Machine-readable companion: [`runtime/artifacts/prediction-review-queue.json`](../../runtime/artifacts/prediction-review-queue.json).

Regenerate queue items:

```bash
python3 scripts/check_event_registry.py --emit-review-queue
python3 scripts/check_voice_enrollment.py --emit-review-queue
```

## Queue types

| Type | Meaning |
| --- | --- |
| `needs_falsifier` | Event lacks `falsifier` and is not `not_falsifiable` |
| `ambiguous_status` | Shelf record label conflicts with registry status |
| `trajectory_without_children` | Broad trajectory event has empty `child_event_ids` |
| `orphan_event_id` | Capture map references unknown registry id |
| `shift_without_note` | Timeline shift without operator note |
| `trail_without_timeline` | Repeated capture stance with no timeline entry |
| `shelf_without_notes_lane` | Generated shelf exists; notes-lane enrollment incomplete |
| `resolved_without_wire_stub` | Resolved event missing canonical wire stub path |
| `review_merge` | Compression engine flagged Macgregor seed overlap — operator must accept or reject merge before deprecate |

## Closed items (operator decisions)

### Macgregor Ukraine cluster — merge rejected (2026-06-29)

**Decision:** **Keep separate** — do not merge into `ukraine_escalation_russian_capitulation`.

| Source `event_id` | Proposed target | Verdict | Rationale |
| --- | --- | --- | --- |
| `ukraine_western_aid_prolongs_war` | `ukraine_escalation_russian_capitulation` | **Reject merge** | Distinct falsifier (aid prolongs war vs Kellogg capitulation mechanism); target already **resolved · no** |
| `nato_strategic_exposure_ukraine` | `ukraine_escalation_russian_capitulation` | **Reject merge** | Distinct falsifier (NATO alliance exposure); same-interview thematic overlap only |

**Context:** All three Macgregor capture-map rows cite `source-diesen-macgregor-victory-day-russia-already-won-the-war-2025-05-09.md`. Fingerprints differ on question + falsifier (Phase 3 Rule B). Phase 4.5 signals remain per-event.

**Compression review:** closed in [`compression_engine.py`](../../scripts/registry_pipeline/compression_engine.py) via `MACGREGOR_MERGE_REJECTED` — pipeline no longer emits open `review_merge` rows for these pairs.

## Open items

_See JSON artifact for current machine queue; populate via check scripts._
