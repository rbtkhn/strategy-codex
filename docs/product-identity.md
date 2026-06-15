# Product identity — strategy-codex

**Work only; not Record.**

## What this repo is

**strategy-codex** is a **governed interpretive machine**: sources land verbatim in archive; bounded synthesis and transaction objects carry judgment; operator work routes through **statecraft** and **singularity**.

It is **not** primarily a system for growing a personal cognitive fork. The embedded Grace-Mar Record is a **frozen legacy sidecar**. See [`grace-mar-instance-boundary.md`](grace-mar-instance-boundary.md).

## System map

```mermaid
flowchart TB
  subgraph membrane [Work membrane active]
    Archive[source-archive/statecraft]
    Voices[statecraft/voices]
    States[statecraft/states]
    Daily[statecraft/daily]
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

Cross-channel theses at [`essays/README.md`](../essays/README.md); bounded notes stay in channel `notes/` only ([`prose-index.md`](prose-index.md)). Full operator map: [`start-here.md — System map`](start-here.md#system-map).

## Canonical essay

Full argument and success metrics: [`essays/from-accumulation-to-governed-interpretive-machine.md`](../essays/from-accumulation-to-governed-interpretive-machine.md)

**Essay shelf (primary):** [`essays/README.md`](../essays/README.md) — cross-channel stand-alone theses. Channel `notes/` remain scoped to statecraft or singularity only.

## Operator entry

- [`start-here.md`](start-here.md)
- [`essays/README.md`](../essays/README.md) — primary essay shelf (cross-channel theses)
- [`operator-two-channel-architecture.md`](operator-two-channel-architecture.md)
- [`AGENTS.md`](../AGENTS.md)
