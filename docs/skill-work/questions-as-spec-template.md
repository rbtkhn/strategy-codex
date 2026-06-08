# Questions-as-spec template

**Purpose:** Default PLAN success shape for **heavy** multi-file or long-document work — meaningful questions that encode standards, not a single eval rubric.

**Use with:** [operator-agent-lanes.md](../operator-agent-lanes.md) (PLAN lane), [context-folder-assembly](../../skills-portable/_drafts/context-folder-assembly/SKILL.md) (`questions.md` in working folders), [context-folder-operator-cheatsheet.md](./context-folder-operator-cheatsheet.md) (one-page flow), optional `inspection.questionsSpec` on [workbench receipts](../skill-work/work-dev/workbench/WORKBENCH-RECEIPT-SPEC.md).

**WORK only** — not Record truth.

---

## Paste block

Copy into `questions.md`, a PLAN reply, or a working folder. Replace `...` with task-specific content.

```markdown
## Questions-as-spec

### Outcome questions
- What must be true when this task is done?
- What is the single deliverable (file, section, artifact)?

### Comparison / context questions
- Compared to what baseline, prior period, or peer artifact?
- What would make the output misleading without that context?

### Boundary questions (out of scope / must not break)
- What must we not edit, merge, or flatten?
- What lanes or surfaces are explicitly out of scope?

### Evidence questions (what would convince us / falsify)
- What observation would prove we were wrong?
- What is thin or proxy-only and must be labeled honest?

### Task shape (fill after back-and-forth)
- Deliverable:
- In / out:
- Ready to EXECUTE: yes | no
```

---

## Agent guidance

- Produce **3–7** questions total across the first four sections before EXECUTE on heavy work.
- Questions must be **decidable or falsifiable** — avoid rhetorical filler.
- **Task shape** is sealed only after operator approves; then optional **context folder** assembly or direct EXECUTE.
- Post-run: optional workbench `questionsSpec` array mirrors the questions that defined “done.”
