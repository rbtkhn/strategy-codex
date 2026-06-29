---
audience: operator
authority: doctrine
record_status: frozen
---

# strategy-codex

**strategy-codex** — A **governed interpretive machine** for statecraft and singularity operator work: source archive → synthesis → notes → essays. **Product identity:** [docs/product-identity.md](docs/product-identity.md).

| Term | Plain meaning |
| --- | --- |
| **source archive** | Verbatim saved source material ([source-archive/statecraft/](source-archive/statecraft/README.md)) |
| **synthesis** | Interpreted daily/monthly judgment ([statecraft/synthesis/](statecraft/synthesis/METHOD.md)) |
| **note** | Bounded, source-backed analytical work product ([statecraft/notes/](statecraft/notes/README.md)) |
| **essay** | Polished cross-channel argument ([essays/](essays/README.md)) |
| **receipt** | Operational proof (ship, validation, handoff) — not default prose |
| **membrane** | Authority boundary — what a surface may own, cite, or promote ([work-membrane-v2.md](docs/work-membrane-v2.md)) |
| **archive (frozen)** | Historical / Record material — not default operator work ([grace-mar.md](docs/archive/grace-mar.md)) |

Older docs may use "transaction" for bounded lane objects. Going forward, use **note** for durable analytical work products. Use **transaction** only for operational receipts or machine workflow events.

**Glossary:** visitor terms → [public-orientation.md](docs/public-orientation.md) · Record/operator terms → [glossary.md](docs/glossary.md).

## Why this exists now

Model intelligence is getting cheaper. The scarce layer is the harness around it: source truth, context routing, artifact authority, review discipline, and accountable output.

**strategy-codex** is that harness for **statecraft** and **singularity** work — a **governed interpretive machine** that does not try to be the model; it governs how models, operators, sources, and judgment objects interact.

**Membrane** = an authority boundary that defines what a surface may contain, cite, mutate, promote, export, or regenerate. See [docs/work-membrane-v2.md](docs/work-membrane-v2.md).

**Deeper read:** [docs/intelligence-harness.md](docs/intelligence-harness.md) · [product-identity.md](docs/product-identity.md) · [from-accumulation essay](essays/from-accumulation-to-governed-interpretive-machine.md)

**Strategy-codex corpus:** [`codex/`](codex/README.md) is the first-class home for the polyphonic cognition streams, raw inputs, chapters, compiled views, and strategy-codex artifacts. The old `docs/skill-work/work-strategy/strategy-notebook/` path is deprecated compatibility only.

**New here?** [docs/start-here.md](docs/start-here.md) · [Essays](essays/README.md).

## Start here

This repository has **three canonical entry points**:

- **Human (operator):** [docs/start-here.md](docs/start-here.md)
- **Agent (LLM routing):** [LLM-ROUTING.md](LLM-ROUTING.md)
- **Machine (route registry):** [repo-map.yaml](repo-map.yaml)

All other navigation surfaces are secondary and should not be treated as entry points.

Grace-Mar is archived/frozen. Active strategy-codex work does not grow the fork. See [docs/archive/grace-mar.md](docs/archive/grace-mar.md).

**OB1 / legacy fork onboarding:** [docs/start-here-ob1-users.md](docs/start-here-ob1-users.md)

## Essays index — cross-channel theses {#essays-index}

Stand-alone arguments that may span **statecraft and singularity** live at repo-root **`essays/`** (not channel `*/essays/` compatibility stubs). Bounded seams stay in [statecraft/notes/](statecraft/notes/README.md) or [singularity/notes/](singularity/notes/README.md). Class law: [docs/prose-index.md](docs/prose-index.md).

**Shelf front door:** [essays/README.md](essays/README.md) — full inventory (titles, clusters, “open when…”). Do not duplicate that table here.

**Start here essay:** [from-accumulation-to-governed-interpretive-machine.md](essays/from-accumulation-to-governed-interpretive-machine.md)

Workshop **sheets** under `singularity/workshop/sheets/` remain the operating surface for live passes; link from each essay’s **Return Path** when you need the pass worksheet.

## Claude Code / Cursor surfaces

Model-portable harness (not a single-vendor stack): [docs/intelligence-harness.md](docs/intelligence-harness.md).

**Claude Code mental-model map** (skills, commands, memory, rules, review queue → repo equivalents): [docs/claude-surface-contract.md](docs/claude-surface-contract.md) — do not duplicate tables here.

**Related:** [docs/architecture.md](docs/architecture.md) · [docs/runtime-vs-record.md](docs/runtime-vs-record.md) · [docs/start-here.md](docs/start-here.md) · [docs/start-here-ob1-users.md](docs/start-here-ob1-users.md) · [docs/portable-working-identity.md](docs/portable-working-identity.md)

## Concept

**Active objective:** Operate a governed interpretive machine — [source-archive/statecraft/](source-archive/statecraft/README.md) → [statecraft/synthesis/day/](statecraft/synthesis/METHOD.md) → [statecraft/](statecraft/README.md) lane objects under **statecraft** and **singularity** channels. Cross-channel theses: [essays/](essays/README.md). See [docs/operator-two-channel-architecture.md](docs/operator-two-channel-architecture.md).

## Architecture

**System map (mermaid), promotion ladder, and operator ship loop:** [docs/start-here.md](docs/start-here.md) — do not duplicate here.

**Active system design:** [docs/architecture.md](docs/architecture.md) · [docs/operator-two-channel-architecture.md](docs/operator-two-channel-architecture.md) · [docs/harness-architecture-map.md](docs/harness-architecture-map.md)

**Promotion is governed, not ambient.** No artifact becomes more authoritative merely because it was summarized, reused, exported, or generated. Membrane SSOT: [docs/work-membrane-v2.md](docs/work-membrane-v2.md).

**Repo layout:** [docs/root-directory-map.md](docs/root-directory-map.md) · **Paths:** [docs/canonical-paths.md](docs/canonical-paths.md) · **Export CLI:** [docs/EXPORT-CLI.md](docs/EXPORT-CLI.md) · **Contribute:** [contributing.md](contributing.md)

## Quick Start — strategy-codex operator

1. Read [docs/start-here.md](docs/start-here.md).
2. Run **`coffee`** in Cursor — default user `strategy-codex`; Steward **A** favors boundary/git, not gate.
3. Statecraft front door: [statecraft/README.md](statecraft/README.md). Daily synthesis: [statecraft/synthesis/METHOD.md](statecraft/synthesis/METHOD.md).

```bash
python3 scripts/harness_warmup.py -u strategy-codex --compact
python3 scripts/check_repo_health.py --quick
```

## Developer preflight

Local tests and CI-shaped checks: [contributing.md](contributing.md) · [docs/perf-budgets.md](docs/perf-budgets.md) · [docs/cmc-routing.md](docs/cmc-routing.md)

## For AI coding assistants

Read [AGENTS.md](AGENTS.md) and [docs/agent-rules/deep-rules.md](docs/agent-rules/deep-rules.md). Default work: **statecraft** / **singularity** WORK.

## Credits

The ideas behind this project draw on the work of: Alexander Wissner-Gross (causal entropic forces), Peter Diamandis (abundance), Nick Bostrom (superintelligence), Ray Kurzweil (singularity), Brian Roemmele (multimodal AI), Scott Adams (systems thinking), Julian Jaynes (bicameral mind), and Satoshi Nakamoto (decentralized trust).

## License

- **Code and tooling:** Proprietary. All rights reserved.
- **Record / user data:** See [license-record](docs/archive/license-record) — user Records (SELF, EVIDENCE, etc.) are personal data owned by the user; the system holds them in trust.

