# last30days Research Skill Example

> **Deprecated (2026-06):** The `last30days` skill stub redirects to [`periodic-statecraft-review` runbook](../../skills/runbooks/periodic-statecraft-review.runbook.md). This page remains a **research workflow example** only.

**Status:** WORK / skill example. This page demonstrates usage only; it does not add live connectors, scheduled research, or Record authority.

Use **`runbook periodic review`** (or legacy `last30days` trigger → runbook redirect) when a strategy topic needs a short current frontier scan with dates, links, uncertainty labels, and one optional inbox-ready line.

## Workflow Hooks

- **Manual:** say `last30days "<topic>"` whenever a current topic needs a recent-source check.
- **Coffee:** offer it inside **C. Historian -> A. Intel** when today's strategy frontier is stale; do not add a sixth hub line and do not run it during Step 1.
- **Conductor:** use it as one possible A-C action when a master pass needs fresh external signal: Toscanini for verification, Furtwängler for tension mapping, Bernstein for stakes, Karajan for month-arc fit, Kleiber for one-query scope control.
- **Dream:** leave at most one tomorrow breadcrumb such as `run last30days on <topic>`; do not browse or write notebook lines during dream by default.

## Example Prompt

```text
last30days "Iran / Russia diplomatic and military signaling" depth: brief sources: web, video, social
```

## Example Brief Shape

# Research Brief: Iran / Russia diplomatic and military signaling

## Time Window

Last 30 days when source dates are available. Sources without reliable date filtering are labeled `most-recent-found`.

## Key Signals

- Iran/Russia diplomatic coordination appears as a watch item only when anchored to official statements, primary interviews, or dated reporting.
- Military-signaling claims from social posts should remain low confidence unless backed by primary footage, official confirmation, or reputable dated reporting.
- Commentary can be useful for narrative tracking, but it should not be treated as wire evidence.

## Debates / Conflicts

- Social and commentator accounts may disagree about whether a move is deterrence, escalation, bargaining, or theater.
- Treat unverified battlefield, naval, or intelligence claims as `verify:pending-primary` or keep them out of the inbox line.

## Implications for Grace-Mar

- Strategy routing: add at most one inbox line when the signal is fresh and source-dated.
- Possible Record / evidence candidate: none by default; only after explicit operator review.
- Operator watch items: whether official Iranian or Russian channels repeat, deny, or reframe the signal.

## Provenance Log

| Source | Date | Link / locator | Used for | Confidence |
|--------|------|----------------|----------|------------|
| Official statement or primary interview | YYYY-MM-DD | URL | Diplomatic claim | high if directly attributed |
| Dated news report | YYYY-MM-DD | URL | Context / chronology | medium-high |
| Social post or repost | YYYY-MM-DD if visible | URL or profile locator | Sentiment / claim signal | low unless primary |

## Optional Strategy Inbox Line

```text
web | cold: Iran/Russia official or directly attributed signal on <specific issue> // hook: fresh diplomatic/military-signaling watch item for today | <URL> | verify:primary-or-dated-report+last30days | IRAN | US-RU
```

## Boundary Notes

- Do not edit `daily-strategy-inbox.md` unless the operator asks for that separate action.
- Do not write to `days.md`, author threads, or `strategy-page` blocks from this skill.
- Do not treat `--stage` as automatic recursion-gate writing. In v1 it means prepare stage-only review material when explicitly requested.
- Do not claim Reddit, X, YouTube, finance, or filings coverage unless the current host actually searched those surfaces.
