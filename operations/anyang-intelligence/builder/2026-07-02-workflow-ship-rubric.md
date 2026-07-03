# Builder spec — Workflow ship rubric (100-point scale)

Operator material; not Record.

**Date:** 2026-07-02  
**Program:** AI Operator Accelerator — Workflow Ship Sprint  
**Pass bar:** **≥80/100** at week 12 (internal calibration — do not market externally until first cohort scored)  
**Strategist input:** [2026-07-02-workflow-ship-sprint-wedge.md](../strategy/2026-07-02-workflow-ship-sprint-wedge.md)

---

## How to score

- Score each dimension **0–max** using anchors below.
- **Fail automatic** if any dimension marked **Fail** in falsifiers section.
- Facilitator + peer reviewer both score; final score = average unless disputed (facilitator tie-break).
- Store completed scorecard with week-12 milestone artifact.

---

## Dimensions

### 1. Problem clarity (10 points)

| Score | Anchor |
| --- | --- |
| 0–3 | Vague pain; no baseline metric |
| 4–7 | Clear workflow; baseline estimated but weak |
| 8–10 | Named workflow, owner, baseline metric documented with evidence |

### 2. Production readiness (20 points)

| Score | Anchor |
| --- | --- |
| 0–5 | Demo/prototype only; not in target environment |
| 6–12 | Runs in target environment with manual babysitting |
| 13–17 | Runs in production path; known failure modes |
| 18–20 | Production use by team; rollback/disable documented |

### 3. Measurable impact (20 points)

| Score | Anchor |
| --- | --- |
| 0–5 | No before/after; anecdotal only |
| 6–12 | Directional improvement; weak measurement |
| 13–17 | One solid metric improved (time, errors, throughput) |
| 18–20 | Before/after documented; metric credible to third party |

### 4. Operator runbook quality (15 points)

| Score | Anchor |
| --- | --- |
| 0–4 | Author-only knowledge |
| 5–10 | Partial docs; pair can run with help |
| 11–15 | Cold handoff succeeded; maintenance owner named |

### 5. Reliability & safety (15 points)

| Score | Anchor |
| --- | --- |
| 0–4 | No failure testing; no privacy/data note |
| 5–10 | Some edge tests; human review on risky outputs |
| 11–15 | Induced failure handled; data boundary explicit |

### 6. Architecture simplicity (10 points)

| Score | Anchor |
| --- | --- |
| 0–3 | Over-engineered; scope creep |
| 4–7 | Works but fragile or opaque |
| 8–10 | Minimal viable path; understandable by reviewer |

### 7. Milestone discipline (10 points)

| Score | Anchor |
| --- | --- |
| 0–3 | Missed wk 4/8 gates without documented recovery |
| 4–7 | Gates met late or thin |
| 8–10 | Wk 4 prototype, wk 8 integration, wk 6 ROI filed on time |

**Total:** 100 points

---

## Automatic falsifiers (any one = do not pass)

| Falsifier | Evidence |
| --- | --- |
| **Fake production** | Workflow only runs in demo/sandbox; claimed as production |
| **No baseline** | Before-metrics missing or invented after the fact |
| **Facilitator-built** | Core automation built by instructor, not participant/team |
| **Unbounded scope** | Workflow tries to automate entire function without boundary |
| **Privacy breach** | Live PII/secrets in shared logs or public demo |
| **Missed ROI checkpoint** | Week-6 artifact absent in pilot run |

---

## Proof obligation alignment

| External claim | Requires rubric + artifact |
| --- | --- |
| "Shipped workflow solution" | Dimension 2 ≥13 and week-12 milestone complete |
| "Measurable ROI" | Dimension 3 ≥13 and [week-06-roi-checkpoint](templates/week-06-roi-checkpoint.md) filed |
| "Certified operator" | Pass ≥80 + first cohort receipt in `reports/` |
| "Behavior change product" | Rubric pass **plus** habit log + relapse protocol (wk 10) — rubric alone insufficient |

---

## Scorecard template

```text
Participant/team:
Workflow name:
Facilitator:
Date (week 12):

Dimension 1  Problem clarity      __ / 10
Dimension 2  Production readiness __ / 20
Dimension 3  Measurable impact    __ / 20
Dimension 4  Runbook quality      __ / 15
Dimension 5  Reliability & safety __ / 15
Dimension 6  Architecture simplicity __ / 10
Dimension 7  Milestone discipline __ / 10
                              TOTAL __ / 100

Automatic falsifiers triggered? Y / N
Pass (≥80, no falsifiers)? Y / N
Peer reviewer:
Notes:
```
