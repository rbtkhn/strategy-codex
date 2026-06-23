---
name: last30days
description: Research a recent topic with last-30-days discipline, source-class routing, provenance, uncertainty labels, and stage-only governance boundaries.
preferred_activation: last30days
activation: last30days
portable: true
version: 1.0.0
category: judgment-enhancement
status: active
scope_class: repo-governed
tags:
  - research
  - strategy
  - provenance
  - governance
---
# Last 30 Days Research

**Preferred activation:** say **`last30days`**, **`research last30days`**, or **`last 30 days research`** with a query.

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
