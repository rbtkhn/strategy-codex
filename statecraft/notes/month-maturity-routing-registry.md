---
note_id: month-maturity-routing-registry
note_type: synthesis
authority_level: shelf-native
source_basis: mixed
essay_candidate: false
created_at: 2026-06-01
updated_at: 2026-06-28
archive_links:
  - source-archive/statecraft/2025-11.md
  - source-archive/statecraft/2025-12.md
  - source-archive/statecraft/2026-01.md
  - source-archive/statecraft/2026-02.md
  - source-archive/statecraft/2026-03.md
  - source-archive/statecraft/2026-06-13/source-glenn-diesen-mearsheimer-karaganov-nuclear-strike-europe-restore-deterrence-2026-06-13.md
---
WORK only; not Record.

# Month maturity routing registry

## Purpose

Preserve one readable front door for the `month maturity routing stack` so the operator can see, at a glance, which statecraft months are being treated as `benchmark`, `watchlist`, or `closure-audit` objects and why.

This is a shelf-native operational note, not a doctrine file and not a replacement for the month-specific notes it points to.

Machine-readable companion surface:

- [month-maturity-routing-registry.json](../data/month-maturity-routing-registry.json)

Generated routing-support metadata:

- [month-routing-metadata.json](../data/month-routing-metadata.json)

## Current Registry

| Month | Route class | Maturity label | Status | Primary supporting surfaces | Next honest move |
| --- | --- | --- | --- | --- | --- |
| `2025-11` | `benchmark` | late pre-2026 fragmentation benchmark | `stable` | [November benchmark](november-2025-benchmark-note.md) | Use November as a narrower late-2025 benchmark month unless a specific speaker-month contradiction queue later appears. |
| `2025-12` | `benchmark` | late pre-2026 convergence benchmark | `stable` | [December benchmark](december-2025-benchmark-note.md) | Use December as the first late-2025 benchmark month unless a specific speaker-month contradiction queue later appears. |
| `2026-01` | `benchmark` | opening continuity/setup benchmark | `stable` | [January benchmark](january-2026-benchmark-note.md) | Keep January as an opening benchmark unless a bounded speaker-local contradiction queue later appears. |
| `2026-02` | `benchmark` | dense bridge/setup benchmark | `stable` | [February benchmark](february-2026-benchmark-note.md) | Keep February as a bridge/setup benchmark rather than reopening it as a generic backfill field. |
| `2026-03` | `benchmark` | early mature Iran-war benchmark | `stable` | [March benchmark](march-2026-benchmark-note.md), [March routing](march-2026-closure-method-application.md) | Preserve March for comparison work unless a finite, URL-backed contradiction queue later appears. |
| `2026-04` | `closure-audit` | audited cross-host bridge month | `audited-and-confirmed` | [April audit](wilkerson-april-2026-contradiction-audit.md), [April postmortem](april-2026-wilkerson-intake-sequence-postmortem.md), [Wilkerson April note](../voices/wilkerson/wilkerson-april-2026-note.md) | Treat April as an audited and confirmed closure month unless a new bounded contradiction object appears. |
| `2026-05` | `watchlist` | late negotiation/settlement pressure month with one live Parsi seam | `stable-with-live-seam` | [May watchlist](may-2026-speaker-watchlist.md), [May closure method](may-2026-closure-method-application.md), [Parsi/Wilkerson queue](parsi-wilkerson-may-2026-backfill-attention.md) | Falsify the remaining Parsi authored-middle candidate, then restate whether May closes as complete enough or remains slightly thin by archive truth. |
| `2026-06` | `watchlist` | opening watchlist | `open` | [June opening watchlist](june-2026-opening-watchlist.md) | Keep June in watchlist-first status until the month is large enough for either benchmark promotion or a bounded contradiction object. |

## Route Rule

Use the stack this way:

- `benchmark`
  The month is already dense and coherent enough to preserve for later comparison rather than reopen by default.

- `watchlist`
  The real job is honest archive-coverage judgment, with backfill attention only where evidence supports it.

- `closure-audit`
  The month has a finite, URL-backed contradiction queue or bounded completeness claim that can be falsified, repaired, or closed.

## Registry Boundary

The registry keeps cross-month routing legible, but the month notes still own their local arguments.

- use the registry to see the current route and next honest move
- use the month note itself for the substantive month reading
- use the machine-readable JSON and routing metadata when a script or skill needs persistent month state
- scaffold a starter note with `scripts/scaffold_statecraft_month_note.py --month YYYY-MM` and add `--route` only when the month is not yet registered

## Use Rule

Use this note when the operator asks:

- `what is this month routing stack called`
- `what month should we do next`
- `how are the current months classified`
- `which months are benchmark vs watchlist vs closure-audit`

Do not use this note as a substitute for the underlying month notes. Its job is to keep the routing stack persistent, readable, and reusable across sessions.
