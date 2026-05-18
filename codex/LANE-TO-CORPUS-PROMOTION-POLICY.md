# Lane-to-Corpus Promotion Policy

**Purpose:** Define when one of the eight `codex/years/2026` strategy-author lanes should remain a **notebook-first lane over shared intake** and when it should be promoted into a **dedicated external corpus**. **WORK only**; not Record.

## Default model

The default strategy-codex pattern is:

- `codex/years/2026/<lane>/` is the **internal notebook lane**
- shared intake lives in:
  - `codex/years/2026/raw-input/`
  - `research/external/work-strategy/`
  - `research/external/youtube-channels/`
- a lane **consumes** shared external intake unless there is strong evidence that a dedicated corpus would improve retrieval, continuity, and analysis

This means the eight current lanes are **not** external by default:

- `alkorshid`
- `crooke`
- `davis`
- `diesen`
- `mercouris`
- `pape`
- `parsi`
- `ritter`

They are notebook-first strategy-author lanes that sit on top of shared upstream source infrastructure.

## Why Jiang is different

Jiang is the exception/template, not the default commentator-lane model.

`work-jiang` is already a corpus-first research program because it has:

- book-scale structure
- prediction-scale structure
- dedicated source registry and metadata
- recurring evidence-pack and chapter workflow
- clear payoff from chronology, quote discipline, and cross-episode tracking

That is why Jiang justifies a dedicated external corpus at `codex/predictive-history/`. The eight commentator lanes do **not** inherit that shape automatically.

## Promotion rule

A lane should be promoted to a dedicated external corpus only when shared intake no longer provides enough:

- structure
- continuity
- retrieval value
- quote discipline
- recurring-pattern tracking

Promotion is a workflow decision, not a prestige decision.

## Strict promotion threshold

A lane should meet **all or nearly all** of the following before promotion:

- **High corpus volume**
  - sustained accumulation of transcripts, essays, interviews, or posts over time

- **Strong recurrence in notebook work**
  - the lane appears repeatedly as a major analytical voice, not just in isolated bursts

- **Longitudinal analytical value**
  - the main payoff comes from cross-episode continuity rather than single-capture use

- **Workflow pressure on shared intake**
  - the shared substrate is no longer enough for retrieval, chronology, quote discipline, or recurring-pattern tracking

- **Need for corpus-specific structure**
  - dedicated claims, chronology, quote bank, source registry, evidence packs, divergence tracking, or similar surfaces would clearly improve the work

- **Tooling payoff**
  - lane-specific normalization, indexes, or crosswalks would save real effort rather than create ornamental complexity

### Not enough by itself

These are **not** sufficient reasons to promote a lane:

- lane importance alone
- operator interest alone
- one burst of raw-input activity
- one strong month of coverage
- vague arguments that a commentator “matters”
- the fact that Jiang already has a corpus

## Promoted target shape

When a lane is promoted, the target is a **dedicated external corpus** under `research/external/`, not an improvised scattering of files.

### Standard minimal skeleton

Use this minimal shape unless a later plan explicitly justifies more:

- `research/external/<lane-or-project>/README.md`
- `metadata/` or `sources/`
- `transcripts/` or equivalent source-text layer
- `analysis/`
- `claims/` or equivalent recurring-judgment layer

Optional additions only when justified:

- `quote-bank/` or quote index
- `chronology/`
- `prediction-tracking/`
- `evidence-packs/`
- `divergence-tracking/`

### Boundary rules after promotion

Promotion does **not** change the core architecture:

- `codex/years/2026/<lane>/` remains the canonical notebook lane
- `research/external/<lane-or-project>/` becomes the upstream structured source world for that lane
- promoted corpora remain **external/operator research**, not Record
- notebook judgment still lives in the strategy-codex lane files

## Current-state matrix for the eight lanes

This matrix is provisional and should be revised only when workflow evidence changes.

| Lane | Current status | Why |
|------|----------------|-----|
| `alkorshid` | **Stay shared** | Host/interviewer lane; value comes from mirrored guest episodes and host framing, not from a standalone corpus-first world. |
| `crooke` | **Stay shared** | Recurring and useful, but current use still fits shared intake plus lane-local notebook synthesis. |
| `parsi` | **Stay shared** | Important scope lane, but not yet showing enough corpus pressure to justify dedicated external structure. |
| `pape` | **Stay shared** | Strong analytical lane, but still largely manageable through shared raw-input plus notebook tracking. |
| `ritter` | **Watch for promotion** | High recurrence and volume pressure are visible, but the shared substrate is not yet clearly failing. |
| `davis` | **Near threshold** | Recurrent long-form material, repeated strategy use, cross-lane reuse, and growing continuity/retrieval pressure. |
| `diesen` | **Near threshold** | Dense recurring output and repeated strategic reuse suggest that a dedicated corpus may soon pay for itself. |
| `mercouris` | **Near threshold** | One of the densest recurring lanes; chronology, quote discipline, and cross-episode continuity may soon justify promotion. |

### Reading the matrix

- **Stay shared** means shared intake is still the correct default.
- **Watch for promotion** means the lane should be monitored for workflow pain, not promoted yet.
- **Near threshold** means the lane is the strongest candidate for a future promotion plan, but not an automatic promotion now.
- **Promote now** should be used only when the workflow evidence is overwhelming. No current lane in the eight-stream set is being marked that way in this policy pass.

## Non-goals and safeguards

### Non-goals

This policy does **not** mean:

- one lane = one corpus by default
- every important commentator deserves a Jiang-like structure
- promotion makes the lane itself external
- promotion is a prestige marker
- dedicated corpora are always better than shared intake

### Safeguards

- prefer shared intake until pain is proven
- do not split a lane into a corpus unless it will actually be maintained
- do not duplicate the same source world across multiple promoted corpora without explicit ownership
- treat host/interviewer lanes as especially poor candidates for standalone corpora unless the host framing becomes analytically primary

## Naming

Preferred phrase:

- **lane promotion to dedicated external corpus**

Avoid looser phrases such as:

- lane expansion
- source upgrade
- corpusification
- lane migration

Those blur the distinction between notebook lanes and external corpora.
