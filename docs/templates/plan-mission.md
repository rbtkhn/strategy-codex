# Plan Mission: [Concise Task Title]

**Date:** YYYY-MM-DD
**Version:** 1.0
**Origin Plan-for-Plan:** plan-for-plan-YYYY-MM-DD-[slug].md
**Author / Operator:** [Your Name]
**Lane / Territory:** work-dev | work-strategy | work-[other]
**Status:** Draft -> Reviewed -> Approved -> Executing -> Complete

## 1. Objective
[One-sentence clear goal]

## 2. Success Criteria
- [Measurable outcome 1]
- [Measurable outcome 2]
- ...
- All changes must fully respect runtime vs Record boundary and gate protocol

## 3. Key Constraints & Invariants
- Runtime memory vs canonical Record separation
- No direct durable Record changes (must stage via recursion-gate.md)
- AGENTS.md Layer-1 rules
- Skill modularity (THINK / WRITE / WORK / STEWARD)
- Evidence grounding
- Context budgeting

## 4. Architecture & Design Decisions
[High-level system design, file structure changes, new components, data flow, etc.]

## 5. Detailed Execution Steps
1. [Step 1 - detailed]
2. [Step 2 - detailed]
...

**Model Routing Plan:**
- Primary high-reasoning tasks -> Claude 4.7 Opus / equivalent
- Review & critique -> Gemini 3 / Grok
- High-volume generation -> cheaper model
- Orchestration -> runtime container / EC2

## 6. Second-Order Strategic Review
- What are the downstream / second-order effects of this change?
- How might this affect long-term system coherence, incentives, or governance?
- Does this strengthen or weaken key invariants (recursion, agency, evidence grounding)?
- Historical / structural analogy: What past patterns does this resemble?
- Per-token leverage: Is this high-value thinking or high-volume noise?
- Recursive self-improvement impact: How does this help the system improve itself?

## 7. Agentic Risk & Safety Review
Complete this section for any task involving agents, tools, delegated execution, automation, skill admission, external integrations, or write-capable workflows. If not applicable, write `not_applicable` with one sentence explaining why.

- **Human-context vs agent-context:** What can a human see or do that the agent cannot? What context is intentionally withheld from the agent?
- **Permission scope and blast radius:** What files, tools, credentials, surfaces, or lanes can the agent touch? What is the worst credible failure if compromised or confused?
- **Audit receipts:** Which existing receipt surfaces will show intent, tools/actions, model/runtime, and outcome (for example: git history, `pipeline-events.jsonl`, `merge-receipts.jsonl`, cadence events, compute ledger, sandbox receipts, runtime observability)?
- **Revocation / stop path:** Who can halt the agent or workflow, how, and how quickly?
- **Pressure default:** Under deadline pressure, does the system deny, stay read-only, or escalate to the gate/operator rather than widening access?

## 8. File Changes & Artifacts
**Files to Create / Modify:**
- `path/to/file1.md` -> [purpose]

**Files to Stage for Gate Review:**
- List of proposed Record updates

## 9. Testing & Validation Plan
- Unit / integration tests
- Consistency checks against self.md, AGENTS.md, recursion-gate.md
- Manual gate review checklist

## 10. Risks & Mitigations
- Risk -> Mitigation
- Gate rejection risk -> ...

## 11. Gate Preparation
- Proposed changes to `recursion-gate.md`
- Evidence links
- Summary of impact on the Record

---

**End of Plan Mission**

**Approval Gate:** For high-risk work, this Plan Mission should receive:
- Execution Review (clarity, feasibility, cost)
- Strategic Review (second-order effects, invariants, recursive self-improvement)
before full execution.
