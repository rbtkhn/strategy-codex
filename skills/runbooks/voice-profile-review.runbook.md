---
name: voice-profile-review
description: Compose voice-profile-panel QA pass for named speaker profiles.
portable: true
version: 0.1.0
scope_class: repo-governed
skills:
  - voice-profile-panel
outputs:
  - voice profile QA receipt for named speaker
authority: advisory_only
verification_level: receipt_required
risk_tier: low
---

# Voice Profile Review

## Purpose

Run a bounded QA pass on a named speaker voice profile using the voice-profile-panel skill.

## Trigger

**Operator phrases:** `runbook voice profile review`, `QA mercouris profile`.

## Skills Composed

| Step | Skill | Role |
|---:|---|---|
| 1 | `voice-profile-panel` | Panel QA on profile fingerprint and drift |

## Inputs Required

- Speaker id (mercouris, mearsheimer, barnes, …)
- Profile path under `statecraft/voices/`

## Workflow Steps

1. Confirm speaker and profile path.
2. Run **`voice-profile-panel`** procedure.
3. Report drift items and suggested fixes; profile edits require operator approval.

## Human Approval Points

- Before editing `*-profile.md` SSOT

## Stop Conditions

Stop if:

- profile missing
- speaker unmapped

## Verification / Proof Standard

Do not call this runbook complete unless:

- panel checklist completed
- drift items listed or clean receipt stated

## Outputs

- QA memo with drift list
- Optional patch proposal (operator approval required)

## Return Paths

- [skills/runbooks/README.md](README.md)
- [statecraft/voices/README.md](../../statecraft/voices/README.md)
