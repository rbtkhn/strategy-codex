---
name: mercouris-daily-continuity-extraction
description: "Draft workflow for extracting Alexander Mercouris / The Duran long-form updates into disciplined daily continuity: timeline deltas, diplomacy-room reads, Ukraine/Iran/Russia operational claims, elite-politics inferences, source-confidence tiers, comparative speaker seams, and statecraft inputs. Use for Mercouris says, Mercouris daily, Mercouris latest, Duran Mercouris, continuity check, Kiev crisis, Moscow reaction, Geneva talks, Hormuz blockade, and compare Mercouris to another speaker."
preferred_activation: mercouris-continuity
portable: true
version: 0.1.0-draft
category: domain-pack
status: draft
tags:
  - draft
  - work-strategy
  - mercouris
  - daily-continuity
  - speaker-state
  - statecraft
---
# Mercouris daily continuity extraction

Use this draft skill when the operator asks for Mercouris-specific extraction, especially:

- `Mercouris says`
- `Mercouris latest`
- `Mercouris daily`
- `Duran Mercouris`
- `check stream Mercouris`
- `continuity check`
- `what changed since yesterday`
- `Kiev crisis`
- `Moscow reaction`
- `Geneva talks`
- `Hormuz blockade`
- `Trump-Xi meeting`
- `diplomatic visit postmortem`
- `what did the summit produce`
- `compare Mercouris to <speaker>`
- `wire Mercouris into statecraft`
- `ground Mercouris in CIV-MEM`
- `Mercouris with civilizational memory`
- `use Mercouris for recommendations`

Goal: extract Mercouris's value as a high-frequency continuity and diplomacy-room analyst without flattening long narrative confidence into verified fact.

## Start files

Open speaker and stream surfaces first:

- `codex/speakers/mercouris/mercouris-speaker-object.md`
- `codex/speakers/mercouris/mercouris-cross-host-note.md`
- `codex/years/2026/mercouris/README.md`
- `codex/years/2026/mercouris/mercouris-shelf-2026-05.md`
- `codex/years/2026/mercouris/mercouris-thread.md`
- `codex/years/2026/mercouris/mercouris-transcript.md`

For every Mercouris analysis, consider CIV-MEM/statecraft context as a quiet background discipline. Open these when the topic is heading toward a recommendation, statecraft analysis, durable output, or civilizational pattern claim:

- `codex/academy/statecraft/sheets/civilizational-pattern-to-statecraft.md`
- relevant national lane files under `codex/academy/statecraft/{america,russia,china,iran}/`
- optional CIV-MEM routes under `research/repos/civilization_memory/content/civilizations/`

Then search raw captures:

- `codex/years/2026/raw-input/**/transcript-*mercouris*.md`
- `codex/years/2026/raw-input/**/*mercouris*.md`
- dated Mercouris day pages and shelf pages under `codex/years/2026/mercouris/`.

## Source boundary

Keep source classes separate:

- **Mercouris claim:** what Alexander Mercouris says in a transcript or operator capture.
- **Duran host framing:** Alex Christoforou title, intro, or prompt.
- **Second-hand report:** what Mercouris attributes to Reuters, Bloomberg, Strana, Rybar, Russian MoD, Ukrainian media, officials, or unnamed sources.
- **Operator cleanup / OCR:** transcript text may be cleaned, partial, or user-provided.
- **Assistant synthesis:** continuity spine, statecraft implication, or confidence tier.

Do not treat Mercouris's institutional inference as wire evidence. Preserve his read, then tier it.

## Extraction workflow

1. Search Mercouris speaker state, shelf pages, and raw-input captures with `rg`.
2. Identify the continuity delta:
   - what is new since the previous Mercouris item;
   - what prior claim is repeated, hardened, weakened, or contradicted;
   - what actor changed position, language, or timing.
3. Classify each claim:
   - diplomacy-room read;
   - official-language interpretation;
   - frontline / operational claim;
   - elite-politics inference;
   - economic / energy mechanism;
   - media-source triangulation;
   - rumor / unnamed-source hypothesis;
   - statecraft implication.
4. Assign a confidence tier.
5. Extract source evidence when asked for quotes or when the claim is high-leverage.
6. Add falsifiers and revisit triggers.
7. Run a quiet CIV-MEM/statecraft discipline pass for authority, restraint, and settlement; surface it only when it improves the answer.
8. Convert the reusable lesson into speaker-state, crisis-test, or statecraft input.

## Continuity delta discipline

Every Mercouris answer should try to answer:

- What did he say before?
- What does he say now?
- What changed in the claimed facts, actor posture, or timing?
- Is the change evidence-driven, inference-driven, or rhetoric-driven?
- What would falsify the new read within 24-72 hours?

Useful output shape:

| Field | Use |
|---|---|
| **Previous read** | Prior Mercouris claim or line of analysis. |
| **New read** | Today's or latest claim. |
| **Delta** | Hardened, softened, reversed, extended, or unchanged. |
| **Evidence tier** | Official, named media, open-source map, transcript inference, rumor. |
| **Revisit trigger** | Next official statement, battlefield update, negotiation event, market move, or denial. |

## Diplomatic visit postmortem mode

Use this when Mercouris analyzes a summit, leader visit, delegation meeting, negotiation round, or ceremonial diplomatic encounter.

Minimum useful fields:

| Field | Question |
|---|---|
| **Protocol signal** | Who met whom, who was absent, what rank handled arrival, and what ceremony or venue implied. |
| **Announced deliverables** | What agreements, contracts, communiques, or concrete concessions were publicly announced. |
| **Public readout** | What the official readouts emphasized, omitted, warned about, or repeated. |
| **Pressure ask** | What one side wanted the other to do for a third-party crisis, such as Iran, Ukraine, Taiwan, sanctions, energy, or rare earths. |
| **Material leverage** | What supply chain, military, financial, energy, legal, or alliance leverage made the meeting asymmetrical. |
| **Mercouris read** | His synthesis of the room, actor posture, institutional sequencing, and likely next move. |
| **Confidence tier** | Split protocol/readout evidence from Mercouris inference. |
| **Post-trip risk** | Whether a failed visit increases escalation, face-saving pressure, or a compensatory move elsewhere. |
| **Revisit trigger** | Next communique, contract announcement, sanction move, military deployment, tariff change, or follow-up visit. |

Rules:

- Treat courtesy as evidence of ceremony, not evidence of agreement.
- Do not infer deliverables from warm language.
- Separate public readout facts from Mercouris's room-read inference.
- Track absent concessions as claims only when the local source identifies expected concessions or prior pressure asks.
- When comparing with Ritter, let Mercouris own the protocol and institutional sequence while Ritter owns force constraints and coercive feasibility.

## Confidence tiers

Use these labels:

- **Tier A - primary / official:** direct text from officials, ministries, courts, parliaments, central banks, named public statements, or official readouts.
- **Tier B - named media / named analyst:** Reuters, Bloomberg, FT, Strana, Rybar, Military Summary, War Mapper, named Russian/Ukrainian/Western media, or named analysts.
- **Tier C - Mercouris inference:** his synthesis from patterns, body language, sequencing, institutional behavior, or unstated motives.
- **Tier D - rumor / unnamed-source:** claims based on unnamed officials, Telegram fragments, speculation, or "reports suggest" without a clear source.
- **Tier E - narrative atmosphere:** confidence, mood, sarcasm, historical analogy, or elite-psychology interpretation without independently pinned evidence.

If a claim includes several tiers, split it. Do not launder Tier D through Tier C prose.

## CIV-MEM statecraft spine

CIV-MEM is part of the default background discipline for Mercouris analysis. Use it as an invisible statecraft spine: it should shape the answer's limits, carriers, and settlement logic without turning every response into a visible CIV-MEM report.

Mercouris supplies the **current continuity read**. CIV-MEM supplies **historical recurrence, state continuity, and civilizational pattern discipline**. Keep them distinct:

- Mercouris evidence supports claims about the current event chain.
- CIV-MEM supports analogy, recurrence, state continuity, authority, restraint, and settlement design.
- CIV-MEM is not proof that Mercouris is factually correct.
- Do not cite CIV-MEM as evidence for current facts, casualty claims, targeting chains, negotiations, troop movements, or unnamed-source reports.
- CIV-MEM may discipline a Mercouris recommendation, but it must not override current-source evidence.
- If no strong CIV-MEM pattern fits, skip it silently rather than announcing a failed lookup.

Preferred chat shape:

- Compact, dense, seamless prose.
- No visible CIV-MEM path citations unless the operator asks for receipts, exact sources, or the answer is being written to disk.
- Use a table only when it clarifies a decision or comparison.
- Weave authority, restraint, and settlement into the recommendation rather than labeling them mechanically.

When writing a durable artifact, or when the operator asks for receipts, use this explicit support shape:

| Field | Use |
|---|---|
| **Mercouris continuity read** | The live sequence, actor posture, or room-read from Mercouris. |
| **CIV-MEM pattern** | The historical/civilizational recurrence or analogy being used. |
| **Fit / break** | Why the pattern helps and where it must be restrained. |
| **Authority / restraint / settlement** | The statecraft conversion test. |
| **Citations** | Mercouris source path(s) plus CIV-MEM/statecraft path(s). |

Routing:

- For Russia questions, prefer `RUSSIA` CIV-MEM routes when present and the Russia statecraft lane.
- For Iran questions, use `PERSIA` as the default CIV-MEM root and the Iran statecraft lane as the current authority/instrument home.
- For China questions, prefer China/Sinic CIV-MEM routes when present and the China statecraft lane.
- For America questions, prefer America/U.S./Anglo-imperial continuity routes when present and the America statecraft lane.
- For cross-system crises, use `codex/academy/statecraft/sheets/national-perspective-orthogonality.md` and the relevant four national lanes before final recommendations.

When the local CIV-MEM checkout is present and the entity is clear, use existing repo tooling to pick sources rather than silently improvising:

```text
python scripts/suggest_civ_mem_from_relevance.py <ENTITY>
```

If that script or relevance spine is unavailable, use targeted `rg` over `research/repos/civilization_memory` for planning or durable work. If no suitable CIV-MEM support is found in ordinary chat, continue without visible CIV-MEM language.

Use the academy-statecraft hinge:

```text
pattern / narrative -> authority / restraint / settlement
```

The internal recommendation is not complete until it has considered all three. In chat, name them only when doing so improves the prose or the operator asks for the scaffold.

## Source-illustrated answer default

When the operator asks what Mercouris says, what changed, or how to use a Mercouris read, include source evidence by default when local lines are available.

Minimum useful shape:

- **Claim:** one sentence naming the read.
- **Excerpt:** a short exact excerpt from a transcript or Mercouris page, with file and line citation.
- **Tier:** A-E confidence label.
- **Delta:** what changed versus prior Mercouris continuity.
- **Use:** statecraft, speaker-state, crisis-test, or verification task.

Rules:

- Prefer recent raw-input transcripts for "latest" questions.
- Prefer shelf/page summaries for continuity across several days.
- Keep exact quotations compliant with source limits. If the strongest passage is longer than allowed, quote the densest allowed excerpt and paraphrase the rest.
- Cite every exact excerpt to local source path and line number whenever possible.
- For ordinary non-quoted chat analysis, keep source paths invisible unless the operator asks for receipts or the answer is destined for a durable file.
- If a capture is rough OCR, operator-cleaned, or has mojibake, flag transcript uncertainty.

## Comparative speaker mode

Use this when the operator asks to compare Mercouris with another speaker.

Minimum useful shape:

- **Boundary:** name each speaker's source class and role.
- **Register:** Mercouris = continuity / diplomacy-room / institutional inference; name the other speaker's role separately.
- **Excerpts:** include at least one exact source excerpt from Mercouris and one from the comparison speaker when available.
- **Convergence / divergence:** use a compact table.
- **Combined use:** state what the paired reading makes possible.
- **Falsifier:** name what would weaken the combined read.

Comparison rules:

- With **Ritter**, separate operational feasibility from Mercouris institutional sequencing.
- With **Parsi**, separate diplomacy architecture from Mercouris room-read continuity.
- With **Pape**, separate forecast thresholds from Mercouris daily event chain.
- With **Crooke**, separate structural/metapolitical rupture from Mercouris current political read.
- With **Marandi**, separate inside-Iran state account from Mercouris external analyst synthesis.
- With **Davis**, separate operational feasibility and U.S. audience framing from Mercouris institutional narrative.

## Statecraft conversion

For each Mercouris extraction, produce these fields when useful:

- **Continuity claim:** what line of events is being carried forward.
- **Actor posture:** who changed position, language, timing, or leverage.
- **Mechanism:** negotiation, escalation, attrition, sanctions, logistics, energy, domestic politics, or alliance discipline.
- **Tier:** A-E confidence label.
- **Falsifier:** what would weaken the claim.
- **Revisit:** specific next event, date, official statement, map update, or economic indicator.
- **State lanes:** usually `russia`, `america`, `iran`, `china`, or cross-lane.
- **CIV-MEM support:** historical pattern, fit/break, authority/restraint/settlement discipline, and cited paths only when writing durable artifacts or when receipts are requested.
- **Use:** verification task, crisis-test input, transaction input, negotiation brief, or speaker-state note.

Durable outputs from Mercouris+CIV-MEM synthesis belong in `codex/academy/statecraft/` lanes, transactions, or state objects by default. Do not write them into Mercouris speaker surfaces unless the operator explicitly asks for Mercouris-lane memory.

## Anti-patterns

- Do not treat The Duran title as Mercouris's exact claim.
- Do not merge Christoforou framing with Mercouris analysis.
- Do not turn Mercouris into generic pro-Russia mood.
- Do not treat "obvious" institutional inference as verified fact.
- Do not collapse a six-topic daily monologue into one undifferentiated thesis.
- Do not omit confidence tiers for frontline, casualty, ORBAT, negotiation-room, or elite-politics claims.
- Do not skip line citations when raw-input is local.
- Do not let Mercouris carry another speaker's role: he is not Pape's forecast clock, Ritter's force-constraint voice, Parsi's settlement architect, or Marandi's inside-state authority.
- Do not let CIV-MEM become decorative analogy. If it does not change authority, restraint, or settlement, omit it or mark it as background only.
- Do not use CIV-MEM to launder current-event uncertainty into false confidence.
