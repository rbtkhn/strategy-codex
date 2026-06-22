# START-HERE — strategy-codex

**Work only; not Record.** Governance law: [AGENTS.md](../AGENTS.md). Route discovery: [LLM-ROUTING.md](../LLM-ROUTING.md) → [statecraft/voices/INDEX.md](../statecraft/voices/INDEX.md).

---

## What this repo is

Canonical definition: [product-identity.md](product-identity.md). **Default path:** **C** (operator). Record under [`archive/grace-mar-instance/`](../archive/grace-mar-instance/) is **frozen**; [`self-library.md`](../self-library.md) stays active for reference; [`self-memory.md`](../self-memory.md) is session continuity — not Record.

**Namespace (voices / states / hosts):** [routing-reference.md](routing-reference.md) · `statecraft/voices/` · `statecraft/states/` · `statecraft/hosts/`

---

## Choose your path {#choose-your-path}

Pick **one letter**. **Default:** **C**. Seed calibration: [seed-phase-survey § Calibrate](seed-phase-survey.md#calibrate-from-your-start-here-path).

| Pick | You are… | Start here |
|------|----------|------------|
| **A** | Companion (fork revive / seed) | [grace-mar-instance-boundary.md](grace-mar-instance-boundary.md) |
| **B** | Parent or guardian | [seed-phase-survey.md](seed-phase-survey.md) |
| **C** | **Operator (default)** | Promotion ladder below · [statecraft/README.md](../statecraft/README.md) |
| **D** | Technical contributor | [skill-work/work-dev/](skill-work/work-dev/) |
| **E** | Curious visitor | [harness-architecture-map.md](harness-architecture-map.md) · [product-identity.md](product-identity.md) · [from-accumulation essay](../essays/from-accumulation-to-governed-interpretive-machine.md) |
| **F** | Journalist / blogger | [Door F](#door-f) |

<a id="door-f"></a>

### Door F — public-safe orientation {#door-f}

No seed intake or private operator material. [harness-architecture-map.md](harness-architecture-map.md) · [intelligence-harness.md](intelligence-harness.md) · [essays/README.md](../essays/README.md) · [ph-civ](https://github.com/rbtkhn/ph-civ).

---

## System map {#system-map}

```mermaid
flowchart TB
  subgraph membrane [Work membrane active]
    Archive[source-archive/statecraft]
    Voices[statecraft/voices]
    States[statecraft/states]
    Synth[statecraft/synthesis]
    Tx[statecraft lane transactions]
  end

  subgraph channels [Operator channels]
    SC[statecraft]
    SG[singularity]
  end

  Essays[essays/ primary prose shelf]

  subgraph frozen [Frozen sidecar]
    Record[self.md recursion-gate.md]
  end

  Archive --> Voices --> States
  Voices --> Daily --> Tx
  SC --> membrane
  SG --> singularity/
  SC --> Essays
  SG --> Essays
  Tx -.fork revive only.-> Record
```

Essays: [essays/README.md](../essays/README.md) · membrane: [work-membrane-v2.md](work-membrane-v2.md) · channels: [operator-two-channel-architecture.md](operator-two-channel-architecture.md)

---

## Promotion ladder (statecraft)

```
operator source
  → source-archive/statecraft/<pub_date>/<slug>.md   [verbatim SSOT]
  → generated day/month/year/thread indices
  → statecraft/synthesis/day/<YYYY-MM-DD>.md                 [daily synthesis]
  → statecraft/<lane>/transactions/<object>.md       [transaction object — default ceiling]
```

Fork revive only: `recursion-gate.md` → `process_approved_candidates.py --apply` · map: [strategy-codex-redesign-brief.md](strategy-codex-redesign-brief.md)

---

## Operator loop & commands

```text
intake → sync check → intake queue → synthesis → commit → ship receipt → push
```

| Step | Command / surface |
|------|-------------------|
| Land + indices | `python3 scripts/refresh_statecraft_archive_indices.py` (`--check` for CI) |
| Archive ↔ daily sync | `python3 scripts/check_statecraft_intake_daily_sync.py --day YYYY-MM-DD` or `--latest` |
| Intake queue | `python3 scripts/statecraft_intake_queue.py --day YYYY-MM-DD` — [spec](statecraft-intake-queue.md) |
| Daily synthesis | `statecraft/synthesis/day/YYYY-MM-DD.md` or `state synthesis`; validate: `validate_statecraft_daily_synthesis.py` |
| Session warmup | `python3 scripts/harness_warmup.py -u strategy-codex --compact` |
| Ship receipt / push | `operator_handoff_check.py` → commit lane slices → `git push` when clean |
| Gate review | **Fork revive only** — [archive/grace-mar.md](archive/grace-mar.md) |

Conventions: [work-menu-conventions — Ship receipt](skill-work/work-menu-conventions.md#6a-ship-receipt) · script index: [contributing.md](../contributing.md)

---

## Index surfaces

**Operator default:** [statecraft/README.md](../statecraft/README.md) · archive SSOT: [source-archive/statecraft/README.md](../source-archive/statecraft/README.md) · daily method: [statecraft/synthesis/METHOD.md](../statecraft/synthesis/METHOD.md). Full map: [LLM-ROUTING.md](../LLM-ROUTING.md) · [architecture.md](architecture.md) · [deprecated-surfaces.md](deprecated-surfaces.md)
