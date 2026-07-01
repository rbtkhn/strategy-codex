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

## Open items

_See JSON artifact for current machine queue; populate via check scripts._
