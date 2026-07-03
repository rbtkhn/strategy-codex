# Builder spec — Hybrid supervision rubric (overlay)

Operator material; not Record.

**Date:** 2026-07-03  
**Program:** AI Operator Accelerator — Workflow Ship Sprint hybrid overlay  
**Role:** **Optional supplemental** scoring on top of [workflow ship rubric](2026-07-02-workflow-ship-rubric.md) — **not** a replacement pass bar  
**Strategist input:** [2026-07-03-agentic-era-adaptation-brief.md](../strategy/2026-07-03-agentic-era-adaptation-brief.md)  
**Module:** [Agent Orchestration & Supervision Basics](2026-07-03-agent-orchestration-supervision-module.md)

---

## How to use

- **Base pass (required):** [Workflow ship rubric](2026-07-02-workflow-ship-rubric.md) ≥80/100 at week 12 — unchanged.
- **Hybrid overlay (optional until calibrated):** Score **0–40** supplemental points below when cohort runs the hybrid module.
- **Do not market** "agent supervisor certification" externally until at least one hybrid pilot is scored and filed in `reports/`.
- Facilitator scores; peer may review governance dimension. Store with [week-12 hybrid pilot template](templates/milestone-week-12-hybrid-pilot.md).

**Calibration note:** First cohort uses overlay for internal learning only — pass/fail for certificate remains base rubric only.

---

## Overlay dimensions (40 points total)

### 1. Governance & guardrails (10 points)

| Score | Anchor |
| --- | --- |
| 0–3 | No written scope limits; agent runs unconstrained |
| 4–7 | Scope limits exist; authorization informal |
| 8–10 | Documented guardrails; explicit approve-before-execute on high-risk steps |

### 2. Exception handling & escalation (10 points)

| Score | Anchor |
| --- | --- |
| 0–3 | Failures unhandled or silent |
| 4–7 | Ad-hoc escalation; no named owner |
| 8–10 | Documented escalation path; ≥1 real exception handled with receipt |

### 3. Orchestration & observability (8 points)

| Score | Anchor |
| --- | --- |
| 0–2 | Opaque agent chain; no execution log |
| 3–5 | Partial log; steps not reconstructable |
| 6–8 | Multi-step chain visible; tool calls / decisions auditable |

### 4. Human review quality (7 points)

| Score | Anchor |
| --- | --- |
| 0–2 | Rubber-stamp approvals |
| 3–5 | Reviews exist; weak rationale |
| 6–7 | ≥3 documented approve/reject/escalate decisions with rationale |

### 5. Hybrid ROI linkage (5 points)

| Score | Anchor |
| --- | --- |
| 0–1 | No link to week-6 ROI checkpoint |
| 2–3 | Directional link; weak metric |
| 4–5 | Supervision layer tied to before/after metric from [week-06 ROI template](templates/week-06-roi-checkpoint.md) |

---

## Overlay score summary

| Field | Value |
| --- | --- |
| Governance & guardrails | __ / 10 |
| Exception handling | __ / 10 |
| Orchestration & observability | __ / 8 |
| Human review quality | __ / 7 |
| Hybrid ROI linkage | __ / 5 |
| **Hybrid overlay total** | __ / 40 |

---

## Automatic falsifiers (overlay)

Fail hybrid overlay (score capped at 20) if any:

- Agent ran production actions without human approval path documented
- No escalation owner named for high-risk workflow
- Execution log missing for multi-step agent chain claimed as "supervised"

---

## Combined filing (week 12)

| Rubric | Score | Pass |
| --- | --- | --- |
| Base workflow ship | __ / 100 | Y / N (≥80 required) |
| Hybrid overlay | __ / 40 | informational / optional |

---

## Related

| Topic | Link |
| --- | --- |
| Base rubric | [2026-07-02-workflow-ship-rubric.md](2026-07-02-workflow-ship-rubric.md) |
| Hybrid module | [2026-07-03-agent-orchestration-supervision-module.md](2026-07-03-agent-orchestration-supervision-module.md) |
| Week-12 hybrid template | [milestone-week-12-hybrid-pilot.md](templates/milestone-week-12-hybrid-pilot.md) |
