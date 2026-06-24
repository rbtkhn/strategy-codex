---
name: last30days
description: Deprecated legacy judgment-review skill. Use the periodic-statecraft-review runbook for new work.
preferred_activation: last30days
activation: last30days
portable: true
version: 0.2.0
category: legacy-redirect
status: deprecated
replacement: periodic-statecraft-review
scope_class: repo-governed
review_date: 2026-12-31
tags:
- operator
- deprecated
- statecraft
portable_source: skills/last30days/SKILL.md
synced_by: sync_portable_skills.py
---
# Deprecated — last30days

**Status:** Deprecated. Do not use this skill for new work.

**Use instead:** [`skills/runbooks/periodic-statecraft-review.runbook.md`](../runbooks/periodic-statecraft-review.runbook.md).

This file remains only for legacy trigger compatibility.

## Legacy activation

When the operator says `last30days`, route to the `periodic-statecraft-review` runbook if a time-window review is still intended.

## No independent methodology

This file must not contain independent judgment-review doctrine. Put workflow composition in the runbook and current methodology in active skills.


## Cursor / strategy-codex instance

Grace-Mar paths and strategy-notebook routing for `last30days`.

| Topic | Path |
|-------|------|
| Portable core | [skills/last30days/SKILL.md](../../../skills/last30days/SKILL.md) |
| Portable skills schema | [skills/_schema.md](../../../skills/_schema.md) |
| Portable skills manifest | [skills/manifest.yaml](../../../skills/manifest.yaml) |
| Governance contract | [AGENTS.md](../../../AGENTS.md) |
| Knowledge boundary | [docs/knowledge-boundary-framework.md](../../../docs/knowledge-boundary-framework.md) |
| Runtime vs Record | [docs/runtime-vs-record.md](../../../docs/runtime-vs-record.md) |
| Runtime complements | [docs/runtime/runtime-complements.md](../../../docs/runtime/runtime-complements.md) |
| MCP overview | [docs/mcp/mcp-stack-overview.md](../../../docs/mcp/mcp-stack-overview.md) |
| Strategy notebook hub | [docs/skill-work/work-strategy/strategy-notebook/README.md](../../../docs/skill-work/work-strategy/strategy-notebook/README.md) |
| Strategy notebook contract | [docs/skill-work/work-strategy/strategy-notebook/NOTEBOOK-CONTRACT.md](../../../docs/skill-work/work-strategy/strategy-notebook/NOTEBOOK-CONTRACT.md) |
| Strategy daily inbox | [docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md](../../../docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md) |
| Research skill example | [docs/skills/research/last30days.md](../../../docs/skills/research/last30days.md) |

## Grace-Mar defaults

- Treat `last30days` as a **WORK methodology skill**. It does not add a CLI, connector, scheduler, API credential flow, or live MCP server.
- Default strategy-notebook integration is **inbox-first**: produce a short brief, provenance log, and one optional paste-ready inbox line.
- Do **not** edit the daily inbox, `days.md`, author threads, `strategy-page` blocks, protected Record files, or prompt unless the operator explicitly requests a separate governed edit.
- Require primary attribution before recommending `thread:<expert_id>`. Otherwise use topical tags, `verify:` tails, or a watch item.
- Keep weak social/media claims in `Debates / Conflicts` unless the operator explicitly asks for a review stub.

## Workflow hooks

Use the relationship map in [docs/skills/research/last30days.md](../../../docs/skills/research/last30days.md): **manual** is primary, **coffee** may offer it under Historian/Intel, **conductor** may use it as one action-menu option, and **dream** may leave one tomorrow breadcrumb. None of those hooks run research, append inbox lines, or stage material automatically.

## Artifact and review routes

When the operator asks for an artifact, prefer:

```text
runtime/artifacts/research/last30days/<slug>.md
runtime/artifacts/research/last30days/<slug>.json
```

When the operator asks for stage-only material, prepare an inspectable review artifact or stub and state that it is **not** canonical truth. Use existing Grace-Mar staging/evidence-stub scripts only in a separate explicit execution step, after confirming the target surface.

## Strategy inbox line

Use the local one-liner shape:

```text
<source> | cold: <attribution-safe claim> // hook: <why it matters today> | <URL or locator> | verify:<status tags>
```

Recommended strategy tags include topic tags such as `IRAN`, `US-RU`, `NUC`, `ENERGY`, `SANCTIONS`, `NATO`, plus `verify:primary`, `verify:pending-primary`, `verify:most-recent-found`, or `verify:low-confidence` as appropriate.
