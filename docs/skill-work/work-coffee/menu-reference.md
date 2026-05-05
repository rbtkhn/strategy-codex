# Coffee â€” menu and protocol reference

**Canonical Step 2 menu (grace-mar):** **five** hub lines â€” **A** Steward, **B** Engineer, **C** Historian, **D** Capitalist, **E â€” Conductor** (**hub `E` does not preview** last master â€” label only). **`coffee` hub E** **auto-continues** **`last_logged_conductor`** from cadence when present ([coffee SKILL Â§ Hub E](../../../.cursor/skills/coffee/SKILL.md#hub-e-auto-continue)). **No** masters MCQ row printed **under** the hub list; the five Symphony masters (**Toscanini â€¦ Bernstein**) disambiguate via **Conductor MCQ** only when needed â€” **hub E** otherwise jumps to orientation + **Conductor action MCQ** after **`coffee`**; **standalone** master name / **`conductor`** / [conductor skill](../../../.cursor/skills/conductor/SKILL.md) without `coffee` â€” see [CONDUCTOR-PASS.md](CONDUCTOR-PASS.md). **No** micro-hints row under the hub list. Executable contract: [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md).

**Historian C â€” three-option submenu:** Choosing **C â€” Historian** presents exactly three actionable options and nothing else:

```markdown
Historian menu â€” reply Aâ€“C
A. Intel â€” daily brief / current-events watch
B. Elicit knowledge â€” self-knowledge MCQs â†’ IX-A candidates
C. Notebook synthesis â€” History Notebook / Predictive History with Tri-Frame lenses
```

**C-B Elicit knowledge:** [.cursor/skills/elicit-knowledge/SKILL.md](../../../.cursor/skills/elicit-knowledge/SKILL.md) â€” default **6** topic-anchored MCQs plus **one** open-ended follow-up question, **â‰¤2** date-primary stems, strictness default **top2**, staged candidates only; no merge without companion approval.

**C-A Intel / `last30days`:** [.cursor/skills/last30days/SKILL.md](../../../.cursor/skills/last30days/SKILL.md) may be offered inside **Intel** when a current-events or strategy frontier is stale and the operator wants one fresh, source-dated scan. It is not a new coffee hub line and does not run automatically during Step 1. Default output is a short brief, provenance log, and optional paste-ready `daily-strategy-inbox.md` one-liner; no `days.md`, author-thread, strategy-page, or Record edits.

**C-C Notebook synthesis / `skill-elicitation`:** [.cursor/skills/skill-elicitation/SKILL.md](../../../.cursor/skills/skill-elicitation/SKILL.md) may be offered inside **Notebook synthesis** when strategy-codex work is blocked by ambiguous stream ownership, page shape, raw-input routing, contrapuntal comparison, or civ-mem lens choice. It is an optional checkpoint, not a new hub line, and it must not run automatically during Step 1.

**Capitalist D â€” bookshelf product use:** D may use bookshelf for offers, teaching, grace-gems, product packaging, or public copy. It does **not** own IX-A bookshelf recursion. Catalog stance membrane remains a scripted secondary path when requested or when a pressing organizational membrane issue applies.

**Symphony / Conductor:** [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../../../codex/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) + [CONDUCTOR-PASS.md](CONDUCTOR-PASS.md). **self-skill-write** / PRP / Lexile / prompt proposals â†’ hub **D â€” Capitalist** or explicit **`write`** / **`skill-write`** without opening **`coffee`**.

<a id="conductor-fork-d-menu"></a>
<a id="conductor-fork-d1-d5"></a>

The sections below retain **legacy Aâ€“G workload detail** (seven letters) for **scope** descriptions; map to the coffee SKILLâ€™s current **Aâ€“E** hub (**Daily Brief â†’ C-A Intel**, **Bookshelf self-knowledge quiz â†’ C-B**, **History Notebook / Predictive History â†’ C-C**, **Build â†’ B Engineer**, **Steward â†’ A**, **Symphony continuation â†’ hub E** or standalone **`conductor`**; commercial / teaching bookshelf uses â†’ **D Capitalist**). **Signing-off** add-ons, cadence tables, explicit phrase modifiers, and companion survey track follow.

**Exit:** There is **no** â€œclose hubâ€ letter. The operator leaves coffee by **C** (normal workflow unless **`stay in coffee`**), by **Later** on the [steward follow-up fork](#steward-follow-up-fork-implement-now-vs-later) (which returns to the full menu), or by starting a non-coffee task. **A**, **B**, **D**, and **E** re-offer the full **coffee** hub **Aâ€“E** **after** the branch completes â€” **unless hub E** opened **Conductor action MCQ** in **that same reply**, in which case **wait** for **Conductor** **reply A-C** **first** (no duplicate **coffee** hub menu in that message). The coffee ritual does **not** use a **no menu** opt-out.

### Bare **`compass`** vs **`coffee`** then **`C`**

**Full ritual:** Say **`coffee`** (Step 1 scripts + full menu), then choose **`C`** when you want the Historian submenu: **A Intel**, **B Elicit knowledge**, or **C Notebook synthesis**. **Bare `compass`** (or strategy without opening **`coffee`**) means **strategy lane only**â€”agents may deliver work-strategy / **ROME-PASS** content **without** re-running Step 1 unless you ask for **`coffee`** first, **`stay in coffee`**, or a cold-thread stack (**`operator_coffee.py --mode reentry`**).

---

## Context paste budgets (operator)

**Not** Record truth. JSON under [`config/context_budgets/`](../../../config/context_budgets/) caps ritual paste size: **`coffee.json`** drives collapsed **Last dream** line count, optional civ-mem / coffee-rollup lines, and session-tail depth in **`scripts/operator_daily_warmup.py`**; **`dream.json`** drives **`scripts/auto_dream.py`** civ-mem echo limits, rollup allow, and integrity/governance suppress rules before **`last-dream.json`** is written. Defaults keep the collapsed Last dream block thin; opt in with **`--show-civ-mem`** / **`--show-rollup`** on `operator_daily_warmup.py`, or forward the same flags from **`operator_coffee.py`** / **`operator_reentry_stack.py`**. Approximate footprint: **`python3 scripts/audit_context_tax.py -u grace-mar`**. See [`config/context_budgets/README.md`](../../../config/context_budgets/README.md) and [`docs/skill-work/work-dream/README.md`](../work-dream/README.md) (handoff fields).

---

## Cadence by weekday

Default rhythm (operator can override any day):

| Day | Mode | What to run |
|-----|------|-------------|
| **Monday** | **Full** | Complete coffee flow: operator + harness + branch snapshot in Step 1. **Internet intel** (Polymarket, independent polls, Massie X): **not** Step 1 â€” run on **menu C â€” Historian** (full Monday weight) or explicit request. **Daily brief:** **menu C** only (Historian / daily brief path). |
| **Tuesdayâ€“Friday** | **Lighter** | Same Step 1 as Monday (scripts + branch snapshot). **Polling + Polymarket + Massie X:** only when **C / Historian** (compact) or explicit request. **Daily brief:** **menu C** only (Step 1 one-lines the path pattern). |
| **Sunday** | **Week ahead (~10 min)** | Lighter coffee (week-ahead focus, not Monday-full). Focus: **FEC / compliance dates** and **voter registration** â€” use **last on-disk** `daily-brief-*.md` calendar slice if present, else [brief-source-registry.md](../work-politics/brief-source-registry.md) (`needs_refresh`, `watch`). **Generating** today's brief remains **menu C â€” Historian**. Optional: run `operator_work_politics_pulse.py` or check weekly-brief readiness. |
| **Friday** | **Lighter + post-mortem** | Same as Tueâ€“Fri **plus** two lines at the end of the reply: **(1)** What repeated this week? **(2)** What to drop from the routine? |

If the operator says **`coffee`** on a **Sunday** (or legacy **`hey`**), default to **week-ahead** mode unless they ask for the full Monday stack. Still run **Step 1** scaled to that mode, then **Step 2** with the full menu (labels can be shorter; meanings unchanged).

---

## Explicit phrases (override default cadence when stated)

**`coffee light`** (or clear equivalent; legacy **`hey light`** still works):

- Run **`operator_daily_warmup.py`** and, when instance state matters, **`harness_warmup.py`**.
- **Internet intel** (Polymarket, polls, Massie X) is **never** Step 1 â€” same as full coffee; choose **C â€” Historian** when you want it (or ask explicitly). **Light** keeps **branch snapshot** compact (one line unless multiple branches).
- **Daily brief:** **do not** generate in Step 1 â€” one-line pointer to **menu C** and path pattern `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` (e.g. `daily-brief-2026-03-29.md`).
- Deliver a **compact brief** from script outputs + thread context; then the **full Step 2 menu**. On later turns, **A**, **B**, **D**, or **E** re-offer the full menu; **A** uses the [steward follow-up fork](#steward-follow-up-fork-implement-now-vs-later) when reading canonical **A â€” Steward**; **C** exits to normal workflow by default after the reply. **Engineer (B):** **compact** work-dev/skills focus â€” **Engineer menu**: **3â€“5 options** as **Aâ€“E** (fresh letter run), **one option per line**, with explicit **`Engineer menu â€” reply Aâ€“E`** heading; branch/`git status` lives under **A â€” Steward**, **git/ship** track when chosen. **Not** a full sweep unless the operator asks.

**`coffee minimal`** (or clear equivalent; legacy **`hey minimal`** still works):

- Run **`harness_warmup.py`** only when instance state matters; **do not** run `operator_daily_warmup.py` unless the operator asks.
- Step 1 has **no** Polymarket / Massie X / poll web search unless the operator **explicitly** asks in the same message. **Daily brief** still **only** via **menu C** (never Step 1).
- Optional **one-line** gate pointer (e.g. pending count from warmup output if already pasted, or "see `recursion-gate.md`").
- Still output the **full Step 2** menu. On later turns, **A**, **B**, **D**, or **E** re-offer the full menu; **A** uses the [steward follow-up fork](#steward-follow-up-fork-implement-now-vs-later); **C** exits to normal workflow by default after the reply. **Engineer (B):** **minimal** â€” **3â€“5 labeled** Engineer next moves (**one line each**); **git/ship** â†’ **`A git`** if needed; no unrelated sweeps.

**`coffee survey`** (or **`coffee + survey`** / clear equivalent; legacy **`hey survey`** still works):

- Run **Step 1** using the same cadence or explicit phrases as if they had said plain **coffee** (they may combine with **coffee light** or **minimal** â€” apply both: thin work-politics steps *and* survey intent).
- In the **Step 1 warmup brief**, add a short **Companion survey** block (2â€“4 lines): purpose (IX-B / IX-C refinement), suggested cadence hint (e.g. **monthly micro** 3â€“5 questions vs **quarterly** deeper pass), pointer that execution is **menu C â€” Historian** this session unless they choose another letter first.
- **Step 2** remains the **same fixed menu** (do not drop letters). When the operator chooses **C**, run the [Companion survey track](#companion-survey-track) for that turn (skip Polymarket/Massie unless the operator also wants intel in the same turn). After the survey turn, exit to normal workflow by default unless the operator says **`stay in coffee`**.
- **Pipeline:** survey work **stages** `recursion-gate.md` candidates only â€” **no merge** without companion approval; same rule as the rest of this skill.

---

<a id="ah-table"></a>

## Legacy Aâ€“G workload table (detail; canonical menu is the current coffee menu)

**Canonical Step 2** today: [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md) â€” **Aâ€“E** (hub only). **Standalone Conductor** / masters MCQ â€” [CONDUCTOR-PASS.md](CONDUCTOR-PASS.md). The **rows below** keep **historical seven-letter labels** for workload scope. **Map:** old **Daily Brief â†’ current C-A Intel**; old **Bookshelf self-knowledge quiz â†’ current C-B**; old **Book / Jiang / Predictive History â†’ current C-C Notebook synthesis**; old **Build â†’ current B**; old **Steward â†’ current A**; commercial bookshelf uses â†’ **D**; **Conductor continuation â†’ hub E**.

The **first** coffee reply ends **Step 2** with the fixed menu. **Follow-up behavior (canonical letters):** **A**, **B**, **D**, and **E** re-offer the full menu once the branch settles (**exception:** choosing **coffee** hub **`E`** yielded **orientation + Conductor action MCQ** â€” **do not** re-offer **`coffee`** hub **`Aâ€“E`** in **that same reply**; reply to **Conductor** **`A-C` first** â€” see **[Exit]** above Â· [coffee SKILL â€” Exit / re-offer](../../../.cursor/skills/coffee/SKILL.md)); **A** uses the [steward follow-up fork](#steward-follow-up-fork-implement-now-vs-later) (full menu only after **Later** or when nothing actionable surfaced); **C** exits to normal workflow by default after the reply. Wording may vary; **roles must not**.

| Letter | Mode | What it means when chosen |
|--------|------|---------------------------|
| **A** | **Daily Brief** | Legacy detail now maps to **current C-A Intel**. Step 1 never runs the brief generator or KY-4 web intel. C-A owns the brief file, Putin/Vance/PRC/IRI watches, optional KY-4, brief registry, campaign, and queue. Tri-Frame is not automatic here; it belongs to **current C-C Notebook synthesis**. |
| **B** | **Build** | **work-dev execution + skills/meta** â€” **not** git/ship ( **E â€” Steward**, **git/ship** track); **not** Record/template/integrity audits ( **E â€” integrity/exports** ). **(1) Work-dev** â€” `docs/skill-work/work-dev/`, [work-dev-sources.md](../work-dev/work-dev-sources.md) spot-check when in scope; **one** implementation next step (specs, integration, tooling). **(2) Skills / meta** â€” [skills-portable/skill-candidates.md](../../../skills-portable/skill-candidates.md), [extract-skill-from-session](../../../.cursor/skills/extract-skill-from-session/SKILL.md), [portable-skills-sync](../../../.cursor/skills/portable-skills-sync/SKILL.md) when the operator says **skills** / **meta** with **B** or asks after Build. **Pending RECURSION-GATE candidates** are **not** Build â€” use **E â€” Steward** (gate). **Not** **G** â€” **G** is **only** the first open line in [workspace.md](../work-dev/workspace.md) Â§ **Next actions**. Full layer breakdown: [Build (B) â€” detailed scope](#build-b--detailed-scope). |
| **C** | **Compass** | Legacy detail now maps to **current C-C Notebook synthesis** when the work is History Notebook / Predictive History / Rome-shaped synthesis, and to **current C-A Intel** when the work is current-events brief work. WORK only; no SELF/EVIDENCE/prompt merge without gate + companion approval. |
| **D** | **Book** | Legacy work-jiang / Predictive History detail now maps to **current C-C Notebook synthesis**. D in the current hub is Capitalist, so bookshelf belongs under D only for offers, teaching, grace-gems, product packaging, public copy, or scripted catalog stance membrane. |
| **E** | **Steward / System choice** | Legacy self-knowledge quiz detail now maps to **current C-B Elicit knowledge**. Steward tracks remain under current **A â€” Steward**; Conductor remains current **E â€” Conductor**. **Read-only membrane invariant:** no merge without companion `approve` + `process_approved_candidates.py`. |
| **F** | **Cici next** | **work-cici â€” one next task** when chosen. Ground in Step 1 **`lane next hints`** from `scripts/coffee_lane_next_hints.py` (also runnable alone). Canonical docs: [INDEX.md](../work-cici/INDEX.md), [SYNC-DAILY.md](../work-cici/SYNC-DAILY.md), [WORK-LEDGER.md](../work-cici/WORK-LEDGER.md), [DAILY-OPS-CARD.md](../work-cici/DAILY-OPS-CARD.md). Deliver **one** prescribed step; expand mirrors / BrewMind / runbooks only if needed for that step. In the canonical menu, this workload usually maps to **E** (system choice). **Re-offer** the full menu after the turn unless the operator exits. |
| **G** | **Dev next** | **work-dev â€” next task only** from [workspace.md](../work-dev/workspace.md) Â§ **Next actions**: the first **open** numbered line (not leading with `~~`). **One** concrete step â€” **no** default piggyback of a full legacy **B** (Build / work-dev+skills) or **E git/ship** pass. In the canonical menu, this workload usually maps to **E** (system choice). **Re-offer** the full menu after the turn unless the operator exits. |

<a id="tri-frame-daily-brief"></a>

### Historian C â€” Intel, Elicit Knowledge, Notebook

**Operator intent (grace-mar default):** **`coffee` â†’ C â€” Historian** does **not** auto-run daily brief and does **not** auto-offer Tri-Frame. It presents exactly three actionable options:

- **A. Intel** â€” daily brief file + Â§1d / Â§1e / Â§1g / Â§1h (PRC / IRI when load-bearing) + optional KY-4 intel + optional `last30days` frontier check.
- **B. Elicit knowledge** â€” self-knowledge MCQs toward IX-A candidates plus one open-ended follow-up question; default 6 questions, â‰¤2 date-primary, top2 strictness, staged candidates only.
- **C. Notebook synthesis** â€” History Notebook / Predictive History synthesis. Tri-Frame minds **Barnes â†’ Mearsheimer â†’ Mercouris** live here; use [daily-brief-minds-menu.md](../work-strategy/daily-brief-minds-menu.md) and [minds/DAILY-BRIEF-MINDS-WORKFLOW.md](../work-strategy/minds/DAILY-BRIEF-MINDS-WORKFLOW.md) when a synthesis pass needs those lenses.

When **C-C Notebook synthesis** is blocked by tacit operator judgment, offer one bounded `skill-elicitation` checkpoint and then return to the notebook synthesis path. Do not ask elicitation questions from the coffee hub itself.

<a id="build-b--detailed-scope"></a>

### Engineer (B) â€” detailed scope (legacy anchor id: Build)

**Role:** **Work-dev execution layer** â€” specs, integration, sources, portable skills â€” **not** git/ship ( **A â€” Steward**, **git/ship** ) and **not** membrane audits ( **A** other tracks ).

| Layer | What belongs here | Typical moves |
|-------|-------------------|---------------|
| **Work-dev implementation** | Specs, integration steps, source deltas, tooling that **changes behavior** | [workspace.md](../work-dev/workspace.md), [INTEGRATION-PROGRAM.md](../work-dev/INTEGRATION-PROGRAM.md), [work-dev-sources.md](../work-dev/work-dev-sources.md) |
| **Skills / meta (tooling)** | Portable skill sync, candidates row, extract-skill | [skills-portable/README.md](../../../skills-portable/README.md), `sync_portable_skills.py` â€” **validate_skills.py** as a pre-commit check is fine here; **integrity / derived truth** as the main question â†’ **A â€” integrity** |

**Not Engineer (use Steward **A**):** **git/ship** (branches, status, commit plan); `validate-integrity.py`; `refresh_derived_exports.py` (ship); `template_diff` / companion-self parity; **RECURSION-GATE** review ( **A â€” gate** ).

**Engineer vs G:** **G** is **only** the first **open** line in **workspace.md** Â§ **Next actions**. **B** is broader work-dev + skills in one turn when chosen.

**Coffee `hub B` â€” Engineer:** When the operator picks **B â€” Engineer** after **`coffee`**, reply with **`Engineer menu â€” reply Aâ€“E`** (or **Aâ€“D**): **3â€“5** repo-grounded stubs, **letters A onward, one row per letter**, fresh alphabet for **this** submenu. **Not** a single prose-only path. Same **present vs execute** rhythm as Conductor action MCQ; **label menus** when both **coffee hub** letters and submenu letters appear in proximity.

**When the Steward turn includes template/boundary / companion-self parity**, the reply must end with a **Reconciliation code** block:

```markdown
### Reconciliation code
- **Upstream (grace-mar â†’ companion-self):** *(specific paths + one line each, or "none â€” â€¦")*
- **Downstream (companion-self â†’ grace-mar):** *(specific paths + adopt command if any, or "none â€” â€¦")*
```

Per [work-companion-self Â§ Reconciliation code audit](../work-companion-self/README.md#reconciliation-code-audit-upstream-and-downstream).

<a id="steward-follow-up-fork-implement-now-vs-later"></a>

### Steward follow-up fork â€” **Implement now** vs **Later**

After **`A â€” Steward`** (legacy tables below may still say **`B`** or **`E â€” Steward`**), the assistant **does not** always return to the full menu.

**Actionable possibilities** (any one is enough for the fork):

- **Gate track:** â‰¥1 candidate with `status: pending` in `recursion-gate.md` (above `## Processed`).
- **Template/boundary track:** **Reconciliation code** lists something **beyond** both lines being *none / no slice / docs-only with no adopt path* â€” e.g. **pull-needed** files, `only_template` scripts, merge-slice targets, or explicit adopt/refresh commands. **Exception (orientation-only):** if the only â€œextraâ€ content is **policy-documented expected drift** (e.g. [expected-template-drift.json](../work-companion-self/expected-template-drift.json)) and **no** new merge/adopt step is indicated â†’ **not** actionable for the fork (re-offer the full menu).
- **Integrity/exports track:** `validate-integrity.py` reports **failure** / violations, or the pass shows **clear remediation** (e.g. must run `refresh_derived_exports.py` â€” still **proposal + Implement now**, not silent write).
- **Git/ship track:** **Actionable** dirty tree, stale/`[gone]` branches, or a **clear** commit/push grouping that needs operator **Implement now** (still read-only until they ship).

**If actionable â†’ two options only** (no full coffee menu this turn):

1. **Implement now** â€” **Template/boundary:** proposal (scope, files, approach) then ship per operator lane (**EXECUTE** / **EXECUTE_LOCAL** / explicit approval). **Gate:** deepen **read-only** review (recommendations, id+summary echo); **never** merge without companion **approve** + `process_approved_candidates.py`. **Integrity/exports:** proposal to run **`refresh_derived_exports.py`** or fix reported issues â€” **ship** per lane; **never** refresh derived exports silently from coffee. **Git/ship:** proposal to **commit** / **push** / merge or delete branches per plan â€” operator executes. If the operator wants gate **status** edits, they must approve wording; assistant does not merge Record from steward alone.
2. **Later** â€” Immediately present the **full coffee menu** again.

**If not actionable** (gate empty for pending; template reconciliation only expected drift / **none** upstream & downstream per exception above; **integrity** clean with no remediation; **git/ship** clean or â€œno prescriptionâ€) â†’ **skip the fork**; re-offer the **full menu** as after **A** / **B** / **D** / **E**.

**Why Steward (A) does not silently implement:** Steward stays **orientation** until **Implement now**; scope stays explicit so instance paths and Record boundaries stay safe.

**Non-bypass:** **Implement now** on gate work **does not** replace companion **approve** + merge script. Template **upstream** PRs stay human-gated per [work-companion-self README](../work-companion-self/README.md).

<a id="steward-audit-vs-eship"></a>

**Synonyms:** **`A+ship`**, **`A implement`**, or **`EXECUTE` / `EXECUTE_LOCAL`** + slice â€” treat as **Implement now** when the operator uses them on the turn after **`A â€” Steward`** (legacy docs may still say **`B`** or **`E`**).

---

<a id="signing-off-intent"></a>

## Signing-off intent (closeout merged â€” no separate menu)

**Trigger:** Operator says **`coffee`** (or **`hey`**) with **signing-off** intent â€” end of session, wrapping the day, stepping away.

**Step 1:** Handoff-weighted â€” `python3 scripts/operator_coffee.py -u <id> --mode closeout` or `operator_handoff_check.py` (see [coffee SKILL.md](../../../.cursor/skills/coffee/SKILL.md)). Same paste + short paragraph as before.

**Step 2:** The **same** menu as work-start (**order A, B, C, D, E**). There is **no** separate closeout menu and **no** closeout-only letter.

**Per-letter add-ons when Step 1 was signing-off** (optional emphasis â€” do not duplicate the whole handoff block):

| Letter | Signing-off add-on |
|--------|---------------------|
| **A** | **Steward** â€” same **single-track default** as work-start (**gate** if pending candidates, else **template/boundary**); **`A integrity`**, **`A git`**, **`A all`** when explicit. If handoff flagged **dirty tree / branch noise** â†’ prefer **`A git`**; **manifest / derived churn** â†’ **`A integrity`**. Follow-up: [Implement now vs Later](#steward-follow-up-fork-implement-now-vs-later). |
| **B** | **Engineer** carryover from Step 1 when relevant; one concrete work-dev / skills step. |
| **C** | Brief + strategy carryover only if **C** chosen; optional pointer to the next brief / strategy day. |
| **D** | **Capitalist** â€” work-business, grace-gems, bookshelf membrane, commercial cici, skill-write slice as filled on the hub line. |
| **E** | **Conductor** â€” continuity pass via **`last_logged_conductor`** after pick; hub menu line **E** says **Conductor** only (**no last-master preview**); resolve slug **after** selection; **not** a substitute for standalone **`conductor`** when closing without hub picks. |

---

<a id="companion-survey-track"></a>

## Companion survey track

**When:** Operator chose **coffee C â€” Historian** and the pick is survey â€” or they began with **coffee survey** and then chose **C** (default survey under **Historian**). **Signing-off intent + A** without a sub-track â†’ **system pick** may include survey as the one recommendation.

**Goal:** Refresh **self-curiosity (IX-B)** and **self-personality (IX-C)** on a **cadence** (typical: **monthly micro** 3â€“5 questions, or **quarterly** longer refinement), without bypassing the gated pipeline.

**Operator / agent actions (read-only unless operator switches to ship):**

1. **Scope** â€” Pick one wave type: **micro** (few questions, one candidate per answer cluster) vs **theme** (one candidate synthesizing a short battery). Prefer **split candidates** (one mergeable gate block per theme) like the Abigail refinement pattern: `CANDIDATE-0092`â€“`0097`-style rows.
2. **Grounding** â€” Each staged block must carry **literal companion answers** (or transcript pointer) under `source_exchange`; no inferred facts beyond the log.
3. **Draft** â€” Output **ready-to-paste YAML blocks** with `status: pending` for operator/companion review.
4. **Close the loop** â€” Optionally suggest **one** `suggested_followup` the Voice or parent can try in real life after merges.
5. **Merge** â€” Companion **approve** in gate â†’ operator runs `python3 scripts/process_approved_candidates.py -u grace-mar --quick CANDIDATE-XXXX --approved-by companion`. **Agent does not merge** without approval.

**Cadence hint for Step 1:** If helpful, mention "last survey wave" from recent **Processed** blocks or session memory.


