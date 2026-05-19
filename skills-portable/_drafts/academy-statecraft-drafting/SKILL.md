---
name: academy-statecraft-drafting
preferred_activation: academy-statecraft
description: "Draft workflow for turning speaker-state and historical statecraft discipline into treaties, policy papers, negotiation briefs, crisis memos, and four-lane crisis transaction bundles. Use for academy-statecraft, state-russia/state-china/state-iran/state-america, crisis transaction, four-lane transaction, do it again, make it concrete, settlement spine, civilization / empire, and Richelieu/Bismarck prompts."
portable: true
version: 0.1.0-draft
tags:
  - draft
  - work-strategy
  - statecraft
  - drafting
  - speaker-state
---

# Academy statecraft drafting

Use this draft skill when the operator asks for:

- `statecraft`
- `academy-statecraft`
- `draft a treaty`
- `draft a policy paper`
- `policy paper from speaker state`
- `national lane`
- `state-russia`
- `state-china`
- `state-iran`
- `state-america`
- `Pape index`
- `Mearsheimer scoreboard`
- `Richelieu/Bismarck test`
- `do it again`
- `make it concrete`
- `settlement spine`
- `civilization / empire`

The goal is to convert contemporary geopolitical analysis into a practical instrument: treaty language, policy memo, negotiation brief, sanctions/off-ramp mechanism, crisis brief, or institutional design note.

## Operator trigger points

Treat these ordinary workflow signals as likely statecraft activations:

- **Repeat workflow:** `do it again`, `same for this crisis`, `make another bundle`.
- **Concretize theory:** `make it concrete`, `harden this`, `wire this into statecraft`.
- **Crisis object:** `Hormuz`, `nuclear latency`, `sanctions relief`, `transit guarantee`, `non-regime-change`, `ceasefire`, `regional architecture`.
- **Four-lane comparison:** `compare the four states`, `orthogonality`, `America/Russia/China/Iran`, `settlement spine`.
- **State commands:** `state-russia`, `state-china`, `state-iran`, `state-america`.
- **Speaker-to-instrument:** `Pape says...`, `Parsi argues...`, `Ritter warns...`, or `Crooke frames...` when followed by policy, treaty, compact, framework, clause, or settlement language.
- **Coffee C handoff:** after `coffee` -> `c`, treat crisis or policy language as statecraft unless the operator redirects.
- **Civilizational hinge:** `Richelieu`, `Bismarck`, `Plutarch`, `civilization / empire`, `helix`, `authority / restraint / settlement`.

Routing rule:

- Single state plus crisis object -> draft a lane transaction or brief.
- All four states, `do it again`, `same for this crisis`, or orthogonality language -> draft a four-lane transaction bundle.
- Speaker insight plus policy language -> convert the insight into a statecraft instrument or source-backed transaction input.
- `What did we learn?` after a bundle -> identify method, skill, architecture, or template refinement candidates.

Recent bundles such as `hormuz-transit-sanctions-relief-compact` and `iran-nuclear-latency-recognition-framework` are examples of the pattern, not mandatory templates.

## Crisis object classification

Before drafting a crisis instrument, identify the contested object whose legal or political character drives the game.

Use this compact sequence:

1. Name the contested object.
2. List rival classifications.
3. Mark which classifications create coercion, escalation, or war pressure.
4. Choose the classification that creates settlement space.
5. Convert that classification into the first clause, memo thesis, or negotiation instruction.

Examples:

- Zangezur: road, sovereign transit, extraterritorial corridor, monitored route, military access, customs exception.
- Hormuz: free navigation, blockade, escorted transit, collective guarantee, coercive bargaining chip.
- Nuclear latency: deterrent ambiguity, inspection bargain, recognition claim, sanctions trigger, red-line instrument.

## Core rule

Academy-statecraft synthesizes two inputs:

1. **Contemporary speaker state** - compact current-state analysis from speaker folders, scoreboards, ledgers, helixes, routing notes, and raw-input-backed lanes.
2. **Historical statecraft discipline** - Richelieu for durable state interest and institutional carrier; Bismarck for limited aims, alliance geometry, equilibrium, and restraint.

Every statecraft output must establish historical continuity with the current state form. Separate current government, current state, predecessor institutions, geography, civilizational memory, and possible successor authority. Do not assume regime continuity is the same thing as state continuity.

Canonical PH-CIV / statecraft hinge: **Civilizational pattern and narrative become statecraft only when converted into authority, restraint, and settlement.** Short form: `pattern / narrative -> authority / restraint / settlement`.

Do not produce generic commentary. End with a draftable instrument or a concrete preparation surface for one.

## Start files

Open the statecraft surface first:

- `codex/academy/statecraft/README.md`
- `codex/academy/statecraft/METHOD.md`

Then choose the smallest useful tool:

- National lane: `america`, `russia`, `china`, or `iran`.
- Sheet: national perspective, power metric, Pape index, Mearsheimer scoreboard, or speaker-insight memo.
- Template: treaty framework, policy paper, or negotiation brief.

When historical or civilizational pattern/narrative is invoked, also open `codex/academy/statecraft/sheets/civilizational-pattern-to-statecraft.md`.

## Command aliases

Treat these as direct lane activators:

| command | opens | default posture | output bias |
| --- | --- | --- | --- |
| `state-america` | `codex/academy/statecraft/america/` | America as current U.S. federal actor plus possible successor continental power center. | Bound coercive centers, preserve command legitimacy, avoid overextension, define successor-stable instruments. |
| `state-russia` | `codex/academy/statecraft/russia/` | Russia as security-depth disruptor and multipolar balancer. | Exploit disruption without entrapment, preserve optionality, seek recognition and equilibrium. |
| `state-china` | `codex/academy/statecraft/china/` | China as industrial pole and anti-disorder stabilizer. | Preserve leverage without energy disorder, protect supply chains, use quiet compact design. |
| `state-iran` | `codex/academy/statecraft/iran/` | Iran as coercive-center / denial-power actor seeking legitimated leverage. | Monetize leverage without losing control, preserve dignity, seek sanctions relief and regional architecture. |

When one of these commands appears alone, respond with a compact statecraft brief from that lane unless the operator asks for file edits. When paired with a topic, draft from that lane's point of view. When paired with `compare`, run the mirror test against the other three lanes.

## National lane workflow

Use a national lane when the output should be written from one state's point of view.

1. Open the matching lane:
   - `codex/academy/statecraft/america/`
   - `codex/academy/statecraft/russia/`
   - `codex/academy/statecraft/china/`
   - `codex/academy/statecraft/iran/`
2. Extract the lane's core question, state interest, historical continuity, fear, leverage, constraints, preferred instruments, red lines, and off-ramps.
3. Classify the crisis object if the problem turns on the legal or political status of a route, chokepoint, guarantee, recognition claim, sanction, capability, or authority surface.
4. Separate current-government interests from deeper state or successor-power interests.
5. Pull only the speaker-state inputs needed for the problem.
6. Apply Richelieu and Bismarck checks.
7. Produce the requested artifact.

Do not turn the lane into a country encyclopedia.

## Speaker-state intake

Use speaker state as analytical input, not as authority by itself.

Typical roles:

- **Pape** - forecast clocks, coercive-center leverage, shortage/system pressure, falsifiers.
- **Mearsheimer** - structural realism, balance-of-power incentives, overextension, regional-hegemon logic.
- **Parsi** - diplomacy, off-ramps, settlement architecture, sanctions relief, regional security arrangements.
- **Ritter** - force constraints, operational risk, escalation danger, military feasibility.
- **Crooke** - structural misreading, order rupture, metapolitical context, Western mechanism failure.

Preserve source boundaries. If a claim matters, link or cite the speaker compact state, ledger, helix, interview map, or raw-input-backed surface that carries it.

## Scoreboard choice

Use the scoreboards only when the draft needs power-metric discipline.

- Use `pape-coercive-center-index.md` when the question is: **Who can force the system to reorganize around them under pressure?**
- Use `mearsheimer-structural-realist-scoreboard.md` when the question is: **Who has the structural position, geography, capability base, and balancing environment to survive, expand, deter, or dominate?**

Do not collapse them. The same event can move them in opposite directions.

## Historical checks

Apply both checks before finalizing the artifact.

If an output invokes historical or civilizational pattern/narrative, it must name **authority**, **restraint**, and **settlement** before becoming a statecraft instrument.

**Richelieu check**

- What durable state interest is being served?
- What historical continuity links the current state form to predecessor institutions or successor authority?
- Which institution can carry the policy after leaders or slogans change?
- What administrative, fiscal, legal, military, or intelligence capacity is required?
- Where does ideology hide or distort the state interest?

**Bismarck check**

- What is enough?
- Which adversary must not be unified with another adversary?
- Which ally must be reassured, restrained, or kept neutral?
- What settlement preserves equilibrium after advantage?
- What demand would convert a tactical gain into a strategic trap?

## Output shapes

Choose one concrete output:

- treaty clause or annex;
- policy-paper thesis and recommendation set;
- negotiation brief;
- sanctions or relief sequence;
- alliance architecture note;
- crisis memo;
- off-ramp design;
- warning against overreach.

If the operator asks for brainstorming, produce options but mark which one is most draftable next.

## Verification

Before closing a repo-editing pass:

1. Confirm no Record surfaces were edited.
2. Confirm statecraft links resolve if Markdown was changed.
3. Run `git diff --check -- codex/academy/statecraft` for statecraft edits.
4. If a skill or docs candidate was changed, run `git diff --check` on the touched files.

## Anti-patterns

- Do not produce abstract grand strategy without an instrument.
- Do not import a speaker's whole worldview when one mechanism is enough.
- Do not let a historical analogy replace current incentives.
- Do not treat America as only Washington when the `america` lane is tracking possible successor continental power.
- Do not let Iran-as-coercive-center erase India-as-comprehensive-power comparator.
- Do not promote this draft skill to manifest until it has been reused successfully.
