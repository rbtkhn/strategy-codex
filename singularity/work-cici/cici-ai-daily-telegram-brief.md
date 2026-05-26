# cici-ai Daily Telegram Brief

**Status:** WORK / operator brief spec  
**Scope:** daily team/group message for `cici-ai` Telegram  
**Boundary:** This brief is a coordination and activation surface. It is not Cici's Record, not a legal commitment surface, and not a substitute for evidence review.

---

## 1. Purpose

Design a daily Telegram message that helps the `cici-ai` team do three things well:

1. know what moved in the last 24 hours,
2. know what concrete action matters next,
3. stay inside the lane's evidence and governance boundaries.

The brief should make the group feel active and coordinated without pretending that every signal is equally verified.

The message is not a newsletter. It is a **daily operating brief** for a beginner-heavy cohort.

---

## 2. Design goals

The daily brief should:

- reward real activity, not passive membership,
- point to one or two concrete next actions,
- separate visible evidence from self-report,
- keep confidence and uncertainty visible,
- make it easy for quiet members to re-enter,
- support the monthly lane arc:
  - Telegram creates motion,
  - Core keeps the path safe,
  - Progress proves what actually happened.

The brief should **not**:

- sound like a hype post,
- overstate activation,
- create employment, scholarship, or payment commitments,
- speak as if `work-cici` is Cici's governed instance,
- hide weak evidence behind polished summary language.

---

## 3. Operator rule

The daily brief should be generated from the strongest available evidence in this order:

1. direct artifact or repo-visible evidence,
2. operator-observed private evidence with a pointer,
3. member self-report,
4. explicit follow-up ask when evidence is missing.

If evidence is weak, the brief should narrow rather than improvise.

Use the same confidence tags already established in the dashboard:

- **A** = direct artifact or repo-visible evidence
- **B** = direct operator observation or private evidence pointer
- **C** = indirect claim, self-report, or inferred activity requiring confirmation

---

## 4. Daily brief shape

The message should stay short enough for Telegram and should usually fit into **5 blocks**:

1. **Pulse**
2. **What moved**
3. **What matters today**
4. **Who needs action**
5. **How to reply**

### Recommended length

- target: `120-220` words
- hard cap: `300` words

### Tone

- clear
- practical
- quietly encouraging
- evidence-first
- one level more human than a dashboard, one level less promotional than outreach copy

---

## 5. Canonical message template

```text
Daily cici-ai brief - {DATE}

Pulse
{1 sentence on the current state of motion.}

What moved
- {Member or team movement #1} [{confidence}]
- {Member or team movement #2} [{confidence}]
- {Any repo / artifact / comment / onboarding signal worth noting} [{confidence}]

What matters today
- {Primary task or ask}
- {Secondary task or ask, optional}

Who needs action
- {Name or cohort slice}: {next concrete step}
- {Name or cohort slice}: {next concrete step}

Reply format
- Reply with: {single artifact or proof ask}
```

---

## 6. Content rules by block

### Pulse

One sentence only.

Use it to answer:
- are we in intake,
- setup,
- proof,
- or review mode?

Examples:
- `We have movement, but most of it is still setup-stage rather than proof-stage.`
- `The group is past introductions; today is about turning visible fork activity into first-task proof.`

### What moved

Include only changes that matter to the funnel:

- joined
- introduced
- goal stated
- fork / repo visible
- first task completed
- returned within 7 days
- issue / PR / artifact
- helper behavior
- Predictive History comment movement
- Apprentice Studio task movement

Do not pad with reactions, greetings, or generic enthusiasm.

### What matters today

This should be the wedge.

Prefer:
- one main ask
- one optional secondary ask

Examples:
- `Post your OB1 fork URL or a screenshot showing the fork in your GitHub account.`
- `If you already forked, post one artifact from your first task so we can count it as proof.`

### Who needs action

This is the routing block.

It should:
- name the member or subgroup,
- name the exact next step,
- avoid shame,
- make re-entry easy.

Good:
- `Members with visible forks but no proof packet: post one screenshot or artifact today.`
- `Anyone still blocked on setup: reply with the exact screen or error you hit.`

Bad:
- `Everyone please be more active.`

### Reply format

Always end with a single concrete reply instruction.

Preferred asks:
- one URL
- one screenshot
- one artifact
- one sentence with a defined format

The group should never have to guess what a useful reply looks like.

---

## 7. Daily modes

The brief should adapt to the lane's actual state.

### Mode A - Intake

Use when new joins and introductions dominate.

Emphasize:
- who joined,
- what the group is for,
- one simple first artifact.

### Mode B - Setup

Use when members are trying to fork, clone, or open workspaces.

Emphasize:
- repo-visible setup progress,
- repeated setup blockers,
- one setup proof ask.

### Mode C - Proof

Use when members are active but evidence is thin.

Emphasize:
- first-task proof packets,
- artifact links,
- what counts as completion.

### Mode D - Public-output

Use when Predictive History comments or Apprentice Studio outputs are active.

Emphasize:
- posted outputs,
- quality and reach,
- whether output became reusable or still needed rescue.

### Mode E - Review / Reset

Use when the group needs a cadence reset.

Emphasize:
- what worked,
- what confused people,
- the one next ask for the next 24 hours.

---

## 8. Source map for automation

The automated brief should pull from a bounded set of surfaces:

### Primary

- [cici-ai-community-dashboard.md](cici-ai-community-dashboard.md)
- [cici-ai-lanes.md](cici-ai-lanes.md)
- [cici-ai-first-task-proof-packet.md](cici-ai-first-task-proof-packet.md)
- [cici-ai-weekly-governance-review-template.md](cici-ai-weekly-governance-review-template.md)

### Evidence / operator inputs

- `singularity/work-cici/evidence/`
- `singularity/work-cici/reviews/`
- `singularity/work-cici/cici-ai-progress/`
- `singularity/work-cici/cici-ai-telegram/`
- [predictive-history-comment-tracker.md](predictive-history-comment-tracker.md)
- [apprentice-studio-pilot-ops.md](apprentice-studio-pilot-ops.md)

### Optional source classes

- GitHub-visible fork / repo movement
- Telegram-exported operator notes
- proof packets
- review receipts

---

## 9. Automation contract

The automation should produce **two layers**:

### Layer 1 - Operator digest

A structured internal object such as:

- date
- mode
- top evidence-backed movements
- confidence labels
- members needing follow-up
- primary ask
- draft Telegram message

### Layer 2 - Telegram-ready output

A cleaned brief designed for direct posting.

Important:

- the Telegram message should **not** expose internal uncertainty notes in awkward ways,
- but it **should** avoid overclaiming where evidence is thin.

The operator digest may be longer than the final Telegram message. The Telegram message should feel simple because the internal selection work already happened.

---

## 10. Fallback behavior under weak evidence

This brief must follow the graceful-constraint rule.

If evidence is weak:

- do not invent momentum,
- do not promote self-report into proof,
- do not pretend the dashboard is fresher than it is,
- do not flatten setup noise into activation.

Instead:

- state that verification is still underway,
- ask for one concrete artifact,
- reduce the number of claims,
- shift the message toward re-entry and proof.

Example:

```text
Daily cici-ai brief - YYYY-MM-DD

Pulse
We have some movement, but most of it still needs proof-level confirmation.

What moved
- A few members report setup progress, but not all of it is artifact-linked yet. [C]

What matters today
- Reply with your fork URL or one screenshot showing the current step you reached.

Who needs action
- Anyone who has not posted setup proof yet: send one artifact so we can help or count it.

Reply format
- Reply with: fork URL + one-line status
```

---

## 11. Good daily questions

The automation should answer these before drafting:

1. What actually changed in the last 24 hours?
2. Which lane is blocking progress right now: Telegram, Core, or Progress?
3. What is the single most useful ask for today?
4. Which names or subgroup slices need routing?
5. What claim would be overreach today?

---

## 12. Sample brief

```text
Daily cici-ai brief - 2026-05-22

Pulse
We have visible setup motion, but today is about turning setup into proof.

What moved
- Several members now have visible fork activity or repo motion linked to the cohort. [A]
- A smaller group still needs cleaner handle mapping before we count their setup as confirmed. [B]
- The public-output lane is active, but quality and posting receipts matter more than volume. [B]

What matters today
- If you already forked, post one screenshot or artifact from your first task.
- If you are blocked, post the exact screen or error so we can route help quickly.

Who needs action
- Members with visible forks but no proof packet: send one artifact today.
- Members still unresolved on GitHub/Telegram mapping: reply with your exact GitHub handle.

Reply format
- Reply with: fork URL or screenshot + one-line status
```

---

## 13. Recommended implementation path

Build this in three stages:

1. **Manual template stage**
   - operator fills the brief from dashboard + evidence pointers
2. **Semi-automated digest stage**
   - [scripts/generate_cici_ai_daily_brief.py](../../../scripts/generate_cici_ai_daily_brief.py) assembles candidate movements, names, and asks
3. **Telegram-posting stage**
   - script or assistant emits the final post-ready message after operator review

Do not automate posting before the digest proves reliable.

---

## 14. Success criteria

This brief is working if:

- more replies contain usable artifacts,
- more members move from setup to proof,
- operator rescue time decreases,
- the group needs fewer repeated explanations,
- daily messages become easier to draft, not more elaborate.

This brief is failing if:

- it becomes generic motivation copy,
- it counts noise as activation,
- it hides stale evidence,
- it creates obligation without proof,
- it grows longer as the group gets more confused.

---

## 15. Boundary reminder

The daily Telegram brief may summarize, encourage, and route. It does not:

- update Cici's Record,
- make employment or scholarship commitments,
- stand in for proof packets, review notes, or governance review,
- replace source reading when a load-bearing decision depends on the evidence.
