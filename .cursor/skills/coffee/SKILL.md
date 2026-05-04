---
name: coffee
preferred_activation: coffee
requires: [handoff-check]
description: "Grace-Mar operator cadence and tempo. Primary trigger: coffee. Step 2 = hub AÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“E only (Steward / Engineer / Historian / Capitalist / Conductor). Standalone Conductor (master name or conductor skill) remains separate from the hub list. Before Step 1, Recent rhythm. Signing-off: same AÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“E menu; closeout in Step 1. Coffee also acts as the default checkpointed re-entry ritual."
---

# Coffee

**Preferred activation (operator):** say the exact phrase **`coffee`**. Legacy **`hey`** still works as a compatibility alias, but **`coffee`** is the canonical trigger now.

**Signing-off intent** (end of session, wrapping the day, stepping away) uses the **same** **`coffee`** trigger and the **same** **A, B, C, D, E** hub menu. There is **no** separate closeout branch or closeout-only menu item. **Step 1** switches to handoff-weighted output when intent is signing off; **Step 2** is unchanged.

`coffee` is not a startup ceremony. `coffee` is a **repeatable sip of coherence**.

Its purpose is to help the operator become more awake to the actual situation, more coherent about priorities, and more directed about the next move. A coffee session does not need to complete the day's thinking. It only needs to improve orientation enough that action becomes easier.

Multiple `coffee` sessions per day are normal. That is not redundancy; it is the point. Each `coffee` is another sip.

`coffee` is also the default checkpointed re-entry ritual. In a fresh chat, it should resume from the most recent authoritative grace-mar checkpoint on disk, using cadence and handoff state to recover orientation. If more than one plausible checkpoint exists, prefer the latest on-disk authority and surface the ambiguity instead of guessing. This is a checkpoint, not a transfer seal: it restores continuity, but it does not commit, push, or generate a bridge packet.

**Coffee Hub Menu (terminology):** **`coffee` Step 2** fixed **AÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“E** hub (**Steward / Engineer / Historian / Capitalist / Conductor**) is the **Coffee Hub Menu**. When routing continues into **Conductor**, resolution uses the **Master Selection Menu** (masters **A.ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“E.** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Toscanini ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ Bernstein) and then typically the **Conductor Action Menu** (three repo-grounded next moves ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [CONDUCTOR-PASS ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Conductor action MCQ](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md#conductor-action-mcq)). Layer map: [CONDUCTOR-LAYER-MAP.md](../../../docs/skill-work/work-coffee/CONDUCTOR-LAYER-MAP.md).

## Guardrails

- Do not turn `coffee` into a heavy maintenance ritual by default.
- Do not overload each run with every possible obligation or stale thread.
- Prefer a small number of salient next paths over exhaustive review.
- Keep the operator in the position of renewed agency, not procedural burden.
- `coffee` is for orientation; heavier consolidation belongs to `dream`.
- This is read-only planning. Do not merge or stage just because the warmup mentions candidates.
- If integrity fails, surface that before optional improvements.
- **Contextual stewardship:** Agents have no cross-thread institutional memory; authority for the Record is **on-disk files + gated pipeline** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not model recall or chat summary.

## Relation to dream

`coffee` and `dream` form a biological-cognitive pair:
- **`coffee`** = repeated framing dose (many per day)
- **`dream`** = end-of-day consolidation pass (usually once)

`coffee` should feel like a sip. `dream` should feel like sleep. See `.cursor/skills/dream/SKILL.md` Ãƒâ€šÃ‚Â§ *Cadence choreography* for the day's sequence and data handoff.

<a id="conductor-only-no-coffee"></a>

## Conductor session (outside `coffee` hub menu)

Use this path when the operator wants **Conductor** **without** going through **`coffee` Step 2 hub letter E**.

The **five masters** (**Toscanini**, **FurtwÃƒÆ’Ã‚Â¤ngler**, **Karajan**, **Kleiber**, **Bernstein**) are **not** listed as separate lines on the **`coffee`** hub ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â hub **E** is the **single** in-`coffee` slot for **Conductor continuation** after **`coffee`** Step 1. Call masters **directly** (this section) when **`coffee`** was not opened or when the operator prefers **`conductor`** / master name **instead** of **`coffee`**.

**Triggers (examples):** master name or prefix (**`toscanini`**, **`furtwangler`**, **`karajan`**, **`kleiber`**, **`bernstein`**), **`conductor`** with optional fragment, or plain language (**"Toscanini pass"**, **"run Kleiber on the notebook"**). If intent is unclear, ask once. **Legacy:** bare **`D`** + fragment still resolves like a conductor turn when the message is clearly conductor-only (no **`coffee`**).

**First-turn activation note:** bare conductor slugs like **`toscanini`**, **`furtwangler`**, **`karajan`**, **`kleiber`**, and **`bernstein`** should route straight into Conductor on the first command, not be treated as ambiguity.

**Do not** run `operator_coffee.py`, **do not** paste work-start or closeout **Step 1** output, and **do not** lead with **Recent rhythm** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â unless the same message also says **`coffee`** or **`hey`**.

**Standalone Conductor** (no **`coffee`** in this turn): show **`build_conductor_mcq_for_user('grace-mar')`** when the master is **not** yet disambiguated; resolve via `resolve_d_conductor` + [work-cadence-events.md](../../../docs/skill-work/work-cadence/work-cadence-events.md).

**After `conductor=<slug>` resolves** (standalone pick **or** **`coffee` hub E** auto-continue per [**Ãƒâ€šÃ‚Â§ Hub E**](#hub-e-auto-continue)): deliver the **short** orientation in [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md) and [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../../../codex/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md). **Then, always** deliver the **Conductor action MCQ** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **three** **A-C** repo-grounded next moves ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â per [CONDUCTOR-PASS ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Conductor action MCQ](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md#conductor-action-mcq) and [conductor skill](../conductor/SKILL.md). **Skip** the action menu **only** if the operator said **"orientation only"** / **"no action menu"** in the same turn.

**Logging:** `log_cadence_event.py --kind coffee_pick -u grace-mar --ok --kv picked=conductor conductor=<slug>` (e.g. `karajan`, `toscanini`). **Legacy** lines may still use `picked=D`; both are fine for rollups. **`coffee` hub letter E** uses **`picked=E conductor=<slug>`** with **`<slug>`** the resolved conductor (**auto-continued** **or** chosen after Masters MCQ) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see [Ãƒâ€šÃ‚Â§ Cadence audit](#cadence-audit). **Do not** append a separate **`coffee`** event unless they actually ran `coffee` Step 1.

**Conductor close (optimal loop):** Same as before ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [CONDUCTOR-CLOSE-TEMPLATE.md](../../../docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-CLOSE-TEMPLATE.md) in **`days.md`** / page **Reflection**, or **`coffee_conductor_outcome`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [CONDUCTOR-IMPROVEMENT-LOOP.md](../../../docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md). For auditability, every new outcome line should carry **`conductor=<slug>`** and **`verdict=`**, plus **`notebook_ref=`** or **`falsify=`** (both preferred). If a pass ended without that line, log a repair outcome on the next turn rather than leaving the close implicit.

**Loop surfacing:** When the derived reader finds live pressure, show **Open loops due for revisit** before the Conductor action MCQ via `build_conductor_revisit_block('grace-mar')`. Keep it advisory, prefer the active lane first, and include the shared **`Tension`** subsection when multiple streams disagree on the same horizon.

**After the reply:** return to **normal workflow** unless the operator says **`stay in coffee`** or **`coffee`**.

<a id="hub-e-auto-continue"></a>

**Hub E (`coffee` Step 2) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â automatic continuation:** When the operator chooses **E ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Conductor** after **`coffee`** Step 1, **`last_logged_conductor`** from cadence (**`coffee_pick`** with **`conductor=`**) is the **default resolved slug**.

- **If a slug exists:** **Continue that master immediately** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â short orientation + **Conductor action MCQ** for that slug. **Do not** paste the **Masters MCQ** (`build_conductor_mcq_for_user`) row **unless** the operator asks to switch masters in the same turn (e.g. master name / prefix, ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œmastersÃƒÂ¢Ã¢â€šÂ¬Ã‚Â, ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œpick a cardÃƒÂ¢Ã¢â€šÂ¬Ã‚Â, ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œswitchÃƒÂ¢Ã¢â€šÂ¬Ã‚Â) **or** cadence has **no** qualifying prior conductor.
- **If no slug exists:** Paste **`build_conductor_mcq_for_user('grace-mar')`** **or** prompt once for master name / **`conductor`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **do not** invent a default.

Optional **one line** after auto-continue prose: *Say a master name or ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œmastersÃƒÂ¢Ã¢â€šÂ¬Ã‚Â to open the five-master row instead.*

**Letter-collision:** If both the **coffee hub** and a **Conductor action MCQ** appear in one reply, **label** them ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â e.g. **`Coffee hub ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Reply AÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“E`** vs **`Conductor action MCQ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Reply AÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“C (this pass)`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and never use bare ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œpick **E**ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â without naming which menu ([CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md)).

---

## "Coffee" = start here (two steps)

When the operator begins with **`coffee`** (or clearly the same intent; legacy **`hey`** still counts), treat it as opening a **coffee session**.

### Step 0 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Recent rhythm (before Step 1 scripts)

**Read first** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `operator_coffee.py` appends a new **`coffee`** line at the **end** of a successful run, so the log must be read **before** those commands if the rhythm read is to exclude this session.

1. Open **`docs/skill-work/work-cadence/work-cadence-events.md`**. Below `_(Append below this line.)_`, collect lines matching `- **YYYY-MM-DD HH:MM UTC** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â kind (user) ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦`.
2. Take the **last 4** such lines already in the file. If there are fewer than four, use what exists; if none, **Recent rhythm:** _(no prior events)_ in the reply.
3. **Synthesize in plain prose** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **2ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“4 short sentences** for a human, **not** a telemetry dump: **do not** lead with a wall of `key=value` pairs. **Companion-facing UX:** label this block **Recent rhythm** (or prose only); **do not** put **dates, UTC, or clock times** in this prose (use order and light anchors like ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œafter dream,ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œthen bridge,ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œearlier todayÃƒÂ¢Ã¢â€šÂ¬Ã‚Â without timestamps). **Must anchor in specifics** from those four lines ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â name what actually happened (e.g. **bridge** with **commit refs** if present, **coffee** **work-start** vs **standard**, **coffee_pick** / **conductor** when present, legacy **`thanks`** **park** text when non-empty, **dream** pass/fail or integrity/governance in ordinary words, **harvest** packet vs not). **Avoid** generic process filler that could apply without reading the file. Do **not** paste raw log lines unless they are already very short.

   **Cadence voice:** Follow the **cadence voice principle** ([work-cadence README](../../../docs/skill-work/work-cadence/README.md#cadence-voice-principle-all-rituals)). Lead with *felt* acknowledgment of what was settled or decided, end with the **optimal next direction**. Use **"we"** framing. The operator should feel **seen, grounded, and ready** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not debriefed. Name what was learned or decided, not what was executed. No commit hashes, no process names ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â warm, direct, future-facing.
4. In the reply, place **Recent rhythm:** at the **top** of Step 1 content (immediately before script output / warmup paste). Same rule for **signing-off** Step 1 (before `operator_coffee.py --mode closeout` or handoff-only flow).

If the file is missing or empty below the anchor, state that under **Recent rhythm** and continue Step 1.

### Step 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Automated actions (one flow, two weights)

**Detect intent**

- **Signing off / closeout / end of session / wrapping the day** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ use **closeout-weighted Step 1** below.
- Otherwise ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ **work-start Step 1** (scale with explicit phrases or weekday cadence).

**Work-start Step 1** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run the consolidated coffee script (preferred):

```bash
python3 scripts/operator_coffee.py -u grace-mar                   # work-start (default)
python3 scripts/operator_coffee.py -u grace-mar --mode light      # lighter pass
python3 scripts/operator_coffee.py -u grace-mar --mode minimal    # compact harness only
python3 scripts/operator_coffee.py -u grace-mar --mode reentry    # cold-thread full stack
```

**Signing-off Step 1** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â handoff-weighted (same trigger **`coffee`**, not a second ritual name):

```bash
python3 scripts/operator_coffee.py -u grace-mar --mode closeout
```

Or directly: `python3 scripts/operator_handoff_check.py -u grace-mar`. Include the output in your reply. Add a **short paragraph**: what moved today, what is parked, gate + Jiang carryovers, suggested re-entry prompt. Full spec: [`.cursor/skills/handoff-check/SKILL.md`](../handoff-check/SKILL.md).

If the operator **explicitly** wants **both** full warmup **and** signing-off in one message, run work-start then append handoff (rare).

Add `--compact` for shorter harness output. Individual scripts (`operator_daily_warmup.py`, `harness_warmup.py`, `operator_handoff_check.py`, `operator_reentry_stack.py`) are still available.

**Dream handoff:** If `dream` ran overnight, the daily warmup includes a last-dream block from `users/grace-mar/last-dream.json` (**"Last dream (night handoff)"** when there is something to read out, or a **one-line "quiet handoff"** when `integrity` / `governance` / digest counts are clean and there are no followups). A successful dream may add **`last_coffee_echo`**: a single warm line (from the 24h cadence rollup) that ties yesterdayÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢s `coffee` into morning startupÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â**cadence / runtime only**, not Record. **Signal days** (issues, followups, or non-zero digests) still use the fuller collapsed block. Extra lines (civ-mem summary, coffee 24h rollup) are **off** by default; tune `config/context_budgets/coffee.json` or pass `--show-civ-mem` / `--show-rollup` on `operator_daily_warmup.py`, `operator_coffee.py`, or `operator_reentry_stack.py`. After that block (or alone if the Last dream section is turned off), warmup prints one line **`Dream ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ coffee menu:`** mapping dreamÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢s suggested execution path to **A / B / C** (**Steward / Engineer / Historian**) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â operational hint only; see [dream/SKILL.md](../dream/SKILL.md) Ãƒâ€šÃ‚Â§ *Five-second closeout*. Approximate paste footprint: `python3 scripts/audit_context_tax.py -u grace-mar`. These files are operator scaffolding, not Record. For full paths / snippets / followups, use **`--verbose-dream`**. When pasting warmup for the operator, prefer **collapsed** unless they ask for detail.

**Step 1 deliverables (work-start):** Warmup brief (priorities, gate, work-politics snapshot where relevant, integrity), branch snapshot, daily brief + intel defer line (path pattern + **menu C ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Historian** when ready), optional PH/Jiang line. **No** Polymarket / poll / Massie blocks in Step 1 unless the operator explicitly asked in the same message.

**Memory observability:** `operator_coffee.py` may print a single **`Memory observability:`** line after lane hints when the derived continuity dashboard is `watch`, `stale`, or `missing`. Do not paste the full dashboard into coffee. If the line is absent, treat memory observability as quiet/ok for this run. The dashboard is WORK-derived only; it does not edit MEMORY, the Record, or the gate.

**Step 1 guardrail:** Stay read-only ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no merge/stage unless they switch lanes or use a pipeline phrase ("we ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦").

**Done when:** Script output is pasted in the reply, Recent rhythm is at the top, and the full coffee menu follows immediately.

For cadence tables and explicit phrase definitions (`coffee light`, `coffee minimal`, `coffee survey`): see [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md).

### Multiple coffees per day

The operator may say **`coffee`** **more than once per calendar day** for reorientation. This is normal. Each new `coffee` runs Step 1 again and starts a new **A, B, C, D, E** cycle. If **`coffee`** arrives mid-hub, treat it as a **reorientation restart**: run Step 1 again, then offer a fresh menu.

<a id="coffee-step-2-hub"></a>

### Step 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Hub menu (five lines only)

Immediately **after** Step 1 content, output the **hub** menu ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **five lines** (**AÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“E**).

**One option per line:** Each hub letter is **its own line** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **`A.` ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ `E.`** as **five separate lines**, not multiple letters on one line and not a single paragraph listing AÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“E. (Sub-menus inside **D** **Capitalist** forks or **Steward** branches are separate from this rule when you open a follow-up.)

**Letter-collision:** The **Symphony masters** disambiguation row (**masters A.ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“E.**) and the **Conductor action MCQ** (**three actions A-C** for the resolved slug) use **the same letter range** as the hub. When **both** a **coffee hub** menu and a **Conductor action MCQ** could appear in one reply, **label** them explicitly ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md). **Do not** reuse bare ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œpick **E**ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â without naming which menu.

**Do not** append the **masters** **MCQ** row **under** the five hub lines; masters disambiguation belongs to **Conductor** turns ([Ãƒâ€šÃ‚Â§ Conductor session (outside `coffee` hub menu)](#conductor-only-no-coffee), [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md)). **After hub E is chosen:** when **`last_logged_conductor`** resolves, **skip** the **Masters MCQ** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â deliver orientation + **Conductor action MCQ** immediately ([**Ãƒâ€šÃ‚Â§ Hub E ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â automatic continuation**](#hub-e-auto-continue)).

**Do not** add micro-hints, fork shorthand, or F/G/Xavier/Dev tags **under** the hub list.

**Hub menu (example):**

```
A. Steward
B. Engineer
C. Historian
D. Capitalist ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <one short line: work-business / grace-gems / commercial angle / bookshelf product or teaching use>
E. Conductor
```

**Hub line E:** **`E ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Conductor`** only ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **do not** preview **`last_logged_conductor`** in the hub menu copy. **`operator_coffee.py`** Step 1 prints a script section headed like `Coffee hub Step 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â hub **E**` whose body is **`format_coffee_hub_e_line`** output (label only). Auto-continue behavior is unchanged ([**Ãƒâ€šÃ‚Â§ Hub E ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â automatic continuation**](#hub-e-auto-continue)).

**Filling D ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Capitalist:** **work-business**, **grace-gems**, revenue/offers framing; **work-cici** when business/teaching-commercial; one prescribed next step. Bookshelf belongs here only when the use is **commercial / teaching / product packaging**. **Self-knowledge bookshelf quiz** belongs under **C ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Historian**.

**Capitalist ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â bookshelf / product use:**

- Bookshelf may support offer design, teaching angles, grace-gems packaging, course/product framing, or public copy.
- Do **not** use D as the default route for IX-A bookshelf recursion; route that to **C ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Historian ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ B. Bookshelf quiz**.
- **Catalog stance membrane** (`bookshelf-membrane-round.json` + `build_bookshelf_membrane_candidates.py`) remains secondary and scripted: use it only when the operator requests catalog organization or a pressing organizational membrane issue applies.

**Fixed option (Capitalist angle, hub line wording):** may read **Bookshelf product/teaching angle** or **Bookshelf stance membrane (scripted)** when those commercial or catalog intents are live.

**Catalog stance membrane (scripted path only ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â branch 2 above):**

- Session is **multi-round**: 5ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“10 MCQs per round when using the scripted stance round artifact.
- After each round, ask continue/stop.
- On stop, produce:
  - `docs/skill-work/work-strategy/history-notebook/research/BOOKSHELF-MEMBRANE-REPORT.md`
  - `docs/skill-work/work-strategy/history-notebook/research/BOOKSHELF-MEMBRANE-CANDIDATE-DRAFTS.md`
- Output is draft-only; no direct writes to `users/grace-mar/recursion-gate.md` unless explicitly requested.

**Write-shaped** work is **not** an extra letter ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it defaults under **D** when skill-write/commercial, or when the operator says **`write`** / **`skill-write`** without **`coffee`**. State it plainly in the angle-bracket line; **do not** add a separate ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œmicro-hintsÃƒÂ¢Ã¢â€šÂ¬Ã‚Â row.

**Filling E ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Conductor:** Hub line is **`E ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Conductor`** only (no last-master preview). **When the operator picks hub E:** **[`last_logged_conductor`](#hub-e-auto-continue)** **defaults** the session ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **orientation + Conductor action MCQ** for that slug **without** interposing the **Masters MCQ**, unless cadence has **no** prior **`coffee_pick` `conductor=`** **or** the operator asks to switch masters (name / ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œmastersÃƒÂ¢Ã¢â€šÂ¬Ã‚Â / ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œpick a cardÃƒÂ¢Ã¢â€šÂ¬Ã‚Â). **If no slug:** paste **`build_conductor_mcq_for_user`** **or** prompt once ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **do not** invent a default master.

**Step 1 context for B / D:** `operator_coffee.py` prints **`Lane context (for hub B / D ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Engineer & Capitalist hints)`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â two lines from `scripts/coffee_lane_next_hints.py` (work-cici + work-dev). Use when choosing **B**, **D**, or when wording those lines.

**Step 1 context for hub E:** After lane hints, **`operator_coffee.py`** prints the script block that includes **`format_coffee_hub_e_line`** output ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a single **label** line **`E ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Conductor`** for Step 2 (no last-master preview on that line).

**Default recommendation line:** Step 1 may print `Session load: ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ (recommended: X)` and `Recommended default: X ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â say "go" to accept, or pick another hub letter.` (**A** / **B** / **C**). When present, surface that recommended default once before or after the hub menu. The fixed hub menu still remains five lines only. For **Conductor** emphasis outside the hub, say **once** that **`conductor`** / master name works **without** opening **`coffee`** ([Ãƒâ€šÃ‚Â§ Conductor session](#conductor-only-no-coffee)). **Not** micro-hints under the hub list.

**Quick reference (modes):**

- **A. Steward** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **Governance membrane:** **gate** \| **template/boundary** \| **integrity/exports** \| **git/ship**. **Default if the operator says `A` only:** **gate** if pending candidates; else **template/boundary**. **`A integrity`** / **`A git`** / **`A ship`** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ that track; **`A both`** / **`A all`** as in [menu-reference ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Steward](../../../docs/skill-work/work-coffee/menu-reference.md#ah-table). Gate merges never without companion **approve** + `process_approved_candidates.py`. *(Legacy hub letter **B**.)*

- **B. Engineer** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **work-dev + skills/meta** (not git/ship or full membrane audits ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â those are **A**): `docs/skill-work/work-dev/` + [work-dev-sources.md](../../../docs/skill-work/work-dev/work-dev-sources.md); **skills / meta** when **`skills`** / **`meta`** with **B**. **work-cici** ops when engineering-shaped. **When hub B is chosen:** After **one short orientation line**, deliver **Engineer next moves** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **3ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“5 options** labeled **A through E** (**or AÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“D** if four), **each option its own line**, under an explicit heading such as **`Engineer menu ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â reply AÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“E`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **not** `B1`ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“`B5` and not unlabeled lists. Each new submenu **restarts letters from A**; disambiguate from the **Coffee hub** with the menu title (same idea as **letter-collision** labeling for Conductor action MCQ vs hub). Each line is a **repo-grounded** plausible next step (work-dev wedge, script, CI, **skills** path) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **enumeration only** until the operator picks. Use Step 1 **`Lane context (for hub B / D)`** and [workspace.md](../../../docs/skill-work/work-dev/workspace.md) Ãƒâ€šÃ‚Â§ **Next actions** when helpful. **Detail:** [menu-reference Ãƒâ€šÃ‚Â§ Engineer (B) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â detailed scope](../../../docs/skill-work/work-coffee/menu-reference.md#build-b--detailed-scope) *(legacy letter **Build** / old hub **A**).*

- **C. Historian** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Opens exactly three actionable options and nothing else. Do **not** auto-run the daily brief or auto-offer Tri-Frame before this submenu. Output:
  - `Historian menu ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â reply AÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“C`
  - `A. Intel ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â daily brief / current-events watch`
  - `B. Bookshelf quiz ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â self-knowledge MCQs ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ IX-A candidates`
  - `C. Notebook synthesis ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â History Notebook / Predictive History with Tri-Frame lenses`

  **C-A Intel** owns the daily brief path: generator and/or `daily-brief-YYYY-MM-DD.md`, **Ãƒâ€šÃ‚Â§1d** / **Ãƒâ€šÃ‚Â§1e** / **Ãƒâ€šÃ‚Â§1g** / **Ãƒâ€šÃ‚Â§1h** (PRC / IRI when load-bearing), optional **KY-4** (Polymarket, polls, Massie X per cadence), and optional **`last30days` frontier check** when the operator wants one fresh, source-dated scan for today's inbox. Do **not** auto-run `last30days` from coffee Step 1 or merely because C-A is opened; offer or run it only when the operator chooses Intel and the frontier is stale / explicitly requested. Output remains a short brief + optional `daily-strategy-inbox.md` one-liner, not a `days.md` / thread / gate edit. **C-B Bookshelf quiz** uses [.cursor/skills/bookshelf-knowledge-mcq-to-gate/SKILL.md](../bookshelf-knowledge-mcq-to-gate/SKILL.md): default **6** source-bound, topic-anchored MCQs from `bookshelf-quiz-anchors.yaml`, with academic inline citations visible to the operator and hidden `self-library-bookshelf` receipts in the gate, **at most two** date-primary stems, strictness default **top2**, and stage candidates only through `recursion-gate.md`; never merge without approval. **C-C Notebook synthesis** owns History Notebook / Predictive History synthesis; Tri-Frame minds **Barnes ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Mearsheimer ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Mercouris** live here, using [daily-brief-minds-menu.md](../../../docs/skill-work/work-strategy/daily-brief-minds-menu.md) as the lens menu when useful. When C-C is blocked by ambiguous stream ownership, page shape, raw-input routing, or civ-mem lens choice, offer one bounded `skill-elicitation` checkpoint; do not run it automatically and do not add another coffee hub option. **Companion survey** still lives under C when invoked by `coffee survey`. *(Legacy hub **C ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Strategy (daily brief)**.)*

- **D. Capitalist** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **work-business**, **grace-gems**, revenue/offers; **work-cici** when business/teaching-commercial angle; bookshelf only for commercial / teaching / product packaging or scripted catalog stance membrane; **not** IX-A bookshelf recursion. **One** prescribed next step.

- **E. Conductor** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **`coffee` hub E** **[auto-continues](#hub-e-auto-continue)** **`last_logged_conductor`** (orientation + **Conductor action MCQ**); hub menu line is **Conductor** only. **Not** a substitute for standalone **`conductor`** when **`coffee`** was not invoked.

**Exit / re-offer:** After **A**, **B**, **D**, or **E**, re-offer the full **coffee** hub **AÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“E** **after** the **current** branch settles ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **except:** when **hub E** yielded **orientation + Conductor action MCQ**, **do not** paste **coffee hub** **AÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“E** in that **same** reply ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â wait for **Reply AÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“C** against **Conductor action MCQ** (**label menus** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [Ãƒâ€šÃ‚Â§ Letter-collision](#coffee-step-2-hub)); re-offer **coffee hub** on the following turn (or after Conductor closes) unless the operator exited **`coffee`**. After **C**, **exit** to normal workflow unless **`stay in coffee`**. After **A** (Steward), see [menu-reference Ãƒâ€šÃ‚Â§ Steward follow-up fork](../../../docs/skill-work/work-coffee/menu-reference.md#steward-follow-up-fork-implement-now-vs-later) *(legacy docs may still say **B** for Steward ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â read **A**).* Synonyms **`A+ship`** / **`EXECUTE`** ÃƒÂ¢Ã¢â‚¬Â°Ã‹â€  **Implement now** on steward track. **Decision-fatigue rule:** after a hub branch opens one submenu, the next assistant turn should execute the selected item, recommend one default, or report the blocker rather than opening another broad menu.

Legacy **AÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“G** detail tables in [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md) still describe **workloads**; map letters: old **Daily Brief ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ C-A Intel**, old **self-knowledge bookshelf quiz ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ C-B Bookshelf quiz**, old **Book / Jiang / Predictive History ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ C-C Notebook synthesis**, **Build ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ B**, **Steward ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ A**, commercial / teaching bookshelf uses ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ **D**, and **Symphony conductors ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ E** on hub after **`coffee`**, or **standalone** **`conductor`** / master name without **`coffee`**.

**Done when:** The operator has picked **AÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“E** (or combo), the selected branch has been executed, and the re-offer or exit rule has been applied.

---

## Session trail (optional)

Sessions begin when the operator says **`coffee`** (optional modifiers). To keep a trail: use **`users/<id>/session-transcript.md`** and/or append dated bullets to **`docs/skill-work/work-*/*-history.md`**. **Not** the gated Record; **not** `self-memory`. See [work-menu-conventions.md](../../../docs/skill-work/work-menu-conventions.md).

<a id="cadence-audit"></a>

## Cadence audit

Each successful coffee run appends one line to `docs/skill-work/work-cadence/work-cadence-events.md` via `scripts/log_cadence_event.py`. This is automatic ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no operator action required. The line always includes **`cursor_model=ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦`** (audit parity with bridge/harvest **Agent surface**): set **`CURSOR_MODEL`** in the environment, or pass **`--cursor-model "ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦"`** to `operator_coffee.py`, using the model name from the Cursor UI. If unset, **`unknown`**.

**After the operator states their menu letter** (and steward track if **A**), the assistant may append a **`coffee_pick`** cadence line (same file) for rollup:  
`python3 scripts/log_cadence_event.py --kind coffee_pick -u grace-mar --ok --kv picked=A steward=gate --cursor-model "<from Cursor UI>"`  
(`steward=` only when `picked=A`; values: `gate`, `template`, `integrity`, `git`, `both`, or `all`.) For **hub** picks: **`picked=A`..`E`**. **`picked=E`** should include **`conductor=<slug>`** when the Conductor master is resolved. For **Conductor sessions** outside hub letter picks: **`picked=conductor`** with **`conductor=<single-slug>`** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **no** `+` in new logs. Legacy files may still contain **`picked=D`** + `conductor=` or older shapes. **Optional closure after a conductor run:** `python3 scripts/log_cadence_event.py --kind coffee_conductor_outcome -u grace-mar --ok --kv verdict=watch conductor=kleiber notebook_ref=docs/path.md` (see [CONDUCTOR-IMPROVEMENT-LOOP.md](../../../docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md) Ãƒâ€šÃ‚Â§ 3 for `notebook_ref` / `falsify` examples). Optional: `scripts/log_operator_choice.py --context COFFEE --picked A` for `session-transcript.md`.

## Related files

- `docs/skill-work/work-cadence/README.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **Cadence choreography** (ordering, handoffs, Step 0 recent rhythm window depths, harvest vs triad)
- `docs/skill-work/work-coffee/README.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â territory rationale and boundaries
- `docs/skill-work/work-coffee/menu-reference.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cadence, survey track, signing-off add-ons; legacy **AÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“G** workload tables (map to the current coffee Step 2 above)
- `docs/skill-work/work-coffee/work-coffee-history.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â lane breadcrumbs
- `docs/skill-work/work-cadence/work-cadence-events.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â per-run cadence telemetry
- `.cursor/skills/dream/SKILL.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â night-side counterpart
- `.cursor/skills/thanks/SKILL.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **`thanks`** **deprecated** for grace-mar workflow; prefer **conductor** or **`coffee` light/minimal`
- `docs/skill-work/work-politics/polling-and-markets.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â KY-4 polling (**menu C ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Historian** / daily brief)
- `docs/skill-work/work-strategy/daily-brief-minds-menu.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Tri-Frame **three minds** (Barnes / Mearsheimer / Mercouris) for **C ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Historian** second stage
- `docs/skill-work/work-politics/america-first-ky/guardrail-stress-test.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â messaging discipline
- `.cursor/skills/bookshelf-knowledge-mcq-to-gate/SKILL.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **C ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Historian / Bookshelf quiz** MCQs toward IX-A / gate staging

