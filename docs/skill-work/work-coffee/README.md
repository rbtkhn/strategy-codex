# work-coffee

**Purpose:** Operator cadence, activation, re-entry, signing-off (merged into **`coffee`** Step 1 + **A-D** hub), and workflow-state design for strategy-codex's `coffee` ritual. **Standalone Conductor** remains available without `coffee` by conductor name (`toscanini`, `furtwangler`, `karajan`, `kleiber`, or `bernstein`) or **`conductor <name>`**; bare **`conductor`** asks for a name. This territory is where the system explains and evolves the ritual architecture. The executable trigger surface lives in [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md).

**Deprecation guard:** `companion-self` template sync and Grace-Mar-vs-template reconciliation are legacy/archive concerns in strategy-codex. They do not belong to the default coffee Steward path unless the operator names that obsolete migration lane.

**Not** Record truth. **Not** MEMORY. **Not** a second merge path. **Not** generic repo hygiene, and **not** a broad health/caffeine territory. `work-coffee` is a WORK lane for ritual architecture and operator ergonomics.

## Conductor Stack At A Glance

- **Compression path (active):** [CONDUCTOR-COMPRESSION-SPEC.md](CONDUCTOR-COMPRESSION-SPEC.md) — coffee hub + attention phrases + extended `coffee_close`; compress standalone conductor ritual in phases.
- **Continuity:** `dream_coffee_rollup.py` remembers what is still warm enough to matter next.
- **Observability:** `build_work_pass_ledger.py` shows work-pass closes over a review window (`build_conductor_ledger.py` = deprecated shim).
- **Durable learning:** [recursive-learning-journal.md](../../../statecraft/recursive-learning-journal.md) + [recursive-learn skill](../../../.cursor/skills/recursive-learn/SKILL.md) record machine law; [conductor-arc-impact-journal.md](../work-strategy/conductor-arc-impact-journal.md) scores conductor arc generalization.

Fast doorway:
- overview and rationale: [README.md](/C:/dev/strategy-codex/docs/skill-work/work-coffee/README.md)
- one-glance map: [CONDUCTOR-LAYER-MAP.md](/C:/dev/strategy-codex/docs/skill-work/work-coffee/CONDUCTOR-LAYER-MAP.md)
- portable pass shape: [CONDUCTOR-PASS.md](/C:/dev/strategy-codex/docs/skill-work/work-coffee/CONDUCTOR-PASS.md)

---

## Role

| Role | Description |
|------|-------------|
| **Cadence architecture** | Defines work-start vs signing-off **Step 1** weight, **one** fixed **`coffee` hub** (**A-D**: Steward, Engineer, Statecraft, Singularity), **standalone name-only Conductor** sessions, re-entry behavior, and cadence modifiers. |
| **Operator activation** | Holds the rationale for why the `coffee` ritual exists: activation, rhythm, state shift, and workflow dopamine replacement. |
| **Boundary surface** | Explains what belongs in WORK-only docs/history versus what must escalate to `RECURSION-GATE` or change review. |
| **Session trail guidance** | Clarifies how `session-transcript`, `work-*-history.md`, and `memory` relate without collapsing into one another. |

---

## Relationship to `coffee`

- **`coffee` skill** = executable ritual contract, trigger behavior, and exact coffee-menu semantics.
- **`work-coffee` territory** = prose home for rationale, boundaries, history, and evolution of the ritual.

This split is intentional:

- the skill should stay optimized for invocation and agent behavior
- the territory should hold the longer-form doctrine and lane-specific history

**`coffee` C - Statecraft** now opens a WORK-only repo-root [statecraft](../../../statecraft/README.md) router-first entry: **A. Deploy**, **B. Compact**, **C. Speaker-Bridge**, and **D. Lane Direct**. The second lane menu appears only after **D**, where **A. America**, **B. China**, **C. Persia**, and **D. Russia** remain the direct lane choices. After that lane pick, the next honest submenu is transcript-grounded intake, not an immediate jump to `helix`, `state`, `bridge`, or `transactions`. Agents should **not** auto-run the daily brief, `check streams`, bookshelf elicitation, or archived Tri-Frame before this submenu. Those remain explicit named routes unless the operator asks to convert source material into a statecraft instrument.

Named follow-on: after **C. Statecraft**, the operator may also invoke **`civ-state`** directly to open the upstream CIV-STATE analysis bench ([civ-state skill](../../../.cursor/skills/civ-state/SKILL.md); legacy alias: `statecraft civ-state`). That command is for `Frame / Retrieve / Promote / Review`, not default lane drafting and not default book-writing.

**Symphony / Conductor:** Conductor is standalone name-only; strategy-notebook cadence lives in [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) + [CONDUCTOR-PASS.md](CONDUCTOR-PASS.md). Invoke by conductor name, **`conductor <name>`**, or [conductor skill](../../../.cursor/skills/conductor/SKILL.md) without opening **`coffee`** when preferred.

### Why the conductor stack helps

The conductor stack exists so the system can do three different human jobs without confusing them:

- **continuity** - remember what was just alive enough to matter next
- **observability** - measure the pattern of picks, closes, and falsifiers over time
- **durable learning** - decide what the system actually learned and whether that lesson generalized

In repo terms:

- `dream_coffee_rollup.py` is the warm handoff surface
- `build_work_pass_ledger.py` is the derived review surface (`build_conductor_ledger.py` = deprecated shim)
- `recursive-learning-journal.md` + [recursive-learn skill](../../../.cursor/skills/recursive-learn/SKILL.md) is the machine-law surface
- `conductor-arc-impact-journal.md` is the conductor arc scoring surface

This matters because a system that mixes those jobs becomes hard to trust. It either overstates a warm impression as truth, or buries a useful human lesson inside raw counters.

---

## Gate Threshold

`work-coffee` is **WORK-only by default**.

Keep changes in docs/history only when they are about:

- menu wording or ergonomics
- pacing and rhythm
- re-entry patterns
- `stay in coffee` behavior
- warmup or signing-off Step 1 phrasing
- operator workflow preferences

Stage to **`recursion-gate.md`** only when a `work-coffee` insight would change governed behavior, such as:

- companion-facing museum knowledge section B / museum knowledge section C intake
- durable prompt or policy behavior
- approved survey/cadence structures that alter Record intake
- enduring governance changes that should not live as docs only

Use **change review first** when the change is architectural or cross-surface, for example:

- it revises how multiple governed systems relate to each other
- it changes the boundary between WORK, MEMORY, and the Record
- it changes more than one durable governance surface at once

This territory never creates a second merge path. `RECURSION-GATE` remains the membrane, and companion approval remains required before any governed merge. See [AGENTS.md](../../../AGENTS.md).

---

## Candidate shape when escalation is warranted

When a `work-coffee` insight should stage a gate candidate, prefer:

- `source: operator â€” work-coffee`
- `signal_type: operator_cadence_refinement`
- literal `source_exchange` from the operator session that motivated the change

Default rule: if the insight is still primarily about operator preference or ritual tuning, keep it here in WORK. Escalate only when the ritual implication becomes durable governed behavior.

---

## Continuity and trail

`work-coffee` does **not** replace any existing continuity surface.

- **Raw continuity:** `session-transcript.md`
- **Lane breadcrumbs:** `docs/skill-work/work-coffee/work-coffee-history.md`
- **Optional continuity memory:** `memory.md`
- **Governed durable changes:** `recursion-gate.md`

Per [work-menu-conventions.md](../work-menu-conventions.md) and [work-modules-history-principle.md](../work-modules-history-principle.md), `coffee` sessions may leave WORK-choice trails and per-lane breadcrumbs, but those are not Record truth.

---

## Adjacent surfaces

- [operator-session-review-checklist.md](operator-session-review-checklist.md) â€” session UX / procedure verification (manual + pytest pointers).
- [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md)
- [work-menu-conventions.md](../work-menu-conventions.md)
- [work-dev/git-branch-hygiene.md](../work-dev/git-branch-hygiene.md)
- [work-strategy/README.md](../work-strategy/README.md)
- [work-politics/polling-and-markets.md](../work-politics/polling-and-markets.md)
- [work-companion-self/README.md](../work-companion-self/README.md)

---

## Conductor semantics (machine)

Mechanical helpers (continuity from recent picks plus recommendation from dream + session load) live in
[`scripts/cadence_conductor_resolution.py`](../../../scripts/cadence_conductor_resolution.py).
Human contract and menu order: [CONDUCTOR-PASS.md](CONDUCTOR-PASS.md).

Run the illustration tests:

`python3 -m pytest tests/test_conductor_coffee_illustration.py -k illustration -v`

---

## Scope boundaries

In scope:

- operator cadence design
- activation rituals
- work-start / signing-off (merged into one fixed coffee flow; treaty/policy/negotiation drafting lands under **C - Statecraft**; singularity-academy activation lands under **D - Singularity**; Rome / Jiang / notebook synthesis, museum identity knowledge (archive) bookshelf quiz, skill-write, and commercial slices route by explicit request outside the coffee hub unless converted into statecraft output; Conductor is standalone by name; see [coffee SKILL](../../../.cursor/skills/coffee/SKILL.md))
- reorientation and multi-`coffee` behavior
- survey/cadence workflow design
- relationship between hub flow and territory execution

Out of scope:

- broad health or caffeine optimization
- generic git/repo hygiene as a standalone territory
- work-politics content itself
- work-dev integration doctrine itself
- Record merges or prompt edits without the gate

