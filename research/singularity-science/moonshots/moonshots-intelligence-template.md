# Moonshots Intelligence Document — template

work only; not Record.

**Output shape SSOT** for compiled intelligence documents. The compiler (`scripts/compile_moonshots_intelligence.py`) fills this structure when emitting `moonshots-ep-<N>-intelligence.md` (or `moonshots-emerging-<slug>-intelligence.md`).

Do not edit per-episode instances here — this file defines the canonical sections only.

---

## Provenance

- Archive: `{archive_path}`
- Episode: `{episode_number}`
- Source: `{source_url}`
- Compiler: `{compiler_version}` · prompt `{prompt_id}` · model `{model}`
- Generated: `{generated_at}`

## I. Core Thesis

`{core_thesis}`

## II. Dual-Layer Bullets

Each bullet (10+ when `--strict`):

### Bullet N (`{evidence_ref}`)

- **Claim:** `{claim}`
- **Mechanism:** `{mechanism}` — causal structure required
- **Implication:** `{implication}`

**Evidence (verbatim, ≥30 words):**

> `{evidence}`

## III. Concept Primitives

`{concept_primitives}`

## IV. Feedback Loops

### Reinforcing

`{feedback_loops.reinforcing}`

### Balancing

`{feedback_loops.balancing}`

## V. Meta-Insight Layer

`{meta_insight}`

## VI. NST Mapping (optional, `--nst`)

| evidence_ref | Object (claim) | Morphism (mechanism) | Functor (implication) | Ground anchor |
| --- | --- | --- | --- | --- |
| E1 | … | … | … | verbatim evidence |

---

**Invariant:** Evidence blocks must be verbatim substrings of [`source-archive/singularity/moonshots/`](../../../source-archive/singularity/moonshots/) — never paraphrased or stitched.
