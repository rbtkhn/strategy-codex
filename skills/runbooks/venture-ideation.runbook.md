---
name: venture-ideation
description: Compose ideation-engine, mtp, and abundance-native-ventures into a product strategy chain.
portable: true
version: 0.1.0
scope_class: repo-governed
skills:
  - ideation-engine
  - mtp
  - abundance-native-ventures
outputs:
  - bounded venture thesis and MTP-aligned next steps
authority: advisory_only
verification_level: receipt_required
risk_tier: low
---

# Venture Ideation

## Purpose

Generate venture options, filter through MTP purpose alignment, and shape abundance-native framing.

## Trigger

**Operator phrases:** `runbook venture ideation`, `ideation then mtp`, commercial strategy pass.

## Skills Composed

| Step | Skill | Role |
|---:|---|---|
| 1 | `ideation-engine` | Top-N venture/thesis options |
| 2 | `mtp` | Purpose alignment and governor filter |
| 3 | `abundance-native-ventures` | Abundance-native venture framing on winner |

**Cadence overlays (Cursor-only):** `coffee`, `dream`, `repo-hygiene-pass`, `pros-and-cons` — see sequences below.

## Inputs Required

- Operator scope (venture lane, audience, constraints)
- Optional existing thesis or backlog item

## Workflow Steps

1. Run **`ideation-engine`** — produce Top 3 (or operator count).
2. Operator picks winner or combo.
3. Run **`mtp`** on winner — purpose/governor pass.
4. Run **`abundance-native-ventures`** when abundance-native framing applies.
5. Optional: **`pros-and-cons`** on final thesis (Cursor skill).

### Cadence sequences (from legacy mtp-coffee-dream)

| Order | When |
|-------|------|
| `coffee` → **A Confirm** → `mtp` → `repo-hygiene-pass` | Pre-ship wedge on large dirty tree |
| `ideation-engine` → `mtp` → `pros-and-cons` | Venture filter after Top 3 |
| `dream` → next `coffee` → `mtp` | Morning after noisy day when purpose drift flagged |

## Human Approval Points

- Before external outreach or publish
- Before treating thesis as committed roadmap

## Stop Conditions

Stop if:

- operator declines all ideation options
- MTP governor rejects thesis without alternative

## Verification / Proof Standard

Do not call this runbook complete unless:

- ideation output captured
- MTP pass recorded (keep/kill/pivot)
- abundance framing applied or explicitly skipped

## Outputs

- Venture thesis memo (chat or docs candidate)
- MTP alignment line

## Return Paths

- [skills/runbooks/README.md](README.md)
- [skills/mtp/SKILL.md](../mtp/SKILL.md)
