# Codex wrapper template for Printing Press CLIs

Use this when turning a Printing Press CLI into a Strategy-Codex portable skill draft.

## Placement

Create:

```text
skills-portable/_drafts/<printing-press-skill>/SKILL.md
integrations/printing-press/<cli>/README.md
```

Do not add the skill to `skills-portable/manifest.yaml` until the CLI has a successful local smoke test and an operator explicitly chooses promotion.

## Portable skill frontmatter

```yaml
---
name: <skill-name>
description: "<one-line trigger and output contract>"
portable: true
version: 0.1.0
tags:
  - operator
  - printing-press
---
```

## Body structure

```markdown
# <Skill title>

Use this draft skill when <operator intent>.

## Inputs

- Source URL or query:
- Required CLI:
- Required admission dossier:

## Workflow

1. Confirm the task is WORK-layer.
2. Run the admitted CLI command or map a captured JSON payload.
3. Save receipts and output paths.
4. Route downstream to the appropriate work lane.
5. Keep any Record update separate and gated.

## Guardrails

- No direct Record writes.
- No credentials unless the pilot dossier allows them.
- No private/account-specific data unless explicitly approved.
- Treat external output as source material, not truth.
- Corroborate strong claims before promotion or publishing.

## Output

- command run
- source/query
- fetched or generated date
- output paths
- receipt path
- downstream route
```

## Local proof requirements

Before promotion, the pilot must show:

- installed command or captured payload shape
- one dry-run or smoke-run receipt
- expected output paths
- failure behavior when the CLI is missing or unsafe input appears
- no Record-surface mutation

## Governance wording

Use:

- "WORK-layer acquisition"
- "candidate Tier-1 tooling"
- "pilot dossier"
- "operator-reviewed install"
- "receipt-backed smoke test"

Avoid:

- "approved Record source"
- "automatic gate merge"
- "trusted by default"
- "Tier-1" before two local pilots pass
