---
note_id: intake-digest-TEMPLATE
note_type: intake
authority_level: draft
source_basis: mixed
essay_candidate: false
created_at: 2026-06-18
updated_at: 2026-06-28
archive_links:
  - source-archive/statecraft/YYYY-MM-DD/source-example-slug-YYYY-MM-DD.md
  - source-archive/statecraft/<day>/day-index.md
---

# Statecraft Intake Digest — YYYY-MM-DD

Precursor to [daily synthesis](../../synthesis/METHOD.md) — not a substitute. Generate with:

```bash
python3 scripts/statecraft_intake_queue.py --day YYYY-MM-DD --write-digest
```

Spec: [docs/statecraft-intake-queue.md](../../../docs/statecraft-intake-queue.md)

## Top signals (queue)

| Rank | Source | Status | Threads | Why it matters |
| ---: | --- | --- | --- | --- |
| 1 | `source-example-slug` | new | thread-a | v0 rule-based reasoning from frontmatter |

## Promote to daily synthesis

- [source-example-slug](../../../../source-archive/statecraft/YYYY-MM-DD/source-example-slug-YYYY-MM-DD.md) — operator promotes into `statecraft/synthesis/day/YYYY-MM-DD.md`

## Hold / watch

- _(sources awaiting sidecar or operator review)_

## Discard / low signal

- _(operator-marked `discarded` in sidecar)_

## Already in daily

- _(sources linked from daily synthesis)_
