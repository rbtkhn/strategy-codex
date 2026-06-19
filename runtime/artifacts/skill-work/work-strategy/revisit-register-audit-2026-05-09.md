# Revisit Register Noise Audit

**Date:** 2026-05-09  
**Conductor:** `furtwangler`  
**Scope:** Strategy-codex revisit / judgment-loop surfacing  
**Status:** Work-layer audit, not a notebook verdict  

## Question

The conductor revisit block surfaced a very large tension register. This pass asks which entries are real strategic conflicts and which are duplicate or generated noise.

## Receipt

Read-only sample from `build_judgment_loop_report(Path("codex"), user_id="strategy-codex")`:

- Open / due loops: `141`
- Generated tension groups: `107`
- Grouping rule observed in `scripts/strategy_notebook/judgment_loops.py`: cross-stream loops are grouped when they share any extracted `topic_key` and one side has positive polarity while the other has negative polarity.

That rule is useful as an alarm, but too loose as a judgment surface. A shared token plus opposite polarity is not enough to prove a real strategic contradiction.

## Real Strategic Conflicts To Preserve

These are not single generated labels. They are clusters that should remain visible for future composition.

| Conflict | Preserve because | Example generated labels that point at it |
|----------|------------------|-------------------------------------------|
| Hormuz / blockade mechanics vs bargaining logic | The notebook has a genuine unresolved conflict between operational feasibility, commodity leverage, legal/diplomatic framing, and whether blockade pressure creates an off-ramp or a trap. | `blockade`, `hormuz`, `energy`, `commodity`, `currency`, `centcom` |
| Trap / ratchet vs third-party off-ramp | The Davis / Pape / Par­si / Mercouris material repeatedly distinguishes coercive escalation from bargaining runway. This is a real strategic fork, not just wording noise. | `alliance`, `audience`, `legitimacy`, `merge`, `primaries`, `false` |
| Material clocks vs structural incentives | Barnes / Mearsheimer-style tension appears as a real composition problem: one lens asks whether posture can be sustained, another asks whether settlement is credible at all. | `mearsheimer`, `clock`, `falsifiers`, `judgment` |
| Operational claims vs theory / analogy | Ritter / Pape / Mercouris lanes are often being mixed: order-of-battle or logistics claims should not become proof of theoretical claims, and theory should not verify ORBAT. | `analytic`, `orbat`, `ground`, `military`, `analogy`, `means` |
| Lebanon / Israel / ceasefire scope | The April notebook contains a genuine scope conflict: ceasefire-as-everywhere vs U.S./Israel narrowing and walk-back. This is real even when the generated topic label does not say `lebanon`. | `israel`, `diplomacy`, `official`, `framing` |
| Market relief vs next-phase war risk | Crooke / Mercouris-style market and diplomacy readings create a real time-horizon conflict: whether visible relief is a stabilizer or a mask before escalation. | `markets`, `serious`, `diplomacy` |

## Duplicate Clusters To Collapse

These are meaningful only as aliases of a larger conflict. They should not each become separate revisit work.

| Collapse into | Duplicate labels / symptoms |
|---------------|-----------------------------|
| Hormuz / blockade mechanics vs bargaining logic | `blockade`, `hormuz`, `energy`, `commodity`, `currency`, `centcom`, `chain`, `control` |
| Trap / ratchet vs off-ramp | `alliance`, `audience`, `legitimacy`, `merge`, `primaries`, `dated`, `canonical`, `false` |
| Operational claims vs theory | `orbat`, `analytic`, `ground`, `military`, `casualty`, `history`, `falsifiers` |
| Source / verification hygiene | `claims`, `facts`, `source`, `verify`, `official`, `primaries` |
| Same-page inherited weave text | repeated calls beginning with "One arc, three seams", "Weave (this page)", "Abstract (this page)", or "Bridges ..." |

## Generated Noise To Suppress

These labels should not be treated as strategic conflicts without a stronger co-occurrence rule:

- `abstract`
- `after`
- `before`
- `bearing`
- `research/bridges`
- `capture`
- `carries`
- `chapter`
- `choreography`
- `cites`
- `clean`
- `commentary`
- `counts`
- `cross`
- `crosses`
- `default`
- `definition`
- `delegation`
- `episode`
- `explicit`
- `first`
- `frame`
- `language`
- `links`
- `operator`
- `planes`
- `primary`
- `promoting`
- `refined`
- `single`
- `speech`
- `still`
- `tracks`
- `verify`
- `weave`

These may appear inside good prose, but as labels they mostly indicate extraction artifacts, inherited scaffold words, or connective tissue. They are breath marks, not conflicts.

## Failure Modes

- **Token-level grouping is too permissive:** one shared word can create a group even when the underlying claims are unrelated.
- **Generic prose tokens are under-filtered:** words such as `abstract`, `research/bridges`, `frame`, `chapter`, and `weave` survive topic extraction.
- **Inherited page scaffolds duplicate across streams:** repeated phrases create artificial agreement or conflict across Davis / Diesen / Mercouris / Pape / Ritter.
- **Polarity cues are too blunt:** `pause`, `reopen`, `war`, `blockade`, and `escalation` can flip a loop into positive or negative without understanding the actual claim.
- **Same macro-conflict appears as many topics:** one real conflict can produce ten generated groups, making the register feel more complex than the judgment actually is.

## Furtwangler Judgment

The register should not be discarded. It is hearing real pressure. But it is hearing that pressure through a noisy room.

The living tensions are mostly six large conflicts, not 107 separate ones. The next Strategy-codex composition pass should preserve those six conflicts while suppressing generic topic labels and collapsing duplicates. Furtwangler says: keep the undertow, not every ripple.

## Recommended Repair

For a future implementation pass:

- Expand `TOPIC_STOPWORDS` with generic scaffold words listed above.
- Require at least one domain anchor before emitting a tension group, such as `hormuz`, `blockade`, `lebanon`, `israel`, `diplomacy`, `orbat`, `markets`, `mearsheimer`, `pape`, or `ritter`.
- Collapse generated topics into named conflict families before display.
- Hide tension groups where the only shared key is a scaffold word.
- Show a maximum of five tension families in conductor orientation, with a count of suppressed duplicates.

## Close

`Held open`: the audit does not resolve any strategy judgment. It identifies which tensions deserve preservation and which labels should be treated as generated noise.
