---
name: domain-lane-survey
description: Compose landscape scan before building a new work territory — existing tools, verdicts, gaps, and lane checklist.
portable: true
version: 0.1.0
scope_class: repo-governed
skills:
  - repo-hygiene-pass
outputs:
  - bounded SURVEY markdown under docs/skill-work/work-[lane]/
authority: advisory_only
verification_level: receipt_required
risk_tier: low
---

# Domain Lane Survey

## Purpose

Scan the landscape before creating a new `work-*` territory or adopting a tool/framework. Avoid rebuilding what already exists; enter the lane with grounded awareness.

## Trigger

**Operator phrases:** `runbook lane survey`, `runbook survey [lane]`, `lane survey`.

**Legacy triggers:** `lane survey`, `survey [lane-name]` — route here (`lane-survey` skill is deprecated).

**Use when:**

- starting a new `work-*` lane
- evaluating whether a tool, framework, or approach already solves the problem
- operator asks "what's out there for [domain]?" before committing to build

**Do not use when:**

- the lane already exists and only needs hygiene — run **`repo-hygiene-pass`**
- the question is proposal tradeoffs without a landscape scan — use **Think lane** / [operator-style.mdc](../../.cursor/rules/operator-style.mdc) unpack (legacy `pros-and-cons` archived)

## Skills Composed

| Step | Surface | Role |
|---:|---|---|
| 1 | Lane README or stated objective | Anchor scope |
| 2 | **Survey workflow** (this runbook) | Landscape scan, verdicts, gaps |
| 3 | [work-template.md](../../docs/skill-work/work-template.md) | Lane creation checklist after survey |
| 4 | Optional **`repo-hygiene-pass`** | After lane scaffold exists |

## Inputs Required

- Lane name or operator-stated goal
- Optional existing notes or prior art the operator already knows

## Workflow Steps

1. **Read the lane objective** — If `docs/skill-work/work-[lane]/README.md` exists, read it; otherwise use the operator's stated goal.

2. **Web search** (3–5 targeted queries) for open-source tools, commercial products, published frameworks, and community prior art in that domain.

3. **Assess fit** for each significant finding:
   - solves the problem already?
   - partial fit (reference only)?
   - different problem (ignore)?

4. **Classify verdicts:**

   | Verdict | Meaning |
   |---------|---------|
   | **Adopt** | Use directly — do not rebuild |
   | **Reference** | Learn from it; build your own version |
   | **Ignore** | Different problem or low quality |

5. **Write results** to `docs/skill-work/work-[lane]/SURVEY_[lane].md`:
   - landscape summary (2–3 sentences)
   - findings table (name, verdict, notes)
   - gaps and opportunities
   - recommendations (adopt vs build)

6. **Proceed to lane creation checklist** in [work-template.md](../../docs/skill-work/work-template.md) step 4.

7. **Optional — unpack recommendations** (Think lane only): if the operator asks for tradeoffs on survey recommendations, restate scope, list pros/cons, name **disproportion**, and recommend — per [operator-style.mdc](../../.cursor/rules/operator-style.mdc). No repo edits unless they switch to ship.

## Human Approval Points

- Before adopting external tooling
- Before creating new lane scaffold on disk

## Stop Conditions

Stop if:

- operator declines survey — use structured knowledge capture instead
- no web search available — structure operator's existing knowledge into the survey format

## Verification / Proof Standard

Do not call this runbook complete unless:

- lane name and objective are named
- survey output path is named (`SURVEY_[lane].md` or explicit skip reason)
- at least three findings classified or operator knowledge structured equivalently
- recommendations state adopt vs build explicitly

Evidence to report:

- survey file path
- queries run (or knowledge-only mode stated)
- verdict table summary

If verification cannot be completed:

- state what was not surveyed
- stop before lane scaffold commits

## Outputs

- One-page (aim) survey markdown under the target `work-*` lane
- Verdict table and concrete next steps

## Return Paths

- [skills/runbooks/README.md](README.md)
- [docs/skill-work/recipes/onboard-new-lane.md](../../docs/skill-work/recipes/onboard-new-lane.md)
- [docs/skills-map.md](../../docs/skills-map.md)

## Guardrails

- Survey findings are **WORK-layer only** — not Record
- Survey does not commit to adoption; operator decides
- Keep the survey short — decision aid, not a research paper
