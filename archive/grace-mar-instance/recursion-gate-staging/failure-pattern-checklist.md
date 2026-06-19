# Failure pattern checklist (operator)

Run on **major** proposals, large OpenClaw handbacks, or multi-step agent runs before elevating content toward merge. **Not** Record truth â€” a discipline aid only.

**Related:** [agent-reliability-playbook.md](../../../docs/skill-work/work-dev/agent-reliability-playbook.md); digest [nate-b-jones-ai-job-market-seven-skills-2026.md](../../../research/external/work-dev/transcripts/nate-b-jones-ai-job-market-seven-skills-2026.md); [creative-pipeline.md](../../../docs/skill-work/work-dev/creative-pipeline.md) (visual / UI work).

---

## Checklist

- [ ] **Context degradation** â€” Long session or huge context: quality drop risk? Trim or re-anchor spec?
- [ ] **Specification drift** â€” Does final output still match the **original** intent and constraints?
- [ ] **Sycophantic confirmation** â€” Did the agent agree with **bad** source data and build on it?
- [ ] **Tool selection error** â€” Wrong tool or wrong framing (too many tools, vague descriptions)?
- [ ] **Cascading failure** â€” Can one sub-step break the whole run without a correction loop?
- [ ] **Silent failure** â€” Output **plausible** but could be **wrong in production** (metadata, edge paths, policy)?
- [ ] **Blast radius** â€” Worst case impact understood?
- [ ] **Reversibility** â€” Can we undo (draft vs committed / irreversible action)?
- [ ] **Frequency** â€” How often does this path run? Scale of exposure?
- [ ] **Verifiability** â€” **Functional** correctness provable, not only â€œsounds rightâ€?
- [ ] **`DESIGN.md` changes** â€” If [`DESIGN.md`](../DESIGN.md) changed, run `python3 scripts/validate-design-md.py` (see creative pipeline).

---

## If anything is unchecked or â€œunknownâ€

- **Reject**, **narrow scope**, or **add mitigations** (eval harness, human gate, smaller blast radius) before treating output as merge-ready.

**Reminder:** Merging into SELF / EVIDENCE / prompt only via companion approval and `scripts/process_approved_candidates.py` per [AGENTS.md](../../../AGENTS.md).

