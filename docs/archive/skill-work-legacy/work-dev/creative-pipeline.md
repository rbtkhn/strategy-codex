# Creative pipeline â€” Grace-Mar v1.0

**Last updated:** 2026-03-27  
**Territory:** work-dev (operator). **Not** Record truth until the companion approves merges through [RECURSION-GATE](../../../archive/grace-mar-instance/recursion-gate.md) and `scripts/process_approved_candidates.py` per [AGENTS.md](../../../AGENTS.md).

**Purpose:** A repeatable, governed, agent-augmented creative workflow for high-clarity visual, UI, video, and 3D artifacts while preserving intention and reducing drift.

**Related:** [Specification precision template](templates/specification-precision.md); [failure pattern checklist](../../../archive/grace-mar-instance/recursion-gate-staging/failure-pattern-checklist.md); [external signals](external-signals.md); Nate B. Jones / Stitch framing â€” [transcript (ASR)](../../../research/external/work-dev/transcripts/nate-b-jones-google-stitch-design-markdown-meeting-transcript-2026.txt).

---

## Core philosophy

Design, video, and 3D are treated as **code-first, agent-readable, version-controlled creative primitives** that plug into the companion-self workflowâ€”not as separate, handoff-only disciplines.

The goal is to raise the **density of real creative decisions** while cutting operational friction (pixel pushing, one-off exports, context loss).

This pipeline supports the seven high-value agentic skills (spec precision, eval / judgment, decomposition, failure patterns, guardrails, context architecture, token economics) as described in [work-dev-sources](work-dev-sources.md) and the Nate digest linked above.

---

## DESIGN.md â€” single source of truth for visual systems

Creative outputs should **reference** the canonical `DESIGN.md` and **update** it when the visual system changes, with gate discipline when those changes are Record-facing.

**Location:** [`DESIGN.md`](DESIGN.md) (operator / interface spec draft until merged through the pipeline).

**Rule:** Generated UI should be checked against this file. Deviations that affect product or public presentation need explicit companion reviewâ€”not silent drift.

### Expected sections (for validator alignment)

- Principles  
- Color Palette  
- Typography  
- Spacing Rules  
- Component Library (reference)  
- Rules for Agents  

---

## Phase 0 â€” Specification precision (mandatory)

Start from a structured brief:

**Template:** [creative-brief.md](templates/creative-brief.md)

Align intent with [specification-precision.md](templates/specification-precision.md) where the run is large or multi-step.

---

## Phase 1 â€” Generation (command-line first)

Preferred tools (operator choice; respect vendor ToS):

| Tool | Role |
|------|------|
| **Google Stitch** | UI / multi-screen; voice or text; export agent-readable design artifacts + code paths per vendor |
| **Remotion + Claude Code skill** | Programmatic video (code â†’ MP4), not generic â€œAI video from pixelsâ€ |
| **Blender MCP** | 3D / immersive scenes via MCP + natural language |

External discourse on Stitch / Remotion / Blender / MCP is captured in the transcript linked at the top.

---

## Phase 2 â€” Evaluation and failure patterns

Before accepting an artifact:

1. Run the **creative output review checklist** (below).
2. If `DESIGN.md` changed or defines the target, run:

   `python3 scripts/validate-design-md.py`

3. For large proposals, also run [failure-pattern-checklist.md](../../../archive/grace-mar-instance/recursion-gate-staging/failure-pattern-checklist.md).

### Creative output review checklist

- [ ] Matches `DESIGN.md` colors, spacing, and typography (where applicable)?
- [ ] **Specification drift** â€” Does output still serve the original brief?
- [ ] **Silent failure** â€” Looks polished but wrong hierarchy, wrong audience, or wrong story?
- [ ] **Context degradation** â€” Did the agent drop earlier design constraints?
- [ ] **Edge cases** â€” Empty states, long text, errors, dark mode (if in scope)?
- [ ] **Blast radius** â€” Easy to iterate and revert?
- [ ] **Token / compute** â€” Cost proportionate to value?

If any item fails â†’ reject, narrow the brief, or add mitigations before treating output as done.

---

## Phase 3 â€” Integration and governance

- **Record-facing changes** (SELF, EVIDENCE, prompt): stage candidates; companion approves; merge only via `process_approved_candidates.py`.
- **Do not** append standing sections to `recursion-gate.md` without approval. Paste filled review blocks into Candidates when ready (same idea as [work-career opportunity review](../work-career/job-opportunity-review-template.md)).
- **Commit hygiene:** When updating the design system, commit `DESIGN.md` changes with the artifact or a clear operator note.
- **Artifact storage (operator):** Final exports and working files live under [`runtime/artifacts/creative/`](../../../runtime/artifacts/) (see folder README). Optional subfolder `portfolio/` for job- or partner-facing bundles.

**Not** under `self-archive/placeholders/evidence/` as a fake evidence tree â€” canonical EVIDENCE remains [`self-archive.md`](../../../archive/grace-mar-instance/self-archive.md) per [canonical-paths.md](../../canonical-paths.md).

---

## Phase 4 â€” Automation and scheduling (optional)

When scheduling primitives fit your setup (e.g. recurring agent jobs):

- Changelog â†’ summary motion piece (Remotion-style pipelines)  
- Milestone â†’ refreshed UI mocks + `DESIGN.md` delta  
- Portfolio refresh only after gate-approved material exists  

Keep **stage-only** discipline: automation proposes; the companion gate decides what becomes Record truth.

---

## DESIGN.md compliance (operator)

When `DESIGN.md` is in play:

- [ ] Run `python3 scripts/validate-design-md.py`
- [ ] No errors (warnings reviewed if any)
- [ ] New colors / components reflected in `DESIGN.md`

`validate-change-review.py` remains for **JSON change-review queues** under `demo` / `platform/template` only; it does not replace the DESIGN validator.

---

## Current limitations (March 2026)

Vendor tools evolve quickly; treat speaker and vendor claims as **directional** until you verify on your stack.

- Stitch-class tools: strong for exploration and MVP; senior polish often still human.  
- Remotion-class: strong for clean motion and demos; complex overlapping motion may need iteration.  
- Blender MCP: lowers the 3D floor; complex organic modeling may still need expertise.  

Judgment and taste remain load-bearing; tools amplify themâ€”they do not remove them.

---

## Success metric

Creative iteration runs at the speed of **clear language** and **tight specs**, while eval bars (including `DESIGN.md` checks) stay high.

---

## Approval and version control

Material changes to this pipeline doc are operator edits in **work-dev**; anything that should alter the Record still goes through the gate. **Next review:** after a full end-to-end run (e.g. brief â†’ generated artifact â†’ checklist â†’ `validate-design-md.py` â†’ committed outputs under `runtime/artifacts/creative/`).

