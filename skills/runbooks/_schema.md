# Runbook Schema

A runbook composes portable skills into a repeatable workflow. Runbooks are **orchestration surfaces** — not new methodology sources for the skills they call.

## Filename

Use:

`<workflow-name>.runbook.md`

Example:

`source-to-daily-synthesis.runbook.md`

## Frontmatter

Required:

- `name`
- `description`
- `portable`
- `version`
- `scope_class`
- `skills`
- `outputs`
- `authority`

Optional:

- `tags`
- `requires`
- `host_notes`
- `verification_level`
- `risk_tier`
- `surfaces` — repo-relative paths to non-skill surfaces (sheets, routers); validated with `Path.exists`

### `skills` vs `surfaces`

- `skills:` — portable/manifest-listed skill names only (validator resolves to `skills/manifest.yaml` or `skills/<name>/SKILL.md`).
- `surfaces:` — optional paths such as `statecraft/sheets/transaction-router.md`.
- **Skills Composed** table in the body may also reference Cursor-only skills and repo paths with explicit links.

## Required sections

1. Purpose
2. Trigger
3. Skills Composed
4. Inputs Required
5. Workflow Steps
6. Human Approval Points
7. Stop Conditions
8. Verification / Proof Standard
9. Outputs
10. Return Paths

## Authority

`authority` must be advisory-only (e.g. `advisory_only`, `advisory-only`). Runbooks must not claim merge, publish, or canon authority.

## Example frontmatter

```yaml
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
```

## Return paths

Every runbook should link back to:

- [skills/README.md](../README.md)
- [skills/_schema.md](../_schema.md)
- [docs/harness-architecture-map.md](../../docs/harness-architecture-map.md) (when harness context matters)
