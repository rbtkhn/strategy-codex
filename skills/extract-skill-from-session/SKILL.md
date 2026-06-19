---
name: extract-skill-from-session
preferred_activation: save skill
description: "After a successful multi-step task, assess whether the workflow should become a skill candidate or portable skill. Triggers: save skill, skill from session, add a skill from this, turn this into a skill."
portable: true
version: 1.0.0
scope_class: repo-governed
tags:
  - operator
  - work-dev
  - skills
---

# Extract Skill From Session

**Preferred activation (operator):** say **`save skill`**. **Alias:** **`skill from session`**.

Use this skill when the operator completed (or is finishing) a task that worked well and wants to capture it as a reusable procedure — without repeating manual instructions next time.

## When to run

- Operator says "add a skill from this," "turn this into a skill," "save as a skill," or similar.
- Operator describes a workflow to repeat and document.
- A session produced a clear, repeatable process and the operator wants it reusable.

## Skill Candidate Assessment (run first)

Answer before writing any skill file:

1. Did this session reveal a **repeated** procedure (not a one-off)?
2. Is the procedure **non-obvious** (guardrails, ordering, verification)?
3. Would preserving it reduce future re-explanation?
4. Does it have clear **trigger conditions**?
5. Does it have explicit **boundaries** (when not to use)?
6. Does it have **verification requirements** (what counts as done)?
7. What **`scope_class`** fits: `personal`, `project-local`, `repo-governed`, or `public-portable`?

**Default:** output assessment only. **Full skill creation** only when operator explicitly asks after assessment.

### Assessment output template

```markdown
## Skill Candidate Assessment

Decision: no / maybe / yes

Reason:

Candidate row:

| date | working name | trigger phrase | pointer | scope_class | verification need |
|------|--------------|----------------|---------|-------------|---------------------|
| YYYY-MM-DD | hyphenated-name | trigger | commit or thread | repo-governed | one line |
```

If **yes** or **maybe** with operator confirm: propose appending a row to the host skill-candidates backlog (see host appendix).

## Steps (when operator asks for full skill)

1. **Identify what was done** — steps, scope, guardrails, commands.
2. **Name the skill** — lowercase, hyphens, max 64 chars.
3. **Write description (frontmatter)** — third person; WHAT + WHEN; single line under 1024 chars.
4. **Write the body** — concise steps; include `## Verification / Proof Standard` per portable schema.
5. **Create files** — portable draft first; promote only on explicit operator ask (host appendix paths).

## Output

- **Default:** Skill Candidate Assessment only.
- **On explicit ask:** portable draft under host `_drafts/` path, or promoted portable core + manifest + sync per host pipeline.

## Guardrails

- Do not overwrite an existing skill without explicit confirmation.
- Do not auto-promote to manifest or sync without operator approval.
- If session context is thin, ask for a brief workflow summary before generating.
- Match existing project skill tone and length when samples exist in the host repo.

## Verification / Proof Standard

Do not call this complete unless:

- Skill Candidate Assessment was delivered (decision + reason)
- if **yes**: candidate row is complete or draft path is named
- if full skill created: portable file exists with `portable: true`, one-line `description`, and verification section
- no manifest or sync changes unless operator explicitly approved promotion

Evidence to report:

- assessment decision
- candidate row or draft path
- sync/validate exit codes when promotion path ran

If verification cannot be completed:

- state missing context
- offer **maybe** with pointer-only row instead of full skill
