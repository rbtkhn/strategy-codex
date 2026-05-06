# Day 1 (No Terminal) â€” Xavier

**Rule:** No terminal commands required in this flow.  
**Target session length:** 30-45 minutes.

---

## Step 1 â€” Open the right docs

Open and read in order:
1. [README.md](README.md)
2. [first-good-morning-runbook.md](first-good-morning-runbook.md)
3. [SESSION-0-OPERATOR.md](SESSION-0-OPERATOR.md)

---

## Step 2 â€” Complete Session 0 capture

**In Xavierâ€™s `companion-xavier` repo** (see [INSTANCE-PATHS.md](INSTANCE-PATHS.md)). Open:
- `docs/seed-survey/seed-survey-initiation.md` (read only; path may match template layout)
- `docs/seed-survey/seed-survey-capture.md` (edit here)

Fill all rows (Q1-Q30) in capture.  
Do not edit initiation file.

---

## Step 3 â€” Ask Cursor AI to stage candidates (copy/paste prompt)

```text
Help me stage Session 0 outputs safely.

Inputs (paths relative to **her** repo root):
- docs/seed-survey/seed-survey-capture.md
- xavier/recursion-gate.md

Tasks:
1) Read my capture answers.
2) Propose candidate entries for recursion-gate (do not edit self.md).
3) Keep claims neutral and sourceable.
4) Add candidates only under the Candidates section.
5) Show me the diff before finalizing.

Rules:
- No content copied from **
- No hand-merge into self.md
- Stop and ask me before write actions
```

---

## Step 4 â€” Initialize business workspace (no terminal)

Open `docs/skill-work/work-business/xavier/README.md`, then ask Cursor AI:

```text
Use my Session 0 capture and any business docs I provided to initialize work-business/xavier starter files.

Create:
- docs/skill-work/work-business/xavier/source-index.md
- docs/skill-work/work-business/xavier/objectives-and-constraints.md
- docs/skill-work/work-business/xavier/week-0-priority-stack.md

Rules:
- WORK only (no self.md edits)
- cite source file names for each extracted claim
- keep recommendations concrete and 7-day actionable
```

---

## Step 5 â€” Review checklist before saving

- [ ] Candidates are in `recursion-gate.md` only
- [ ] `self.md` unchanged
- [ ] No references to `**`
- [ ] Language is factual and reviewable

---

## Step 6 â€” Log completion

Add one line to **her** repo:
- `xavier/session-log.md`

Template:
- `YYYY-MM-DD: Day 1 no-terminal onboarding complete; Session 0 captured; candidates staged; work-business/xavier starter pack initialized.`

---

## If blocked

If any step is unclear for more than 10 minutes:
1. Pause
2. Ask companion for live walkthrough
3. Do not improvise merge or posting


