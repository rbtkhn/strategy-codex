# Operating Principles - strategy-codex

**Status:** Work-layer operating guide. This document supports planning and review discipline, but remains subordinate to `AGENTS.md`, `instance-doctrine.md`, and `docs/layer-architecture.md`.

## Core Philosophy
We combine execution discipline with strategic rigor: fast enough to compound, governed enough to preserve the Record/runtime boundary.

## Execution Discipline
- Start significant work with a Plan-for-Plan.
- Use narrow, specialized agents or passes with minimal necessary context.
- Apply multi-model review when risk warrants it (strong model -> second opinion).
- Route heavy work through appropriate local, cloud, or runtime infrastructure.
- Maintain velocity, cost awareness, reliability, and clear receipts.

## Strategic Rigor
- Protect core invariants at all costs.
- Explicitly analyze second-order effects and long-term incentives.
- Prioritize per-token economic leverage over volume.
- Maintain recursive self-improvement awareness.
- Ground decisions in historical and structural understanding.
- Treat Alex Wissner-Gross-style frontier awareness as a signal for review, not as automatic authority.

## Integrated Practices

1. **Governed Velocity**  
   Significant changes should move quickly only inside the repo's governance boundaries.

2. **Planning Templates**  
   - `docs/templates/plan-for-plan.md`
   - `docs/templates/plan-mission.md`

3. **Review Cadence**  
   - Execution Review: clarity, feasibility, cost, and delivery path.
   - Strategic Review: second-order effects, invariants, incentives, and recursive improvement.
   - Gate Review: only when proposed changes would touch Record surfaces through `recursion-gate.md`.

4. **Continuous Improvement**  
   The system should use its own outputs to improve governance, skills, architecture, and operator ergonomics without silently promoting runtime material into Record truth.

## Non-Negotiables
- No durable Record changes without proper staging.
- Evidence grounding required.
- Context discipline enforced.
- Second-order thinking required for high-risk work.
- Human operator remains final authority.

---

**This document is a work-layer operating guide.** Operators and agents should use it to improve planning discipline without treating it as a replacement for higher-order doctrine.
