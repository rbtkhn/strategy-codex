---
name: transcript-intake
description: Compose YouTube/transcript cleanup chain from raw input through source-clean before archive land.
portable: true
version: 0.1.0
scope_class: repo-governed
skills:
  - youtube-raw-input-transcript
  - transcript-cleanup
  - transcript-proper-noun-normalization
  - source-clean
outputs:
  - cleaned transcript text ready for statecraft-source-intake
authority: advisory_only
verification_level: receipt_required
risk_tier: low
---

# Transcript Intake

## Purpose

Run the default transcript hygiene chain before **`statecraft-source-intake`** lands an archive object.

## Trigger

**Operator phrases:** `runbook transcript intake`, `clean transcript chain`, pasted ASR with cleanup intent.

**Use when:**

- transcript text exists but needs normalization before archive land
- operator wants the full cleanup ladder, not a single skill in isolation

**Do not use when:**

- archive land is the immediate goal with clean text — use **`statecraft-source-intake`** directly
- roster discovery is needed — use **`check-sources`** first

## Skills Composed

| Step | Skill | Role |
|---:|---|---|
| 1 | `youtube-raw-input-transcript` | Materialize or stage raw transcript input (legacy paths only when explicitly requested) |
| 2 | `transcript-cleanup` | ASR/format cleanup |
| 3 | `transcript-proper-noun-normalization` | Entity and place-name normalization |
| 4 | `source-clean` | Final source-clean pass before intake handoff |
| 5 | `statecraft-source-intake` | Archive land (next runbook or explicit operator step) |

## Inputs Required

- Transcript text or authorized fetch
- Source URL and publication date when available
- Speaker/family routing hint when non-obvious

## Workflow Steps

1. Confirm transcript body is present; stop if missing.
2. Run **`transcript-cleanup`** on the body.
3. Run **`transcript-proper-noun-normalization`** for entity pass labels.
4. Run **`source-clean`** for final hygiene.
5. Hand off cleaned text to **`statecraft-source-intake`** (operator approval before land).

## Human Approval Points

- Before archive land (`statecraft-source-intake`)
- Before deleting operator-original paste

## Stop Conditions

Stop if:

- transcript is empty or fetch unauthorized
- cleanup scripts fail without recovery path
- operator declines archive land

## Verification / Proof Standard

Do not call this runbook complete unless:

- each skill step was run or explicitly skipped with reason
- cleaned text is ready for intake with provenance noted
- entity normalization receipt or deferral is stated

Evidence to report:

- before/after line count or sample diff
- scripts run and exit codes
- handoff path for intake

## Outputs

- Cleaned transcript text (chat or staging path)
- Receipt for intake handoff

## Return Paths

- [skills/runbooks/README.md](README.md)
- [skills/README.md](../README.md)
- [skills/_schema.md](../_schema.md)
