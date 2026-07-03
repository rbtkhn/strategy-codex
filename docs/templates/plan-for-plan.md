# Plan-for-Plan Usage Guide

Use this template to draft a compact plan request before asking a stronger model to expand it into a full Plan Mission. For high-risk work, send the completed Plan Mission to a different strong model for second-opinion stress testing, revise from that feedback, and only then execute.

## Second-Opinion Protocol

Second opinion is required when the plan affects architecture, governance, Record/runtime boundaries, automation, model routing, cost, privacy, external-source dependence, broad hard-to-revert changes, or other high-risk work. For small reversible edits, second opinion is optional.

Use a different strong model. Ask for risks, hidden assumptions, failure modes, missing validation, governance issues, and concrete revisions. Treat reviewer output as advisory; the human operator remains final authority. If this protocol is reused frequently across lanes, capture it as a skill candidate before promoting it to a portable skill.

# Plan-for-Plan: [Concise Task Title]

**Date:** YYYY-MM-DD  
**Author / Operator:** [Your Name]  
**Lane / Territory:** work-dev | work-strategy | work-[other]  
**Related Surfaces:** recursion-gate.md, self.md, self-skills.md, self-library.md, etc.  
**Priority / Urgency:** Low / Medium / High / Critical  

## 1. Objective (One-sentence goal)
[Clear, outcome-focused statement]

## 2. Success Criteria (Measurable)
- [Criterion 1]
- [Criterion 2]
- ...
- Must respect: runtime vs Record boundary, gate protocol, AGENTS.md invariants

## 3. Scope & Boundaries
**In Scope:**
- ...

**Out of Scope:**
- ...

**Explicit Constraints (must check every time):**
- [ ] Runtime memory vs canonical Record separation (`docs/runtime-vs-record.md`)
- [ ] No durable changes without staging in `recursion-gate.md`
- [ ] AGENTS.md Layer-1 rules (authority, governance unbundling)
- [ ] Skill modularity (THINK / WRITE / WORK / STEWARD)
- [ ] Context budgeting & prepared-context rules
- [ ] Evidence grounding requirement

## 4. Key Documents to Reference (pull latest)
- `self.md`
- `recursion-gate.md`
- `AGENTS.md`
- `docs/architecture.md`
- `docs/governance-unbundling.md`
- Relevant lane: `docs/archive/skill-work-legacy/work-*/...`
- Other: [list]

## 5. Proposed Approach (High-level)
[Initial strategy, architecture ideas, model routing suggestions]

## 6. Risks & Failure Modes
- Risk 1 -> Mitigation
- Risk 2 -> Mitigation
- Gate rejection risk?

## 7. Model / Resource Plan
- **Primary Reasoning Model:** Claude 4.7 Opus / equivalent
- **Review / Second Opinion:** Gemini 3 / Grok / Claude Haiku
- **High-volume / Cheap Work:** [cheaper model]
- **Orchestration:** Local Docker / EC2 / Render / runtime container?
- **Estimated Cost:** ~$X-$Y

## 8. Execution Steps (Draft)
1. ...
2. ...
3. ...

## 9. Validation & Gate Preparation
- How will this be tested?
- What artifacts will be staged for gate review?
- Evidence links required?

---

**End of Plan-for-Plan**

**Next Action:** Feed this entire document to your strongest model -> generate full **Plan Mission**.  
For high-risk work, obtain a risk-based second opinion from a different strong model before execution.
