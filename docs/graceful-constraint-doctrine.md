# Graceful Constraint Doctrine

**Purpose:** State a system-wide design rule for strategy-codex: a governed layer is only truly trustworthy if it can preserve its discipline under degraded conditions, not just under ideal ones.

**Status:** Repo doctrine note. Read alongside [OPERATING-PRINCIPLES](operating-principles.md), [PORTABILITY](portability.md), [RUNTIME-VS-RECORD](runtime-vs-record.md), and [RECURSION-GATE](../recursion-gate.md).

## Core rule

**Design for graceful constraint, not just expressive abundance.**

A layer is only truly governed if it can keep its boundary, provenance, and verification behavior when the room gets poorer:

- dependencies missing
- context thinner than expected
- evidence incomplete
- toolchains degraded
- sessions interrupted
- runtime comfort absent

The test is not whether the layer behaves beautifully when everything it prefers is available. The test is whether it remains legible, honest, and bounded when those comforts disappear.

## Why this matters

Abundance can hide weak architecture.

A system may look elegant when every helper is present, every dependency resolves, and every context surface is loaded. But if verification falls silent, provenance blurs, or authority drifts the moment those conveniences disappear, then the governance was ornamental rather than structural.

Constraint is therefore a truth test. It reveals:

- whether verification is core or optional
- whether portability is real or merely comfortable
- whether abstention is available when context thins
- whether the human gate still holds when automation frays
- whether derivative artifacts can fail visibly instead of bluffing freshness

## Failure modes

| Mode | Behavior under pressure | What it means |
|------|--------------------------|---------------|
| **Abundance-only design** | Works beautifully while every dependency and helper is present; loses coherence when comfort disappears. | Elegance without resilience. |
| **Graceful degradation** | Narrows capability, preserves provenance, and stays explicit about what still holds. | The target state. |
| **Silent drift** | Keeps acting confident while verification, freshness, or authority boundaries have already weakened. | The most dangerous failure. |
| **Visible abstention** | Stops, names the missing condition, and preserves the boundary rather than bluffing continuity. | Honest constraint handling. |

## Where the principle applies

### 1. Record and gate governance

If normal helpers are unavailable, the boundary must still hold:

- no silent merge
- no approval bypass
- no authority drift
- human review remains load-bearing

### 2. Derived artifacts

Rebuildable surfaces should remain honest under degraded toolchains.

If an artifact cannot be refreshed, the system should:

- fail visibly
- degrade narrowly
- preserve provenance

It should not bluff freshness or silently widen assumptions.

### 3. Memory and continuity

A continuity layer should still help under sparse context.

If memory only works when every supporting surface is fully loaded, then it is not yet a robust continuity layer. Thin-context continuity is part of the design bar.

### 4. Voice and prompt behavior

A trustworthy voice is not just fluent under full context. It must also:

- abstain cleanly
- name uncertainty
- preserve the knowledge boundary
- refuse to invent continuity it cannot justify

### 5. WORK execution lanes

A work lane is more mature when its routing, receipts, and review surfaces still work under friction:

- missing dependencies
- partial sources
- mixed or dirty trees
- interrupted sessions
- thin evidence

## Next surfaces to apply this to

### 1. [runtime-vs-record.md](runtime-vs-record.md)

This surface already names the distinction, but it should say more directly what happens when regeneration fails, context thins, or runtime helpers disappear. The key question is not only what is canonical, but what must abstain rather than bluff freshness.

### 2. [prepared-context-doctrine.md](prepared-context-doctrine.md)

Prepared context is where abundance can most easily masquerade as truth. This surface should explicitly describe partial, stale, and unverifiable bundles, and what stronger claims they are not allowed to carry.

### 3. [operator-surface-staleness.md](operator-surface-staleness.md)

This is the operator-facing version of the same principle. It should make visible degradation states and return paths to authority surfaces more concrete, so a polished dashboard tone never outruns epistemic honesty.

## Design implications

When building or revising a layer, prefer:

1. **Visible degradation over silent improvisation**
2. **Narrow fallbacks over broad permissiveness**
3. **Explicit unsupported cases over fake universality**
4. **Reproducible receipts over unaudited convenience**
5. **Human-readable failure over hidden fragility**

The system does not need to do everything under scarcity. It needs to remain truthful about what it can and cannot still do.

## Portable-skills example

The portable-skills verifier repair is a concrete instance of this doctrine.

First, the portable layer contract was hardened: host-equivalent placeholders, approval-first wording, no duplicate-lane sprawl, cleaner runtime/source separation.

Then the verifier path was repaired so that the same layer could still be checked in the bundled runtime even when `PyYAML` was unavailable. That second step mattered because portability without runnable conscience is only declared portability.

This is the pattern the doctrine names:

- harden the contract
- restore the conscience under constraint

## Practical test

Before calling a layer governed, ask:

1. What happens if a preferred dependency disappears?
2. What happens if the context gets thinner?
3. What happens if regeneration cannot complete?
4. What boundary still holds under that degradation?
5. What receipt or verifier can still speak honestly?

If the answer is "the layer becomes unverifiable but still claims to be governed," the work is incomplete.

## Bottom line

Portability is not just the freedom to travel. It is the ability to keep one's discipline after comfort disappears.
