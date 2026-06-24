---
name: civ-state-primary-text
description: Compose civ-state entry with primary text acquisition workflow.
portable: true
version: 0.2.0
scope_class: repo-governed
skills:
  - civ-state
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

Legacy **`civ-state-primary-text-acquisition`** triggers redirect here.

## Skills Composed

| Step | Surface | Role |
|---:|---|---|
| 1 | `civ-state` | Orient volume, lane, and authority boundaries |
| 2 | **Primary-text workflow** (this runbook) | Acquire, classify, store primary text |

## Inputs Required

- Civilization/volume target
- Source URL or operator-owned text
- Acquisition class (public domain, licensed, operator paste)

## Workflow Steps

1. Run **`civ state`** entry — confirm volume and lane.
2. **Fix source identity** — civilization, era, branch, title, author/body, source type.
3. **Create or refine source record** — stable `source_id`; rights, witness, storage metadata before text.
4. **Classify rights early** — `public_domain`, `official_government_text`, `operator_authored_transcription`, `modern_translation_restricted`, or `unclear`; narrow if unclear.
5. **Locate lawful witness** — official archive → PD library → academic edition → stable transcription → rights-safe scan → bounded manual transcription.
6. **Lock witness and working translation** — one canonical working translation; alternates as metadata only.
7. **Store by class** — `metadata_only`, `excerpt_only`, or `full_text_sidecar`; report path and classification; stop before canon claims.

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
