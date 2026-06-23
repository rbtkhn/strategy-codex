# Cursor Automations Ã¢â‚¬â€ grace-mar probe (WORK)

**Prompts SSOT (paste-ready):** [docs/automation/](../../automation/) Ã¢â‚¬â€ policy + per-use-case prompts. **Automation governance (R0Ã¢â‚¬â€œR5, max authority by surface):** [automation-readiness-policy.md](../../automation/automation-readiness-policy.md) and the repo-native table in [automation-readiness-ledger.md](../../automation/automation-readiness-ledger.md) Ã¢â‚¬â€ use them before enabling new automations; see [automation-classification-template.md](../../automation/automation-classification-template.md) for proposals. This file is an earlier **friction/CI** survey; new work should not duplicate the contract text.

**Status:** Evidence pass from repo + skills; **not** Record. **Purpose:** Map this instanceÃ¢â‚¬â„¢s cadence, scripts, and CI to [Cursor Automations](https://cursor.com/docs/cloud-agent/automations) triggers and tools, with red lines from [AGENTS.md](../../../AGENTS.md) and [instance-doctrine.md](../../../instance-doctrine.md).

**Operator validation:** The **top 5 frictions** below are **proposed** from structure; adjust after a 15Ã¢â‚¬â€œ20 min pass.

---

## 1. Workflow inventory (beats Ã¢â€ â€™ artifacts Ã¢â€ â€™ commands)

| Beat / habit | On-disk artifacts | Primary commands / skills | Typical frequency | Human decision point |
|--------------|---------------------|----------------------------|-------------------|----------------------|
| **coffee** (work-start) | `work-cadence-events.md` (append **`coffee`**), `pipeline-events.jsonl` (optional) | `python3 scripts/operator_coffee.py -u grace-mar` (modes: `light`, `minimal`, `reentry`, `closeout`); [coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md) Step 0-2 | Many per day | **Hub A-D**; Conductor is standalone name-only |
| **coffee** (signing-off) | same + handoff output | `operator_coffee.py --mode closeout` or `operator_handoff_check.py` | 0Ã¢â‚¬â€œ1 per day | same menu; seal vs continue |
| **Conductor** (standalone) | `coffee_pick` line (`picked=conductor` `conductor=<slug>`; legacy `picked=D`) | `cadence_conductor_resolution.resolve_d_conductor`, `log_cadence_event.py`; [conductor/SKILL.md](../../../.cursor/skills/conductor/SKILL.md) | As needed | Name-only conductor routing + **Conductor Action Menu**; disk close |
| **dream** | `last-dream.json`, `work-cadence-events.md` (**`dream`**), `memory.md` touches, integrity/governance block | `scripts/auto_dream.py` (per [dream/SKILL.md](../../../.cursor/skills/dream/SKILL.md)) | Usually once per day | What to fix vs defer; no merge from dream |
| **bridge** | git state, Ã¢â‚¬Å“transfer promptÃ¢â‚¬Â in chat; optional cadence line | [bridge/SKILL.md](../../../.cursor/skills/bridge/SKILL.md) | Per session end | commit/push scope, what ships to next thread |
| **thanks** | one **`thanks`** line via `log_cadence_event.py` | [thanks/SKILL.md](../../../.cursor/skills/thanks/SKILL.md) | **Deprecated** operator habit Ã¢â‚¬â€ prefer **conductor** | Legacy micro-pause if invoked |
| **handoff / re-entry** | `recursion-gate.md`, worktree, PH closeout block | `python3 scripts/operator_handoff_check.py -u grace-mar`; `operator_reentry_stack.py` for cold start | On pause or resume | Gate triage, re-entry prompt wording |
| **Steward / gate (manual)** | `recursion-gate.md` | `operator_gate_review_pass.py` Ã¢â€ â€™ **human approve** Ã¢â€ â€™ `process_approved_candidates.py --apply` (never autonomous) | Weekly / on approve | **Companion approval** for every merge |
| **integrity / derived** | `manifest.json`, `grace-mar-llm.txt`, `fork-manifest.json`, runtime bundle, etc. | `validate-integrity.py`, `regen_grace_mar_derived.sh` (see [work-cadence README](../../work-cadence/README.md)) | After Record/prompt commits | regen batch vs single export |
| **work-strategy** (default lane) | `strategy-notebook/**`, inbox, `days.md` | skill-strategy, manual compose | Daily / session | Judgment, verify tier, promote |
| **work-jiang** | `codex/predictive-history/**`, registries | `scripts/validate_predictive_history_boundary.py` and boundary docs | On explicit boundary work only | validate freeze contract |

**Script safety (for automation design):**

| Class | Examples | Unattended cloud agent? |
|-------|----------|-------------------------|
| **Read-only / report** | `operator_handoff_check.py`, `validate-integrity.py`, `audit_cadence_rhythm.py`, `governance_checker.py` | **Yes** if prompt forbids writes to gate/Record |
| **Appends cadence / operator telemetry** | `log_cadence_event.py`, `operator_coffee.py` | **Risky** Ã¢â‚¬â€ changes repo meaning; only if you want a **bot** identity + explicit scope |
| **Record / gate merge** | `process_approved_candidates.py --apply` | **No** Ã¢â‚¬â€ human gate only ([AGENTS.md](../../../AGENTS.md)) |
| **Consolidation** | `auto_dream.py` | **No** for cloud replacement of ritual; **optional** as scheduled **read-only preflight** that only *reports* |

---

## 2. GitHub Actions (deterministic; do not duplicate with LLM)

| Workflow | Triggers (summary) | What it enforces | Automations *add* value whenÃ¢â‚¬Â¦ |
|----------|-------------------|------------------|--------------------------------|
| [test.yml](../../../.github/workflows/test.yml) | `push`/`PR` to `main` | pytest, package smoke, civ-mem / MEM suggester smokes, extended tests | You want a **narrative** Ã¢â‚¬Å“what failed and where to lookÃ¢â‚¬Â after **CI completed** Ã¢â‚¬â€ not a second test runner |
| [governance.yml](../../../.github/workflows/governance.yml) | `push`/`PR` | `governance_checker.py`, `validate-integrity.py`, template sync; PR **gated Record** message check | Comment that explains *why* a governance line failed in **operator** terms |
| [harness.yml](../../../.github/workflows/harness.yml) | `push`/`PR` | Counterfactual Pack (needs `OPENAI_API_KEY`) | Same Ã¢â‚¬â€ triage / owner routing only if harness flakes |
| [naming-check.yml](../../../.github/workflows/naming-check.yml) | `push`/`PR` | Deprecated naming, work-cici drift | Rarely needs LLM; deterministic is enough |
| [library-index.yml](../../../.github/workflows/library-index.yml) | `push`/`PR` | `build_library_index.py` must match artifact | Suggest Ã¢â‚¬Å“run this commandÃ¢â‚¬Â in a PR comment (could be static template) |
| [prp-refresh.yml](../../../.github/workflows/prp-refresh.yml) | `push` to `main` (paths: `self.md`, `archive/grace-mar-instance/bot/prompt.py`, Ã¢â‚¬Â¦) | Auto-commit `grace-mar-llm.txt` | **Do not** layer automations on top for same paths Ã¢â‚¬â€ already auto |
| [lane-pr-hint.yml](../../../.github/workflows/lane-pr-hint.yml) | PR opened/sync | Infers `lane/*` if missing, comments | [lane-scope.yml](../../../.github/workflows/lane-scope.yml) already enforces; LLM only if you want *richer* lane rationale |
| [lane-scope.yml](../../../.github/workflows/lane-scope.yml) | PR | `check_lane_scope.py` Ã¢â‚¬â€ blocks cross-lane drift | N/A (deterministic) |
| [work-jiang.yml](../../../.github/workflows/work-jiang.yml) | `push`/`PR` (paths) | Predictive History boundary validation | Triage only if the frozen-boundary guardrail fails |
| [newsletter.yml](../../../.github/workflows/newsletter.yml) | Monday schedule + `workflow_dispatch` | `generate_newsletter.py` + commit | You already have scheduled **Actions**; Cursor Automations would **duplicate** unless you want **LLM** rewrite of digest (separate product decision) |
| [pages.yml](../../../.github/workflows/pages.yml) / [deploy-profile.yml](../../../.github/workflows/deploy-profile.yml) | `push` / `workflow_dispatch` | Profile deploy to Pages | Post-deploy smoke narrative only if needed |

**Net:** CI owns **pass/fail**; Cursor Automations fit **post-fail triage**, **PR onboarding comments**, and **cadence/integrity summaries** that are *not* yet scripted.

---

## 3. Friction vs routine (Phase 2) Ã¢â‚¬â€ proposed top 5

**Routine** (repetitive checks): integrity after edits, regen drifts, PR lane + gated message, handoff/gate queue visibility.

**Contextual** (judgment, poor fit for naive automation): strategy-notebook compose, Conductor *substance*, pipeline approve, `dream` as closure ritual, bridge transfer prompt *voice*.

| # | Friction | Why it bites | Routine / contextual |
|---|----------|--------------|------------------------|
| 1 | **Stale derived + integrity red** after platform/profile/PRP-adjacent work | [work-cadence](../../work-cadence/README.md) calls out manifest/PRP/bundle drift; easy to forget `regen_grace_mar_derived.sh` | Routine check; human chooses when to regen |
| 2 | **PR cognitive load** (lane label, scope, gated `[gated-merge]`, many jobs) | Multiple workflows fire; [lane-pr-hint](../../../.github/workflows/lane-pr-hint.yml) helps label only | Mix Ã¢â‚¬â€ mechanics routine, *intent* contextual |
| 3 | **Gate queue** (`recursion-gate.md`) visibility between sessions | [instance-doctrine](../../../instance-doctrine.md) wants queue processed; [operator-weekly-review](../../../docs/operator-weekly-review.md) rhythm | Reminder = routine; **merge** = always human |
| 4 | **Cold re-entry** (what to run, whatÃ¢â‚¬â„¢s safe to ignore) | `operator_reentry_stack.py` / handoff exist but require **you** in Cursor or shell | Contextual; optional **scheduled nudge** is weak substitute for `coffee` |
| 5 | **work-jiang** / path-filtered CI failures | Boundary guardrail can fail when someone accidentally edits frozen PH residue; not everyoneÃ¢â‚¬â„¢s daily lane | Routine triage for that lane; specialist |

**You should reorder or drop** one slot if e.g. Slack or Sentry is your real pain (not visible from repo alone).

---

## 4. Friction Ã¢â€ â€™ Automations trigger (Phase 3)

| Friction | Candidate A | Candidate B |
|----------|-------------|-------------|
| **1 Integrity / derived** | **Scheduled** (e.g. weekly): clone or use repo in cloud agent, run `validate-integrity.py --json` + summarize failures + paste **exact** `regen` command from work-cadence README Ã¢â‚¬â€ **Slack** or **issue** only, no auto-commit | **Push to `main` webhook / CI completed** on branches that include `` or `archive/grace-mar-instance/bot/prompt.py`: **comment** on workflow run (if exposed) or open **draft** Ã¢â‚¬Å“integrity checklistÃ¢â‚¬Â **issue** Ã¢â‚¬â€ still no commit |
| **2 PR load** | **PR opened** / **synchronized**: after Actions, **comment** with *human-readable* map: which workflows ran, what `lane/*` is for, link to [lane-scope](../../../.github/workflows/lane-scope.yml) and gated-record hint Ã¢â‚¬â€ template-heavy, **LLM optional** | **CI completed** + failure: one comment with **failing job** + *first* file to look at (from log excerpt) Ã¢â‚¬â€ **judgment-light** triage |
| **3 Gate queue** | **Scheduled** (e.g. Monday): read-only `recursion-gate` **count** + list **CANDIDATE-** ids (cap at N) + Ã¢â‚¬Å“run `process_approved_candidates` only after approveÃ¢â‚¬Â **boilerplate** | **Not** `process_approved_candidates` in automation Ã¢â‚¬â€ violates doctrine |
| **4 Re-entry** | **Low fit** for full cloud replacement of `coffee` | If you insist: **scheduled** Ã¢â‚¬Å“integrity + handoff_check stdout summaryÃ¢â‚¬Â to **Slack** as *telemetry*, not a ritual substitute |
| **5 work-jiang** | **CI completed** (work-jiang workflow only): on failure, comment with the boundary-validator result and the first blocked path | **Push** in `codex/predictive-history/**`: optional reminder that PH edits belong in the external canonical repo Ã¢â‚¬â€ **high** governance value; **low** implementation complexity |

**Slack / Linear / Sentry / PagerDuty:** only wire if those integrations are in your *actual* stack; repo gives no signal they are required for grace-mar core.

---

## 5. Safe automation contract (Phase 4) Ã¢â‚¬â€ paste into automation prompt header

1. **No merge** into `self.md`, `self-archive.md`, `recursion-gate.md` (except moving to Processed *via human-approved* script you run), `archive/grace-mar-instance/bot/prompt.py`, or EVIDENCE from this automation. **No** running `process_approved_candidates.py --apply` unattended.
2. **No** staging gate candidates or approving **`CANDIDATE-`**. Suggest and link only.
3. **Open PR** / **comment**: propose diffs in comments or a **draft** branch you review; do not push **direct** Record edits.
4. **Memories** tool: **off** for untrusted/PR-sourced input; if on, **non-sensitive** ops only and short TTL policy.
5. **Deterministic checks** (pytest, `validate-integrity`, governance) stay in **GitHub Actions**; this agent only **interprets** or **explains** results unless you explicitly add a *new* script that Actions calls.
6. **Identity / billing:** choose **Private** vs **Team Owned** [per docs](https://cursor.com/docs/cloud-agent/automations#permissions) before enabling PR-creating automations; note **webhook** key rotation on scope promotion.
7. **Cadence:** do **not** present scheduled output as `coffee`, `dream`, or `bridge`; label as Ã¢â‚¬Å“integrity/cadence reportÃ¢â‚¬Â to avoid substituting human ritual.
8. If **MCP** enabled: only servers you trust; assume tools can read private repo paths.

---

## 6. Prioritized opportunities (Phase 5)

| Priority | Idea | Rationale |
|----------|------|-----------|
| **High** | **PR: CI-failure triage comment** (trigger: `CI completed` + failure) | Clear event, no gate risk, high leverage vs reading raw logs; complements deterministic jobs |
| **High** | **Scheduled: integrity summary** with regen *commands* (read-only scripts) | Directly addresses documented drift class; no merge |
| **Medium** | **PR opened: onboarding comment** (lane + gated record + Ã¢â‚¬Å“what ranÃ¢â‚¬Â) | Mostly **templatable**; use LLM only if you want natural language |
| **Medium** | **Monday: gate queue nudge** (count + id list + *non-merge* next steps) | Improves [pipeline health](../../../instance-doctrine.md) awareness; must stay read-only |
| **Low** | **Replace** `newsletter` or `dream` with cloud agent | **newsletter** already scheduled in Actions; **dream** is doctrine **Maintenance** mode Ã¢â‚¬â€ *do not* substitute |
| **Low** | **Cold re-entry** via daily cloud agent | Overlaps `operator_reentry_stack` and **coffee**; risk of Ã¢â‚¬Å“paperwork agentÃ¢â‚¬Â you ignore |

**Non-goals (per probe):** autonomous gate processing; automating `coffee` / `dream` / `bridge` as the **same** ritual; second copy of `pytest` in the cloud.

---

## 7. Next step (operator)

1. Re-rank the **top 5 frictions** (Ã‚Â§3) to match your *felt* week.
2. Pick **one** **High** item, add it at [cursor.com/automations](https://cursor.com/automations), and paste **Ã‚Â§5 Safe automation contract** at the top of the prompt.
3. If you use **Slack** for nudges, add **Send to Slack** with read scope only as needed; otherwise **comment on PR** is enough for GitHub-centric workflow.

`python3 scripts/validate_skills.py` unchanged by this doc; it is not a registered skill.

