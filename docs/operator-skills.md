# Operator skills

Project-local workflow skills for Grace-Mar operator routines.

These skills package recurring "morning coffee" and territory pulse workflows into reusable commands for Cursor agents. They do not change the gated merge rule, and they do not create new memory lanes. They are read-only workflow surfaces over canonical repo state.

For multi-turn Codex campaign work with explicit objectives, plans, completion, and blocked states, see [goal-mode-playbook.md](goal-mode-playbook.md).

**Gate alias:** `knowledge-gate` and `recursion-gate` mean the same human approval membrane. The canonical file path remains `recursion-gate.md`.

## Contextual stewardship

- **Agents have no cross-thread institutional memory.** Authority for the Record stays **on-disk files** + **gated pipeline** (`AGENTS.md`, RECURSION-GATE, companion-approved merges) ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â not chat summaries or model recall.
 - **Skills are weather reports, not policy.** They surface state; they do not replace reading `recursion-gate.md` / `self-evidence.md` when decisions are on the line. In operator speech, `knowledge-gate` is accepted as a synonym for `recursion-gate`.
- **Encoded judgment** = gate workflow + receipts + CI/tests you run before ship ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â not prompt length alone.

---

## Preferred activation (operator chat)

Each `.cursor/skills/*/SKILL.md` declares YAML **`preferred_activation`** (one or two words). Say the **exact phrase** in chat, including multi-word phrases with spaces, or use **`use <skill-name>`** to steer the agent. Aliases in the skill body still work.

| Skill | Say this | Note |
|------|----------|------|
| `coffee` | **coffee** | Canonical cadence skill; **signing-off** intent = handoff-weighted Step 1, same **A-D** Coffee Hub Menu (**A** Steward, **B** Engineer, **C** Statecraft, **D** Singularity). Coffee **C** now opens four civilizational-state lanes: America, China, Persia, Russia. Conductor is standalone via **`conductor`** / master name, not a coffee hub letter. Legacy **hey** still works. |
| `conductor` | **conductor** | **work-devÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“associated** execution recursion (pick ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ disk ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ falsify ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ log); **Symphony** names in [CONDUCTOR-PASS](skill-work/work-coffee/CONDUCTOR-PASS.md) + [coffee ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§ Conductor session](../.cursor/skills/coffee/SKILL.md#conductor-only-no-coffee). [workspace](skill-work/work-dev/workspace.md) can ground **Kleiber** action MCQ when the pass is **ship** / **harness**. See `.cursor/skills/conductor/SKILL.md`. |
| `thanks` | **thanks** | **Deprecated** for new workflow ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â prefer **`conductor`** or **`coffee` light/minimal`. Legacy: park line + `log_cadence_event.py --kind thanks`. See `.cursor/skills/thanks/SKILL.md`. |
| `handoff-check` | **handoff check** | |
| `gate-review-pass` | **gate review** | |
| `weekly-brief-run` | **weekly brief** | |
| **`strategy` (doc-first)** | **strategy** | Alt: **strategy pass**, **work-strategy**. **No skill file** — [DEFAULT-PATH.md](skill-work/work-strategy/DEFAULT-PATH.md) + [strategy-codex-pass.mdc](../.cursor/rules/strategy-codex-pass.mdc). Dissolved: [SKILL-STRATEGY-DEPRECATED.md](skill-work/work-strategy/SKILL-STRATEGY-DEPRECATED.md). |
| `tri-mind` | **tri-mind** | **Deprecated (2026-06).** Do not use in new workflow. Prefer **`periodic-statecraft-review`** runbook, **`state-synthesis`**, or a **named single mind**. Legacy: [tri-mind SKILL.md](../.cursor/skills/tri-mind/SKILL.md) · [TRI-MIND-DEPRECATED.md](skill-work/work-strategy/TRI-MIND-DEPRECATED.md). |
| `politics-massie` | **massie x** | Portable core: `skills/politics-massie/` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ run `sync_portable_skills.py` after edits. |
| `work-jiang-feature-checklist` | **jiang check** | |
| `portable-skills-sync` | **sync skills** | Portable core: `skills/portable-skills-sync/`. |
| `extract-skill-from-session` | **save skill** | Alt: **skill from session**. |
| `pros-and-cons` | **unpack** | **Archived.** Use [operator-style.mdc](../.cursor/rules/operator-style.mdc) Think-lane unpack; legacy stub only. |
| `fact-check` | **fact check** | Alt: **verify this**, **check this claim**. |
| `pol-dashboard` (doc/runbook) | **pol dash** | No `SKILL.md`; miniapp + [pol-dashboard.md](pol-dashboard.md). |

---

## Included skills

| Skill | Purpose | Default command |
|------|---------|-----------------|
| `coffee` | **Step 1** work-start warmup + harness + branch snapshot + lane context; **Step 2** fixed **A-D** Coffee Hub Menu: **A** Steward, **B** Engineer, **C** Statecraft, **D** Singularity. Coffee **C** routes first to the civilizational-state lanes America, China, Persia, and Russia; treaty, policy, negotiation, and Richelieu/Bismarck drafting move downstream into those lanes. Conductor is standalone via `conductor` / master name and may route to the four-movement Conductor Action Menu after master selection. | **`operator_coffee.py`** (modes) + agent steps |
| `conductor` | **Conductor** - work-dev execution spine + Symphony pointers: `build_conductor_mcq_for_user`, orientation + **`coffee_pick`**, four-movement Conductor Action Menu, optional [CONDUCTOR-IMPROVEMENT-LOOP](../codex/CONDUCTOR-IMPROVEMENT-LOOP.md) close. Bare master slugs (**toscanini / furtwangler / karajan / kleiber / bernstein**) are first-turn activations. | Agent: `.cursor/skills/conductor/SKILL.md` + `log_cadence_event.py` when logging |
| `thanks` | **Deprecated** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â use **conductor** or **`coffee` light/minimal** for mid-day beats. Legacy micro-pause: optional **park** + **`thanks`** line in [work-cadence-events.md](skill-work/work-cadence/work-cadence-events.md) | Same command if explicitly invoked (agent: `.cursor/skills/thanks/SKILL.md`) |
| `weekly-brief-run` | Weekly brief readiness pass plus scaffold generation for `work-politics` | `python3 scripts/operator_weekly_brief_run.py -u grace-mar` |
| `gate-review-pass` | Recommendation-oriented review pass over pending `RECURSION-GATE` candidates | `python3 scripts/operator_gate_review_pass.py -u grace-mar` |
| `handoff-check` | Stop/resume summary with **RECURSION-GATE** (frozen unless fork revive), **Predictive History night closeout** (work-jiang), recent commits, local work, runtime noise, and a re-entry prompt | `python3 scripts/operator_handoff_check.py -u strategy-codex`; cold paste stack: `python3 scripts/operator_reentry_stack.py -u strategy-codex` (`--compact` optional); one-liner: `python3 scripts/harness_warmup.py -u strategy-codex --receipt` |
| `pros-and-cons` | **Archived.** Think-lane **unpack** when a proposal is unclear: restate, pros, cons, disproportion, recommendation — follow [operator-style.mdc](../.cursor/rules/operator-style.mdc) | Agent: operator-style unpack (legacy stub archived) |
| `fact-check` | **Triage-first** check on pasted/named claims: **lean** verdict table, **one cite** per claim when enough, **high abstention** + **Escalate** when stakes need deeper audit; **not** Record merge unless gated pipeline | Agent: follow `.cursor/skills/fact-check/SKILL.md` |
| **`strategy` (doc-first)** | **Strategy / codex pass** — [DEFAULT-PATH.md](skill-work/work-strategy/DEFAULT-PATH.md); promote to [STRATEGY.md](skill-work/work-strategy/STRATEGY.md) when stable; **not** work-politics pulse | Agent: [strategy-codex-pass.mdc](../.cursor/rules/strategy-codex-pass.mdc) + DEFAULT-PATH |
| `tri-mind` | **Deprecated (2026-06).** Legacy tri-lens A/B/C pass — use **`periodic-statecraft-review`** runbook, **`state-synthesis`**, or a **named single mind**. [TRI-MIND-DEPRECATED.md](skill-work/work-strategy/TRI-MIND-DEPRECATED.md) · legacy [tri-mind/SKILL.md](../.cursor/skills/tri-mind/SKILL.md) | Agent (legacy only): `.cursor/skills/tri-mind/SKILL.md` |
| `work-jiang-feature-checklist` | Branch hygiene, scope, canonical verify block, and commit granularity for `codex/predictive-history` + `scripts/work_jiang/` | Agent: follow `.cursor/skills/work-jiang-feature-checklist/SKILL.md` |
| `politics-massie` | Real-time news search + suggested @usa_first_ky X drafts (human approves; no auto-post) | Agent: follow `.cursor/skills/politics-massie/SKILL.md` |
| `portable-skills-sync` | Regenerate Cursor `SKILL.md` from `skills/` + `manifest.yaml` + `CURSOR_APPENDIX.md`; run `--verify` before commit | `python3 scripts/sync_portable_skills.py --verify` then sync; agent: `.cursor/skills/portable-skills-sync/SKILL.md` |
| `extract-skill-from-session` | Codify a finished multi-step workflow as a new `SKILL.md` | Agent: `.cursor/skills/extract-skill-from-session/SKILL.md` |
| `pol-dashboard` | Internal miniapp UI at `/pol` (legacy `/wap`) ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â work-politics job tracker (token: `POL_DASHBOARD_TOKEN` or legacy `WAP_DASHBOARD_TOKEN`) | [pol-dashboard.md](pol-dashboard.md) |

**Stale derived exports** (manifest, PRP, fork-manifest, runtime bundle): audit under **coffee A ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â integrity/exports** (`validate-integrity.py`); **`refresh_derived_exports.py` writes** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ship per operator lane after proposal. Quick commands: [development-handoff.md ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§ Quick Resume](development-handoff.md#quick-resume-commands).

**Skill discovery:** Pointer backlog [skills/skill-candidates.md](../skills/skill-candidates.md), draft lane `skills/_drafts/`, ladder in [skills/README.md](../skills/README.md). After substantive **EXECUTE** / **DOCSYNC** ships, optional one-line prompt per [.cursor/rules/operator-style.mdc](../.cursor/rules/operator-style.mdc) (Skill discovery). **Skills / meta:** **coffee B ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Engineer** + say **skills** or **meta**; **handoff-check** summary may mention the same.

### Gate review ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â pattern notes (doc-only)

When **`gate review`** recommendations repeatedly mis-rank or duplicate-hint wrong, capture **one line** here or in [.cursor/skills/gate-review-pass/SKILL.md](../.cursor/skills/gate-review-pass/SKILL.md) ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§ *After a batch review*. No automation ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â this is institutional memory for the operator and agents.

---

## Suggested daily pattern

1. Start with `coffee` when opening a new work block or a new agent thread. Work-start `coffee` runs Step 1 (scripts, branch snapshot, lane context) and then the fixed A-D Coffee Hub Menu: **A Steward**, **B Engineer**, **C Statecraft**, **D Singularity**. Coffee **C** opens the civilizational-state lane chooser: America, China, Persia, or Russia. Conductor is standalone by `conductor` or master name, not a coffee hub letter. Use `coffee light` / `coffee minimal` for lighter repeat passes. Route commercial/write-shaped work by explicit `write`, `skill-write`, `work-business`, or named commercial request, not by Coffee D.
2. When the day includes campaign work, brief prep, or X/content operations, run `python3 scripts/operator_work_politics_pulse.py -u grace-mar` (territory pulse ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â no dedicated skill).
3. Use `politics-massie` when you want breaking-news hooks and draft tweets for the Massie shadow X account.
4. Use `weekly-brief-run` for the actual work-politics brief cycle after checking source freshness. If the cycle covers **high-stakes** topics (war powers, ethics/insider, cartel-economy legal claims, border + civil liberties), complete **weekly brief ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§8** / `docs/skill-work/work-politics/america-first-ky/` stress-test before treating drafts as final.
5. Use `gate-review-pass` when you want a queue review recommendation without taking action yet.
6. End the day with **`coffee`** + **signing-off** intent: **`handoff-check`** (or `operator_coffee.py --mode closeout`) is **Step 1**; agent then shows the **same** menu as work-start (**A ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Steward** alone = system pick). To resume mid-thread without the full `coffee` flow, use `handoff-check` alone per `../../../../../../.cursor/skills/handoff-check/SKILL.md`.

---

## Output contract

### `coffee`

**Legacy:** Cursor skill folder/id was `daily-warmup`, then `operator-cadence`. Update bookmarks to `.cursor/skills/coffee/`.

Must answer:

- What needs attention first?
- Are there pending gate items?
- Is work-politics blocked or stale?
- Is repo integrity healthy?
- Is the worktree noisy enough to affect the next move?
- **Coffee:** **Polymarket** + **volume** + **independent** horserace poll (or none) ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â **only** after **menu C ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Historian** (intel path) or explicit same-message request; same caveats and procedure as [polling-and-markets.md](skill-work/work-politics/polling-and-markets.md). Step 1 does **not** include this block.
- **Coffee:** After **Step 1**, show the fixed **A-D** hub with no micro-hints row: **A Steward**, **B Engineer**, **C Statecraft**, **D Singularity**. Coffee **C** then opens the civilizational-state lanes America, China, Persia, and Russia before any instrument drafting. **D Singularity** opens the WORK-only singularity-academy route for agency under acceleration, agent control planes, alignment/substrate/displacement tests, and reusable artifacts. Conductor remains standalone by `conductor` or master name. Commercial, prose, offer, and `skill-write` work route by explicit request outside the Coffee D default.
- **Signing-off `coffee`:** After **Step 1** (`operator_handoff_check.py` + paragraph), **same** fixed menu as work-start; **A ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Steward** without gate/template split ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ **system pick**. See [menu-reference ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â signing-off intent](skill-work/work-coffee/menu-reference.md#signing-off-intent).

### `weekly-brief-run`

Must answer:

- Are the weekly brief sources fresh enough?
- What must be refreshed first?
- Was a scaffold emitted or intentionally withheld?
- What human review is still required before use?
- If the brief touches high-stakes areas (see `weekly-brief-template.md` ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§8), has the operator been pointed at the factorial stress-test template and framework under `docs/skill-work/work-politics/america-first-ky/`?

### `gate-review-pass`

Must answer:

- What can likely be approved now?
- What looks stale?
- What likely duplicates existing Record content?
- What needs manual escalation instead of quick review?

### `pros-and-cons` (archived)

Must answer (via [operator-style.mdc](../.cursor/rules/operator-style.mdc), not the archived skill stub):

- What is the proposal **in one plain sentence** (and rough in/out scope)?
- What are the **pros** and **cons** as concrete bullets?
- **Which side is heavier** (disproportion) and why?
- What is the **recommendation** (do / defer / revise), without assuming approval to implement?

### `handoff-check`

Must answer:

- What is **pending in RECURSION-GATE** (work-politics vs companion), and what **proposed steps** does the script give to clear the queue (without merging in the skill)?
- What was recently committed?
- What meaningful local work is still in progress?
- What looks like runtime-only noise?
- What is the best first prompt for the next session?

### `work-jiang-feature-checklist`

Must answer:

- Is the working tree clean enough to review (unrelated untracks isolated)?
- Does scope stay in the Geo-Strategy lane unless the task says otherwise?
- Was the full verify block (or an explicitly justified subset) run before ship?
- Are commits or phases aligned to the plan (quotes / counter-readings / chronology / CI)?

---

## Parallel operator pass

When you want the same leverage pattern as the video workflow, run these in parallel:

```bash
python3 scripts/operator_daily_warmup.py -u grace-mar
python3 scripts/operator_work_politics_pulse.py -u grace-mar
```

Use the first output to choose the work block. Use the second to choose the work-politics action inside that block. There is **no** Cursor skill for the pulse script ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â invoke the script directly (or ask the agent to run it).

For a fuller operator pass:

```bash
python3 scripts/operator_daily_warmup.py -u grace-mar
python3 scripts/operator_work_politics_pulse.py -u grace-mar
python3 scripts/operator_gate_review_pass.py -u grace-mar
```

Use `weekly-brief-run` when the first two workflows say the territory is ready to produce a weekly scaffold.

---

## Guardrails

- These skills are read-only summaries over canonical files.
- `recursion-gate.md`, `self.md`, `self-evidence.md`, and work-politics docs remain the source of truth.
- work-politics remains a `WORK` surface; Record changes still require staged approval and merge flow.
- `weekly-brief-run` produces a first-pass scaffold, not final-use campaign output.
- `handoff-check` should treat runtime audit noise separately from meaningful worktree changes.
