---
name: current-event
preferred_activation: current-event
description: "Verify a named current event, separate fact from interpretation, then convert it into a statecraft-ready object. Use when the operator says current-event, current event, event read, or asks to analyze a recent news item for statecraft, negotiation, policy, sanctions, alliance, sovereignty, or crisis-object implications."
---

# Current Event

`current-event` is an explicit bridge from live news to statecraft. It is not `coffee C`, not `check streams`, and not a generic daily brief.

Use it when the operator names a recent event and wants judgment or an instrument from it, for example:

- `current-event Putin arrives China May 19`
- `current-event Hormuz insurance spike`
- `event read Vance speech Munich`
- `statecraft current event: China export controls`

## Boundary

- WORK only; not Record.
- Verify unstable facts with current sources before analysis.
- Do not create raw-input captures unless the operator asks for capture or transcript materialization.
- Do not route to `check streams` unless the task is "what went up today across tracked streams?"
- Do not route to daily brief unless the operator asks for a broad brief.
- Convert sources into **statecraft objects**, not commentary sprawl.

## Workflow

1. **Verify event fact.** Confirm date, actors, location, and what happened with primary or reputable sources. Name source confidence briefly.
2. **Separate fact from interpretation.** State what is known, what is inferred, and what remains unverified.
3. **Classify the crisis object.** Name the contested object: alliance signal, sanctions channel, transit route, nuclear latency, recognition claim, ceasefire monitor, protected legitimacy good, etc.
4. **Map actor interests.** For each main actor, name durable interest, immediate crisis leverage, constraint, and likely institutional carrier.
5. **Choose output shape.** If the operator has not chosen one, default to the smallest useful artifact:
   - **event read** for orientation;
   - **negotiation brief** when bargaining is live;
   - **policy paper** when a decision is needed;
   - **treaty / mechanism sketch** when obligations or verification matter;
   - **Richelieu/Bismarck stress test** when overreach risk is the point.
6. **Draft the instrument.** Produce the chosen statecraft artifact with red lines, concessions, verification, fallback, and off-ramp as relevant.
7. **Check for recursive update candidates.** If the event exposes a durable civilization pattern, empire instrument, state regulator, helix crosswalk, transaction precedent, falsifier, or revisit trigger, suggest a compressed candidate for the relevant `<lane>/updates/pending.md`. Do not require a candidate for every event.
8. **Offer four calibrated option paths.** End every default current-event read with exactly four labeled paths calibrated to the specific event, actors, crisis object, and likely instruments. Do not reuse generic template labels as the option text.

## Default Output

If the operator gives only an event and no artifact type, output:

```markdown
**Verified Event**
- Date / actors / what happened
- Sources

**Statecraft Object**
- Contested object:
- Why it matters:

**Actor Map**
- Actor: interest / leverage / constraint / carrier

**Instrument**
- Narrow ask or policy move:
- Verification:
- Fallback:

**Stress Test**
- Main objection:
- Falsifier:

**Recursive Update Candidate**
- Needed: yes / no
- Lane / target:
- Candidate summary:
- Suggested action:

**Option Paths - reply A-D**
A. [topic-specific treaty / mechanism path] - name the parties, object, and verification problem
B. [topic-specific policy decision path] - name the decision-maker, decision, and institutional carrier
C. [topic-specific negotiation path] - name the bargaining problem, ask, concession, and fallback
D. [topic-specific stress-test path] - name the overreach risk, alliance geometry, or restraint problem
```

## Statecraft Hand-Offs

When the operator replies with a letter after a current-event read, execute the matching calibrated option rather than reprinting the menu:

- `A` = the event-specific treaty / mechanism path
- `B` = the event-specific policy decision path
- `C` = the event-specific negotiation path
- `D` = the event-specific Richelieu/Bismarck stress-test path

Use `codex/academy/statecraft/METHOD.md` and the relevant template or lens. For power comparisons, apply the `strategic-power-analysis` distinction: structural power versus immediate crisis leverage.

## Nested Menu Rule

When a chosen path naturally opens another menu, keep that menu calibrated too. Do not fall back to generic choices like "more analysis" or "draft memo."

Each nested option must name:

- the actor or institutional carrier;
- the specific contested object;
- the failure mode or instrument to test;
- and the next output shape.

For example, after a Hormuz mechanism draft, prefer:

- `A. China refusal test - what Beijing rejects, acceptable wording, and the price it might demand`
- `B. Iran evasion test - selective safe passage, proxy ambiguity, and insurance warfare`
- `C. U.S. overreach test - where a narrow transit channel becomes anti-China or regime-pressure escalation`
- `D. Clause-set revision - patch the mechanism against the strongest objections`

## Calibrated Option Rule

Each option must be a concrete next move that could only belong to the named event.

For example, for `current-event Trump Xi last week`, avoid:

- `A. Treaty framework - parties, interests, obligations...`

Prefer:

- `A. Hormuz stability channel - draft a U.S.-China mechanism for Iran/Hormuz signaling, oil-flow restraint, and verification`
- `B. Taiwan-trade compartment memo - decide how Washington keeps Taiwan deterrence from collapsing the trade/fentanyl channel`
- `C. Dual-use/fentanyl negotiation brief - define the narrow U.S. ask, Chinese face-saving concession, and enforcement fallback`
- `D. Beijing arena stress test - test whether treating China as broker overstates Xi's leverage and drives Russia/Iran closer`
