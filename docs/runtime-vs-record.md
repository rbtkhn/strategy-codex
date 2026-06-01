# Runtime vs durable Record

**Purpose:** One-screen map of what is **canonical and governed** versus what is **temporary, derived, or operator-only** — so skill cards, lane compression, and harness output stay in the right bucket.

Primary doctrine in this repo stays **derived / rebuildable / non-canonical**. If `shadow layer` is used informally for some rebuildable outputs, it is only a metaphor and does not replace the terms here.

**Companion:** [operator-mental-model.md](operator-mental-model.md) (navigation-oriented summary).

**Shared membrane:** [work-membrane-v2.md](work-membrane-v2.md) defines the typed model across `Record`, `governed adjacent`, `instrumental work`, `runtime / derived`, and `external complements`. This page stays focused on authority and freshness, not the full lane overlay grammar.

**Constraint rule:** Read alongside [GRACEFUL-CONSTRAINT-DOCTRINE](graceful-constraint-doctrine.md). When regeneration fails, dependencies disappear, or context thins, the system should degrade visibly and preserve authority boundaries rather than bluffing freshness.

---

## Durable Record (four surfaces)

These change only through the **gated pipeline** and companion-approved merge ([AGENTS.md](../AGENTS.md)):

| Surface | On-disk anchors (typical) | Holds |
|---------|---------------------------|--------|
| **SELF** | `self.md` | Identity, SELF-KNOWLEDGE (IX-A/B/C), narrative |
| **SELF-LIBRARY** | `self-library.md` | Governed reference, CIV-MEM scopes |
| **SKILLS** | `self-skills.md` | Capability index (THINK / WRITE / work skills as documented) |
| **EVIDENCE** | `self-archive.md` | Activity log, artifacts log, approved evidence |

**Approval Inbox:** `recursion-gate.md` — staging only until processed.

---

## Work territories (`docs/skill-work/work-*`)

Work lanes are for planning, judgment, notebooks, and execution support. They are **not** Record truth. In membrane-v2 terms they are primarily `instrumental work`, while some durable outputs they produce may stabilize as `governed adjacent` or `runtime / derived` surfaces. Promotion into SELF / EVIDENCE / prompt requires the same **gate + merge script** as any other profile change.

---

## Runtime-only and derived (not Record)

| Kind | Examples | Rule |
|------|------------|------|
| **Session / harness paste** | Warmup output, operator menus, chat context | Weather, not policy; do not treat as SELF |
| **MEMORY** | `self-memory.md` | Continuity; **not** a substitute for gated facts |
| **Skill cards** | `artifacts/skill-cards/*.json` from [`build_skill_cards.py`](../scripts/build_skill_cards.py) | Derived from portable skills; [spec](skills/skill-card-spec.md) |
| **Active lane compression** | `artifacts/context/active-lane-*.md` from [`compress_active_lane.py`](../scripts/compress_active_lane.py) | Points back to lane README and `self-work.md`; [doc](skill-work/active-lane-compression.md) |
| **Vector index** | `.chroma` | Retrieval aid; rebuild from Record |
| **Runtime observations ledger** | `runtime/observations/index.jsonl` | Append-only work-lane notes; [README](../runtime/observations/README.md); not Record |
| **Tacit capture** | `runtime/tacit/` (`inbox/`, `normalized/`, `candidates/`, optional `index.jsonl`) | Markdown intake → JSON → review-only candidates; [README](../runtime/tacit/README.md), [doc](tacit-capture/README.md); not Record |
| **Retrieval-miss ledger** | `runtime/retrieval-misses/index.jsonl` | Append-only retrieval-miss log for debugging; [doc](retrieval-miss-ledger.md); not Record |
| **Runtime memory payloads** | `src/grace_mar/runtime/runtime_memory.py` | Strategy Codex runtime-only payload builders for continuity, retrieval, and briefing; adjunct to the OB1 bridge; [doc](runtime/runtime-memory.md); not Record |
| **Hybrid retrieval** | `scripts/runtime/hybrid_retrieve.py` | Non-canonical ranked search across surfaces; [doc](hybrid-retrieval.md); not Record |
| **Chunk indexes** | `runtime/chunks/**/*.chunks.jsonl` | Generated retrieval-aid chunks; rebuildable; [doc](chunked-retrieval.md); not Record |
| **Runtime worker** | `runtime/runtime-worker/` (`proposals/`, `traces/index.jsonl`, `receipts/`) | Disposable inspect / optional LLM summary; [doc](runtime-worker.md), [execution receipts](runtime/execution-receipts.md); not Record |
| **Workflow depth receipts** | `runtime/workflow-depth/index.jsonl` | Halt/continue log for adaptive `build_budgeted_context` runs; [context-budgeting](runtime/context-budgeting.md); not Record |
| **Runtime complements (membrane v1)** | `runtime/runtime-complements/` (`exports/`, `inbox/`, `receipts/`, `examples/`); [export](../scripts/runtime/export_runtime_context.py) / [import](../scripts/runtime/import_runtime_observation.py) | Bundles and inbox imports for external harnesses; receipts are audit-only; not Record; [doctrine](runtime/runtime-complements.md) |

### Runtime complements (membrane v1)

External runtimes (Letta, Mem0, Thoth, etc.) exchange material with this repo only through **explicit export bundles** and **inbox + receipt** imports, not by walking Record trees. The membrane extends live interaction and operator workflow; it does **not** change what counts as governed Record. Anything that should become SELF, EVIDENCE, or prompt still stages and passes through the normal gate. See [docs/runtime/runtime-complements.md](runtime/runtime-complements.md).

## Degraded conditions

When preferred helpers or regeneration paths are unavailable:

- **Record authority does not move.** SELF, SELF-LIBRARY, SKILLS, EVIDENCE, and the approval inbox remain authoritative even if every derived convenience surface is stale or absent.
- **Derived surfaces must fail visibly.** A skill card, lane compression, runtime memory payload, or dashboard may become incomplete, stale, or unavailable; it must not silently posture as current Record truth.
- **Runtime layers may narrow, not promote.** If continuity aids are thin, the system may abstain, shorten output, or fall back to direct source reading. It must not compensate by treating runtime material as canonical.
- **Provenance outranks fluency.** Under constraint, it is better to name the missing regeneration or missing source than to keep a polished surface that has lost its evidentiary footing.

### Practical rule

If a runtime-only or derived surface cannot currently prove freshness, treat it as advisory or historical until it is rebuilt or checked against source. Constraint does not weaken Record authority; it narrows what derivative layers may honestly claim.

---

## Must never bypass approval

- No “helpful” merges into `self.md`, `self-archive.md`, or `bot/prompt.py` without **RECURSION-GATE** + documented merge path.
- No treating **derived** summaries as new facts in the Voice or Record.
- No collapsing portable-record rationale schemas, rebuild receipts, and `/artifacts/` directory policy into one undifferentiated “artifact” concept.

---

## Forecasting boundary

Forecast outputs belong to work unless and until a human separately stages a downstream conclusion for review.
A forecast artifact is not a Record fact.
It is a provisional planning object with explicit assumptions, invalidators, and uncertainty.
See [docs/skill-work/work-forecast/forecast-protocol.md](skill-work/work-forecast/forecast-protocol.md).

## Forecast receipts and observability

Forecast artifacts, forecast receipts, and forecast observability reports belong to work.
They are rebuildable legibility surfaces, not Record truth.

A forecast may inform planning.
A forecast may not directly redefine identity, memory, or canonical claims.

## Forecast references inside work-strategy

Forecast artifacts may be cited inside watches, notebooks, and decision points in work.
That citation does not make the forecast a Record fact.

Forecasting belongs to planning and judgment support.
Record changes still require separate staging and approval.

---

## Where to read next

- [conceptual-framework.md](conceptual-framework.md) — triad and knowledge boundary  
- [docs/skill-work/context-efficiency-layer.md](skill-work/context-efficiency-layer.md) — CEL  
- [artifacts/README.md](../artifacts/README.md) — derived artifact policy
- [portable-record/promotion-rules.md](portable-record/promotion-rules.md) — how approved external candidates enter canonical surfaces  
