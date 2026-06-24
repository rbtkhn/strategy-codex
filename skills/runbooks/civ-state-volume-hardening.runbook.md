---
name: civ-state-volume-hardening
description: Compose civ-state entry with volume hardening pass for CIV-STATE structure.
portable: true
version: 0.2.0
scope_class: repo-governed
skills:
  - civ-state
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

Legacy **`civ-state-volume-harden`** triggers redirect here.

## Skills Composed

| Step | Surface | Role |
|---:|---|---|
| 1 | `civ-state` | Domain pack entry and routing |
| 2 | **Volume-hardening workflow** (this runbook) | Harden volume structure and proof surfaces |

## Inputs Required

- Volume id or path
- Operator goal (spine, STATUS, proof hardening)

## Workflow Steps

1. Run **`civ state`** — confirm volume scope.
2. **Identify target layer** — front-door doctrine, volume README pass, opener normalization, or civilization-state audit.
3. **Resolve sovereignty chain** — what survives rupture, mutates, and current carrier; legitimacy sequence or explicit gap.
4. **Run five required checks** — civilization-state claim; sovereignty chain; deep grammar / sovereign opening / current carrier; legitimacy sequence; retrieval consequence per layer.
5. **Inspect lane `state-memory`** — compression, ratification, contested inheritance, founder smoothness before widening.
6. **Write opener block + thesis together** — deep grammar, sovereign opening, current carrier; force asymmetry where truth requires it.
7. Report validator/sync receipts; stop before public publish boundary changes.

## Human Approval Points

- Before public PH-CIV publish boundary changes

## Stop Conditions

Stop if:

- volume path missing
- hardening scope undefined
- any of the five required checks still blurry

## Verification / Proof Standard

Do not call this runbook complete unless:

- hardening outputs listed
- STATUS/spine paths cited or deferral stated

## Outputs

- Updated volume STATUS/spine artifacts (candidate)

## Return Paths

- [skills/runbooks/README.md](README.md)
- [skills/civ-state/SKILL.md](../civ-state/SKILL.md)
