# Intelligence harness — strategy-codex

**Work only; not Record.**

This page is a **bridge doc** for visitors arriving from the AI-enterprise conversation. It adds external legibility without replacing canonical doctrine. Full argument: [from-accumulation essay](../essays/from-accumulation-to-governed-interpretive-machine.md). Product map: [product-identity.md](product-identity.md). **Architecture routing hub:** [harness-architecture-map.md](harness-architecture-map.md).

---

## Two names, one system

| Layer | Phrase |
|-------|--------|
| Internal / precise | **governed interpretive machine** |
| External / legible | **intelligence harness** for statecraft and singularity work |

Bridge sentence:

```text
strategy-codex surrounds cheap model intelligence with source truth, context routing,
artifact authority, review discipline, memory, and transaction objects so that
interpretation can become accountable judgment rather than disposable output.
```

**strategy-codex** is not an OpenAI, Claude, Grok, Cursor, or local-model system. It is the governed harness that lets any sufficiently capable model operate inside bounded context, authority, and review rules. See [portable-working-identity.md](portable-working-identity.md).

---

## Harness vs script harness

**Intelligence harness (product)** — the repo's governed structure around models: archive truth, membrane classes, skills, validators, operator loop, ship receipts, transaction ceilings.

**Harness script (tooling)** — operational scripts and eval surfaces that *implement* parts of that structure:

| Name | Role |
|------|------|
| `scripts/harness_warmup.py` | Operator session warmup / re-entry snapshot |
| `docs/harness-inventory.md` | **Grace-Mar fork** component inventory (legacy; gate-centric) |
| `run_conductor_eval_harness.py`, carry harness, MCP mock harness | Bounded eval / replay tooling |

Default **strategy-codex** operators: start here and [start-here.md](start-here.md). Fork-era gate inventory: [harness-inventory.md](harness-inventory.md) on explicit **`fork revive`** only.

---

## What cheap AI gives vs what we supply

| Cheap AI gives you | strategy-codex must supply |
| ------------------ | -------------------------- |
| summarization | source-truth discipline ([source-archive](../source-archive/statecraft/README.md)) |
| synthesis | bounded analytical objects ([work-membrane-v2.md](work-membrane-v2.md)) |
| memory | authority-ranked surfaces (Record vs runtime; [runtime-vs-record.md](runtime-vs-record.md)) |
| agents | transaction ceilings ([promotion ladder](#default-operator-loop)) |
| speed | review and ship receipts ([work-menu-conventions — Ship receipt](skill-work/work-menu-conventions.md#6a-ship-receipt)) |
| pattern extraction | validators and drift control ([validator-first skill](../.cursor/skills/validator-first/SKILL.md)) |

The moat is not "many notes." The moat is knowing **what kind of artifact** something is allowed to become. Canonical essay: [from-accumulation](../essays/from-accumulation-to-governed-interpretive-machine.md).

---

## Model / harness / operator / transaction

| Role | What it is | strategy-codex surface |
|------|------------|------------------------|
| **Model** | Cheap, replaceable intelligence | External; any vendor |
| **Harness** | Context, authority, review, routing | Repo doctrine, skills, validators, [work membrane](work-membrane-v2.md) |
| **Operator** | Decision rights, ship, judgment | Human + [work execution layer](glossary.md#work-execution-layer) |
| **Transaction object** | Accountable output ceiling | `statecraft/<lane>/transactions/`, daily synthesis, ship receipt |

Generic AI workflow mapping:

| Generic output | strategy-codex equivalent |
| -------------- | ------------------------- |
| Chat response | disposable |
| Summary | intermediate |
| Daily synthesis | operating context |
| Transaction object | accountable decision artifact |
| Ship receipt | audit trail |

---

## Two channels

| Channel | Harness function |
| ------- | ---------------- |
| **Statecraft** | Turns source streams into bounded **analytical judgment** objects |
| **Singularity** | Turns AI-system observations into bounded **architectural doctrine** |

Routing law: [operator-two-channel-architecture.md](operator-two-channel-architecture.md) — *what system is emerging* vs *what object must be judged*.

Lane overlays: [statecraft/work-membrane.md](../statecraft/work-membrane.md) · [singularity/work-membrane.md](../singularity/work-membrane.md)

---

## Default operator loop

**Promotion ladder (statecraft):**

```text
operator source
  → source-archive/statecraft/<pub_date>/<slug>.md   [verbatim SSOT]
  → generated day/month/year/thread indices
  → statecraft/daily/<YYYY-MM-DD>.md                 [daily synthesis]
  → statecraft/<lane>/transactions/<object>.md       [transaction object — default ceiling]
```

**Ship loop:**

```text
intake → sync check → intake queue report → synthesis/companion → commit → ship receipt → push
```

| Step | Command / surface |
|------|-------------------|
| Land + indices | `refresh_statecraft_archive_indices.py` |
| Archive ↔ daily sync | `check_statecraft_intake_daily_sync.py --day YYYY-MM-DD` |
| Intake queue report | `statecraft_intake_queue.py --day YYYY-MM-DD` ([spec](statecraft-intake-queue.md)) |
| Daily synthesis | `statecraft/daily/YYYY-MM-DD.md` |
| Ship receipt | `operator_handoff_check.py` → `## Ship receipt` |

**Record frozen (default):** Grace-Mar gate promotion applies only on explicit **`fork revive`**. Active work stays in the work membrane — not ambient RECURSION-GATE growth. See [grace-mar-instance-boundary.md](grace-mar-instance-boundary.md).

Full operator map: [start-here.md — Operator ship loop](start-here.md#operator-ship-loop)

---

## Intake queue (agent workbench loop)

Commercial agent stacks often run: **external signal → structured store → score → write-back → digest**. The strategy-codex equivalent adds a **Git-sovereign queue** before daily synthesis:

| Commercial pattern | strategy-codex |
| -------------------- | -------------- |
| Database rows | Archive frontmatter + derived sidecars |
| Lead score | Rule-based intake hints (`reasoning`; v0) |
| Write-back | `synthesis_status` in sidecar JSON |
| Top-five digest | `statecraft_intake_queue.py --write-digest` |

**Promotion is a queue problem, not a summarization problem.** Sidecars never replace archive body or daily synthesis authority.

Full spec: [statecraft-intake-queue.md](statecraft-intake-queue.md)

**Agent boundary:** classify, score, and draft — yes; contact, publish, or canonical merge — operator only.

---

## Three live examples

Pointers only — these are existing artifacts, not new content.

| Artifact type | Example | Role |
|---------------|---------|------|
| Daily synthesis | [statecraft/daily/2026-06-12.md](../statecraft/daily/2026-06-12.md) | Operating context for a landed archive day |
| Transaction object | [Hormuz transit / sanctions relief compact](../statecraft/transactions/hormuz-transit-sanctions-relief-compact/README.md) | Accountable four-lane crisis object with comparison surface |
| Ship receipt | [start-here — Operator ship loop](start-here.md#operator-ship-loop) · [Ship receipt convention](skill-work/work-menu-conventions.md#6a-ship-receipt) | Audit trail after bounded closeout |

**Singularity example:** [keystone-helix.md](../singularity/workshop/keystone-helix.md) (governed adjacent doctrine; also in [work-membrane-live-examples.md](work-membrane-live-examples.md)).

---

## Source-truth floor

As model intelligence gets cheaper, **source integrity gets more valuable**. Cheap synthesis can build on anything; the scarce question is whether it builds on a truthful floor.

In a governed interpretive phase, a bad transcript is more serious than in a loose archive — synthesis, comparisons, validators, and recursive learning may all assume it. See [from-accumulation essay — Why This Matters](../essays/from-accumulation-to-governed-interpretive-machine.md#why-this-matters).

High-leverage repair and intake surfaces:

- [statecraft-source-intake](../.cursor/skills/statecraft-source-intake/SKILL.md) — verbatim archive landing
- [transcript-cleanup](../.cursor/skills/transcript-cleanup/SKILL.md) — study-ready derivatives
- [wire-verify](../.cursor/skills/wire-verify/SKILL.md) — developing-story claim tiers before synthesis

---

## Return path

- [harness-architecture-map.md](harness-architecture-map.md)
- [product-identity.md](product-identity.md)
- [from-accumulation-to-governed-interpretive-machine.md](../essays/from-accumulation-to-governed-interpretive-machine.md)
- [work-membrane-v2.md](work-membrane-v2.md)
- [work-membrane-live-examples.md](work-membrane-live-examples.md)
- [agent-control-plane.md](../essays/agent-control-plane.md)
- [start-here.md](start-here.md)
- [statecraft-intake-queue.md](statecraft-intake-queue.md)
- [README — Why this exists now](../README.md#why-this-exists-now)
