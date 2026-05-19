---
name: ritter-warning-extraction
preferred_activation: ritter-warning
description: "Draft workflow for extracting Scott Ritter's authored and interview warnings into disciplined quote cards, operational mechanisms, escalation paths, authority-carrier reads, falsifiers, comparative speaker reads, and statecraft inputs. Use for Ritter recent streams, Ritter quotes, Ritter on Putin/Zelensky/Trump/Lavrov/Khamenei, Karaganov/Ritter split, Ritter compared to another speaker, Ritter warning, Ritter host lanes, Russia/NATO escalation, operational feasibility, force constraints, and what can we learn/use from Ritter."
portable: true
version: 0.1.0-draft
tags:
  - draft
  - work-strategy
  - ritter
  - speaker-state
  - statecraft
---

# Ritter warning extraction

Use this draft skill when the operator asks for Ritter-specific extraction, especially:

- `what does Ritter say recently`
- `Ritter quotes`
- `top Ritter excerpts`
- `Karaganov/Ritter split`
- `compare Ritter to <speaker>`
- `Ritter warning`
- `Ritter on Putin`
- `Ritter on Zelensky`
- `Ritter on Trump`
- `Ritter on Lavrov`
- `Ritter on Khamenei`
- `Ritter host lanes`
- `what can we learn from Ritter`
- `wire Ritter into statecraft`
- `Russia/NATO escalation`
- `operational feasibility`

Goal: extract Ritter's strongest warning value without letting moral heat, prosecutorial rhetoric, or host pressure flatten the operational analysis.

## Start files

Open the speaker surfaces first:

- `codex/speakers/ritter/README.md`
- `codex/speakers/ritter/ritter-helix.md`
- `codex/speakers/ritter/ritter-interview-appearances-2025-2026.md`
- `codex/years/2026/ritter/ritter-forecast-ledger-2026.md`

Then choose host lane as needed:

- **Diesen:** escalation horizon and order-level mechanics.
- **Davis:** operational feasibility, stockpiles, air defense, basing, and war-plan reality checks.
- **Dialogue Works / Alkorshid:** live war pressure and rapid event interpretation.
- **Napolitano:** legality, war powers, command failure, and institutional absurdity.
- **Cyrus Janssen:** energy, Hormuz, Asia, and economic shock.
- **Consortium News:** adversarial debate and Russia-policy stress test.

## Source boundary

Keep the helix source-separated:

- **Authored strand:** Substack forecast/warning ledger.
- **Interview strand:** host-owned appearances and host-local arcs.
- **Do not merge:** host framing, Ritter claim, raw transcript, and assistant synthesis.

If the operator asks about "recent streams," prioritize interview captures, then bridge back to the authored ledger only when the mechanism matches.

## Extraction workflow

1. Search Ritter speaker state, host arcs, and raw-input captures with `rg`.
2. Identify the immediate warning claim.
3. Classify the claim:
   - operational feasibility;
   - escalation path;
   - deterrence doctrine;
   - force constraint;
   - authority-carrier read;
   - legal/command failure;
   - moral/prosecutorial judgment.
4. Extract 3-5 quote cards if the operator asks for quotes or excerpts.
5. Separate heat from mechanism.
6. Add falsifiers and revisit triggers.
7. Convert the reusable lesson into speaker-state, statecraft, or crisis-transaction input.

## Quote-card discipline

- If the operator asks for quotes, the bullet must contain Ritter's own words.
- Use dense near-limit exact excerpts whenever allowed, with file and line citation.
- Do not answer with tiny fragments when fuller compliant excerpts are available.
- If a requested excerpt length exceeds the quoting limit, state the limit and provide near-limit excerpts plus paraphrase.
- Prefer one strong excerpt per source file when the quote budget would otherwise be exhausted.

## Source-illustrated answer default

When the operator asks what Ritter says, what can be learned from Ritter, or how to use a Ritter warning, include transcript evidence in the answer by default.

Minimum useful shape:

- **Claim:** one sentence naming the warning or mechanism.
- **Excerpt:** a short exact excerpt from a transcript or authored capture, with file and line citation.
- **Mechanism:** one sentence translating the excerpt into operational meaning.
- **Use:** one sentence naming the statecraft, speaker-state, or crisis-test application.

Rules:

- Prefer transcript excerpts for recent-stream questions; use authored Substack excerpts only when the operator asks for the authored strand or the interview material is thin.
- Choose high-density sentences that make the point themselves; do not use six-word fragments unless no stronger exact wording exists.
- Keep exact quotations compliant with source limits. If the strongest passage is longer than allowed, quote the densest allowed excerpt and paraphrase the rest.
- Do not substitute a heading plus explanation for the excerpt. The excerpt must carry Ritter's own point.
- Cite every excerpt to the local source path and line number whenever possible.
- If using multiple transcript sources, use one compact excerpt per source before spending quote budget on a second excerpt from the same file.

## Comparative speaker mode

Use this when the operator asks to compare Ritter with another speaker, for example `compare Ritter to Marandi`, `Ritter vs Pape`, or `how does Ritter differ from Crooke`.

Minimum useful shape:

- **Boundary:** name each speaker's source class and role in the local corpus.
- **Register:** one line for Ritter and one line for the other speaker.
- **Excerpts:** include at least one exact source excerpt from Ritter and one from the comparison speaker, each with local file and line citation.
- **Convergence / divergence:** use a compact table when useful.
- **Combined use:** state what the paired reading makes possible for statecraft, speaker-state, or crisis testing.
- **Falsifier:** name what would weaken the combined reading.

Comparison rules:

- Keep speaker roles orthogonal. Ritter is usually the warning / force-constraint / escalation-mechanics voice; do not flatten insider, diplomatic, economic, or host-native speakers into his register.
- Preserve source-class boundaries. Do not merge authored Ritter essays, Ritter interviews, host claims, and the comparison speaker's claims into one undifferentiated voice.
- When comparing Ritter to an insider voice such as Marandi, separate **external warning** from **inside-state account**.
- When comparing Ritter to a forecast voice such as Pape, separate **operational feasibility** from **threshold / clock / falsifier logic**.
- When comparing Ritter to a structural voice such as Crooke, separate **military-professional warning** from **order-rupture / metapolitical mechanism**.
- If one side has stronger source evidence than the other, say so explicitly and keep the weaker side provisional.
- End with what the comparison lets the notebook do that neither speaker can do alone.

## Heat filter

Ritter often carries three registers at once. Keep them distinct:

- **Military-professional warning:** what he says can or cannot be done.
- **Escalation mechanics:** how a crisis moves from warning to strike to wider war.
- **Moral/prosecutorial heat:** condemnation, contempt, or maximal punishment language.

Do not discard the heat, but do not let it become the mechanism. Ask: what remains true if the rhetoric is lowered by 60 percent?

## Authority carrier mode

Use this when the operator asks `Ritter on <person>` or when the topic is a leader, minister, commander, negotiator, security council, or symbolic sovereign authority.

Minimum useful shape:

- **Role:** what authority function the actor carries in Ritter's account.
- **Decision power:** what the actor can still decide or authorize.
- **Constraint:** what material, institutional, psychological, or alliance pressure limits that actor.
- **Escalation predicate:** the condition that makes restraint fail or makes action unavoidable in Ritter's warning.
- **Excerpt:** at least one source excerpt where Ritter's own words carry the causal claim.
- **Statecraft use:** folder handoff, transaction input, realism filter, or object note.

Common patterns:

- **Putin:** sovereign authority and restrained escalation manager; look for the condition that makes restraint no longer viable.
- **Zelensky:** spoiler or failing authority carrier when remaining agency is escalation, delay, or provocation rather than settlement.
- **Trump:** unstable command carrier when temperament, optics, or ego shapes war termination.
- **Lavrov:** diplomatic carrier when Russian official language, treaty capability, or channel discipline matters.
- **Khamenei:** sovereign-symbolic authority when martyrdom, succession, regime-collapse assumptions, or deterrent legitimacy matter.

Do not turn the person into biography. Ask what state function, command function, bargaining function, or escalation function Ritter assigns to the actor.

## Escalation predicate test

For every major Ritter warning, name the predicate that changes the decision calculus:

- What new material harm is being imposed?
- What sanctuary, proxy, or enabling node makes the harm sustainable?
- What official warning has already been issued?
- What previous restraint no longer solves the problem?
- What concrete instrument does Ritter think becomes likely next?

This prevents the skill from treating every warning as generic doom. The useful Ritter question is: what condition makes the warning operational?

## Karaganov/Ritter split

When Karaganov appears:

- **Karaganov:** restore Western fear through nuclear-threshold pressure.
- **Ritter agreement:** Western impunity and misread restraint can force deterrence restoration.
- **Ritter caveat:** nuclear use cannot be reliably contained once the threshold is crossed.
- **Practical instrument:** look for overwhelming conventional punishment, enabling-node strikes, drone/missile salvos, or political warnings as nuclear substitutes.

Useful statecraft rule: when a nuclear-threat school appears, ask what conventional instrument could deliver the same political message with less terminal risk.

## Statecraft conversion

For each Ritter extraction, produce these fields when useful:

- **Warning:** what bad outcome Ritter says is approaching.
- **Mechanism:** what material or institutional path creates it.
- **Instrument:** what actor uses what concrete tool.
- **Falsifier:** what event would weaken the warning.
- **Revisit:** what date, trigger, or battlefield event should reopen the claim.
- **State lane:** `america`, `russia`, `china`, or `iran`.
- **Use:** transaction input, realism filter, treaty/policy caution, or speaker-state note.

## State-folder handoff

When authority carrier mode produces a durable object, route the reusable output:

- Putin or Lavrov -> `codex/academy/statecraft/russia/state/`
- Trump or Vance -> `codex/academy/statecraft/america/state/`
- Khamenei or Araghchi -> `codex/academy/statecraft/iran/state/`
- Zelensky -> keep as crisis/proxy object unless a Ukraine lane or object folder exists.

Use a handoff when the result names a recurring decision node, not for one-off color commentary.

## Anti-patterns

- Do not turn Ritter into generic "pro-Russia" mood.
- Do not treat his most heated sentence as the whole claim.
- Do not collapse authored warnings and interview warnings into one source class.
- Do not use a host title as proof of Ritter's exact claim.
- Do not omit falsifiers for dramatic forecasts.
- Do not skip line citations when raw-input is local.
- Do not flatten comparison speakers into Ritter's heat or make Ritter carry an insider claim he did not make.
