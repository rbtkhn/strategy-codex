# PH-CIV Promotion Ledger

WORK only; not Record.

This ledger is the compact intake surface for promoting public `ph-civ` insight into `civ-state`.

Its job is narrower than the [CIV-STATE review queue](review-queue.md). The review queue governs upstream corrections to `civ-state` once a source-memory change is actually warranted. This ledger sits one step earlier and records the conversion attempt itself:

- what public `ph-civ` source or pattern was observed
- what mechanism seems extractable
- where it would land in `civ-state`
- what counterweight prevents overreach
- what downstream lane or transaction use it may later support

Short handoff:

`ph-civ source -> promotion ledger -> civ-state destination test -> review queue if warranted -> downstream statecraft use`

## Use Rule

Use this ledger when a `ph-civ` chapter, card, corridor, or commentary surface seems to expose a reusable civilization-state mechanism, but that mechanism has not yet been stabilized into `civ-state`.

Do not use this ledger for:

- pure lecture commentary
- packet-completion tracking
- lane-local drafting ideas that do not change `civ-state`
- direct edits to `ph-civ`
- direct edits to `civ-state` made without staging the conversion logic

If the observation is still mainly a public reading aid, keep it in `ph-civ`. If it already requires a real `civ-state` source-memory change, record it here first, then escalate to [review-queue.md](review-queue.md) when the destination and counterweight are clear enough.

## Promotion Test

Before opening a new ledger entry, ask:

1. Is the source public and stable enough to cite by `ph-civ` path, `source_id`, `pattern_id`, or chapter surface?
2. Can the insight be rewritten as a continuity, legitimacy, geography, carrier, failure-mode, or counterweight mechanism?
3. Does it survive compression out of lecture-local rhetoric?
4. Is there a plausible `civ-state` destination object already waiting for it?
5. Is there a counterweight that prevents propaganda, false analogy, or overreach?

If the answer to `2`, `3`, or `5` is no, the observation is not ready for promotion.

## Entry Shape

Valid destination classes include:

- `civilization-<civ>.md`
- `empire-<civ>.md`
- `statecraft-<civ>.md`
- `geo-strategy-<civ>.md`
- `game-theory-<civ>.md`
- `secret-history-<civ>.md`
- sacred grammar
- state-memory
- review queue

Use this block for each promotion candidate:

```markdown
## PHCIVPROMO-YYYYMMDD-XX
- PH-CIV source:
- Source type: chapter / card / corridor / commentary / route / other
- Candidate mechanism:
- Destination `civ-state` object:
- Why this belongs in `civ-state`:
- Counterweight:
- Possible downstream lane or transaction use:
- Needs `civ-state` review-queue escalation? yes / no
- Status: observing / distilled / escalated / rejected
```

## Status Meanings

- `observing` - interesting, but not yet compressed enough for promotion
- `distilled` - mechanism is clear and destination is plausible
- `escalated` - a real upstream `civ-state` candidate now belongs in [review-queue.md](review-queue.md)
- `rejected` - useful as `ph-civ`, but not a valid `civ-state` promotion

## Boundary Note

This ledger is a membrane-thickening tool, not a silent rewrite path.

- `ph-civ` remains the public source world.
- `civ-state` remains the compact source-memory substrate.
- [review-queue.md](review-queue.md) remains the actual upstream change surface.

This file exists so the conversion step is explicit and auditable before doctrine moves.

## Ledger

_pending_
