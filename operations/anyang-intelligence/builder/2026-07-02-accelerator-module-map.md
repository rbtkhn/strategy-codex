# Builder spec — AI Operator Accelerator module map (12 weeks)

WORK only; not Record. Offer-sensitive — not public copy without review.

**Date:** 2026-07-02  
**Agent:** Builder  
**Status:** pilot skeleton — ready for facilitator run  
**Strategist input:** [2026-07-02-workflow-ship-sprint-wedge.md](../strategy/2026-07-02-workflow-ship-sprint-wedge.md)  
**Rubric:** [2026-07-02-workflow-ship-rubric.md](2026-07-02-workflow-ship-rubric.md)  
**Milestones:** [templates/](templates/)

**Delivery mix:** ~70% doing · ~20% social (cohort + accountability pair) · ~10% formal (live session)

---

## Program outcome

Each participant or team ships **one production AI workflow** with documented before/after metrics. Pass internal bar **≥80/100** on [workflow ship rubric](2026-07-02-workflow-ship-rubric.md) at week 12. Do not market certification externally until first cohort receipt exists in `reports/`.

---

## Week-by-week map

### Week 1 — Orient

| Field | Content |
| --- | --- |
| **Module name** | Operator stance + workflow selection |
| **Skill outcome** | Name one real workflow pain; commit to measurable before-state |
| **Hands-on exercise** | Workflow audit worksheet: inputs, steps, failure modes, weekly time cost |
| **System design notes** | Cohort roster; accountability pair assignment; shared doc template for before-metrics |

**Ship gate:** None. **Deliverable:** signed workflow charter (problem, owner, baseline metric, scope boundary).

---

### Week 2 — Build: map the workflow

| Field | Content |
| --- | --- |
| **Module name** | Workflow decomposition |
| **Skill outcome** | Break target workflow into automatable vs human-only steps |
| **Hands-on exercise** | Current-state map + candidate AI touchpoints (max 5) |
| **System design notes** | Tool stack check (approved list per org); data/privacy boundary note |

**Ship gate:** None. **Deliverable:** workflow map v1.

---

### Week 3 — Build: design the automation

| Field | Content |
| --- | --- |
| **Module name** | Automation architecture (minimal) |
| **Skill outcome** | Design smallest viable automation path — no scope creep |
| **Hands-on exercise** | One-page architecture: triggers, model/tool calls, human review step, output sink |
| **System design notes** | Failure handling: what happens when AI is wrong |

**Ship gate:** None. **Deliverable:** architecture doc approved by pair reviewer.

---

### Week 4 — Ship milestone: prototype

| Field | Content |
| --- | --- |
| **Module name** | Working prototype |
| **Skill outcome** | Demonstrate end-to-end run on real (sanitized) inputs |
| **Hands-on exercise** | Record 3-minute demo + log first automated run |
| **System design notes** | Use [milestone-week-04-prototype.md](templates/milestone-week-04-prototype.md) |

**Ship gate:** **Week 4** — prototype runs once without facilitator rescue.

---

### Week 5 — Build: harden inputs/outputs

| Field | Content |
| --- | --- |
| **Module name** | I/O contracts + edge cases |
| **Skill outcome** | Define valid inputs, rejection rules, output schema |
| **Hands-on exercise** | Test matrix (≥5 cases: happy, empty, malformed, edge) |
| **System design notes** | Version tag on prompt/config |

**Ship gate:** None. **Deliverable:** test log with pass/fail.

---

### Week 6 — ROI checkpoint (program + Growth feed)

| Field | Content |
| --- | --- |
| **Module name** | Mid-program ROI review |
| **Skill outcome** | Quantify early signal: time saved, error rate, or throughput vs baseline |
| **Hands-on exercise** | Complete [week-06-roi-checkpoint.md](templates/week-06-roi-checkpoint.md) → copy summary to `reports/` when pilot runs |
| **System design notes** | Facilitator + pair review; **no scale marketing** until this artifact exists (proof obligation) |

**Ship gate:** **Week 6** — ROI checkpoint filed (internal).

---

### Week 7 — Build: operator runbook

| Field | Content |
| --- | --- |
| **Module name** | Runbook + handoff |
| **Skill outcome** | Another team member can run workflow without author present |
| **Hands-on exercise** | Runbook doc + shadow run by pair partner |
| **System design notes** | Rollback / disable procedure |

**Ship gate:** None. **Deliverable:** shadow-run sign-off.

---

### Week 8 — Ship milestone: integration

| Field | Content |
| --- | --- |
| **Module name** | Production integration |
| **Skill outcome** | Workflow connected to real tool chain (email, CRM, sheet, ticket system, etc.) |
| **Hands-on exercise** | Live integration test in target environment |
| **System design notes** | Use [milestone-week-08-integration.md](templates/milestone-week-08-integration.md) |

**Ship gate:** **Week 8** — integration runs in target environment (not localhost-only).

---

### Week 9 — Build: reliability + monitoring

| Field | Content |
| --- | --- |
| **Module name** | Reliability pass |
| **Skill outcome** | Add logging, alert on failure, define owner for maintenance |
| **Hands-on exercise** | Induce one failure; verify detection + recovery path |
| **System design notes** | Maintenance cadence (weekly/monthly) |

**Ship gate:** None. **Deliverable:** incident log from induced failure drill.

---

### Week 10 — Embed preview: habit design

| Field | Content |
| --- | --- |
| **Module name** | Micro-habit protocol (design only) |
| **Skill outcome** | Design 30-second daily operator log + cue-routine-reward for post-cohort sustain |
| **Hands-on exercise** | 7-day personal pilot of log format (facilitator validates format, not 66-day claim) |
| **System design notes** | Relapse/missed-day protocol stub — required before external behavior-change claims |

**Ship gate:** None. **Deliverable:** habit log template + relapse protocol (1 page).

---

### Week 11 — Build: polish + documentation

| Field | Content |
| --- | --- |
| **Module name** | Production documentation |
| **Skill outcome** | Package workflow for handoff: README, config, support contact |
| **Hands-on exercise** | Cold handoff drill — new reader runs from docs alone |
| **System design notes** | Deprecation plan if model/tool changes |

**Ship gate:** None. **Deliverable:** handoff package v1.

---

### Week 12 — Ship milestone: production + rubric

| Field | Content |
| --- | --- |
| **Module name** | Production ship + certification scoring |
| **Skill outcome** | Workflow in production use; scored ≥80/100 on rubric |
| **Hands-on exercise** | Final demo + rubric scorecard + before/after metrics |
| **System design notes** | Use [milestone-week-12-production.md](templates/milestone-week-12-production.md); case study draft → `reports/` (Growth) |

**Ship gate:** **Week 12** — production ship + rubric pass.

---

## Facilitator minimum kit

| Artifact | Path |
| --- | --- |
| Module map (this doc) | `builder/2026-07-02-accelerator-module-map.md` |
| Ship rubric | [2026-07-02-workflow-ship-rubric.md](2026-07-02-workflow-ship-rubric.md) |
| Milestone templates | [templates/](templates/) |
| Live session | 60–90 min/week; async ~3–5 hrs/week per participant |

**Stop rule (Strategist):** Pilot runnable with this kit — no landing page, no video course, no LMS required for v0.

---

## Builder receipts

| Check | Result |
| --- | --- |
| Real-world skill outcome each week | Yes |
| Theory-heavy avoided | Yes — doing-weighted |
| Ship milestones wk 4/8/12 | Yes |
| Week-6 ROI shape for `reports/` | Yes |
| Embed preview without over-claiming | Yes — design + 7-day format pilot only |
| Handoff to Growth | Week 12 case study draft slot defined |
