---
name: civ-state-volume-hardening
description: Compose civ-state entry with volume hardening pass for CIV-STATE structure.
portable: true
version: 0.1.0
scope_class: repo-governed
skills:
  - civ-state
  - civ-state-volume-harden
outputs:
  - hardened volume STATUS and spine receipts
authority: advisory_only
verification_level: receipt_required
risk_tier: medium
---

# CIV-STATE Volume Hardening

## Purpose

Open CIV-STATE and run a bounded volume hardening pass (STATUS, spine, proof objects).

## Trigger

**Operator phrases:** `runbook civ state harden`, `harden civ volume` with named volume.

## Skills Composed

| Step | Skill | Role |
|---:|---|---|
| 1 | `civ-state` | Domain pack entry and routing |
| 2 | `civ-state-volume-harden` | Harden volume structure and proof surfaces |

## Inputs Required

- Volume id or path
- Operator goal (spine, STATUS, proof hardening)

## Workflow Steps

1. Run **`civ state`** — confirm volume scope.
2. Run **`civ-state-volume-harden`** on named volume.
3. Report validator/sync receipts; stop before public publish boundary changes.

## Human Approval Points

- Before public PH-CIV publish boundary changes

## Stop Conditions

Stop if:

- volume path missing
- hardening scope undefined

## Verification / Proof Standard

Do not call this runbook complete unless:

- hardening skill outputs listed
- STATUS/spine paths cited or deferral stated

## Outputs

- Updated volume STATUS/spine artifacts (candidate)

## Return Paths

- [skills/runbooks/README.md](README.md)
- [skills/civ-state/SKILL.md](../civ-state/SKILL.md)
