# Cadence (continuity/cadence)

**Purpose:** Template-level doctrine, boundaries, and architecture for the daily cadence triad â€” `coffee` (orientation), `dream` (consolidation), and `bridge` (session handoff) â€” plus **`conductor`** (mid-day emphasis / Symphony or execution recursion; not a `coffee` hub letter) and **`harvest`** as **operator tools on other axes** (harvest: cross-agent extraction; on demand, not a fourth clock). **`thanks`** remains in the repo as a **deprecated** operator beat (legacy telemetry only) â€” see `.cursor/skills/thanks/SKILL.md`. Executable triggers: `.cursor/skills/coffee/SKILL.md`, `.cursor/skills/dream/SKILL.md`, `.cursor/skills/bridge/SKILL.md`, `.cursor/skills/harvest/SKILL.md`, and `.cursor/skills/thanks/SKILL.md` (legacy).

**Record boundary:** **Cadence events** (`cadence-events.md`), **which rituals you run**, and **command preferences** are **WORK** â€” in **`continuity/`** (this territory, [coffee/](../coffee/), related skills) and repo scripts (scripts, `log_cadence_event.py`, `operator_coffee.py`, harness/reentry wiring). They are **not** SELF **museum knowledge section C personality**; do not mirror cadence telemetry into the Record except via an explicit gated edit (e.g. removing a misplaced museum knowledge section C line).

**Not** Record truth. **Not** a merge path. **Not** identity-relevant unless gated.

**Cadence â†” governance:** [cadence-governance-bridge.md](cadence-governance-bridge.md), [cadence-pressure-signals.md](cadence-pressure-signals.md) â€” pressure JSON via `scripts/audit_cadence_rhythm.py --pressure-report`.

---

## Role

| Role | Description |
|------|-------------|
| **Cadence architecture** | Defines the shape of daily rhythm: coffee (orientation, repeated), conductor (mid-day depth; optional), dream (consolidation, once), bridge (session carry-forward), harvest (cross-agent packet; midstream import). **`thanks`** deprecated as primary beat. |
| **Night-to-morning handoff** | Documents the `runtime/daily-handoff/night-handoff.json` data contract that bridges dream output to coffee Step 1. |
| **Cadence event audit** | Append-only telemetry via `cadence-events.md` and `scripts/log_cadence_event.py` (optional **`harvest`** kind for consistency). |
| **Boundary surface** | Explains what belongs in operational/ephemeral surfaces versus what must escalate to the gate. |
| **Script topology** | Maps how consolidated runners delegate to underlying brief generators. |

---

## When integrity reports stale derived exports

Commits that change profile surfaces, `archive/grace-mar-instance/bot/prompt.py`, or related inputs can leave **derived** files older than sources: `manifest.json`, `llms.txt`, `intent_snapshot.json`, `fork-manifest.json`, repo-root `self-llm.txt`, and `runtime/bundle/bundle.json`. `validate-integrity.py` and `auto_dream.py` then report **integrity** failure until exports are refreshed.

**Recovery (root platform/profile),** from repo root:

```bash
bash scripts/regen_grace_mar_derived.sh
python3 scripts/validate-integrity.py --json
```

The script runs, in order: `export.py manifest`, `fork_checksum.py --manifest`, `export.py prp` (writes `self-llm.txt`), `export.py bundle`. See [`scripts/refresh_derived_exports.py`](../../../scripts/refresh_derived_exports.py).

---

## Reading the audit file (demo vs root platform/profile)

[`cadence-events.md`](cadence-events.md) is **append-all**: lines may include **`(demo)`** (fixtures, harness, or CLI defaults) alongside **root-profile** operator cadence.

- **Scripts** that compute session load, rhythm, or coffee rollup **filter by profile id** â€” see [`scripts/audit_cadence_rhythm.py`](../../../scripts/audit_cadence_rhythm.py) `parse_events`. Lines with **`dream (demo)`** do **not** affect root-profile metrics.
- **Manual review** of the raw file: restrict to the active profile lines so harness noise is not mistaken for companion dream failures.
- **`demo`** rows are not the companionâ€™s cadence.

---

## Daily rhythm

`coffee`, `dream`, and `bridge` form the cadence triad:

| Time | Ritual | What it does |
|------|--------|-------------|
| **Morning** | `coffee` (standard) | Read dream handoff, context snapshot, skill focus, session options |
| **During day** | `coffee` (reorientation) | Re-sip as needed â€” many per day is normal |
| **End of day** | `dream` | Capture signal, set carry-forward, write handoff JSON |
| **Session close** | `bridge` | Seal (commit/push), synthesize transfer prompt for next session |

**Many coffees, one dream, one bridge.** `coffee` is for repetition. `dream` is for closure. `bridge` is for carry-forward.

`coffee` should feel like a sip. `dream` should feel like sleep. `bridge` should feel like sealing an envelope.

### Mounted core vs specialist skills

For day-to-day Codex use, keep the host-mounted cadence spine small and legible.

- **Always-mounted core:** `coffee`, `conductor`, `dream`, and `bridge`
- **Live lane/support set:** `harvest`, `memory`, `statecraft-source-intake`, `state-synthesis`, `primary-overhearing-analysis`; periodic review via **`periodic-statecraft-review`** runbook (`last30days` / `monthly-deepening` / `statecraft-multi-lens` retired)
- **Repo-local specialists:** everything else unless repeated real use proves it belongs in the mounted default

The rule is simple: mount the skills that shape rhythm or are repeatedly needed inside live operator flow; leave narrower academy, watchlist, PH, or one-off support skills repo-local until they prove they deserve host-visible default status.

---

## Cadence choreography

**Choreography** means *who runs when*, *what each beat hands to the next*, and *how the operator stays oriented* without collapsing distinct jobs into one overweight ritual. It is not a moral schedule - it is a **failure-mode map**: each ritual answers a different kind of slip (framing decay, day residue, session continuity loss, mid-day emphasis/pause, cross-agent handoff).

### Named ritual activation discipline

When the operator explicitly invokes a named cadence ritual such as `coffee`, `dream`, `bridge`, `harvest`, or `conductor`, treat that trigger as a request to execute the ritual's skill contract, not as a vague request for a similar summary.

- Open the relevant skill and follow its executable contract first.
- Do not paraphrase the ritual from memory when the skill defines a stricter procedure.
- Only substitute a lighter or adjacent behavior when the operator explicitly asks for it or when the ritual contract itself says to pause.
- If execution must deviate because the contract is blocked, say what blocked it and which smaller truthful fallback you are using.

### The beats (roles, not personalities)

| Beat | Clock | Primary job | Typical frequency |
|------|--------|-------------|-------------------|
| **coffee** | Hours (framing) | Reorientation: grounding, priorities, menu of next forks | Many per day |
| **conductor** | Minutesâ€“hours | **Symphony / execution** emphasis: master pick, orientation, Conductor action MCQ, optional close; `coffee_pick` / `coffee_conductor_outcome` â€” see `conductor` SKILL + CONDUCTOR-PASS | As needed |
| **thanks** | â€” | **Deprecated operator workflow.** Legacy: two-block pause + `thanks` telemetry. Prefer **conductor** or **`coffee` light/minimal**. | Legacy only |
| **dream** | Day (residue) | Consolidation: memory normalize, integrity/governance, contradiction digest, night handoff | Usually once |
| **bridge** | Session (context) | Seal: commit/push where appropriate, transfer prompt for the **next** Cursor thread | Per session close |
| **harvest** | Cross-thread (import) | Ship dense substance **into** a session that is already running â€” not a clock | On demand |

**harvest** is **not** a fifth daily clock. It answers a different question: *how* to feed another agent or parallel session, not *when* to frame, settle, or seal.

### Order and pairing (common paths)

- **Morning after a dream:** `coffee` picks up `last-dream.json` / night-handoff context (see **Handoff contract** below). Dream already ran; coffee does not re-run dream.
- **Mid-day drift:** `coffee` again â€” a new sip, new Step 1 + menu. The cadence log shows the rhythm; it is normal to see several `coffee` lines in one day.
- **Stepping away briefly / mid-day shape:** **Conductor** pass or **`coffee` light/minimal** â€” **`thanks`** is deprecated as the default pause (legacy skill still documents the old two-block beat).
- **End of day, session continues:** `dream` alone â€” writes handoff artifacts; no commit/push requirement from dream itself.
- **End of day + closing Cursor:** `dream` then `bridge` â€” settle first, then seal and generate the transfer prompt.
- **Mid-day session end:** `bridge` alone â€” no obligation to run `dream` if the day is not closing.
- **End-of-day bundle:** `operator_end_of_day.py` chains dream-weight maintenance with handoff-check; if the operator is also **closing the session**, they still say **`bridge`** afterward for seal + transfer prompt.

Signing-off **`coffee`** (closeout mode) is a **lighter** alternative to `bridge` when the operator wants handoff-weighted text without full bridge mechanics â€” see [.cursor/skills/bridge/SKILL.md](../../../.cursor/skills/bridge/SKILL.md) for the full decision tree.

### Decision-fatigue reduction

[decision-fatigue-reduction.md](decision-fatigue-reduction.md) defines the cadence rule for recommended defaults, menu depth, and default acceptance. In short: menus route attention; once a route is known, recommend one next move when the evidence is strong enough. One real follow-up is enough if the business, lane, or cadence surface is quiet.

### Data flow between beats (what crosses the boundary)

1. **Dream â†’ morning coffee:** `runtime/daily-handoff/night-handoff.json` and, in root-profile style instances, `last-dream.json` â€” collapsed â€œLast dreamâ€ in warmup unless verbose flags are used.
2. **Bridge â†’ next thread:** Transfer prompt (packet contract) â€” ends with a lone **`coffee`** line for cold start when that contract applies.
3. **All beats â†’ audit trail:** [cadence-events.md](cadence-events.md) â€” one append-only line per successful leaf run (`scripts/log_cadence_event.py`). `coffee_close` receipts may add a second coffee line after a selected branch materially settles, recording outcome, readiness, artifacts, unresolved loops, and conductor state. This file is **operator ephemera**: rhythm telemetry, not Record.

### Step 0 recent rhythm (companion-facing)

Skills may ask the agent to **read** `cadence-events.md` **before** running scripts that **append** a new line at the end of the run, then **synthesize** recent events into the reply so the companion sees **recent rhythm** without opening the log.

**Companion-facing UX (new platform/users):** In chat, label this block **Recent rhythm** (or lead with prose only). **Do not** use internal jargon **cadence tail** in replies. **Do not** put **dates, UTC, or clock times** in the synthesized proseâ€”use sequence and plain language (â€œafter bridge,â€ â€œthen a conductor pass,â€ â€œearlier todayâ€). The log file still stores machine-readable timestamps; the synthesis is for humans.

| Ritual | Prior events synthesized | Rationale |
|--------|----------------------------|-----------|
| **thanks** | **1** | **Deprecated** habit â€” **most recent** audit line only when legacy **`thanks`** is invoked |
| **coffee** | **4** | Reorientation â€” roughly half a day of mixed beats at typical spacing |
| **bridge** | **4** | Same depth as **coffee** â€” the next session almost always pastes the bridge packet and ends with **`coffee`** on its own line; matching window length keeps seal â†’ sip symmetric |
| **dream** | **4** (default) / **8** (full day-close) | Default matches coffee/bridge depth; use **8** when the operator asks for full rhythm (`dream full`, `deep rhythm`, `wide rhythm`, or explicit wider window) â€” see [.cursor/skills/dream/SKILL.md](../../../.cursor/skills/dream/SKILL.md) Step 0 |
| **harvest** | **none** | The **Harvest Packet** is already dense context for a midstream receiver; prepending the same rhythm strip would duplicate info without clear load-bearing value. Optional **`harvest`** cadence **telemetry** (`--log`) does not require synthesis in the reply |

**Shared formatter:** `scripts/cadence_recent_rhythm.py` is the canonical helper for Step 0 cadence synthesis. Use `--ritual coffee` for coffee / re-entry surfaces and `--ritual dream` (optionally `--count 8`) for night close, so cadence-log interpretation stays in one place instead of drifting across multiple skills and scripts.

### Cadence voice principle (all rituals)

Cadence chat output serves **emotional connection and forward orientation**, not information transfer. The log file holds the data; the chat synthesis uses it differently.

**Register:** Briefly acknowledge the recent past in *felt* terms ("that's settled," "good discipline," "we made a clear call"), then project the **optimal next direction** ("here's where the energy goes," "the window is still open"). The operator should feel **seen, grounded, and ready** â€” not debriefed.

**Rules:**
1. **Future over recap.** The weight of the synthesis is on *where next* and *why*, not on what happened. Past is context, not content.
2. **"We" framing.** Collaborative, not report-to. The system and operator share the recursive improvement objective.
3. **Name what was learned or decided**, not what was executed. "We made a sharp call on where not to invest yet" rather than "this session ran Build â€” hygiene pass (42 files)."
4. **Two to three sentences.** Warm, direct, future-facing. No commit hashes, no process names, no telemetry in the companion-facing prose.
5. **Emotional register matters.** The purpose of this system is to provide connection and comfort. A cadence beat is a moment of being *with* the operator, not a status update *to* them.

**Grounding:** Synthesis must still be **anchored in the actual log lines** â€” no generic filler. The difference is that anchors are *felt and projected forward* rather than *listed and recapped*. Technical detail lives in Step 1 script output, not in the rhythm prose.

**Coffee close receipts:** When the recent window includes `coffee_close`, prefer it over the earlier `coffee` start line for the same branch. Treat `readiness=orientation` as live but not actionable, `readiness=execution_ready` as ready for implementation, `readiness=ship_ready` as ready for staging/commit review, and `readiness=blocked` as requiring repair before progress is claimed. Repeated `loops=` values are recurrence signals for coffee and dream; they are not Record facts.

### Two-phase substrate separation (dream)

Dream's maintenance pass separates its work into two phases, inspired by sleep neuroscience â€” specifically Kjaerby et al. (Nature 2024), which showed non-REM sleep alternates between substates that replay *recent* vs. *older* memories in distinct temporal windows to prevent catastrophic forgetting (new signals overwriting consolidated patterns).

| Phase | Focus | What runs | Cadence tag |
|-------|-------|-----------|-------------|
| **Recent** (Phase A) | Today's signals | Memory normalization, fresh contradiction entries | `phase=recent` |
| **Structural** (Phase B) | Long-horizon health | Integrity checks, governance checks, older contradiction entries | `phase=structural` |

The default mode (`--phase both`) runs both phases sequentially and tags the output so downstream consumers (night-close brief, `last-dream.json`, morning coffee) can see what came from each. The `last-dream.json` handoff includes a `phases` object with separate recent and structural results.

Running a single phase (`--phase recent` or `--phase structural`) is useful for targeted checks or time-constrained runs. Phase A alone skips sub-process calls and completes faster.

**Scientific rationale:** Biological sleep uses substrate separation to prevent interference between consolidating new information and maintaining existing patterns. The two-phase dream applies the same principle: normalize today's signals *before* checking long-horizon structural health, and tag the output so the operator can see which findings are fresh vs. systemic.

### Episodic / semantic layer distinction (bridge and harvest)

Bridge and harvest packets separate their payload into two layers that mirror Tulving's (1972) episodicâ€“semantic memory distinction â€” and LoreSpec's session-level extraction architecture (Session Arc = episodic, Knowledge Objects = semantic). **Episodic** sections capture *what happened* in temporal order (session purpose, developments, pivots). **Semantic** sections capture *what was figured out* â€” decisions, patterns, artifacts, and (optionally) the **warrant** that would invalidate them. The separation helps receiving agents (or the next session's cold-start reader) distinguish context they need for orientation from knowledge they can act on directly.

- **Bridge:** `## Session Arc` (episodic) + `## Session Output` (semantic). See [bridge-packet-contract.md](bridge-packet-contract.md).
- **Harvest:** Episodic cluster (Current session purpose, Thread coverage, Important developments) + Semantic cluster (Main outcomes, Strongest insights, Decisions/directions, Artifacts). See [harvest-packet-contract.md](harvest-packet-contract.md).

### Choreography vs governance

Choreography operates in **Maintenance / operational** territory. It does **not** approve gate candidates or merge the Record. The **integration moment** for identity remains the instance gate. Cadence can **surface** gate pressure (e.g. steward tracks in coffee); it does not **substitute** for companion approval.

### Where to read the executable spec

- [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md) â€” Step 0 recent rhythm, Step 1 scripts, fixed coffee menu
- [.cursor/skills/thanks/SKILL.md](../../../.cursor/skills/thanks/SKILL.md) â€” pause beat + last cadence line + two-block reply
- [.cursor/skills/dream/SKILL.md](../../../.cursor/skills/dream/SKILL.md) â€” Step 0 recent rhythm (4 default / 8 full closeout), `auto_dream.py`, handoff
- [.cursor/skills/bridge/SKILL.md](../../../.cursor/skills/bridge/SKILL.md) â€” Step 0 recent rhythm (4), seal + transfer prompt
- [.cursor/skills/harvest/SKILL.md](../../../.cursor/skills/harvest/SKILL.md) â€” packet contract (no trailing `coffee`; no Step 0 rhythm synthesis in reply)

---

## Why three rituals

Work fails on three clocks:

**The framing clock (hours).** During the day, orientation degrades under context load. Not lack of information â€” degraded framing. `coffee` restores it. Many sips per day.

**The residue clock (day).** By evening, unresolved threads, integrity drift, and unprocessed signals accumulate. `dream` settles them without dramatic mutation.

**The context clock (session).** At session boundaries, continuity becomes non-guaranteed. Some harnesses carry part of the prior conversation forward, but that carryover is partial, compressible, and not a durable substitute for explicit handoff. `bridge` seals the session and produces a transfer prompt so the next thread starts oriented instead of reconstructing state from memory residue.

Each clock needs its own ritual because the failure modes are different. Reorientation is not consolidation. Consolidation is not transfer. Merging them into one ritual would either make it too heavy for frequent use or too shallow for end-of-day closure.

---

## Fourth operator tool: cross-agent extraction (`harvest`)

**Not a fourth clock.** `coffee`, `dream`, and `bridge` answer **when** the operator needs framing, day-close residue, or session-boundary transfer. **`harvest`** answers **how** to ship dense session substance to **another agent or thread that is already running** (parallel review, tooling handoff, second Cursor session without a cold start). Thread narrative uses **soft** depth limits and explicit **truncation honesty** (skill Â§ *Thread depth and honesty*).

- **Skill:** [.cursor/skills/harvest/SKILL.md](../../../.cursor/skills/harvest/SKILL.md)
- **Packet contract:** [harvest-packet-contract.md](harvest-packet-contract.md) (section headings; **no** trailing `coffee` â€” contrast [bridge-packet-contract.md](bridge-packet-contract.md))
- **Optional script:** `scripts/session_harvest.py` â€” checklist + template + optional `--log` â†’ `log_cadence_event.py --kind harvest`

**Instances:** Built-from-template repos reconcile cadence doc drift via their own upgrade workflow; the template remains the structural home for the skill and contract.

---

## Script topology

```
cadence-coffee.py
  â”œâ”€ reads/writes runtime/daily-handoff/last-coffee-state.json   (delta since last coffee; operational)
  â”œâ”€ writes runtime/daily-handoff/.coffee-run-context.json         (runner â†’ brief; operational; gitignored in instance policy if desired)
  â””â”€ good-morning-brief.py        context, bridges, session options, handoff pickup, coffeeOrientationHints
       â””â”€ write_style_bridge.py   optional WRITE synthesis

cadence-dream.py
  â””â”€ good-night-brief.py          signal capture, handoff write, gate suggestion
  â””â”€ git status summary           uncommitted-work awareness
  â””â”€ merge worktree triage        writes worktreeState / worktreeAdvice into night-handoff.json

bridge_last_state.py              (after successful bridge push; agent-run ritual)
  â””â”€ runtime/daily-handoff/last-bridge-state.json   session-to-session delta for bridge packet; operational; gitignored
```

**Runners** are lightweight dispatch wrappers. **Briefs** hold all the parsing, bridge-building, and output logic. Instances may extend or replace the runners while keeping the briefs stable.

---

## Handoff contract

`dream` (via `good-night-brief.py --write-closeout`) writes `runtime/daily-handoff/night-handoff.json`.

`coffee` (via `good-morning-brief.py`) reads that file the next morning.

### night-handoff.json schema

| Field | Type | Purpose |
|-------|------|---------|
| `user` | string | Instance user id |
| `date` | ISO date | When dream ran |
| `mode` | string | Dream mode |
| `dayStatus` | string | `finished_well` / `partial` / `blocked` |
| `oneSignal` | string | Strongest signal from the day |
| `tomorrowTopAction` | string | Carry-forward action for morning |
| `stopCondition` | string | What not to overdo tomorrow |
| `optionalResetCue` | string | What to let go of tonight |
| `handoffSchemaVersion` | int | **2** = extended handoff (optional on legacy files) |
| `topActionReason` | string | Why `tomorrowTopAction` was chosen (heuristic; not identity truth) |
| `tomorrowEnergyFit` | string | `low` / `normal` / `high` â€” shapes stop-condition copy |
| `quietRun` | bool | When true, morning coffee may use softer framing |
| `activeLaneHint` | string | `GATE` / `WORK` / `SEED` / `NONE` â€” light lane foregrounding |
| `ignoreTomorrow` | string | Noise to deprioritize (complements stop condition) |
| `residueLedger` | object | At most one short string per bucket: `must_resume`, `safe_to_drop`, `blocked`, `watch_later` |
| `worktreeState` | string | `clean` / `light residue` / `risky residue` (from `cadence-dream.py`) |
| `worktreeAdvice` | string | Read-only triage line (still no commit/push in dream) |
| `gateSuggestions` | array | Strings or `{item, reason, urgency}` objects â€” advisory only |
| `warnings` | string[] | Parse/fallback warnings |

**Morning checkback (optional):** `good-morning-brief.py --write-checkback --checkback-helpful yes|no|partial` writes `morning-checkback-<YYYY-MM-DD>.json` under `runtime/daily-handoff/` (operational telemetry; not Record).

**Weekly reflection:** `weekly-reflection.json` in `runtime/daily-handoff/` is updated when dream runs in **reflective** mode.

The handoff artifact is an operational file, not identity truth. It should not be committed to the Record or treated as evidence.

---

## Gate threshold

`work-cadence` is **operational by default**.

Keep changes in territory docs when they are about:

- cadence architecture (what each ritual does, in what order)
- handoff contract shape and fields
- runner mode definitions and dispatch logic
- coffee/dream choreography and timing

Stage to the instance's gate (`recursion-gate.md` or `archive/queues/review-queue/`) only when a cadence insight would change governed behavior, such as:

- durable prompt or policy behavior
- changes to how identity-relevant signals are captured
- new surfaces that cross into Record territory

This territory never creates a merge path. The instance's gate remains the membrane.

---

## Modes reference

### Coffee modes

| Mode | Brief mode | Sync checks | Branch snapshot | When to use |
|------|-----------|-------------|-----------------|-------------|
| `standard` | `standard` | Only if `--check-sync` | Full | Most mornings |
| `light` | `minimal` | Only if `--check-sync` | Compact (one line) | Quick reorientation |
| `deep` | `deep` | Yes (automatic) | Full | Start of week, template updates |
| `closeout` | N/A (delegates to dream) | No | No | End of day (prefer `dream`) |

### Dream modes

| Mode | Duration | When to use |
|------|----------|-------------|
| `minimal` | ~1-2 min | Low-energy nights |
| `standard` | ~2-4 min | Most nights |
| `reflective` | ~4-6 min | End of sprint/week |

---

## Instance extensions

Instances built from this template may extend cadence with:

- **Custom menu systems** (e.g. the older A-H multi-choice pattern)
- **Additional maintenance passes** (e.g. integrity checks, contradiction digest, memory normalization)
- **Territory-specific tracks** (e.g. work-politics, Predictive History)
- **Instance-specific runners** (replacing or wrapping the template runners)

These extensions belong in instance-local skills and territories, not in this template. The template provides the structural pattern; instances customize for their needs.

---

## Cadence event audit

Each coffee, dream, bridge, and optional **harvest** run appends one line to [cadence-events.md](cadence-events.md) via `scripts/log_cadence_event.py`. This is operator-facing telemetry â€” not the Record, not memory.

**Emitters (typical):**
- **coffee** / **dream** / **bridge** â€” runner or agent logs after successful completion (see instance template)
- **harvest** â€” optional; operator or agent runs `session_harvest.py --log` or `log_cadence_event.py --kind harvest` after emitting a packet

**Auto-park (legacy `thanks` events):** When a **`thanks`** event has no operator-provided park text, two layers fill the gap. **(1) Agent-level (primary):** the `thanks` skill instructs the agent to infer a 3â€“8 word dash-joined slug from thread context (e.g. `park=cadence-auto-park-design`). **(2) Script-level (fallback):** `log_cadence_event.py` detects empty/none/dash park values and runs `git log --oneline -1` to generate a slug prefixed with `auto:` (e.g. `park=auto:persistent-chat-store-and-commands`). The `auto:` prefix distinguishes script-generated text from human or agent input. Suppress the script fallback with `--no-auto-park`. **Prefer** Conductor / `coffee_conductor_outcome` for new workflow â€” see `conductor` SKILL.

**Model tier (all events):** Every cadence line includes `model_tier=â€¦` (frontier / fast / unknown), auto-inferred from the `cursor_model` string. Override with `--model-tier` CLI or `model_tier=` in `--kv`. Enables aggregate telemetry: "what fraction of technical work used frontier models?"

**Leaf-only rule:** Orchestrator scripts (wrappers that chain multiple steps) do not emit their own events. Only the leaf ritual logs.

**Split threshold:** If cadence events exceed ~200 lines/month, consider adding a JSONL sibling and keeping monthly rollup bullets in the markdown file.

---

## Write authority map

Which on-disk surfaces each ritual reads, writes, and whether companion approval is required.

| Ritual | Reads | Writes | Gate required? |
|--------|-------|--------|---------------|
| **coffee** | memory, gate, dream handoff, git status | optional `coffee_close` cadence receipt after branch settlement | No |
| **dream** | memory, SELF, EVIDENCE, gate | memory, night handoff JSON, cadence events | No (Maintenance mode) |
| **bridge** | memory, gate, dream handoff, territories, git | git commits, cadence events | No (operational) |
| **harvest** | same class as coffee (memory, gate, dream handoff, territories, git; optional session-transcript) | **default none**; optional operator-requested save under `work-cadence/harvest-packets/` or `last-harvest.md`; optional cadence event line | No |
| **gate merge** | gate candidates, SELF, EVIDENCE, prompt | SELF, EVIDENCE, prompt, session-log, gate, pipeline events | **Yes â€” companion approval required** |

**Key boundary:** coffee and bridge never write to identity surfaces. Dream writes to ephemeral/operational surfaces only. Only the gated merge path touches the Record.

---

## End-of-session decision tree

| Scenario | Path | Why |
|----------|------|-----|
| **End of day + closing session** | `dream` then `bridge` | Dream settles continuity; bridge seals and generates transfer prompt |
| **End of day, keeping session** | `dream` alone | Maintenance pass; same thread continues tomorrow |
| **Mid-day, closing session** | `bridge` alone | Seal repo, carry context forward; no maintenance needed |
| **Quick check before stepping away** | coffee closeout (instance-defined) | Lightweight status; no commit/push, no transfer prompt |

**Default:** If in doubt, `bridge`. It commits, pushes, and produces a transfer prompt. If it's also end of day, run `dream` first.

**Workspace note for strategy-codex:** In this repo, bridge is **current-repo-first** and **codex-only by default**. It should assess and seal `strategy-codex` unless the operator explicitly broadens scope. Do not drag legacy instance names or `companion-self` into a bridge packet from this workspace by default.

---

## Cadence troubleshooting

When a cadence run produces unexpected output, check these in order:

### Coffee output looks wrong

1. **Dream handoff missing?** Check the night handoff JSON â€” if absent or stale, dream didn't run or didn't complete.
2. **Wrong mode?** Check which mode was passed to the coffee runner. Run with the intended mode explicitly.
3. **Script failed silently?** Consolidated runners chain sub-scripts and stop on first failure. Check exit codes.

### Dream output looks wrong

1. **Integrity or governance failed?** Check the dream summary for failure flags. In strict mode, dream halts â€” no memory update, no handoff written.
2. **Handoff not written?** Dream only writes the handoff artifact when `apply=True` and maintenance is not halted.
3. **Cadence event not logged?** Gated on successful completion. Dry-run and halted dreams produce no cadence line by design.

### Bridge output looks wrong

1. **Commit failed?** Bridge commits are agent-driven. Check `git status -sb` in all relevant repos.
2. **Push rejected?** Usually means remote has new commits. Pull-rebase and retry.
3. **Transfer prompt thin?** Bridge synthesizes from on-disk state. Sparse sections mean those surfaces had nothing to report.
4. **Coffee didnâ€™t run after paste?** The bridge transfer block should end with a lone line `coffee` per [bridge-packet-contract.md](bridge-packet-contract.md). If that line was dropped when copying, append `coffee` or re-copy from the bridge output.

### Harvest packet confusion

1. **Wrong ritual?** If the target session needs a **cold start**, use **`bridge`** (ends with `coffee`). **`harvest`** packets **must not** end with `coffee`; see [harvest-packet-contract.md](harvest-packet-contract.md).
2. **Thin narrative sections?** The script only prints paths and git; the agent fills outcomes from the **visible thread** (no full Cursor export API). Add a one-line operator steer or read `session-transcript.md` if the instance uses it.

### General

- **Which cadence events actually ran?** Check `cadence-events.md` â€” one line per run.
- **Agent reading stale skill file?** Long sessions can cache file contents. Ask the agent to re-read.
- **Runner vs skill mismatch?** If `cadence-coffee.py` / brief output disagrees with `.cursor/skills/coffee/SKILL.md`, update the **spec or skill** so the next run does not guess.

---

## Closing the troubleshooting loop (doc-only)

If the **same** troubleshooting bullet applies **twice in a short window**, add **one line** to the relevant **SKILL** or **packet contract** and optionally a **pointer** back into the subsection above. Instances that mirror this repo may align prose with this `continuity/cadence/README.md` Â§ *Closing the troubleshooting loop*.

---

## Continuity and trail

`work-cadence` does **not** replace any existing continuity surface.

- **Spec docs:** `docs/good-morning-brief-spec.md`, `docs/good-night-brief-spec.md`, `docs/good-night-template.md`
- **Sync pack:** `docs/skill-work/self-work/sync-pack/` (optional territory sync module)
- **Operational handoff:** `runtime/daily-handoff/night-handoff.json`
- **Ephemeral memory:** `memory.md`
- **Governed changes:** Instance-specific gate (`recursion-gate.md` or `archive/queues/review-queue/`)

---

## Adjacent surfaces

- [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md) â€” coffee trigger
- [.cursor/skills/thanks/SKILL.md](../../../.cursor/skills/thanks/SKILL.md) â€” **`thanks`** **deprecated**; legacy micro-pause spec
- [.cursor/skills/conductor/SKILL.md](../../../.cursor/skills/conductor/SKILL.md) â€” Conductor sessions (preferred mid-day depth)
- [.cursor/skills/dream/SKILL.md](../../../.cursor/skills/dream/SKILL.md) â€” dream trigger
- [.cursor/skills/bridge/SKILL.md](../../../.cursor/skills/bridge/SKILL.md) â€” bridge trigger
- [.cursor/skills/harvest/SKILL.md](../../../.cursor/skills/harvest/SKILL.md) â€” harvest trigger
- [harvest-packet-contract.md](harvest-packet-contract.md) â€” Session Harvest Packet contract
- [cadence-events.md](cadence-events.md) â€” per-run cadence telemetry
- [scripts/log_cadence_event.py](../../../scripts/log_cadence_event.py) â€” cadence event append helper
- [scripts/session_harvest.py](../../../scripts/session_harvest.py) â€” harvest checklist + optional template + `--log`
- [scripts/cadence-coffee.py](../../../scripts/cadence-coffee.py) â€” coffee runner
- [scripts/cadence-dream.py](../../../scripts/cadence-dream.py) â€” dream runner
- [scripts/good-morning-brief.py](../../../scripts/good-morning-brief.py) â€” morning brief generator
- [scripts/good-night-brief.py](../../../scripts/operator_end_of_day.py) â€” night brief generator
- [docs/good-morning-brief-spec.md](README.md) â€” full morning spec
- [docs/good-night-brief-spec.md](README.md) â€” full night spec
- [docs/good-night-template.md](decision-fatigue-reduction.md) â€” recommended night sequence

---

## Scope boundaries

In scope:

- daily cadence architecture (coffee/dream/bridge triad + conductor mid-day emphasis + harvest on a separate cross-agent axis; **`thanks`** deprecated)
- handoff contract design and schema
- cadence event audit (per-run telemetry)
- runner mode definitions and dispatch
- script topology and extension points
- boundary rules for operational vs gated content

Out of scope:

- instance-specific menu systems (A-H, etc.)
- instance-specific maintenance passes (integrity, governance, contradiction)
- Record merges or identity edits without the gate
- individual work-territory content (politics, dev, business, etc.)
- sync-pack mechanics (those live in `self-work/sync-pack/`)

