# Cici notebook â€” Open Brain (OB1) learning log

**Book:** Daily notes on **learning and building** the **Open Brain** / **Cici** stack: **instance** ([`Cici`](https://github.com/Xavier-x01/Cici)), upstream ([NateBJones-Projects/OB1](https://github.com/NateBJones-Projects/OB1)), and how that ties to **BrewMind** work.

**Discoverability:** The same tree is linked from **`SELF-LIBRARY/cici-notebook`** (repo-relative symlink) for agents and tools that prioritize the companion tree. **LIB:** [LIB-0154](../../../../self-library.md#operator-analytical-books) in [`self-library.md`](../../../../self-library.md) (Operator analytical books).

**Territory:** `docs/skill-work/work-cici/cici-notebook/` in grace-mar â€” **WORK / operator coaching**, not Ciciâ€™s **Record** in grace-mar, not companion Voice knowledge.

**Cursor skill:** [`.cursor/skills/skill-cici/SKILL.md`](../../../../.cursor/skills/skill-cici/SKILL.md) â€” distilled journal rhythm (grace-mar **Mode A** vs Cici **Mode B**); hand off the skill folder to [Cici](https://github.com/Xavier-x01/Cici) for use in the **Cici** instance repo only.

### Routing: dev-journal vs cici-notebook

**One line:** **cici-notebook** = **outward-facing** â€” understanding, coaching, or tracking **Ciciâ€™s** OB1 path from inside grace-mar (instance, upstream, BrewMind, GitHub digest). **dev-journal** = **inward-facing** â€” building grace-marâ€™s **own** work-dev lane. See [dev-journal README (dev-notebook/work-dev/journal)](../../work-dev/dev-notebook/work-dev/journal/README.md#routing-dev-journal-vs-cici-notebook).

**Center of gravity belongs here** when the note is about **Ciciâ€™s** stack and your relationship to it as operator: Cici commits, OB1 direction, instance vs upstream comparison, `cici_journal_ob1_digest.py` day files, inbox coaching notes, same-day synthesis with strategy-notebook when thatâ€™s **about Ciciâ€™s trajectory**.

**Write in [dev-journal](../../work-dev/dev-notebook/work-dev/journal/README.md)** when the center of gravity is grace-mar **internal** tooling: exportâ€“stageâ€“merge in *this* repo, harness wiring, capability contracts, portable skills, OpenClaw integration work â€” reflective narrative about **this** codebaseâ€™s work-dev path.

**Quick test**

- â€œIn **Ciciâ€™s** OB1 world, I observed / coached / compared â€¦â€ â†’ **cici-notebook** (this folder).
- â€œIn **Grace-Mar**, I changed / learned / wired â€¦â€ â†’ **dev-journal**.

**When a day touches both:** split â€” Cici/OB1 observation or coaching **here**; grace-mar implementation reflection **there**.

**How to use**

- One file per calendar day you want to capture: **`YYYY-MM-DD.md`** (same date key as strategy-notebook daily pages). **Journal day** (ordinal â€œDay Nâ€ of this run) lives **inside** the file (`**Journal day:** N`), not in the filename.
- **L1 â€” Git:** The generator pulls **Cici** commits for that calendar day and writes **Day overview (auto from commits)** plus **OB1 repo activity (links to GitHub)**.
- **L2 â€” Operator context:** [`inbox/`](inbox/README.md) notes, optional **[strategy-notebook](../../work-strategy/strategy-notebook/)** same-day block (geopolitical synthesis), and optional **session-transcript** lines â€” merged under **Operator context (ingested)**. **Recommended** end-of-day capture: **`--full-day-synthesis`** (or `CICI_JOURNAL_FULL_DAY_SYNTHESIS=1`) so transcript + strategy work for that date land in the journal without hand-copying; add **`inbox/YYYY-MM-DD.md`** for anything still missing.
- **L3 â€” Artifacts:** Optional repo-relative paths via inbox frontmatter or `inbox/YYYY-MM-DD-artifacts.txt` â€” see [SYNTHESIS-SOURCES.md](SYNTHESIS-SOURCES.md).
- You may edit generated files afterward. **No secrets** (API keys, Supabase URLs with keys, MCP keys). Point to env vars and dashboards in prose only.

### Daily inbox (rolling accumulator)

**File:** [daily-cici-notebook-inbox.md](daily-cici-notebook-inbox.md) â€” **append-only** during the local day for rough OB1/Cici/coaching capture. **`dream`** is the usual time to **fold** that material into **`inbox/YYYY-MM-DD.md`** for the matching date (synthesize; merge with existing inbox body), then run [`cici_journal_ob1_digest.py`](../../../../scripts/cici_journal_ob1_digest.py) so L2 merges as today. **No automatic reset** each dream â€” same **fold + optional prune** pattern as [strategy-notebook daily-strategy-inbox](../../work-strategy/strategy-notebook/daily-strategy-inbox.md). Per-day [`inbox/`](inbox/README.md) files remain the digestâ€™s input; the rolling file is **not** read by the script â€” only by the fold step.

**Daily synthesis**

Canonical OB1 instance repo: **[github.com/Xavier-x01/Cici](https://github.com/Xavier-x01/Cici)** (`main`).

From repo root:

```bash
# Preview today (UTC calendar day); journal day number is inferred from existing entries (`**Journal day:**` or legacy *-day-NN.md)
python3 scripts/cici_journal_ob1_digest.py

# Local calendar day (example): Eastern time
TZ=America/New_York python3 scripts/cici_journal_ob1_digest.py

# Recommended: pull strategy-notebook + session-transcript for the same calendar day
TZ=America/New_York python3 scripts/cici_journal_ob1_digest.py --full-day-synthesis --write
# Or: export CICI_JOURNAL_FULL_DAY_SYNTHESIS=1

# Optional: inbox only, or transcript only, or strategy-notebook only â€” see SYNTHESIS-SOURCES.md
python3 scripts/cici_journal_ob1_digest.py --include-session-transcript --write

# Write the file (refuses to overwrite unless --force)
python3 scripts/cici_journal_ob1_digest.py --write

# Git-only output (ignore inbox)
python3 scripts/cici_journal_ob1_digest.py --no-inbox --write
```

Optional: set **`GITHUB_TOKEN`** (or `GH_TOKEN`) for higher API rate limits; public repo works without auth for light use.

Optional automation: same command on a **cron** or end-of-day **operator** ritualâ€”there is no server-side hook from GitHub into grace-mar by default.

**`dream` ritual:** End-of-day **`dream`** is the canonical time to **generate todayâ€™s** journal file if missing â€” run `cici_journal_ob1_digest.py --full-day-synthesis --write` (or `--write` alone for git-only) with your chosen `TZ` (see [.cursor/skills/dream/SKILL.md](../../../../.cursor/skills/dream/SKILL.md) Â§ *Cici notebook*). **`--full-day-synthesis`** folds **strategy-notebook** and **session-transcript** for that date into the page; use **`inbox/`** for anything not covered. This does not run inside `auto_dream.py`; the agent performs it when executing the full dream skill. If the day file already exists, the script refuses overwrite unless `--force`.

**Full source map:** [SYNTHESIS-SOURCES.md](SYNTHESIS-SOURCES.md) (layers, flags, recursive learning, Phase E backlog).

**Upstream:** Open Brain docs and recipes live in the OB1 ecosystem; this journal is **her** trajectory in grace-mar, not a fork of upstream text.

**vs [work-cici-history.md](../work-cici-history.md):** History = **append-only milestones** (what shipped, paths, same-day `###` blocks). Journal = **optional** day file when reflection helps â€” do **not** duplicate full milestone lists in the journal; one line â€œsee history 2026-04-08â€ is enough.

### Optional habit telemetry

Same **light follow-through** discipline as dev-journal (tomorrow line, blocker carryover, coaching vs raw digest): [journal-metrics-habit.md](../../journal-metrics-habit.md). **Phase 0** = weekly check; **Phase 1** = optional YAML. Snapshot: `python3 scripts/journal_habit_snapshot.py`.

