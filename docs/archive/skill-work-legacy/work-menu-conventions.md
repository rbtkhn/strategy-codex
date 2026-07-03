# WORK menu conventions (Cursor operator)

**Purpose:** When you are in **work-strategy**, **work-politics**, **work-jiang**, or **work-dev**, the assistant ends most substantive turns with **labeled forks** (multiple choice). This doc names the **shape** so menus stay **useful, grounded, and pivot-only** (no faux â€œdoneâ€).

**Rule source:** [`.cursor/rules/menu-option-benefits.mdc`](../../.cursor/rules/menu-option-benefits.mdc) (always-on SSOT) · [`.cursor/rules/operator-style.mdc`](../../.cursor/rules/operator-style.mdc) (WORK menus + execution hygiene).

---

## 1. Real forks only

Each option must be a **different next move** (different file, command, lane, or depth). Avoid filler (â€œcontinueâ€, â€œnothing elseâ€) â€” work **switches**, it does not terminate in-menu.

---

## 1b. Benefit clause (why pick this) — required

**Scope:** Every **assistant-authored** labeled multi-choice block — WORK closing menus, lens/mind offers, steward forks, and other **A–E** pivots. **Not** required when copying **verbatim** coffee / steward text from [menu-reference](work-coffee/menu-reference.md), or when the operator says **no menu** / **no options**.

Each option line states **why** to choose it: one short **because** / **so that** / **in order to** clause on the **same line** as the fork stub (ship, validate, deploy, depth, handoff, unblock CI, falsifier upgrade, remote sync, etc.). Still **no pre-development** of that option’s output until the operator picks.

**Shape:** `**Label** — fork stub, because/so that/in order to payoff`

**Good:**

```text
**A** — Commit the hinge slice only, so that falsifiers ship without unrelated WIP
**B** — Run wire-verify on UAE tranche, because J12-4 may upgrade from contested to partial
```

**Bad:** label-only stubs; benefit on a second line; implied payoff without **because** / **so that** / **in order to**.

**Combo picks (`A+C`):** each listed letter option still carries its own benefit when shown.

**Cursor rule (always-on):** [`.cursor/rules/menu-option-benefits.mdc`](../../.cursor/rules/menu-option-benefits.mdc)

---

## 1c. Menu pick execution (same turn)

When the operator picks a letter for a **bounded run** (validator, sync, build, handoff check):

1. **Execute** the named `scripts/*.py` command **in that turn**.
2. Report **exit code** and **pass/fail** (plus top errors if fail).
3. **Do not** read the full script first; **do not** batch Read+Grep+Shell on the same target before the run.

Stall recovery and validator-first detail: [`.cursor/rules/agent-execution-hygiene.mdc`](../../.cursor/rules/agent-execution-hygiene.mdc) · [`.cursor/skills/validator-first/SKILL.md`](../../.cursor/skills/validator-first/SKILL.md).

---

## 2. Evidence-linked options (Fork explorer)

When a fork touches the **Record** or **gate**, include at least one **explicit anchor** per option where helpful:

- `` `recursion-gate.md` `` and **`CANDIDATE-XXXX`** when relevant
- Repo-relative paths: `` `docs/skill-work/...` ``, `` `scripts/....py` ``
- Links to GitHub are fine for **read-only** context; **canonical edits** stay in this repo

This turns selection into **grounded** handoff without bypassing **RECURSION-GATE**.

---

## 3. Cost and impact tags (heuristic)

Optional short tags on each line, **clearly heuristic** (not estimates of wall-clock certainty):

- **Time:** `~15m`, `~45m` â€” rough order of magnitude
- **Leverage:** `high-leverage`, `hygiene`, `deep` â€” qualitative
- **Do not** present uncalibrated **percentages** as oracle metrics (e.g. fake â€œgate merge probability %â€) unless a **defined script** computes them

---

## 3a. Default acceptance

When a visible menu includes a line like **`Recommended default: X`**, operator replies such as **`go`**, **`default`**, **`yes`**, **`sounds good`**, or equivalent agreement mean **accept the named default** from the current menu. This only applies when the current turn explicitly named the default; otherwise interpret those replies normally.

Keep menu letters as UI conveniences. Durable logs should still use conductor slugs, file paths, lane names, candidate IDs, or script output labels.

---

## 4. Combo and hybrid options

- The operator may answer **`A+C`** (or similar); the assistant executes both compatible branches.
- When two options combine naturally, you may add one line: **Combo:** `B + half of D` â€” *brief label explaining the merge* (still one human pick; do not develop the combo content until selected).
- **`F` â€” All (strategy-notebook hygiene bundle):** In one pass â€” (1) **verify hooks** / Primary-pull targets in `daily-strategy-inbox.md`, (2) **MINDS** cross-pointer to dated mind-file addenda (e.g. `CIV-MIND-MERCOURIS.md` **III.M**), (3) **Carry** lines that tie inbox â†” mind. **Exclude** weaving scratch into `chapters/YYYY-MM/days.md` unless **`dream`** or **explicit operator direction** â€” early **weave** risks duplicate **Judgment** before **Links** verify.
- **`strategy + verify`** â€” **Work-strategy** fork: same intent as **`strategy`** / **`strategy ingest`**, plus a **triage fact-check** ([`.cursor/skills/fact-check/SKILL.md`](../../.cursor/skills/fact-check/SKILL.md)) and/or **web pass** on **load-bearing** claims â€” especially **rosters**, **dates**, and **stats** from **transcripts**. Land outcomes in **`daily-strategy-inbox.md`** (**`verify:`**, **Primary pulls**) and, when folding, **`### Web verification`** / **`### References`** in `days.md` â€” not **`### Reflection`** without sources. Spec: [`.cursor/skills/skill-strategy/SKILL.md`](work-strategy/SKILL-STRATEGY-DEPRECATED.md) (**Modes** â†’ **+ verify**, **Transcript / analyst capture**); architecture: [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../continuity/STRATEGY-NOTEBOOK-ARCHITECTURE.md) Â§ *skill-strategy modes and verification passes*.

---

## 5. Optional confidence / LLM assist (off by default)

If the operator enables an **experimental** â€œconfidenceâ€ or â€œexplain firstâ€ mode:

- Any numeric score is **assistant uncertainty**, not ground truth.
- Prefer a **one-sentence** rationale over blocking the whole menu.

**Scripted morning ranking + optional LLM re-rank:** [`scripts/suggest_morning_forks.py`](../../scripts/suggest_morning_forks.py) (`--llm` requires `OPENAI_API_KEY`).

---

## 6. Auditing picks (Choice journal)

**Do not** auto-append operator menu picks to **`memory.md`** / **memory** from the Voice or analyst without governance change ([`docs/memory-template.md`](../memory-template.md)).

**Do** log picks **explicitly** when the operator wants a trail:

```bash
python3 scripts/log_operator_choice.py -u grace-mar --context WORK --picked A --tags "~20m,gate" --note "optional"
```

Appends `### [WORK-choice]` blocks to **`session-transcript.md`** (operator continuity, not gated Record).

**`coffee` session trail:** Sessions started with **`coffee`** (work-start vs signing-off Step 1; optional light, minimal, survey; legacy **`hey`** still works) can leave traces in **`session-transcript.md`** (raw lines and **`[WORK-choice]`** via `log_operator_choice.py`) and/or dated bullets under **`docs/skill-work/work-*/*-history.md`** (per-lane milestones â€” [work-modules-history-principle.md](work-modules-history-principle.md)). Distinct from **`memory.md`** (companion continuity). See [canonical paths](../canonical-paths.md).

**Aggregate after ~30 days:**

```bash
python3 scripts/menu_choice_evolution.py -u grace-mar --days 30
python3 scripts/menu_choice_evolution.py -u grace-mar --days 30 --print-gate-stub
```

The gate stub is **stdout only** â€” paste and edit **`CANDIDATE-XXXX`** before any merge.

**Strategy ingest session receipt (optional):** End-of-session tally for **X / transcript ingests** without duplicating full lines in `session-transcript.md` â€” the **SSOT** for paste-ready lines stays [strategy-notebook/daily-strategy-inbox.md](../../continuity/daily-strategy-inbox.md). Example:

```bash
python3 scripts/log_operator_choice.py -u grace-mar --context WORK --picked strategy-ingest \
  --tags "count=7" --note "see daily-strategy-inbox 2026-04-12"
```

`--note` is truncated at **500 characters** by the script â€” use a **pointer** (date / file), not a full paste dump. First-class `--context INGEST` is **not** required; `WORK` + `picked` + tags is enough for aggregation.

**Strategy weave ledger (optional):** After weaving [strategy-notebook/daily-strategy-inbox.md](../../continuity/daily-strategy-inbox.md) into `chapters/YYYY-MM/days.md`, append one JSONL event (compression proxies, optional ratings) â€” not session-transcript, not MEMORY:

```bash
python3 scripts/log_strategy_fold.py -u grace-mar --notebook-date 2026-04-13 --fold-kind manual \
  --inbox-chars 12000 --days-delta-chars 4000 --note "tight merge; verify pins next"
python3 scripts/report_strategy_fold_learning.py -u grace-mar --days 30
```

Spec: [FOLD-LEARNING.md](../../continuity/FOLD-LEARNING.md).

**Strategy context (cold start):** `python3 scripts/strategy_context.py -u grace-mar` prints one **â‰¤120-word** re-entry paragraph (notebook **Open**, inbox, daily brief Â§1b, STRATEGY / promotion ladder / commentator index) or **`--compact`** path/status lines; **`--meta`** / **`--minds`** add month **`meta.md`** and Tri-Frame **`minds/outputs`** pointers; **`--recent N`** or **`--history`** (N=20) appends **lightweight history** (fold JSONL + filtered WORK-choice + optional **`--recent-git K`**); **`--log`** appends a **`WORK-choice`** receipt to **`session-transcript.md`** via `log_operator_choice.py` (pointer-only note). See [work-strategy README â€” `strategy-context`](work-strategy/README.md#strategy-session-helpers-skill-strategy).

---

## 6a. Ship receipt

After substantive **`EXECUTE_LOCAL`**, conductor **`bravo`**, intake batch checkpoint, or **signing-off** coffee Step 1, paste a compact **Ship receipt** so the operator does not mentally integrate branch, ahead/behind, uncommitted slices, and push command.

**Script (preferred):**

```bash
python3 scripts/operator_handoff_check.py -u strategy-codex
```

The output includes a `## Ship receipt` block with:

| Field | Meaning |
|-------|---------|
| **Branch** | `git branch --show-current` |
| **Tracking** | ahead/behind from `git status -sb` |
| **origin/main** | resolved SHA when available |
| **Uncommitted slices** | paths grouped by `statecraft/`, `ph-civ`, `singularity/`, `other` |
| **Recent local commits** | last three oneline |
| **Suggested push** | e.g. `git push origin main` when ahead and clean |
| **Excluded WIP** | paths still outside the last commit |

Agents may inline the same shape after a local commit when running the full handoff script is heavy.

**When:** post-commit close, conductor `bravo`, intake archive-checkpoint, signing-off Step 1 tail ([menu-reference — signing-off](work-coffee/menu-reference.md#signing-off-intent)).

---

## 6b. Tiered WORK menus (ship blockers first)

When git shows **ahead > 0** or **meaningful uncommitted** lane files (`statecraft/`, `ph-civ`, `singularity/`), the menu **must** lead with **ship blockers** before deferred forks.

Shape:

```text
**Ship blockers** (if any): uncommitted statecraft slice | push pending | mixed branch
**Deferred forks**: companion wire-in | benchmark rerun | multi-lens pass | …
```

Rule: max **2** blocker slots + **3** deferred forks (5 options total). If no blockers, use the normal 3–5 fork menu without a blocker header.

Blocker examples:

- uncommitted `statecraft/synthesis/day/` after intake close
- branch **ahead 2** with clean tree → push before new lane work
- mixed Jiang + statecraft WIP → name which slice to commit first

---

## 7. Multi-agent fork generation (experimental)

See [work-strategy/multi-agent-fork-generator.md](work-strategy/multi-agent-fork-generator.md) â€” optional two-pass / subagent pattern; human still chooses one branch.

---

## 8. Dated filenames and CLI dates

Dated WORK outputs (daily brief, weekly scaffold, newsletter digest, optional `morning-forks-*.md`) use **`YYYY-MM-DD`** in the basename unless the doc names a compact id pattern. Full rules, UTC timestamps, and **`YYYYMMDD`** exceptions: [Date and time formats](../date-time-conventions.md).

---

## See also

- **Menu benefit clause (always-on):** [`.cursor/rules/menu-option-benefits.mdc`](../../.cursor/rules/menu-option-benefits.mdc) · §1b above
- **`strategy + verify`** (named fork) — §4 **Combo and hybrid options** above; full spec under **work-strategy** in [skill-strategy SKILL](work-strategy/SKILL-STRATEGY-DEPRECATED.md).
- **Fixed session menu (`coffee` - same **A-D** hub for work-start and signing-off; legacy **hey** still works):** not the 3-5 WORK pattern - canonical hub: **A** Steward, **B** Engineer, **C** Statecraft, **D** Singularity. Coffee **C** then routes into the four civilizational-state lanes America, China, Persia, and Russia. Conductor is standalone by `conductor` / master name, not a hub letter. **C** exits the coffee hub by default unless **`stay in coffee`**; **skills** / **meta:** say with **B - Engineer**. Legacy **A-G** workload table for mapping: [menu-reference.md](work-coffee/menu-reference.md)). Roles: [.cursor/skills/coffee/SKILL.md](../../.cursor/skills/coffee/SKILL.md).
- [Operatorâ€“agent lanes](../operator-agent-lanes.md)
- [Coffee skill](../../.cursor/skills/coffee/SKILL.md)
- [Work territory history logs](work-modules-history-principle.md) (`docs/skill-work/work-*/*-history.md`)
- [Bootstrap â€” coffee](../../archive/grace-mar-instance/bootstrap/grace-mar-bootstrap.md)
- [Date and time formats](../date-time-conventions.md)
