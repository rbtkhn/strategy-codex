# Operator dashboards — when to use (agent nudge card)

**Audience:** Operator + assistant after **`coffee`** Step 1 or any substantive WORK turn.

**Authority:** Derived / advisory only. These **do not replace** `coffee`, `harness_warmup`, or `operator_handoff_check` chat paste.

**Full alignment:** [operator-dashboard-consolidation-phase0.md](skill-work/work-dev/operator-dashboard-consolidation-phase0.md)

---

## The three aggregators (Phases 1–3)

| Dashboard | Question | Rebuild command |
|-----------|----------|-----------------|
| **Command Deck** | What should I do next? | `python3 scripts/operator_command_deck.py --max-next-actions 5` |
| **Statecraft War Room** | Which crisis objects are live? | `python3 scripts/statecraft_war_room.py --latest-days 7 --max-objects 12` |
| **Repo Surgeon** | What is structurally broken? | `python3 scripts/repo_surgeon.py --scope docs` (add `--run-existing-checks` for deep triage) |

Outputs: `runtime/artifacts/<bucket>/latest.md` + `latest.json` (gitignored; regenerate locally).

---

## Agent rule — suggest, do not dump

After **`coffee`** Step 1 (or when the operator looks lost mid-session), the assistant **must** emit a short **Dashboard nudge** block:

1. **Name at most two** dashboards worth running **now** (usually Command Deck + one drill-down).
2. Each line: **which tool** + **one because clause** + **optional run command**.
3. **Do not** paste full `latest.md` bodies unless the operator asks.
4. **Offer to run** the command same turn when they pick a hub letter or say `run deck` / `run war room` / `run surgeon`.

**Default on every work-start `coffee`:** suggest **Command Deck** — it ranks next actions from surgeon + war room + git + budget signals.

---

## When to suggest each

### Command Deck (default companion to coffee)

Suggest when **any** of:

- Work-start or reorientation **`coffee`**
- Operator asks "what next?" / "what should I focus on?"
- Dirty git tree + multiple lanes in play
- End of session (after closeout) — regenerate for tomorrow's file

Skip when: operator said **`no menu`** and only wanted a single factual answer.

### Statecraft War Room

Suggest when **any** of:

- Hub pick **C — Deepen** with statecraft / intake / daily / Iran / lane work
- Uncommitted **`statecraft/`** or **`source-archive/statecraft/`** slices in handoff
- Intake backlog, daily synthesis, or "promote capture" language
- Operator names Mercouris, Davis, streams, transaction router, crisis object

Command: `python3 scripts/statecraft_war_room.py --latest-days 7 --max-objects 12`

### Repo Surgeon

Suggest when **any** of:

- Hub pick **B — Test** with ship / docs / link / hygiene intent
- Integrity warnings in warmup, or **`docs/`** / **`work-dev/`** commit planned
- Broken links, path adoption, skill drift, local path leaks mentioned
- Before a large docs DOCSYNC or registry cleanup

Fast: `python3 scripts/repo_surgeon.py --scope docs --no-existing-checks`  
Deep: `python3 scripts/repo_surgeon.py --scope docs --run-existing-checks`

### Command Deck flag `--full-surgeon`

Suggest when Surgeon **blocking** findings are likely and operator is doing maintenance, not statecraft reading.

---

## Coffee hub → dashboard map

| Hub | Often pair with |
|-----|-----------------|
| **A — Confirm** | Command Deck (posture + ranked actions) |
| **B — Test** | Repo Surgeon (then Deck to re-rank) |
| **C — Deepen** | War Room (then Deck if intake queue is long) |
| **D — Reframe** | Command Deck top action + War Room object list |

---

## Operator phrases (agent should recognize)

| Operator says | Agent does |
|---------------|------------|
| `run deck` / `command deck` | Run `operator_command_deck.py`; summarize top 3 actions |
| `run war room` | Run `statecraft_war_room.py`; summarize sync + top objects |
| `run surgeon` | Run `repo_surgeon.py` with appropriate scope; summarize status + fix order |
| `dashboards` | Nudge all three with when-to-use one-liners; run Deck first unless they pick |

---

## What not to do

- Do not replace **`coffee`** Step 1 with dashboard runs (different medium).
- Do not auto-run all three every session (Windows harness cost; operator fatigue).
- Do not treat dashboard output as Record or gate merge authority.
- Do not suggest **`--include-gate`** unless operator invoked fork revive / gate review.
