# Dev journal â€” work-dev learning log

**Parent:** [Work notebook (multi-lane)](../../README.md) â†’ **work-dev** lane â€” this subfolder is the **day-scale journal**; other lanes hold prompts/specs by territory. **Lane index (map + history):** [../README.md](../README.md).

**Discoverability:** The same tree is linked from **`dev-journal`** (repo-relative symlink) for agents and tools that prioritize the companion tree. **LIB:** [dev journal (`docs/skill-work/work-dev/dev-notebook/work-dev/journal/`)](../../../../../../self-library.md#operator-analytical-books) in [`self-library.md`](../../../../../../self-library.md) (Operator analytical books).

**Book:** Short daily notes on **learning and building** the **work-dev** lane in grace-mar: OpenClaw / exportâ€“stageâ€“merge discipline, harness and cadence wiring, integration scripts, capability contracts, portable skills, OB1 â†” companion-self bridge thinking, and adjacent operator infrastructure â€” **without** treating WORK drafts as Record truth.

**Territory:** `docs/skill-work/work-dev/dev-notebook/work-dev/journal/` in grace-mar â€” **WORK / operator trajectory**, not the companion **Record**, not Voice knowledge, not a substitute for [work-dev-history.md](../../../work-dev-history.md) (append-only milestone log) or [workspace.md](../../../workspace.md) (canonical entrypoint).

### Routing: dev-journal vs cici-notebook

**One line:** **dev-journal** (this folder) = **inward-facing** â€” Grace-Marâ€™s own work-dev lane (tooling, integration, scripts in *this* repo). **cici-notebook** = **outward-facing** â€” Xavierâ€™s OB1 / Cici stack and your coaching or tracking of it from inside grace-mar. See [cici-notebook README](../../../../../../README.md#routing-dev-journal-vs-cici-notebook).

**Center of gravity belongs here** when you are building or reflecting on grace-mar **internal** work-dev: OpenClaw, exportâ€“stageâ€“merge discipline, harness/cadence wiring, integration scripts, capability contracts, portable skills, bridge thinking between OB1 and companion-self, and adjacent operator infrastructure.

**Write in [cici-notebook](../../../../../../README.md)** when the center of gravity is **Xavierâ€™s** instance (Cici), upstream OB1, BrewMind tie-ins, same-day commits from Xavierâ€™s repo, or what Xavierâ€™s OB1 trajectory means operationally â€” including digest-driven day files from `scripts/cici_journal_ob1_digest.py`.

**Quick test**

- â€œIn **Grace-Mar**, I changed / learned / wired â€¦â€ â†’ **dev-journal** (this folder).
- â€œIn **Xavierâ€™s** OB1/Cici world, I observed / coached / compared â€¦â€ â†’ **cici-notebook**.

**When a day touches both:** split â€” grace-mar implementation and tooling reflection **here**; Xavier/OB1 observation or coaching **there**.

**How to use**

- One file per **calendar day you choose to capture**: `YYYY-MM-DD-day-NN.md` (**NN** = journal day number from your chosen **anchor** â€” e.g. first entry = Day 1; skip days you do not journal).
- Keep entries **short** (about 10â€“20 lines): focus, actions, wins, blockers, one line for tomorrow.
- **No secrets** (API keys, raw Supabase URLs with keys, MCP secrets, private tokens). Reference env vars, script names, and doc paths only.

### Daily inbox (rolling accumulator)

**File:** [daily-dev-journal-inbox.md](daily-dev-journal-inbox.md) â€” **append-only** during the local day for rough work-dev capture. **`dream`** is the usual time to **fold** into the canonical **`YYYY-MM-DD-day-NN.md`** for that calendar window (create or extend the day file; **NN** follows your journal-day anchor). **No automatic reset** each dream â€” same **fold + optional prune** pattern as [strategy-notebook daily-strategy-inbox](../../../../../../codex/daily-strategy-inbox.md). **Missed `dream`:** resolve stale inbox before appending on a new day (merge into the correct `*-day-NN.md`).

**Relation to other surfaces**

| Surface | Role |
|---------|------|
| **This journal** | Reflective **day-scale** narrative â€” what you understood, tried, or struggled with. |
| [work-dev-history.md](../../../work-dev-history.md) | **Milestone / artifact** log (commits, scripts shipped, gaps closed). |
| [workspace.md](../../../workspace.md) | **Current** blockers and next actions. |

**Contrast:** [cici-notebook](../../../../../../README.md) vs this journal â€” full routing rules under [Routing](#routing-dev-journal-vs-cici-notebook) above.

**vs [work-dev-history.md](../../../work-dev-history.md):** History = **milestones** (SHA, artifact, gap closed). Journal = **narrative** when useful â€” avoid copying every history bullet; link the date or commit and add friction / â€œwhat clickedâ€ only the history line cannot carry.

### Conductor in dev journal

**When** you run [`.cursor/skills/conductor/SKILL.md`](../../../../../../.cursor/skills/conductor/SKILL.md) (or **`conductor`**) on **work-dev** **objects** (harness, export, `workspace` wedge, derived regen), **land** a **durable** pass in this folder:

- Add **`### Conductor close`** to the **day file** you are closing (`YYYY-MM-DD-day-NN.md`) using the same bullet **shape** as [CONDUCTOR-CLOSE-TEMPLATE.md](../../../../../../codex/CONDUCTOR-CLOSE-TEMPLATE.md) (**Stance / conductor**, **Object**, **What moved / seam**, **Falsify / next test**, **Escalation**). Strategy **chapters/â€¦/days.md** is **not** the home for this lane â€” **this** **journal** (or a **spec** under [dev-notebook/work-dev/](../)) is.
- **Optional** cadence only: `coffee_conductor_outcome` with `notebook_ref=` â†’ path to this file â€” [CONDUCTOR-IMPROVEMENT-LOOP.md](../../../../../../codex/CONDUCTOR-IMPROVEMENT-LOOP.md) Â§ 3.

**Kleiber** **action** **MCQ** options may **point** at [workspace.md](../../../workspace.md) and concrete paths under `dev-notebook/work-dev/`.

### Optional habit telemetry

Light **follow-through** discipline (tomorrow line, blocker carryover, friction resolution) without turning this into a dashboard: [journal-metrics-habit.md](../../../../journal-metrics-habit.md). **Phase 0** = weekly 5â€‘minute check; **Phase 1** = optional YAML frontmatter. Rhythm snapshot (filename dates): `python3 scripts/journal_habit_snapshot.py`.
