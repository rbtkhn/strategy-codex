---
name: source-to-daily-synthesis
description: Compose source intake and state synthesis into a bounded archive-to-daily workflow.
portable: true
version: 0.1.0
scope_class: repo-governed
skills:
  - statecraft-source-intake
  - state-synthesis
outputs:
  - source-archive/statecraft object
  - intake queue report
  - statecraft/daily synthesis candidate
authority: advisory_only
verification_level: receipt_required
risk_tier: medium
---

# Source to Daily Synthesis

## Purpose

Turn an operator-supplied transcript-bearing source into a landed archive object, honest queue state, and a bounded daily synthesis candidate on the statecraft side.

## Trigger

**Operator phrases:** `runbook source to daily`, or a pasted transcript with intent to land archive and produce daily synthesis.

**Use when:**

- the operator has a transcript-bearing source in hand
- the next honest move is archive land then day-batch synthesis

**Do not use when:**

- lane ownership is unresolved — route to `state-deploy` first
- the object is cross-lane or objection-shaped — route to `statecraft/compact/` first
- lane entry menus are needed before archive — see `statecraft-lane-intake-router` (Cursor skill)
- daily promotion requires packet gate — run `packet-before-synthesis` before treating synthesis as promotion-ready

## Skills Composed

| Step | Skill / surface | Role |
|---:|---|---|
| 1 | `statecraft-source-intake` | Land full-source archive object with honest provenance |
| 2 | `state-synthesis` | Produce bounded daily synthesis candidate from landed day batch |
| 3 | `packet-before-synthesis` (optional gate) | Verify queue/packet discipline before daily promotion |

## Inputs Required

- Operator-pasted transcript or authorized fetch
- Publication date or `_aired-pending/` staging decision
- Source URL or identifiable title when available
- Family/speaker routing hint when non-obvious

## Workflow Steps

1. Run **`statecraft-source-intake`** — sidecar land recipe; no monolithic archive write on Windows when chunked land applies.
2. Confirm archive file exists under `source-archive/statecraft/<day>/` with frontmatter and provenance.
3. Refresh day source-index (`README.md`) or explicitly defer with reason in the receipt.
4. Run intake queue report or explicitly defer.
5. When the day batch is real, run **`state synthesis`** on that day.
6. If promotion to daily shelf is intended, pass **`packet-before-synthesis`** gate or mark synthesis as **candidate only**.

## Human Approval Points

- Before treating synthesis as promoted daily (operator explicit)
- Before merge, publish, or Record-bearing edits (never automatic)

## Stop Conditions

Stop if:

- required source text is missing
- archive truth is incomplete (stub only, no body)
- verification cannot be performed (no path to confirm land)
- operator approval is required for promotion and not given
- `packet-before-synthesis` fails and operator did not accept candidate-only output

## Verification / Proof Standard

Do not call this runbook complete unless:

- archive capture file exists at expected path with YAML frontmatter
- source URL / provenance is recorded or explicitly marked unknown
- day source-index refresh was run or deferral is stated in the receipt
- intake queue report was run or deferral is stated
- daily synthesis was produced **or** clearly marked **not yet promoted** with reason

Evidence to report:

- archive path(s)
- frontmatter keys present (`source_url`, `kind`, family fields as applicable)
- synthesis output path or explicit deferral
- falsifier line if promotion was skipped

## Outputs

- `source-archive/statecraft/YYYY-MM-DD/source-*.md`
- optional queue report receipt
- `statecraft/daily/` synthesis candidate or promoted daily (operator-gated)

## Return Paths

- [skills/runbooks/README.md](README.md)
- [skills/README.md](../README.md)
- [skills/_schema.md](../_schema.md)
- [docs/harness-architecture-map.md](../../docs/harness-architecture-map.md)
