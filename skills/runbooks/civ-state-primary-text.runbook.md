---
name: civ-state-primary-text
description: Compose civ-state entry with primary text acquisition workflow.
portable: true
version: 0.1.0
scope_class: repo-governed
skills:
  - civ-state
  - civ-state-primary-text-acquisition
outputs:
  - acquired primary text receipt under civ-state volume tree
authority: advisory_only
verification_level: receipt_required
risk_tier: medium
---

# CIV-STATE Primary Text

## Purpose

Open the CIV-STATE domain pack and run primary text acquisition for one bounded volume.

## Trigger

**Operator phrases:** `runbook civ state primary text`, `acquire primary text` with civ-state scope.

## Skills Composed

| Step | Skill | Role |
|---:|---|---|
| 1 | `civ-state` | Orient volume, lane, and authority boundaries |
| 2 | `civ-state-primary-text-acquisition` | Acquire, classify, store primary text |

## Inputs Required

- Civilization/volume target
- Source URL or operator-owned text
- Acquisition class (public domain, licensed, operator paste)

## Workflow Steps

1. Run **`civ state`** entry — confirm volume and lane.
2. Run **`civ-state-primary-text-acquisition`** with bounded scope.
3. Report storage path and classification; stop before canon claims.

## Human Approval Points

- Before treating text as volume-canonical
- Before external publish

## Stop Conditions

Stop if:

- licensing unclear
- volume target ambiguous

## Verification / Proof Standard

Do not call this runbook complete unless:

- primary text stored at declared path
- classification recorded
- civ-state entry receipt cited

## Outputs

- Primary text artifact path
- Acquisition receipt

## Return Paths

- [skills/runbooks/README.md](README.md)
- [skills/civ-state/SKILL.md](../civ-state/SKILL.md)
