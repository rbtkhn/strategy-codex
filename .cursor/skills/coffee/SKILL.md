---
name: coffee
preferred_activation: coffee
requires: [handoff-check]
description: "Strategy-codex operator cadence and tempo. Primary trigger: coffee. Step 2 = hub A-D only (Steward / Engineer / Strategist / Capitalist). Standalone Conductor (master name or conductor skill) remains separate from the hub list. Before Step 1, Recent rhythm. Signing-off: same A-D menu; closeout in Step 1. Coffee also acts as the default checkpointed re-entry ritual."
---

# Coffee

**Preferred activation (operator):** say the exact phrase **`coffee`**. Legacy **`hey`** still works as a compatibility alias, but **`coffee`** is the canonical trigger now.

**Signing-off intent** (end of session, wrapping the day, stepping away) uses the **same** **`coffee`** trigger and the **same** **A, B, C, D** hub menu. There is **no** separate closeout branch or closeout-only menu item. **Step 1** switches to handoff-weighted output when intent is signing off; **Step 2** is unchanged.

`coffee` is not a startup ceremony. `coffee` is a **repeatable sip of coherence**.

Its purpose is to help the operator become more awake to the actual situation, more coherent about priorities, and more directed about the next move. A coffee session does not need to complete the day's thinking. It only needs to improve orientation enough that action becomes easier.

Multiple `coffee` sessions per day are normal. That is not redundancy; it is the point. Each `coffee` is another sip.

`coffee` is also the default checkpointed re-entry ritual. In a fresh chat, it should resume from the most recent authoritative checkpoint on disk, using cadence and handoff state to recover orientation. If more than one plausible checkpoint exists, prefer the latest on-disk authority and surface the ambiguity instead of guessing. This is a checkpoint, not a transfer seal: it restores continuity, but it does not commit, push, or generate a bridge packet.

**Coffee Hub Menu (terminology):** **`coffee` Step 2** fixed **A-D** hub (**Steward / Engineer / Strategist / Capitalist**) is the **Coffee Hub Menu**. **Conductor** is separate and routes directly by conductor name: `toscanini`, `furtwangler`, `karajan`, `kleiber`, or `bernstein`. Bare `conductor` is incomplete and should ask for one of those names. Once a conductor name resolves, emit the **Conductor Action Menu**: four movement-labeled **A-D** repo-grounded next moves; see [CONDUCTOR-PASS - Conductor action MCQ](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md#conductor-action-mcq). Layer map: [CONDUCTOR-LAYER-MAP.md](../../../docs/skill-work/work-coffee/CONDUCTOR-LAYER-MAP.md).

## Guardrails

- Do not turn `coffee` into a heavy maintenance ritual by default.
- Do not overload each run with every possible obligation or stale thread.
- Prefer a small number of salient next paths over exhaustive review.
- Keep the operator in the position of renewed agency, not procedural burden.
- `coffee` is for orientation; heavier consolidation belongs to `dream`.
- This is read-only planning. Do not merge or stage just because the warmup mentions candidates.
- If integrity fails, surface that before optional improvements.
- **Contextual stewardship:** Agents have no cross-thread institutional memory; authority for the Record is **on-disk files + gated pipeline** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â not model recall or chat summary.
- **Encoded workflow first:** Before giving generic elicitation, ad hoc process advice, or a fresh workaround, check whether the repo already defines a coded ritual for the task. If it does, route through that path first.
- **Deviation rule:** Only improvise when the coded path is missing, broken, or explicitly out of scope, and say why you are deviating.
- **Canonical examples:** Bookshelf knowledge should route through shelf anchor -> MCQ -> strictness pick -> gate. Governed Record changes should route through stage -> approve -> process. Root-layout migration should repair path assumptions rather than invent compatibility directories.
- **Strategy-codex deprecation guard:** Do not route active coffee or Steward work through `companion-self` template sync or Grace-Mar-vs-template reconciliation unless the operator explicitly asks for that legacy/archive lane. Bare **A. Steward** means strategy-codex-native gate, boundary hygiene, integrity, or git/ship work.

## Relation to dream

`coffee` and `dream` form a biological-cognitive pair:
- **`coffee`** = repeated framing dose (many per day)
- **`dream`** = end-of-day consolidation pass (usually once)

`coffee` should feel like a sip. `dream` should feel like sleep. See `.cursor/skills/dream/SKILL.md` ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§ *Cadence choreography* for the day's sequence and data handoff.

<a id="conductor-only-no-coffee"></a>

## Conductor session (outside `coffee` hub menu)

Use this path when the operator wants **Conductor** without going through the coffee hub.

The **five masters** (**Toscanini**, **Furtw?ngler**, **Karajan**, **Kleiber**, **Bernstein**) are **not** listed as separate lines on the **`coffee`** hub. Call masters **directly** (this section) when **`coffee`** was not opened or when the operator prefers **`conductor`** / master name instead of **`coffee`**.

**Triggers (examples):** master name or prefix (**`toscanini`**, **`furtwangler`**, **`karajan`**, **`kleiber`**, **`bernstein`**), **`conductor`** with optional fragment, or plain language (**"Toscanini pass"**, **"run Kleiber on the notebook"**). If intent is unclear, ask once. **Legacy:** bare **`D`** + fragment still resolves like a conductor turn when the message is clearly conductor-only (no **`coffee`**).

**First-turn activation note:** bare conductor slugs like **`toscanini`**, **`furtwangler`**, **`karajan`**, **`kleiber`**, and **`bernstein`** should route straight into Conductor on the first command, not be treated as ambiguity.

**Do not** run `operator_coffee.py`, **do not** paste work-start or closeout **Step 1** output, and **do not** lead with **Recent rhythm** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â unless the same message also says **`coffee`** or **`hey`**.

**Standalone Conductor** (no **`coffee`** in this turn): if a conductor name or unambiguous prefix is present, resolve it by name. If only bare **`conductor`** is present, ask once for one of `toscanini`, `furtwangler`, `karajan`, `kleiber`, or `bernstein`; do not show lettered master choices.

**After `conductor=<slug>` resolves** (standalone pick only): deliver the **short** orientation in [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md) and [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../../../codex/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md). **Then, always** deliver the **Conductor action MCQ** - **four** movement-labeled **A-D** repo-grounded next moves - per [CONDUCTOR-PASS - Conductor action MCQ](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md#conductor-action-mcq) and [conductor skill](../conductor/SKILL.md). **Skip** the action menu **only** if the operator said **"orientation only"** / **"no action menu"** in the same turn.

**Logging:** `log_cadence_event.py --kind coffee_pick -u strategy-codex --ok --kv picked=conductor conductor=<slug>` (e.g. `karajan`, `toscanini`). **Legacy** lines may still use `picked=D`; both are fine for rollups. **Do not** append a separate **`coffee`** event unless they actually ran `coffee` Step 1.

**Conductor close (optimal loop):** Same as before ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â [CONDUCTOR-CLOSE-TEMPLATE.md](../../../docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-CLOSE-TEMPLATE.md) in **`days.md`** / page **Reflection**, or **`coffee_conductor_outcome`** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â [CONDUCTOR-IMPROVEMENT-LOOP.md](../../../docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md). For auditability, every new outcome line should carry **`conductor=<slug>`** and **`verdict=`**, plus **`notebook_ref=`** or **`falsify=`** (both preferred). If a pass ended without that line, log a repair outcome on the next turn rather than leaving the close implicit.

**Loop surfacing:** When the derived reader finds live pressure, show **Open loops due for revisit** before the Conductor action MCQ via `build_conductor_revisit_block('strategy-codex')`. Keep it advisory, prefer the active lane first, and include the shared **`Tension`** subsection when multiple streams disagree on the same horizon.

**After the reply:** return to **normal workflow** unless the operator says **`stay in coffee`** or **`coffee`**.

<a id="hub-e-auto-continue"></a>

**Standalone Conductor continuation:** When the operator chooses a master directly after **`coffee`** Step 1, **`last_logged_conductor`** from cadence (**`coffee_pick`** with **`conductor=`**) is the default resolved slug.

- **If a slug exists:** **Continue that master immediately** ? short orientation + **Conductor action MCQ** for that slug. Do not paste any lettered master-selection row; ask for a conductor name only when switching is requested without a name.
- **If no slug exists:** prompt once for a conductor name (`toscanini`, `furtwangler`, `karajan`, `kleiber`, or `bernstein`) ? do **not** invent a default and do **not** show lettered master choices.

Optional **one line** after auto-continue prose: *Say a conductor name to switch.*

**Letter-collision:** If both the **coffee hub** and a **Conductor action MCQ** appear in one reply, **label** them explicitly. The coffee hub no longer has an E slot, so never use bare **`pick E`** at the coffee level. If Conductor is being invoked, say that directly and name the menu ([CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md)).

---

## "Coffee" = start here (two steps)

When the operator begins with **`coffee`** (or clearly the same intent; legacy **`hey`** still counts), treat it as opening a **coffee session**.

### Step 0 ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Recent rhythm (before Step 1 scripts)

**Read first** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â `operator_coffee.py` appends a new **`coffee`** line at the **end** of a successful run, so the log must be read **before** those commands if the rhythm read is to exclude this session.

1. Open **`docs/skill-work/work-cadence/work-cadence-events.md`**. Below `_(Append below this line.)_`, collect lines matching `- **YYYY-MM-DD HH:MM UTC** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â kind (user) ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¦`.
2. Take the **last 4** such lines already in the file. If there are fewer than four, use what exists; if none, **Recent rhythm:** _(no prior events)_ in the reply.
3. **Synthesize in plain prose** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â **2ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“4 short sentences** for a human, **not** a telemetry dump: **do not** lead with a wall of `key=value` pairs. **Companion-facing UX:** label this block **Recent rhythm** (or prose only); **do not** put **dates, UTC, or clock times** in this prose (use order and light anchors like ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œafter dream,ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œthen bridge,ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œearlier todayÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â without timestamps). **Must anchor in specifics** from those four lines ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â name what actually happened (e.g. **bridge** with **commit refs** if present, **coffee** **work-start** vs **standard**, **coffee_pick** / **conductor** when present, legacy **`thanks`** **park** text when non-empty, **dream** pass/fail or integrity/governance in ordinary words, **harvest** packet vs not). **Avoid** generic process filler that could apply without reading the file. Do **not** paste raw log lines unless they are already very short.

   **Cadence voice:** Follow the **cadence voice principle** ([work-cadence README](../../../docs/skill-work/work-cadence/README.md#cadence-voice-principle-all-rituals)). Lead with *felt* acknowledgment of what was settled or decided, end with the **optimal next direction**. Use **"we"** framing. The operator should feel **seen, grounded, and ready** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â not debriefed. Name what was learned or decided, not what was executed. No commit hashes, no process names ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â warm, direct, future-facing.
4. In the reply, place **Recent rhythm:** at the **top** of Step 1 content (immediately before script output / warmup paste). Same rule for **signing-off** Step 1 (before `operator_coffee.py --mode closeout` or handoff-only flow).

If the file is missing or empty below the anchor, state that under **Recent rhythm** and continue Step 1.

### Step 1 ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Automated actions (one flow, two weights)
### Strategist C â€” decision framing and next move
**Detect intent**
**Operator intent (strategy-codex default):** **coffee â†’ C â€” Strategist** does **not** auto-run daily brief and does **not** auto-offer archived Tri-Frame. It presents exactly three strategic options:

- **A. I will identify the real decision hiding inside the request so we stop solving the wrong problem.**
- **B. I will weigh the strongest paths and the tradeoff that matters most so the choice is easier to make.**
- **C. I will recommend the best next move and the reason it wins so you can act without second-guessing.**

**C-A Civ-mem bridge scan** owns the grounding pass: identify the live civ-mem spine, the memory cues that matter, and the constraint map that should stay visible.

**C-B Abundance-pack OS** owns the packaging pass: convert the grounded prompt into an abundance-pack-ready shape without losing the operator's real constraints.

**C-C Bridge idea pack** owns the combined pass: civ-mem first, abundance-pack OS second, then a compact bridge pack with the best next move.

If **C-C Bridge idea pack** is blocked by tacit operator judgment, offer one bounded skill-elicitation checkpoint and then return to the bridge path. Do not ask elicitation questions from the coffee hub itself. Archived Tri-Frame minds **Barnes â†’ Mearsheimer â†’ Mercouris** stay in the legacy reference docs, not the live coffee C first screen.
**Signing-off Step 1** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â handoff-weighted (same trigger **`coffee`**, not a second ritual name):

```bash
python3 scripts/operator_coffee.py -u strategy-codex --mode closeout
```

Or directly: `python3 scripts/operator_handoff_check.py -u strategy-codex`. Include the output in your reply. Add a **short paragraph**: what moved today, what is parked, gate + Jiang carryovers, suggested re-entry prompt. Full spec: [`.cursor/skills/handoff-check/SKILL.md`](../handoff-check/SKILL.md).

If the operator **explicitly** wants **both** full warmup **and** signing-off in one message, run work-start then append handoff (rare).

Add `--compact` for shorter harness output. Individual scripts (`operator_daily_warmup.py`, `harness_warmup.py`, `operator_handoff_check.py`, `operator_reentry_stack.py`) are still available.

**Dream handoff:** If `dream` ran overnight, the daily warmup includes a last-dream block from `last-dream.json` (**"Last dream (night handoff)"** when there is something to read out, or a **one-line "quiet handoff"** when `integrity` / `governance` / digest counts are clean and there are no followups). A successful dream may add **`last_coffee_echo`**: a single warm line (from the 24h cadence rollup) that ties yesterdayÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾Ãƒâ€šÃ‚Â¢s `coffee` into morning startupÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â**cadence / runtime only**, not Record. **Signal days** (issues, followups, or non-zero digests) still use the fuller collapsed block. Extra lines (civ-mem summary, coffee 24h rollup) are **off** by default; tune `config/context_budgets/coffee.json` or pass `--show-civ-mem` / `--show-rollup` on `operator_daily_warmup.py`, `operator_coffee.py`, or `operator_reentry_stack.py`. After that block (or alone if the Last dream section is turned off), warmup prints one line **`Dream ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ coffee menu:`** mapping dreamÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾Ãƒâ€šÃ‚Â¢s suggested execution path to **A / B / C** (**Steward / Engineer / Strategist**) ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â operational hint only; see [dream/SKILL.md](../dream/SKILL.md) ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§ *Five-second closeout*. Approximate paste footprint: `python3 scripts/audit_context_tax.py -u strategy-codex`. These files are operator scaffolding, not Record. For full paths / snippets / followups, use **`--verbose-dream`**. When pasting warmup for the operator, prefer **collapsed** unless they ask for detail.

**Step 1 deliverables (work-start):** Warmup brief (priorities, gate, work-politics snapshot where relevant, integrity), branch snapshot, daily brief + intel defer line (path pattern + **menu C ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Strategist** when ready), optional PH/Jiang line. **No** Polymarket / poll / Massie blocks in Step 1 unless the operator explicitly asked in the same message.

**Memory observability:** `operator_coffee.py` may print a single **`Memory observability:`** line after lane hints when the derived continuity dashboard is `watch`, `stale`, or `missing`. Do not paste the full dashboard into coffee. If the line is absent, treat memory observability as quiet/ok for this run. The dashboard is WORK-derived only; it does not edit MEMORY, the Record, or the gate.

**Step 1 guardrail:** Stay read-only ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â no merge/stage unless they switch lanes or use a pipeline phrase ("we ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¦").

**Done when:** Script output is Step 1 context only. The assistant-facing reply is not complete until Recent rhythm is at the top and the full **Coffee Hub Menu - Reply A-D** follows immediately. Do not end a `coffee` turn with only script output, a recommendation summary, or a smoke-check summary unless the operator explicitly asked for no menu.

For cadence tables and explicit phrase definitions (`coffee light`, `coffee minimal`, `coffee survey`): see [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md).

### Multiple coffees per day

The operator may say **`coffee`** **more than once per calendar day** for reorientation. This is normal. Each new `coffee` runs Step 1 again and starts a new **A, B, C, D** cycle. If **`coffee`** arrives mid-hub, treat it as a **reorientation restart**: run Step 1 again, then offer a fresh menu.

<a id="coffee-step-2-hub"></a>

### Step 2 ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Hub menu (four lines only)

Immediately **after** Step 1 content, output the **hub** menu ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â **four lines** (**AÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“E**).

**One option per line:** Each hub letter is **its own line** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â **`A.` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¦ `E.`** as **four separate lines**, not multiple letters on one line and not a single paragraph listing AÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“E. (Sub-menus inside **D** **Capitalist** forks or **Steward** branches are separate from this rule when you open a follow-up.)

**Letter-collision:** There is no conductor chooser. The only live conductor letters are the resolved **Conductor Action Menu** (**A-D**). When both a Coffee Hub Menu and a Conductor Action Menu could appear in one reply, **label** them explicitly; see [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md).

**Do not** append any lettered masters row under the four hub lines; conductor stance belongs to named Conductor turns ([Conductor session](#conductor-only-no-coffee), [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md)).

**Do not** add micro-hints, fork shorthand, or F/G/Xavier/Dev tags **under** the hub list.

**Hub menu (example):**

```
A. Steward
B. Engineer
C. Strategist
D. Capitalist ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â <one short line: work-business / grace-gems / commercial angle / bookshelf product or teaching use>
<!-- Conductor is standalone only and does not appear as a coffee hub letter. -->
```

**Hub lines end at D:** the coffee hub is four lines only. Conductor is standalone and does not appear as a coffee hub letter.

**Filling D ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Capitalist:** **work-business**, **grace-gems**, revenue/offers framing; **work-cici** when business/teaching-commercial; one prescribed next step. Bookshelf belongs here only when the use is **commercial / teaching / product packaging**. **Self-knowledge elicit knowledge** belongs under **C ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Strategist**.

**Capitalist ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â bookshelf / product use:**

- Bookshelf may support offer design, teaching angles, grace-gems packaging, course/product framing, or public copy.
- Do **not** use D as the default route for IX-A bookshelf recursion; route that to **C ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Strategist ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ B. Elicit knowledge**.
- **Catalog stance membrane** (`bookshelf-membrane-round.json` + `build_bookshelf_membrane_candidates.py`) remains secondary and scripted: use it only when the operator requests catalog organization or a pressing organizational membrane issue applies.

**Fixed option (Capitalist angle, hub line wording):** may read **Bookshelf product/teaching angle** or **Bookshelf stance membrane (scripted)** when those commercial or catalog intents are live.

**Catalog stance membrane (scripted path only ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â branch 2 above):**

- Session is **multi-round**: 5ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“10 MCQs per round when using the scripted stance round artifact.
- After each round, ask continue/stop.
- On stop, produce:
  - `docs/skill-work/work-strategy/history-notebook/research/BOOKSHELF-MEMBRANE-REPORT.md`
  - `docs/skill-work/work-strategy/history-notebook/research/BOOKSHELF-MEMBRANE-CANDIDATE-DRAFTS.md`
- Output is draft-only; no direct writes to `recursion-gate.md` unless explicitly requested.

**Write-shaped** work is **not** an extra letter ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â it defaults under **D** when skill-write/commercial, or when the operator says **`write`** / **`skill-write`** without **`coffee`**. State it plainly in the angle-bracket line; **do not** add a separate ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œmicro-hintsÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â row.

**Standalone Conductor:** the coffee hub ends at D. Direct Conductor activation uses a master name, `conductor`, or the standalone conductor skill.

**Step 1 context for B / D:** `operator_coffee.py` prints **`Lane context (for hub B / D ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Engineer & Capitalist hints)`** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â two lines from `scripts/coffee_lane_next_hints.py` (work-cici + work-dev). Use when choosing **B**, **D**, or when wording those lines.

**Step 1 context for standalone Conductor:** After lane hints, `operator_coffee.py` prints the four-line coffee hub only; Conductor is handled separately.

**Default recommendation line:** Step 1 may print `Session load: ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¦ (recommended: X)` and `Recommended default: X ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â say "go" to accept, or pick another hub letter.` (**A** / **B** / **C**). When present, surface that recommended default once before or after the hub menu. The fixed hub menu still remains five lines only. For **Conductor** emphasis outside the hub, say **once** that **`conductor`** / master name works **without** opening **`coffee`** ([ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§ Conductor session](#conductor-only-no-coffee)). **Not** micro-hints under the hub list.

**Quick reference (modes):**

- **A. Steward** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â **Governance membrane:** **gate** \| **boundary hygiene** \| **integrity/exports** \| **git/ship**. **Default if the operator says `A` only:** **gate** if pending candidates; else **git/ship** when worktree or branch state is the live pressure; else **boundary hygiene**. **`A integrity`** / **`A git`** / **`A ship`** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ that track; **`A both`** / **`A all`** as in [menu-reference ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Steward](../../../docs/skill-work/work-coffee/menu-reference.md#ah-table). Gate merges never without companion **approve** + `process_approved_candidates.py`. Template-sync work is legacy/archive-only unless named explicitly. *(Legacy hub letter **B**.)*

- **B. Engineer** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â **work-dev + skills/meta** (not git/ship or full membrane audits ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â those are **A**): `docs/skill-work/work-dev/` + [work-dev-sources.md](../../../docs/skill-work/work-dev/work-dev-sources.md); **skills / meta** when **`skills`** / **`meta`** with **B**. **work-cici** ops when engineering-shaped. **When hub B is chosen:** After **one short orientation line**, deliver **Engineer next moves** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â **3ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“5 options** labeled **A through E** (**or AÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“D** if four), **each option its own line**, under an explicit heading such as **`Engineer menu ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â reply AÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“E`** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â **not** `B1`ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“`B5` and not unlabeled lists. Each new submenu **restarts letters from A**; disambiguate from the **Coffee hub** with the menu title (same idea as **letter-collision** labeling for Conductor action MCQ vs hub). Each line is a **repo-grounded** plausible next step (work-dev wedge, script, CI, **skills** path) ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â **enumeration only** until the operator picks. Use Step 1 **`Lane context (for hub B / D)`** and [workspace.md](../../../docs/skill-work/work-dev/workspace.md) ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§ **Next actions** when helpful. **Detail:** [menu-reference ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§ Engineer (B) ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â detailed scope](../../../docs/skill-work/work-coffee/menu-reference.md#build-b--detailed-scope) *(legacy letter **Build** / old hub **A**).*

- **C. Strategist** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Opens exactly three bridge options and nothing else. Do **not** auto-run the daily brief or auto-offer archived Tri-Frame before this submenu. Output:
  - `Strategist menu ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â reply AÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“C`
  - `A. Intel ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â daily brief / current-events watch`
  - `B. Elicit knowledge ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â self-knowledge MCQs ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ IX-A candidates`
  - `C. Bridge idea pack ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â civ-mem first, then abundance-pack OS; return three bridge ideas and one recommended next move`

  **C-A Civ-mem bridge scan** owns the daily brief path: generator and/or `daily-brief-YYYY-MM-DD.md`, **ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§1d** / **ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§1e** / **ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§1g** / **ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§1h** (PRC / IRI when load-bearing), optional **KY-4** (Polymarket, polls, Massie X per cadence), and optional **`last30days` frontier check** when the operator wants one fresh, source-dated scan for today's inbox. Do **not** auto-run `last30days` from coffee Step 1 or merely because C-A is opened; offer or run it only when the operator chooses Intel and the frontier is stale / explicitly requested. Output remains a short brief + optional `daily-strategy-inbox.md` one-liner, not a `days.md` / thread / gate edit. **C-B Abundance-pack OS** uses [.cursor/skills/elicit-knowledge/SKILL.md](../bookshelf-knowledge-mcq-to-gate/SKILL.md): default **6** source-bound, topic-anchored MCQs from `bookshelf-quiz-anchors.yaml`, with academic inline citations visible to the operator and hidden `self-library-bookshelf` receipts in the gate, **at most two** date-primary stems, strictness default **top2**, and stage candidates only through `recursion-gate.md`; never merge without approval. **C-C Bridge idea pack** owns the next `hn-*` selection and neutral-spine setup for History Notebook / Predictive History. If the operator wants a full synthesis pass after the spine is chosen, use [daily-brief-minds-menu.md](../../../docs/skill-work/work-strategy/daily-brief-minds-menu.md) and the polyphony workflow. When C-C is blocked by ambiguous stream ownership, page shape, raw-input routing, or civ-mem lens choice, offer one bounded `skill-elicitation` checkpoint; do not run it automatically and do not add another coffee hub option. **Companion survey** still lives under C when invoked by `coffee survey`. *(Legacy hub **C ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Strategist (bridge pack)**.)*

- **D. Capitalist** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â **work-business**, **grace-gems**, revenue/offers; **work-cici** when business/teaching-commercial angle; bookshelf only for commercial / teaching / product packaging or scripted catalog stance membrane; **not** IX-A bookshelf recursion. **One** prescribed next step.

- **Conductor** ? standalone only; not part of the coffee hub.

**Composition benchmark note:** Coffee only routes to Conductor/Kleiber; it does **not** run benchmarks directly or add a standalone benchmark hub item. In V1, Strategy-codex composition benchmarks run only from the resolved **Kleiber** Conductor Action Menu as fixed **D. Finale** (`Run composition benchmark`) per [kleiber-composition-benchmark.md](../../../docs/skill-work/work-dev/kleiber-composition-benchmark.md).

**Exit / re-offer:** After **A**, **B**, or **D**, re-offer the full **coffee** hub **A?D** after the current branch settles. If a standalone Conductor turn was opened, stay on the Conductor track rather than re-offering coffee in the same reply. After **C**, exit to normal workflow unless **`stay in coffee`**. After **A** (Steward), see [menu-reference ? Steward follow-up fork](../../../docs/skill-work/work-coffee/menu-reference.md#steward-follow-up-fork-implement-now-vs-later) *(legacy docs may still say **B** for Steward ? read **A**).* Synonyms **`A+ship`** / **`EXECUTE`** ? **Implement now** on steward track. **Decision-fatigue rule:** after a hub branch opens one submenu, the next assistant turn should execute the selected item, recommend one default, or report the blocker rather than opening another broad menu.

Legacy **AÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“G** detail tables in [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md) still describe **workloads**; map letters: old **Daily Brief ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ C-A Civ-mem bridge scan**, old **self-knowledge elicit knowledge ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ C-B Abundance-pack OS**, old **Book / Jiang / Predictive History â†’ C-C Bridge idea pack**, **Build ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ B**, **Steward ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ A**, commercial / teaching bookshelf uses ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ **D**, and **Symphony conductors ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ E** on hub after **`coffee`**, or **standalone** **`conductor`** / master name without **`coffee`**.

**Done when:** The operator has picked **AÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“E** (or combo), the selected branch has been executed, and the re-offer or exit rule has been applied.

---

## Session trail (optional)

Sessions begin when the operator says **`coffee`** (optional modifiers). To keep a trail: use **`session-transcript.md`** and/or append dated bullets to **`docs/skill-work/work-*/*-history.md`**. **Not** the gated Record; **not** `self-memory`. See [work-menu-conventions.md](../../../docs/skill-work/work-menu-conventions.md).

<a id="cadence-audit"></a>

## Cadence audit

Each successful coffee run appends one line to `docs/skill-work/work-cadence/work-cadence-events.md` via `scripts/log_cadence_event.py`. This is automatic ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â no operator action required. The line always includes **`cursor_model=ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¦`** (audit parity with bridge/harvest **Agent surface**): set **`CURSOR_MODEL`** in the environment, or pass **`--cursor-model "ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¦"`** to `operator_coffee.py`, using the model name from the Cursor UI. If unset, **`unknown`**.

**After the operator states their menu letter** (and steward track if **A**), the assistant may append a **`coffee_pick`** cadence line (same file) for rollup:
`python3 scripts/log_cadence_event.py --kind coffee_pick -u strategy-codex --ok --kv picked=A steward=gate --cursor-model "<from Cursor UI>"`
(`steward=` only when `picked=A`; values: `gate`, `boundary`, `integrity`, `git`, `both`, or `all`; legacy logs may contain `template`.) For **hub** picks: **`picked=A`..`D`**. For **Conductor sessions** outside hub letter picks: **`picked=conductor`** with **`conductor=<single-slug>`** ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â **no** `+` in new logs. Legacy files may still contain **`picked=D`** + `conductor=` or older shapes. **Optional closure after a conductor run:** `python3 scripts/log_cadence_event.py --kind coffee_conductor_outcome -u strategy-codex --ok --kv verdict=watch conductor=kleiber notebook_ref=docs/path.md` (see [CONDUCTOR-IMPROVEMENT-LOOP.md](../../../docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md) ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â§ 3 for `notebook_ref` / `falsify` examples). Optional: `scripts/log_operator_choice.py --context COFFEE --picked A` for `session-transcript.md`.

## Related files

- `docs/skill-work/work-cadence/README.md` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â **Cadence choreography** (ordering, handoffs, Step 0 recent rhythm window depths, harvest vs triad)
- `docs/skill-work/work-coffee/README.md` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â territory rationale and boundaries
- `docs/skill-work/work-coffee/menu-reference.md` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â cadence, survey track, signing-off add-ons; legacy **AÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“G** workload tables (map to the current coffee Step 2 above)
- `docs/skill-work/work-coffee/work-coffee-history.md` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â lane breadcrumbs
- `docs/skill-work/work-cadence/work-cadence-events.md` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â per-run cadence telemetry
- `.cursor/skills/dream/SKILL.md` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â night-side counterpart
- `.cursor/skills/thanks/SKILL.md` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â **`thanks`** **deprecated** for the single-operator workflow; prefer **conductor** or **`coffee` light/minimal`
- `docs/skill-work/work-politics/polling-and-markets.md` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â KY-4 polling (**menu C ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Strategist** / daily brief)
- `docs/skill-work/work-strategy/daily-brief-minds-menu.md` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â archived Tri-Frame **three minds** (Barnes / Mearsheimer / Mercouris) for **C ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Strategist** second stage
- `docs/skill-work/work-politics/america-first-ky/guardrail-stress-test.md` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â messaging discipline
- `.cursor/skills/elicit-knowledge/SKILL.md` ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â **C ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â Strategist / Elicit knowledge** MCQs toward IX-A / gate staging
