# Predictive History (Research Overlay Module)

## Status

This is a research-stage analytical module.

## Scope Clarification

This module is explicitly:

- **ABOUT** the external system: [https://github.com/rbtkhn/predictive-history/](https://github.com/rbtkhn/predictive-history/)
- **NOT** part of it
- **NOT** modifying it
- **NOT** implementing it

## Classification

`singularity/research/predictive-history/`

## Purpose

To provide:

- theoretical analysis
- formal modeling
- structural critique
- conceptual extensions

of the referenced predictive-history system.

## Key Principle

Separation of:

- **external implementation** (source repo)
- **internal research interpretation** (this module)

## Non-modifying research constraint

All outputs in this folder are interpretive, analytical, or theoretical and **MUST NOT** influence or alter the external system directly.

This module is NOT:

- a fork of the system
- a modification layer
- an implementation extension
- a runtime integration module
- a dependency injection layer

## System hierarchy

```text
external repo (predictive-history)
        ↓  (referenced, not modified)
singularity/research/predictive-history  ← this module (meta-analysis)
        ↓  (only if later formalized)
statecraft/
        ↓
loops/ (execution layer)
```

No direct coupling exists between this folder and external runtime logic.

## Canonical homes (do not duplicate here)

| Surface | Path | Role |
| --- | --- | --- |
| Canonical corpus (EXECUTE) | [rbtkhn/predictive-history](https://github.com/rbtkhn/predictive-history) | Author, validate, push — sole corpus write surface |
| Inbound mirror | [`public/predictive-history/`](../../../public/predictive-history/) | Read-only snapshot in strategy-codex |
| Book / workshop residue | [`continuity/predictive-history/`](../../../continuity/predictive-history/) | Frozen workshop — read/intake only |
| Education factory | [`singularity/education/predictive-history/`](../../education/predictive-history/README.md) | Loop outputs (lessons, media, distribution) |
| YouTube transcript bundle | [`research/external/youtube-channels/predictive-history/`](../../../research/external/youtube-channels/predictive-history/) | External capture library |

Boundary SSOT: [`docs/predictive-history-external-boundary.md`](../../../docs/predictive-history-external-boundary.md)

## Research files

| File | Role |
| --- | --- |
| [external_reference.md](external_reference.md) | External system relationship and purpose |
| [theoretical_supplement.md](theoretical_supplement.md) | Conceptual extensions (WIP) |
| [formal_analysis.md](formal_analysis.md) | Formal decomposition / modeling (WIP) |
| [critique_and_gaps.md](critique_and_gaps.md) | Structural gaps analysis |
| [model_extensions.md](model_extensions.md) | Alternative frameworks (WIP) |
| [assumptions.md](assumptions.md) | Research-stage assumptions |
| [evaluation_framework.md](evaluation_framework.md) | Analytical evaluation criteria (WIP) |
| [evolution_log.md](evolution_log.md) | Version history |
