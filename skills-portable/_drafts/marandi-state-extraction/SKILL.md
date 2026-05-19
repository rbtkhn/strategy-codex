---
name: marandi-state-extraction
preferred_activation: marandi-state
description: "Draft workflow for extracting Seyed Mohammad Marandi's interview claims into disciplined inside-Iran state-position notes, red-line maps, institutional authority checks, retaliation logic, comparative speaker reads, and statecraft inputs. Use for Marandi says, Iranian position, inside Iran, Iran red lines, Supreme National Security Council, Hormuz from Iran's view, Iran retaliation doctrine, and compare Marandi to another speaker."
portable: true
version: 0.1.0-draft
tags:
  - draft
  - work-strategy
  - marandi
  - state-iran
  - speaker-state
  - statecraft
---

# Marandi state extraction

Use this draft skill when the operator asks for Marandi-specific extraction, especially:

- `Marandi says`
- `Iranian position`
- `inside Iran`
- `Iran red lines`
- `Supreme National Security Council`
- `Hormuz from Iran's view`
- `Iran retaliation doctrine`
- `compare Marandi to <speaker>`
- `what can we learn from Marandi`
- `wire Marandi into statecraft`

Goal: extract Marandi's value as an inside-Iran state-position voice without treating his claims as neutral fact or flattening them into external analyst commentary.

## Start files

Open speaker and state surfaces first when available:

- `codex/speakers/marandi/`
- `codex/speakers/marandi/marandi-thread.md`
- `codex/academy/statecraft/iran/README.md`
- `codex/academy/statecraft/iran/state/README.md`
- `codex/academy/statecraft/iran/state/objects/araghchi.md`

Then choose host lane as needed:

- **Diesen:** order-level pressure, China/Russia/Iran alignment, and strategic escalation framing.
- **Davis:** U.S. military feasibility, American audience translation, and Iran institutional resilience under skeptical questioning.
- **Dialogue Works / Alkorshid:** live crisis pressure, Iranian red-line narration, and rapid event interpretation.

## Source boundary

Keep source classes separate:

- **Marandi claim:** what Marandi says in a transcript or capture.
- **Iranian official position:** what he attributes to a named Iranian institution, official, council, or public statement.
- **Host framing:** the host's question or summary.
- **Assistant synthesis:** your own mechanism or statecraft conversion.

Do not describe Marandi's statement as official Iranian policy unless the excerpt names the institution, official, document, or authority carrying it.

## Extraction workflow

1. Search Marandi speaker state and raw-input captures with `rg`.
2. Identify the immediate claim:
   - institutional authority;
   - red line;
   - retaliation doctrine;
   - negotiation condition;
   - Hormuz / transit rule;
   - regime resilience;
   - civilizational or religious legitimacy;
   - accusation about U.S., Israel, GCC, or Europe.
3. Extract source evidence by default.
4. Separate inside-state account from verifiable fact.
5. Name the authority carrier when possible.
6. Add falsifiers and revisit triggers.
7. Convert the reusable lesson into `state-iran`, statecraft transaction input, or comparative speaker-state input.

## Source-illustrated answer default

When the operator asks what Marandi says, what Iran's position is, or how to use a Marandi claim, include source evidence by default.

Minimum useful shape:

- **Claim:** one sentence naming Marandi's inside-state claim.
- **Excerpt:** a short exact excerpt from a transcript or capture, with file and line citation.
- **Authority:** who or what carries the claim: Marandi, SNSC, Supreme Leader, president, Araghchi, parliament, IRGC, armed forces, or public Iranian statement.
- **Mechanism:** one sentence translating the excerpt into operational meaning.
- **Use:** one sentence naming the statecraft, speaker-state, or crisis-test application.

Rules:

- Prefer recent transcript excerpts for live-crisis questions.
- Choose high-density sentences that carry the point themselves.
- Keep exact quotations compliant with source limits. If the strongest passage is longer than allowed, quote the densest allowed excerpt and paraphrase the rest.
- Cite every excerpt to the local source path and line number whenever possible.
- If the capture is rough OCR or a generated transcript, preserve the meaning but flag obvious transcript uncertainty.

## Inside-state filter

Marandi often carries several registers at once. Keep them distinct:

- **Inside-state account:** how he says Iranian institutions decide or interpret events.
- **Advocacy / defense:** how he justifies Iran's conduct or condemns adversaries.
- **Threat signaling:** how he communicates retaliation, endurance, or red lines.
- **Civilizational legitimacy:** how he frames Iran as resilient, Muslim, Shia, oppressed, or anti-imperial.

Do not discard advocacy, but do not let advocacy become the evidence. Ask: what institutional or strategic claim remains if the rhetoric is lowered by 60 percent?

## Authority-carrier check

For each major claim, ask:

- Is this Marandi's interpretation?
- Is he reporting a named official position?
- Is he referring to the Supreme National Security Council, Supreme Leader, Araghchi, parliament, IRGC, or armed forces?
- Is the claim a public red line, a negotiation position, or a forecast?
- Does the claim belong in `state-iran/state/objects/`, `transactions/`, or a crisis-test note?

If no authority carrier is named, mark the claim as `Marandi interpretation` rather than `Iranian policy`.

## Comparative speaker mode

Use this when the operator asks to compare Marandi with another speaker, for example `compare Marandi to Ritter`, `Marandi vs Pape`, or `how does Marandi differ from Crooke`.

Minimum useful shape:

- **Boundary:** name each speaker's source class and role in the local corpus.
- **Register:** one line for Marandi and one line for the other speaker.
- **Excerpts:** include at least one exact source excerpt from Marandi and one from the comparison speaker, each with local file and line citation.
- **Convergence / divergence:** use a compact table when useful.
- **Combined use:** state what the paired reading makes possible for statecraft, speaker-state, or crisis testing.
- **Falsifier:** name what would weaken the combined reading.

Comparison rules:

- Keep Marandi's inside-state role orthogonal to external analysts.
- When comparing Marandi to Ritter, separate **inside-state account** from **external warning / force-constraint logic**.
- When comparing Marandi to Parsi, separate **Iranian state red lines** from **diplomatic off-ramp architecture**.
- When comparing Marandi to Pape, separate **Iranian authority / endurance claims** from **forecast clock / coercive-system leverage logic**.
- When comparing Marandi to Crooke, separate **Iranian insider narration** from **order-rupture / Western misreading theory**.
- If one side has stronger source evidence than the other, say so explicitly.
- End with what the comparison lets the notebook do that neither speaker can do alone.

## Statecraft conversion

For each Marandi extraction, produce these fields when useful:

- **Position:** what Marandi says Iran will not accept or must preserve.
- **Authority carrier:** institution, official, council, or Marandi interpretation.
- **Red line:** what action triggers response or refusal.
- **Instrument:** retaliation, Hormuz control, negotiation clause, sanctions relief condition, transit rule, or regional architecture.
- **Falsifier:** what event would weaken the claim.
- **Revisit:** what date, trigger, negotiation step, or battlefield event should reopen the claim.
- **State lane:** usually `iran`; add `america`, `russia`, or `china` when the claim directly concerns those lanes.
- **Use:** transaction input, treaty/policy constraint, realism filter, or speaker-state note.

## Anti-patterns

- Do not treat Marandi as neutral wire evidence.
- Do not treat every Marandi statement as official Iranian policy.
- Do not flatten Marandi into generic pro-Iran sentiment.
- Do not omit the authority carrier when the claim concerns decision-making.
- Do not collapse host framing and Marandi's answer.
- Do not skip line citations when raw-input is local.
- Do not let external analysts override Marandi's inside-state account without naming the disagreement.
