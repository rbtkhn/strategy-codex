# Builder spec — Agent Orchestration & Supervision Basics (hybrid overlay)

Operator material; not Record.

**Date:** 2026-07-03  
**Program:** AI Operator Accelerator — Workflow Ship Sprint **hybrid overlay** (weeks 8–10)  
**Agent:** Builder (v1.5 prompt)  
**Strategist input:** [2026-07-03-agentic-era-adaptation-brief.md](../strategy/2026-07-03-agentic-era-adaptation-brief.md)

**Invariant:** This module **extends** the primary Workflow Ship Sprint — it does **not** replace [2026-07-02-workflow-ship-sprint-wedge.md](../strategy/2026-07-02-workflow-ship-sprint-wedge.md) or the base [module map](2026-07-02-accelerator-module-map.md). Teams may run the sprint without this overlay until facilitators opt in.

---

## v1.5 output table

| Field | Content |
| --- | --- |
| **Weight Update Module** | **Agent Orchestration & Supervision Basics** — weeks 8–10 overlay on existing Ship phase |
| **Capability Change** | **Before:** Prompt-level single-step automations; operator as executor; ad-hoc tool use. **After:** Define guardrails and goals; approve agent plans; monitor multi-step chains; escalate exceptions with documented audit trail. |
| **Hands-on Exercise** | Joint human+agent workflow ship: (1) goal spec + scope limits doc; (2) guardrails / authorization checklist; (3) agent execution log (tool calls, decisions); (4) human review checklist with approve/reject/escalate; (5) mutual improvement note (what guardrail to add next). |
| **Verification Method** | [Hybrid supervision rubric](2026-07-03-hybrid-supervision-rubric.md) overlay (0–40 supplemental); filed via [week-12 hybrid pilot template](templates/milestone-week-12-hybrid-pilot.md). Base pass still requires [workflow ship rubric](2026-07-02-workflow-ship-rubric.md) ≥80/100. |
| **System Design Notes** | 70/20/10 — 70% hands-on chain supervision, 20% peer review of guardrails, 10% orchestration patterns brief. Pairs with module map weeks 8–10 (integration → production). Minimal tooling: approval workflow (even lightweight — spreadsheet + sign-off), observability log template, exception playbook stub. Embed: micro-log of one supervision decision per week (wk 10–12). |
| **Adaptation Notes** | As agent reliability improves, module emphasis shifts from exception firefighting → orchestration design + audit trails (portable across vendor platforms). Stronger governance layer hedges autonomy erosion — supervision skills remain monetizable premium. |
| **Next Action** | **Growth** — [hybrid growth brief](../growth/2026-07-03-hybrid-supervision-growth-brief.md) and [7-day challenge outline](../growth/2026-07-03-seven-day-agent-challenge-funnel.md) delivered; external hybrid marketing remains proof-gated until `reports/` receipt. **Strategist** if orchestration falsifier triggers. |

---

## Hybrid pattern (required loop)

```text
Human defines goals + guardrails
        ↓
Agent plans + executes (tool use, multi-step)
        ↓
Human reviews → approve / reject / escalate
        ↓
Mutual improvement (update guardrails, rubric, playbook)
        ↺
```

---

## Week placement (overlay on module map)

| Week | Base sprint (existing) | Hybrid overlay add-on |
| --- | --- | --- |
| 8 | [Integration milestone](templates/milestone-week-08-integration.md) | Introduce guardrails doc + approval workflow on integrated workflow |
| 9 | Ship hardening | Agent execution log + exception playbook draft |
| 10 | Pre-production review | Human review checklist; peer review of supervision quality |
| 11–12 | Production + rubric | Optional hybrid pilot filing; [week-12 hybrid template](templates/milestone-week-12-hybrid-pilot.md) |

---

## Deliverables checklist (participant)

- [ ] Goal spec + scope limits (1 page)
- [ ] Guardrails / authorization checklist (signed)
- [ ] Agent execution log (session or weekly summary)
- [ ] Human review checklist (≥3 documented decisions)
- [ ] Exception escalation path (who, when, how)
- [ ] Hybrid rubric self-score (facilitator validates)

---

## Related

| Topic | Link |
| --- | --- |
| Primary wedge | [workflow-ship-sprint-wedge](../strategy/2026-07-02-workflow-ship-sprint-wedge.md) |
| Base rubric | [2026-07-02-workflow-ship-rubric.md](2026-07-02-workflow-ship-rubric.md) |
| Hybrid rubric | [2026-07-03-hybrid-supervision-rubric.md](2026-07-03-hybrid-supervision-rubric.md) |
| Week 4 / 8 / 12 base templates | [templates/](templates/) |
| Builder v1.5 prompt | [AI-OPERATING-SYSTEM.md](../AI-OPERATING-SYSTEM.md#agent-2--builder) |
