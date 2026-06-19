# Prepared Context Doctrine

**Companion-Self template**

[Prepared context](prepared-context-layer.md) is the **staging layer** between [raw evidence](evidence-layer.md) and [governed state](governed-state-layer.md). It is optimized for agents and tools; it is **not** the Record and **not** silent approval.

**Constraint rule:** Read alongside [GRACEFUL-CONSTRAINT-DOCTRINE](graceful-constraint-doctrine.md). Prepared context must remain truthful under sparse, stale, partial, or unverifiable conditions; it may narrow or abstain, but it must not silently become stronger than its evidence base.

---

## Principles

1. **Raw evidence is not automatically good agent context.** Normalize, scope, and cite provenance before heavy use.
2. **Prepared context should be optimized for reasoning**, not mistaken for durable truth or the **Record** (see [concept.md](concept.md)).
3. **Preserve provenance** wherever practical (source path, date, extractor version).
4. **Prefer regenerability** — prepared bundles should often be rebuildable from evidence plus scripts.
5. **Material changes to governed state** still require **gate** or **change-review** pathways ([change-review.md](change-review.md)); refreshing context does not merge identity.

## Degraded prepared context

Prepared context can fail in more than one way:

| Condition | What it means | Correct behavior |
|-----------|---------------|------------------|
| **Partial bundle** | Some sources were available, others were not. | Mark the bundle partial; do not present it as comprehensive. |
| **Stale bundle** | Sources may have changed since generation or review. | Treat it as advisory until rebuilt or checked against source. |
| **Unverifiable bundle** | Provenance, extractor version, or source linkage is missing. | Narrow claims sharply or abstain from stronger synthesis. |
| **Degraded transform** | A preferred normalizer, parser, or toolchain was unavailable. | Preserve raw evidence linkage and say what transform did not occur. |

### Prohibited drift

Prepared context must not:

- silently become Record truth because it is cleaner than the source,
- claim freshness it cannot show,
- mask extraction gaps with polished synthesis,
- outrun the evidence layer simply because the runtime prefers a tidy bundle.

### Practical rule

If a prepared bundle is partial, stale, or unverifiable, the system should say so plainly and stop short of stronger identity, policy, or doctrine claims until source review closes the gap.

---

## Examples

- PDF converted to markdown for analysis  
- Transcript compressed into structured notes with pointers to source  
- Retrieval chunks generated from an evidence corpus  
- Seed survey answers normalized into schema-conformant JSON (seed-phase artifacts are **pre-activation**; after activation, governed updates use the pipeline)  

---

## See also

- [evidence-to-context-pipeline.md](evidence-to-context-pipeline.md)  
- [state-model.md](state-model.md)  
- [abstention-policy.md](abstention-policy.md) — uncertainty envelope on runtime-derived prepared context  
- Starter staging script: `scripts/stage-evidence.py` (optional; creates JSON stubs under `runtime/prepared-context/`)
