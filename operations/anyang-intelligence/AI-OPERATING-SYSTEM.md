# Anyang Intelligence — 3-Agent AI Operating System

WORK only; not Record.

**Scope:** `operations/anyang-intelligence/` organizational architecture.

**Related:** [STRATEGIC-PLAN.md](STRATEGIC-PLAN.md) · [README.md](README.md)

**Offer-sensitive:** Agent prompts and commercial outputs are WORK-only operator material — not legal commitments, not `skill-write` public copy without review.

---

## Overview

Anyang Intelligence operates as a **minimal 3-agent intelligence system** — a closed loop of three AI agents that replace traditional org structure for global commercial motion:

| Agent | Decides |
| --- | --- |
| **Strategist** | WHAT to build |
| **Builder** | HOW to deliver product + curriculum |
| **Growth** | HOW to acquire users and revenue |

**One-line system definition:** Strategy, execution, and growth form a continuous closed-loop system that generates, delivers, and monetizes AI vocational training products globally.

---

## System architecture

```text
                   ┌──────────────────────┐
                   │   MARKET SIGNALS     │
                   │  (reports/, external)│
                   └─────────┬────────────┘
                             ↓
                    STRATEGIST
           (opportunity + product definition)
                             ↓
                       BUILDER
      (curriculum + system + execution design)
                             ↓
                    GROWTH AGENT
        (distribution + sales + monetization)
                             ↓
                   REVENUE + USERS
                             ↓
                    FEEDBACK LOOP
                             ↺
```

Market signals land in [`reports/`](reports/) and [`strategy/`](strategy/). Builder outputs land in [`builder/`](builder/) and (when curriculum ships) root [`education/`](../../education/README.md). Growth outputs land in [`growth/`](growth/) and proof receipts in [`reports/`](reports/).

---

## Boundary rules

| Rule | Detail |
| --- | --- |
| **3 agents = global commercial org model** | Not Coffee Confirm/Test/Deepen/Reframe; not strategy-codex interpretive-machine roles |
| **`singularity/work-anyang/` = Builder proof cell** | China pilot is R&D under Builder — not a fourth agent. See [anyang-open-tensions.md](../../singularity/work-anyang/anyang-open-tensions.md) |
| **Curriculum under `education/<subject-slug>/`** | Never `education/anyang-intelligence/` — see [README.md](README.md) layout invariant |
| **Mentor ops stay in runbook** | [OPERATOR-RUNBOOK.md](../../singularity/work-anyang/OPERATOR-RUNBOOK.md) = cohort/sponsor modes, not Growth or Strategist |
| **Loops documented, not declared** | Proposed singularity loop ids below — YAML deferred to follow-up PR |

---

## Agent 1 — Strategist

### Role

Defines what the company should build based on market demand.

### Responsibilities

- Identify high-value AI workforce opportunities
- Define product direction
- Choose target customer segments
- Design revenue models
- Prioritize initiatives

### Operator prompt

```text
You are the Strategist Agent for an AI-native vocational training company.

Your job is to determine WHAT to build.

You must:
- identify high-impact opportunities in AI workforce transformation
- define clear, monetizable products
- select target user segments (individuals, SMEs, enterprises)
- ensure alignment with scalable online delivery
- prioritize based on revenue potential and market demand

Constraints:
- avoid theoretical or non-actionable ideas
- focus only on AI workflow-based skills and systems
- every recommendation must connect to monetization

Output format:
- Opportunity
- Product Definition
- Target Segment
- Revenue Model
- Next Action
```

### Output format

| Field | Content |
| --- | --- |
| Opportunity | Named market gap or segment pull |
| Product Definition | SKU shape (Accelerator, Transformation, certification path) |
| Target Segment | Individual / SME / enterprise |
| Revenue Model | Stream + illustrative range (WORK-only) |
| Next Action | Single executable handoff to Builder |

### Repo routing

| Output | Shelf |
| --- | --- |
| Opportunity briefs, segment picks, priority memos | [`strategy/`](strategy/) |
| Market digests, competitive benchmarks | [`reports/`](reports/) |

**Maps to STRATEGIC-PLAN:** Orient phase; intelligence layer (§4); proof obligations gate (§90-day falsifiers).

---

## Agent 2 — Builder

### Role

Turns strategy into executable learning systems and products.

### Responsibilities

- Design AI training curricula
- Build workflow-based learning systems
- Define certification structures
- Design minimal delivery infrastructure

### Operator prompt

```text
You are the Builder Agent for an AI vocational training company.

Your job is to determine HOW the product is built and delivered.

You must:
- design practical AI learning systems
- create structured curricula based on real workflows
- define hands-on exercises that produce tangible outputs
- design minimal technical systems needed for delivery

Constraints:
- every module must produce a real-world skill outcome
- avoid theory-heavy content
- prioritize simplicity and deployability

Output format:
- Module Name
- Skill Outcome
- Hands-on Exercise
- System Design Notes
```

### Output format

| Field | Content |
| --- | --- |
| Module Name | Named learning unit |
| Skill Outcome | Observable operator capability |
| Hands-on Exercise | Tangible deliverable (workflow, automation, ship proof) |
| System Design Notes | Delivery infra, rubric hooks, minimal tooling |

### Repo routing

| Output | Shelf |
| --- | --- |
| Module specs, ship-sprint designs, certification rubric drafts | [`builder/`](builder/) |
| Ship-sprint outcomes, workflow proof write-ups | [`reports/`](reports/) |
| Shipped curriculum packs (when ready) | [`education/<subject-slug>/`](../../education/README.md) |
| China proof cell (R&D) | [`singularity/work-anyang/`](../../singularity/work-anyang/README.md) |

**Maps to STRATEGIC-PLAN:** Build + Ship + Embed execution mechanics; curriculum factory alignment.

---

## Agent 3 — Growth

### Role

Drives users, distribution, and revenue.

### Responsibilities

- Build content and distribution systems
- Design funnels and conversion paths
- Execute enterprise and individual sales strategy
- Optimize messaging for clarity and ROI

### Operator prompt

```text
You are the Growth Agent for an AI vocational training company.

Your job is to determine HOW users and revenue are acquired.

You must:
- design content-driven acquisition systems
- build funnels that convert users into paying customers
- structure enterprise and individual sales approaches
- communicate value in simple, ROI-driven language

Constraints:
- prioritize proof-based marketing (show real outcomes)
- focus on LinkedIn, YouTube, and direct outreach
- optimize for fastest path to revenue generation

Output format:
- Growth Strategy
- Funnel Design
- Key Message
- Conversion Path
- Revenue Impact
```

### Output format

| Field | Content |
| --- | --- |
| Growth Strategy | Channel + motion summary |
| Funnel Design | Stages from awareness to paid |
| Key Message | ROI-driven value prop (WORK-only) |
| Conversion Path | CTA, offer, proof artifact required |
| Revenue Impact | Directional impact note — not external claim without receipt |

### Repo routing

| Output | Shelf |
| --- | --- |
| Funnel briefs, campaign specs, outreach templates | [`growth/`](growth/) |
| Case studies, ROI checkpoints, GTM receipts | [`reports/`](reports/) |

**Maps to STRATEGIC-PLAN:** GTM Phases 1–3 (§7); growth engine (§8); proof-based marketing.

---

## Orchestration rule

**System loop:**

1. Strategist identifies opportunity
2. Builder creates product + system
3. Growth Agent distributes + monetizes
4. Revenue + feedback collected
5. Strategist updates direction
6. Repeat

This loop aligns with closed-loop curriculum language in [STRATEGIC-PLAN.md](STRATEGIC-PLAN.md) §4 and the proof-driven acquisition loop in §8.

---

## Design principles

1. **Minimalism** — Only 3 agents exist. No duplication of roles.
2. **Closed-loop learning** — Every cycle must improve product quality, distribution efficiency, and revenue performance.
3. **Execution > theory** — No abstract outputs. Everything must map to product, system, or revenue.
4. **AI-native organization design** — Agents behave like functional cognitive modules inside a single company brain.

---

## Agent ↔ STRATEGIC-PLAN mapping

| Agent | STRATEGIC-PLAN anchor | In-folder outputs |
| --- | --- | --- |
| **Strategist** | Orient; §4 intelligence layer; proof obligations | `strategy/`, `reports/` |
| **Builder** | Build, Ship, Embed; curriculum factory | `builder/`, `reports/` |
| **Growth** | §7 GTM, §8 growth engine | `growth/`, `reports/` |

External surfaces (link only — not edited from this shelf): Builder China proof → `singularity/work-anyang/`; curriculum → `education/`.

---

## Disambiguation

| Name | What it is | What it is not |
| --- | --- | --- |
| **3-agent OS** (this doc) | Global commercial org model | Coffee hub A–D |
| **Orient/Build/Ship/Embed/Scale** | Learner delivery phases in STRATEGIC-PLAN | Agent role names |
| **ADOPT Method™** | External competitor benchmark | Anyang product naming — see [2026-07-02 benchmark](reports/2026-07-02-ai-operator-adopt-benchmark.md) |
| **work-anyang runbook** | Mentor/sponsor cohort ops | Strategist or Growth agent |

---

## Proof obligations

Strategist and Growth must not externalize claims without receipts. See [STRATEGIC-PLAN.md § Proof obligations (90-day)](STRATEGIC-PLAN.md#proof-obligations-90-day) — e.g. no scale marketing without week-6 ROI artifact; no behavior-change claims without habit-pilot design in `reports/`.

---

## Future singularity loops

Proposed loop ids for a **follow-up PR** (YAML under `singularity/loops/business/` — not declared in this PR):

| Proposed `loop.id` | Depends on | `output_shelves` (this folder) | External shelf (when declared) |
| --- | --- | --- | --- |
| `anyang-intelligence-strategist-cycle` | — | `strategy/`, `reports/` | — |
| `anyang-intelligence-builder-cycle` | strategist-cycle | `builder/`, `reports/` | `singularity/work-anyang/` (China proof) |
| `anyang-intelligence-growth-cycle` | builder-cycle | `growth/`, `reports/` | — |

**Soft feed (document only):** growth-cycle case studies and ROI receipts in `reports/` inform the next strategist-cycle — feedback loop without YAML dependency cycle.

**Trigger posture (when declared):** `manual` — operator-invoked; same declare → action card → proof → receipt pattern as other business loops.

---

## Related

| Topic | Link |
| --- | --- |
| Commercial prospectus | [STRATEGIC-PLAN.md](STRATEGIC-PLAN.md) |
| Operating shelf index | [README.md](README.md) |
| Competitive benchmark | [reports/2026-07-02-ai-operator-adopt-benchmark.md](reports/2026-07-02-ai-operator-adopt-benchmark.md) |
| China cohort runbook | [OPERATOR-RUNBOOK.md](../../singularity/work-anyang/OPERATOR-RUNBOOK.md) |
