# Review as Bottleneck — and Interpretive Pause

**Anchor items:**

- [Moonshots (unscheduled) — Anthropic Pause, Recursive Self-Improvement, AI Personhood](../workshop/sheets/moonshots-emerging-anthropic-pause-recursive-personhood.md)
- [When AI builds itself — Anthropic Institute](https://www.anthropic.com/institute/recursive-self-improvement) (June 2026)
- Local product shift: [`docs/product-identity.md`](../../docs/product-identity.md), [`docs/grace-mar-instance-boundary.md`](../../docs/grace-mar-instance-boundary.md)

This note preserves two related seams from the June 2026 Anthropic RSI discussion **as they apply to strategy-codex**, not as vendor statistics to quote.

---

## Part A — Review as the control plane (here)

### Verbatim (local)

**A —** Anthropic’s inner loop makes **execution** cheap: merged code, closed experiment loops, session success on open-ended engineering. Their paper names the next constraint explicitly — **human review** (code review, research taste, org capacity). Amdahl’s law: speeding one stage relocates the bottleneck; it does not remove it.

**B —** In strategy-codex, the same relocation is visible without 80% merge stats. Agents already produce most **perspiration** in a session: verbatim captures, workshop sheets, script fixes, README wiring, fact-check tables, boundary docs. Throughput on WORK surfaces can exceed the operator’s ability to **validate, commit, and promote** each artifact in the same turn.

**C —** The load-bearing review functions in this repo are not “did the patch apply?” They are:

| Review seat | What it guards | Local instrument |
| --- | --- | --- |
| **Taste / routing** | Which lane, which artifact class, what is out of scope | Coffee A–D, PLAN vs EXECUTE, statecraft vs singularity default |
| **Provenance / verify** | Whether synthesis may treat a claim as floor truth | Fact-check triage, `source-archive/` verbatim discipline, workshop boundary warnings |
| **Promotion law** | What may become durable or identity-bearing | Record freeze, RECURSION-GATE (legacy), governed-adjacent membrane |
| **Ship / integration** | What enters git and remote | Commit-on-request, handoff receipt, validator passes with known dirty edges (e.g. submodules) |

**D —** **Algorithmic vs holistic gap** (METR’s reconciliation applies locally): auto-scorable wins — file exists, link wired, script exits 0 — can outrun **merge-ready judgment**. Green `validate-integrity` does not settle whether a podcast stat, a Milei op-ed, or a 52× micro-benchmark belongs in a promoted note.

**E —** The singularity-relevant claim is therefore **control-plane upstream**, not “models got smarter.” Once agent throughput rises, the scarce resources are:

- operator attention for verify and promotion
- explicit receipts (what was checked, what was abstained)
- rollback paths (revert commit, demote sheet → prompt only, freeze surface)

Pair with [coding swarms and human control planes](./coding-swarms-and-human-control-planes.md) for parallelism; this note is the **serial review** complement when one operator steers one interpretive machine.

### Reflection

Do not import Anthropic’s **76% session success** or **52× CPU task** as repo health metrics. Those are internal lab telemetries. The portable insight is **bottleneck migration**: if agents write captures and synthesis faster than the operator can certify them, the system’s quality ceiling moves from generation to **review architecture**.

For strategy-codex that means:

1. **Archive before synthesis** (verbatim SSOT) — reduces rewrite drift, increases review surface area on purpose.
2. **Workshop sheets carry boundary warnings** — synthesis is prompt, not law.
3. **Notes promote one seam** — review cost is bounded per artifact.
4. **Session continuity is contractual** (`docs/archive/skill-work-legacy/work-dev/session-continuity-contract.md`) — new agents do not inherit review state; harness paste is load, not memory.

The failure mode to watch: **review collapse** — treating agent fluency as verification because the next menu pick is already waiting.

### Foresight

- Reuse when intake velocity spikes (Moonshots, daily statecraft batches, multi-file EXECUTE threads).
- Route to [Agent control plane](../essays/agent-control-plane.md) when implementing permissions (read / act / commit / promote).
- Route to `work-dev` when building receipts into handoff-check or intake validators.
- Keep narrower than an essay until multiple lanes show the same review bottleneck with shared fixtures.

---

## Part B — Frozen Record vs Anthropic “option to pause”

### Same mechanism class?

**Partially — same family, different scope and enforceability.**

| Dimension | Anthropic global pause **option** | strategy-codex **Record freeze** |
| --- | --- | --- |
| **Intent** | Preserve ability to slow frontier capability when coordination exists | Stop identity accumulation in embedded fork; redirect growth to interpretive machine |
| **Trigger** | Hypothetical RSI threshold + verifiable multi-lab stop | Product decision (`record_frozen: true`); revive only via explicit tokens |
| **Mechanism** | Build verification infra (hotline class); voluntary coordinated slowdown | Typed membrane: WORK may grow; SELF/EVIDENCE/prompt default no merge |
| **Defection branch** | Competitors or states continue while others pause | Agents or sessions “merge” identity by habit — gate/skills bypass without operator discipline |
| **What still accelerates** | Lab capability, code merge, research loops | Archive intake, synthesis, skills, scripts, validators on governed-adjacent surfaces |
| **What is capped** | None today — only the *option* is argued | Record truth, Voice emulation, default gate nudges in harness |

**Shared structure:** both are **governance precedents** that separate **capability throughput** from **legitimacy throughput**. Anthropic asks the world to build a pause **before** RSI forces it. This repo implemented a **local pause** on one legitimacy channel (interpretive machine growth) while **keeping the inner loop** on interpretation infrastructure.

**Not the same:** Anthropic’s pause is **multilateral arms-control design** (hard verification problem). The Record freeze is **unilateral product architecture** (enforceable in git policy and operator habit). No third party must agree for the freeze to bind WORK routing.

### Interpretive pause (local name)

A useful local label: **interpretive pause** — not slowing agents, but refusing to let their outputs auto-enter identity or canonical truth.

Concrete expressions already in repo:

- `config/strategy_codex.yaml` — `record_frozen`, health nudges toward archive/validators not gate backlog
- Harness / handoff suppress fork-revive metrics when frozen
- `docs/deprecated-surfaces.md`, `bot/DEPRECATED.md` — Voice path closed
- Commit and merge discipline — operator remains review bottleneck for git truth

Anthropic: “If verification existed, we would pause with peers.”  
strategy-codex: “Verification is partitioned — agents may stage WORK; companion/operator gates identity.”

### Tension to preserve

Freezing the Record **does not** pause recursive improvement of the **machine**. Skills proliferate, validators tighten, synthesis objects compound — scenario **2** in the Anthropic paper. The risk is **split-brain**: fast interpretive RSI upstairs, frozen identity downstairs, operators inferring soul from harness weather.

The discipline is the same as Anthropic’s review bottleneck: **taste and promotion** must stay human-visible even when generation is abundant.

### Comparison table (headline)

| Question | Anthropic pause option | Record freeze |
| --- | --- | --- |
| Slows model training? | Only if coordinated + verified | No |
| Slows repo/agent WORK? | No | No — intentionally |
| Slows Record growth? | N/A | Yes — default |
| Builds option value for future crisis? | Yes — stated goal | Yes — for identity crisis / leakage |
| Depends on geopolitical trust? | Yes | No |
| Depends on operator discipline? | Yes (if unilateral) | Yes |

---

### Appendix

- **Parent sheet:** [moonshots-emerging-anthropic-pause-recursive-personhood.md](../workshop/sheets/moonshots-emerging-anthropic-pause-recursive-personhood.md)
- **Related:** [coding-swarms-and-human-control-planes.md](./coding-swarms-and-human-control-planes.md)
- **Related workshop:** [Agent control plane](../essays/agent-control-plane.md)
- **Local doctrine:** [from-accumulation-to-governed-interpretive-machine.md](../../essays/from-accumulation-to-governed-interpretive-machine.md)
- **Boundary:** [grace-mar-instance-boundary.md](../../docs/grace-mar-instance-boundary.md)
