---
name: last30days
preferred_activation: last30days
description: Research a recent topic with last-30-days discipline, source-class routing, provenance, uncertainty labels, and stage-only governance boundaries.
portable: true
version: 1.0.0
tags:
- research
- strategy
- provenance
- governance
portable_source: skills-portable/last30days/SKILL.md
synced_by: sync_portable_skills.py
---
# Last 30 Days Research

**Preferred activation (operator):** say the exact phrase **`last30days`**. **Aliases:** **`research last30days`**, **`last 30 days research`**.

Use this skill when the operator wants a recent-topic research brief that is time-bounded, provenance-rich, and careful about what is known, disputed, or only suggested by weak signals.

This is a methodology skill. It does not assume live connector access, API keys, scheduled jobs, or automatic staging. Use whatever source tools the current host actually provides, and label missing coverage plainly.

## When to Use

- A topic may have changed in the last month.
- The operator wants current signals before deciding whether to capture, watch, or deepen a thread.
- A work lane needs a concise brief with citations and uncertainty, not a broad essay.
- A claim might become a candidate, evidence stub, or notebook line only after review.

## Source Classes

Route the query across source classes only when the current host can access them:

- **Web / news:** current articles, official pages, public reports.
- **Social:** public posts or forum threads; treat as sentiment or claim signals unless primary.
- **Video / audio:** interviews, channels, transcripts, show notes.
- **Finance / filings:** prices, market data, company filings, investor materials.
- **Code / technical:** repositories, release notes, issues, changelogs.
- **Academic / preprint:** papers, abstracts, conference pages, recent citations.
- **Operator-supplied:** pasted links, notes, transcripts, or files.

Do not claim a source class was searched if the host did not actually search it.

## Time Discipline

Default window: **last 30 days** from the operator's current date.

- Use strict publication, filing, upload, or post dates when available.
- If a source tool cannot filter by date, label results as **most recent found**.
- If an important older source is needed for context, put it under **Background**, not **last-30-days evidence**.
- Preserve exact dates in the provenance log whenever possible.

## Workflow

1. **Frame the query.** Restate the topic, date window, likely source classes, and any excluded surfaces.
2. **Gather recent sources.** Prefer primary, official, or directly attributed material before commentary.
3. **Classify signals.** Separate confirmed facts, attributed claims, social sentiment, forecasts, conflicts, and unknowns.
4. **Synthesize briefly.** Lead with the highest-signal findings; keep speculative material visibly labeled.
5. **Write provenance.** For every material claim, include source name, date, link or locator, and confidence note.
6. **Route cautiously.** Recommend capture, watch, or deeper research. Prepare stage-only review material only when the operator asks.

## Output Shape

Use this shape by default:

```markdown
# Research Brief: <query>

## Time Window
<dates searched; note strict vs most-recent-found>

## Key Signals
- <signal> — <source/date/confidence>

## Debates / Conflicts
- <who disagrees or what remains uncertain>

## Implications for Grace-Mar
- Strategy routing:
- Possible Record / evidence candidate:
- Operator watch items:

## Provenance Log
| Source | Date | Link / locator | Used for | Confidence |
|--------|------|----------------|----------|------------|

## Stage Status
<none / operator-requested review artifact prepared / operator-requested candidate draft prepared>
```

## Strategy-Notebook Default

When the query is strategy-notebook work, use **frontier scan for today's inbox** as the default posture.

- Default destination: one optional inbox-ready line, not a page or thread edit.
- Default output: short brief plus provenance log.
- Main value: catch fresh signals before they vanish.
- Recommend persistent author routing only when attribution is primary and the operator likely tracks that voice.
- Keep weak social or media claims in **Debates / Conflicts** with low-confidence labels unless the operator explicitly routes them.

Suggested one-line shape:

```text
<source> | cold: <attribution-safe claim> // hook: <why it matters today> | <URL or locator> | verify:<status tags>
```

## Governance Boundaries

- Do not merge, approve, or treat research output as canonical truth.
- Do not write directly to protected identity, evidence, skill, prompt, or notebook synthesis surfaces.
- Do not stage automatically. Stage-only review material requires an explicit operator request.
- Do not treat social posts, tool summaries, search snippets, or model synthesis as evidence without provenance.
- Abstain or narrow scope when the topic is personal, sensitive, unsafe, or not researchable with available sources.

## Agent Behavior Norms

- **Provenance first** — Prefer fewer claims with dates and links over broader uncited synthesis.
- **Boundary clarity** — Research can inform work; it does not become durable truth by being well written.
- **No fake coverage** — Say which source classes were not searched.
- **Conflict preservation** — Keep disagreement visible when sources conflict.
- **Brevity by default** — Start compact; deepen only when the operator asks.


## Cursor / grace-mar instance

Grace-Mar paths and strategy-notebook routing for `last30days`.

| Topic | Path |
|-------|------|
| Portable core | [skills-portable/last30days/SKILL.md](../../../skills-portable/last30days/SKILL.md) |
| Portable skills schema | [skills-portable/_schema.md](../../../skills-portable/_schema.md) |
| Portable skills manifest | [skills-portable/manifest.yaml](../../../skills-portable/manifest.yaml) |
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
artifacts/research/last30days/<slug>.md
artifacts/research/last30days/<slug>.json
```

When the operator asks for stage-only material, prepare an inspectable review artifact or stub and state that it is **not** canonical truth. Use existing Grace-Mar staging/evidence-stub scripts only in a separate explicit execution step, after confirming the target surface.

## Strategy inbox line

Use the local one-liner shape:

```text
<source> | cold: <attribution-safe claim> // hook: <why it matters today> | <URL or locator> | verify:<status tags>
```

Recommended strategy tags include topic tags such as `IRAN`, `US-RU`, `NUC`, `ENERGY`, `SANCTIONS`, `NATO`, plus `verify:primary`, `verify:pending-primary`, `verify:most-recent-found`, or `verify:low-confidence` as appropriate.
