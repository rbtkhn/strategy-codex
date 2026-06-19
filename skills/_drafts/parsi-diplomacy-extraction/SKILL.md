---
name: parsi-diplomacy-extraction
preferred_activation: parsi-diplomacy
description: "Draft workflow for extracting Trita Parsi's authored and interview claims into disciplined diplomacy architecture: settlement sequencing, sanctions relief logic, ceasefire/Hormuz bargaining, U.S.-Iran constraints, regional security architecture, comparative speaker reads, and statecraft inputs. Use for Parsi says, diplomacy architecture, Iran off-ramp, sanctions relief, regional security framework, Trump-Iran bargaining, and compare Parsi to another speaker."
portable: true
version: 0.1.0-draft
tags:
  - draft
  - work-strategy
  - parsi
  - diplomacy
  - statecraft
  - speaker-state
---

# Parsi diplomacy extraction

Use this draft skill when the operator asks for Parsi-specific extraction, especially:

- `Parsi says`
- `Trita Parsi`
- `diplomacy architecture`
- `Iran off-ramp`
- `sanctions relief`
- `ceasefire sequence`
- `regional security framework`
- `Trump-Iran bargaining`
- `compare Parsi to <speaker>`
- `what can we learn from Parsi`
- `wire Parsi into statecraft`

Goal: extract Parsi's value as a diplomacy and settlement-architecture voice without turning diplomatic possibility into wishful thinking or collapsing authored policy analysis into host-framed interview claims.

## Start files

Open speaker and authored surfaces first:

- `codex/speakers/parsi/README.md`
- `codex/speakers/parsi/parsi-speaker-object.md`
- `codex/speakers/parsi/parsi-helix.md`
- `codex/speakers/parsi/parsi-interview-appearances-2025-2026.md`
- `codex/years/2026/parsi/parsi-forecast-ledger-2025-2026.md`
- `codex/years/2026/parsi/parsi-lane-consolidation-2026-05.md`

Then choose source class:

- **Authored spine:** `substack-parsi-*` and `responsiblestatecraft-parsi-*` for canonical diplomacy mechanism.
- **Interview strand:** host-labeled appearances for live interpretation and pressure testing.
- **X / fast-cycle bundles:** use only when the operator asks for rapid-cycle public-position evidence or corroboration.

## Source boundary

Keep source classes separate:

- **Parsi authored claim:** Substack or Responsible Statecraft by Parsi.
- **Parsi interview claim:** what Parsi says in a host-owned capture.
- **Host framing:** question, title, or host summary.
- **Assistant synthesis:** your settlement mechanism or statecraft conversion.

Do not treat a diplomatic option as feasible just because Parsi names it. Separate desired settlement architecture from actor incentives, enforcement, and sequencing.

## Extraction workflow

1. Search Parsi speaker state, authored ledger, interview map, and raw-input captures with `rg`.
2. Identify the immediate diplomacy claim:
   - ceasefire condition;
   - sanctions relief;
   - sequencing;
   - coercion failure;
   - Trump / Netanyahu / Iranian bargaining constraint;
   - Hormuz or transit bargain;
   - regional security architecture;
   - U.S. interest versus Israeli escalation;
   - implementation versus symbolism.
3. Extract source evidence by default.
4. Separate architecture from advocacy.
5. Add enforcement, incentive, and spoiler checks.
6. Add falsifiers and revisit triggers.
7. Convert the reusable lesson into statecraft transaction input, negotiation brief, treaty clause, or speaker-state note.

## Source-illustrated answer default

When the operator asks what Parsi says, what diplomatic path exists, or how to use a Parsi claim, include source evidence by default.

Minimum useful shape:

- **Claim:** one sentence naming the diplomatic mechanism.
- **Excerpt:** a short exact excerpt from authored or transcript capture, with file and line citation.
- **Architecture:** who gives what, in what order, under what verification or enforcement condition.
- **Spoiler:** who can break it and how.
- **Use:** one sentence naming the statecraft, transaction, treaty/policy, or crisis-test application.

Rules:

- Prefer authored excerpts for durable diplomacy architecture.
- Prefer interview excerpts for live crisis interpretation or current bargaining posture.
- Choose high-density sentences that carry the point themselves.
- Keep exact quotations compliant with source limits. If the strongest passage is longer than allowed, quote the densest allowed excerpt and paraphrase the rest.
- Cite every excerpt to the local source path and line number whenever possible.
- If a capture is rough OCR or transcript-derived, flag obvious transcript uncertainty.

## Diplomacy architecture filter

Parsi often carries several registers at once. Keep them distinct:

- **Settlement architecture:** the structure of a possible agreement.
- **Sequencing logic:** what must come first so the next concession is politically possible.
- **Sanctions relief:** what has to be lifted, returned, licensed, or guaranteed.
- **Coercion critique:** why pressure or bombing fails to produce desired concessions.
- **Regional architecture:** how Iran, GCC states, Israel, China, Russia, Europe, or the U.S. fit into a durable arrangement.
- **Political diagnosis:** who benefits from war or blocks compromise.

Ask: what mechanism remains if the moral or partisan charge is lowered by 60 percent?

## Feasibility checks

For each major Parsi claim, ask:

- What is the first reversible step?
- What is the first irreversible concession?
- Who verifies compliance?
- Who has veto power?
- Who needs a face-saving narrative?
- What sanctions, assets, transit rules, or security guarantees must change?
- Does the proposal reduce leverage too early, or does it transform leverage into settlement?
- What would make the bargain successor-stable?

## Comparative speaker mode

Use this when the operator asks to compare Parsi with another speaker, for example `compare Parsi to Marandi`, `Parsi vs Ritter`, or `how does Parsi differ from Pape`.

Minimum useful shape:

- **Boundary:** name each speaker's source class and role in the local corpus.
- **Register:** one line for Parsi and one line for the other speaker.
- **Excerpts:** include at least one exact source excerpt from Parsi and one from the comparison speaker, each with local file and line citation.
- **Convergence / divergence:** use a compact table when useful.
- **Combined use:** state what the paired reading makes possible for statecraft, speaker-state, or crisis testing.
- **Falsifier:** name what would weaken the combined reading.

Comparison rules:

- When comparing Parsi to Marandi, separate **diplomatic architecture** from **inside-Iran state-position claims**.
- When comparing Parsi to Ritter, separate **settlement design** from **force-constraint / escalation warning**.
- When comparing Parsi to Pape, separate **bargaining sequence** from **forecast clock / coercive-system leverage**.
- When comparing Parsi to Crooke, separate **workable agreement structure** from **order-rupture / Western misreading theory**.
- If one side has stronger source evidence than the other, say so explicitly.
- End with what the comparison lets the notebook do that neither speaker can do alone.

## Statecraft conversion

For each Parsi extraction, produce these fields when useful:

- **Diplomatic mechanism:** ceasefire, sanctions relief, transit guarantee, regional compact, nuclear framework, or non-regime-change guarantee.
- **Sequence:** what happens first, second, third.
- **Verification:** what evidence or monitor proves compliance.
- **Spoiler:** actor most likely to break or sabotage the mechanism.
- **Falsifier:** what event would weaken the claim.
- **Revisit:** date, negotiation event, military trigger, sanctions action, or official proposal.
- **State lanes:** usually `iran` and `america`; add `russia` or `china` when the architecture requires them.
- **Use:** transaction input, treaty clause, negotiation brief, policy memo, realism filter, or speaker-state note.

## Anti-patterns

- Do not turn Parsi into generic pro-diplomacy mood.
- Do not treat a desired settlement as self-enforcing.
- Do not omit the spoiler or enforcement problem.
- Do not collapse authored analysis and interview claims into one source class.
- Do not use host framing as proof of Parsi's exact claim.
- Do not skip line citations when raw-input is local.
- Do not make Parsi carry Marandi's insider claim, Ritter's force-warning claim, or Pape's forecast-clock claim.
