---
name: source-to-transaction-fit
description: Route a verified statecraft source or daily synthesis object through transaction-fit logic.
portable: true
version: 0.1.0
scope_class: repo-governed
skills:
  - statecraft-source-intake
  - state-synthesis
surfaces:
  - statecraft/sheets/transaction-router.md
outputs:
  - transaction fit classification
  - mismatch record when near/none
authority: advisory_only
verification_level: receipt_required
risk_tier: medium
---

# Source to Transaction Fit

## Purpose

Route a verified statecraft source or daily synthesis object through transaction-fit logic without auto-creating transaction directories.

## Trigger

**Operator phrases:** `runbook transaction fit`, or a landed source/daily with question "which transaction object fits?"

**Use when:**

- source floor exists (archive or honest daily wedge)
- crisis object is named enough to compare against the transaction plateau

**Do not use when:**

- archive land is incomplete — run `source-to-daily-synthesis` or `statecraft-source-intake` first
- lane ownership unresolved — `state-deploy`
- cross-lane objection object — `statecraft/compact/`
- lane intake family unresolved — `statecraft-lane-intake-router`

## Skills Composed

| Step | Skill / surface | Role |
|---:|---|---|
| 1 | `statecraft-source-intake` | Ensure source floor exists (land or verify existing) |
| 2 | `state-synthesis` | Name crisis object from day batch when needed |
| 3 | [transaction-router.md](../../statecraft/sheets/transaction-router.md) | Classify exact / near / none fit |

## Inputs Required

- Landed archive path or daily synthesis with named crisis object
- Operator question or transaction hypothesis (optional)

## Workflow Steps

1. Confirm **source floor** — archive file or daily parent link.
2. Name the **object** (crisis object + settlement spine question).
3. Open **transaction router** sheet; apply exact / near / none rules.
4. Record fit class and mismatch notes for near fit.
5. **Do not** create new transaction directories unless operator explicitly asks.

## Human Approval Points

- Before opening or editing transaction bundle files
- Before recommending new transaction candidate promotion

## Stop Conditions

Stop if:

- no source floor
- object unnamed or still contested across lanes
- fit logic would require inventing a new transaction without operator ask

## Verification / Proof Standard

Do not call this runbook complete unless:

- source floor path is cited
- object is named in one line
- fit is **exact**, **near**, or **none** with honest label
- mismatch is recorded for near fit
- no new transaction directory was created unless operator explicitly requested

Evidence to report:

- source/daily path
- fit class + one-line rationale
- opened transaction bundle path (exact fit) or analogy + mismatch (near fit)

## Outputs

- Fit classification (exact / near / none)
- Optional note stub pointing at transaction bundle or mismatch record

## Return Paths

- [skills/runbooks/README.md](README.md)
- [statecraft/sheets/transaction-router.md](../../statecraft/sheets/transaction-router.md)
- [skills/_schema.md](../_schema.md)
