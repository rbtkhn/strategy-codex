# Builder spec — Proof collection pack (`reports/` filing)

Operator material; not Record. Not `skill-write` public copy without review.

**Date:** 2026-07-03  
**Agent:** Builder (v1.6)  
**Status:** active — pilot operator runbook  
**Strategist input:** [workflow-ship wedge](../strategy/2026-07-02-workflow-ship-sprint-wedge.md) · [agentic adaptation brief](../strategy/2026-07-03-agentic-era-adaptation-brief.md) · Builder v1.6 proof-mode handoff (2026-07-03)

**Purpose:** Tie existing milestone templates to explicit `reports/` filing slots so a pilot facilitator never invents proof schema mid-cohort.

**Invariant:** Workflow Ship Sprint remains primary SKU; hybrid week-12 filing is **optional** overlay only.

---

## Who does what

| Role | Responsibility |
| --- | --- |
| **Pilot facilitator** | Ensures templates completed on schedule; files `reports/` artifacts; signs attestations |
| **Participant / team** | Supplies baseline metrics, artifacts, agrees to week-6 summary |
| **Operator (Anyang)** | Reviews before any external marketing; updates [`reports/README.md`](../reports/README.md) index |
| **Growth** | Consumes filed case studies only after operator review — no fabricated Proof Narratives |

China wedge R&D artifacts stay in [`singularity/work-anyang/`](../../../singularity/work-anyang/OPERATOR-RUNBOOK.md) unless explicitly promoted to venture `reports/`.

---

## Filing ladder (week → template → `reports/`)

| Week | Builder template | File to `reports/`? | Minimum to pass gate |
| --- | --- | --- | --- |
| **4** | [milestone-week-04-prototype.md](templates/milestone-week-04-prototype.md) | **No** — cohort working file; reference in week-12 case study | Prototype runs end-to-end once |
| **6** | [week-06-roi-checkpoint.md](templates/week-06-roi-checkpoint.md) | **Yes — required** | Baseline documented; good-faith early signal; facilitator + participant attestation |
| **8** | [milestone-week-08-integration.md](templates/milestone-week-08-integration.md) | **No** — cohort working file; reference in week-12 case study | Target-environment integration (not localhost-only) |
| **12** | [milestone-week-12-production.md](templates/milestone-week-12-production.md) | **Yes — required** | Production use; rubric ≥80; before/after metrics; case study paragraph |
| **12 (opt.)** | [milestone-week-12-hybrid-pilot.md](templates/milestone-week-12-hybrid-pilot.md) | **Yes — if overlay enabled** | Base week-12 pass + documented supervision layer |

**Scoring:** [workflow-ship rubric](2026-07-02-workflow-ship-rubric.md) (base) · [hybrid supervision rubric](2026-07-03-hybrid-supervision-rubric.md) (overlay, informational until first filing).

---

## `reports/` filename convention

```text
reports/YYYY-MM-DD-<slug>-<artifact-type>.md
```

| `artifact-type` | Source template | When to file |
| --- | --- | --- |
| `week-06-roi-checkpoint` | [week-06-roi-checkpoint.md](templates/week-06-roi-checkpoint.md) | End of week 6 (or within 7 days) |
| `workflow-case-study` | [milestone-week-12-production.md](templates/milestone-week-12-production.md) | End of week 12 after rubric scored |
| `week-12-hybrid-pilot` | [milestone-week-12-hybrid-pilot.md](templates/milestone-week-12-hybrid-pilot.md) | Same window as case study, only if hybrid overlay ran |

**`<slug>`:** Lowercase hyphenated workflow or team name (e.g. `acme-invoice-triage`). **`<YYYY-MM-DD>`:** Filing date (not cohort start date).

**Example:**

```text
reports/2026-09-15-acme-invoice-triage-week-06-roi-checkpoint.md
reports/2026-11-01-acme-invoice-triage-workflow-case-study.md
reports/2026-11-01-acme-invoice-triage-week-12-hybrid-pilot.md
```

After filing: add row to [`reports/README.md`](../reports/README.md) index table.

---

## Minimum fields per `reports/` artifact

### 1. Week-6 ROI checkpoint (required)

Copy completed [template](templates/week-06-roi-checkpoint.md). Must include:

- Metadata (cohort id, team, workflow name, date, facilitator)
- Baseline recap from week 1 (primary pain metric + unit)
- Early signal table (≥1 metric vs baseline, confidence noted)
- ROI narrative (what improved / did not; continue/pivot decision)
- Facilitator attestation checkboxes + **signed (name / date)**
- Participant agreement noted

**Unlocks (internal):** Mid-program checkpoint for Strategist/Builder refresh. **Does not unlock** external scale marketing (week-12 case study still required).

**Falsifier:** [No week-6 ROI checkpoint artifact](../STRATEGIC-PLAN.md#proof-obligations-90-day) → no scale marketing.

---

### 2. Workflow case study (required for GTM unlock)

File when [week-12 production milestone](templates/milestone-week-12-production.md) passes. Minimum body:

| Section | Required content |
| --- | --- |
| **Metadata** | Cohort id, team, workflow name, filing date, facilitator |
| **Production statement** | In-production since date; weekly usage approx; maintenance owner |
| **Before / after** | Primary metric (+ optional secondary) with measurement method |
| **Honest limits** | What the workflow does *not* improve |
| **Rubric result** | Total score / 100; pass ≥80; falsifiers none or listed |
| **Artifact pointers** | Links/paths to scorecard, handoff package, demo; refs to week-4/6/8 working files |
| **Case study paragraph** | One paragraph for Growth (internal draft only) |
| **Facilitator sign-off** | Name / date |

**Unlocks:** First published workflow case study → may resume paid acquisition per proof obligations (operator review still required for public copy).

**Falsifiers cleared:** No published workflow case study · No shipped workflow from ship sprint.

---

### 3. Week-12 hybrid pilot (optional)

File only when hybrid overlay enabled. Copy [hybrid template](templates/milestone-week-12-hybrid-pilot.md). Minimum:

- Base week-12 case study filed and passing first
- Supervision owner, approval workflow, escalation path
- Agent chain description + execution log location
- Governance artifacts table filled
- Hybrid rubric score (informational 0–40)
- Facilitator sign-off

**Unlocks:** Hybrid Proof Narrative in [`growth/`](../growth/) briefs; hybrid upsell messaging (operator review). **Does not** unlock Agent Supervisor Certification marketing until operator explicitly approves.

---

## Proof obligations map

| STRATEGIC-PLAN falsifier | Satisfied by |
| --- | --- |
| No published workflow case study with measurable before/after | `workflow-case-study` filing |
| No week-6 ROI checkpoint artifact | `week-06-roi-checkpoint` filing |
| No shipped workflow solution from ship sprint | Week-4/8 working files + week-12 production gate |
| Curriculum revision loop has no receipt | Separate Strategist cycle — not this pack |
| No habit-tracking pilot (60+ day micro-log) | Embed phase design — future `reports/` slot |
| Enterprise pilot has no SOW/LOI | Out of scope — enterprise track |
| Mentor launch chain incomplete | `work-anyang/` — not venture `reports/` |

---

## Pilot week-by-week operator checklist

| Week | Facilitator action |
| --- | --- |
| **1** | Document baseline metrics (feeds week-6 and week-12) |
| **4** | Complete prototype milestone; store in cohort folder |
| **6** | Complete ROI checkpoint → **file to `reports/`** |
| **8** | Complete integration milestone; store in cohort folder |
| **12** | Score rubric; complete production milestone → **file case study to `reports/`** |
| **12+** | If hybrid overlay: file hybrid pilot same date window |

**Stop condition (v1.6):** Pilot operator can run cohort using only this pack + linked templates — no ad-hoc proof schema.

---

## Verification method (Builder v1.6)

**Hands-on Exercise:** Run table-top walkthrough — fill slug `pilot-dry-run` against all three filename patterns with blank templates.

**Verification Method:** Facilitator confirms checklist complete; operator adds dry-run rows to `reports/README.md` or deletes after review.

**Do not claim** first real cohort success until participant-generated metrics appear in filed artifacts (not dry-run).

---

## Repo routing

| Output | Shelf |
| --- | --- |
| This pack | [`builder/`](.) |
| Filed checkpoints and case studies | [`reports/`](../reports/) |
| Cohort working milestones (wk 4/8) | Cohort operator storage (not venture path) |
| Curriculum (when shipped) | [`education/<subject-slug>/`](../../../education/README.md) |

**Next handoff:** **Growth** — pause paid conversion funnels until `workflow-case-study` exists; then refresh Proof Narrative fields in [hybrid growth brief](../growth/2026-07-03-hybrid-supervision-growth-brief.md) from receipts only.

---

## Related

| Topic | Link |
| --- | --- |
| Module map | [2026-07-02-accelerator-module-map.md](2026-07-02-accelerator-module-map.md) |
| Templates index | [templates/README.md](templates/README.md) |
| 3-agent OS (Builder v1.6) | [AI-OPERATING-SYSTEM.md](../AI-OPERATING-SYSTEM.md#agent-2--builder) |
