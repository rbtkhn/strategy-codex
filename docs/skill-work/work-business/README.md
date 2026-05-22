# work-business

**Template mirror:** [companion-self `work-business/README.md`](https://github.com/rbtkhn/companion-self/blob/main/docs/skill-work/work-business/README.md) â€” grace-mar adds instance-specific ventures and accounting; diff is expected; align shared boilerplate when syncing.

**Objective:** Business planning, accounting, marketing, and market research for **operator-owned ventures** (Grace Gems, future ventures). Supports strategy, operations, financial tracking, and positioning. **WORK only**; not Record truth. Any merge to Record goes through RECURSION-GATE + companion approval.

**Singularity-academy consolidation:** This lane remains canonically `work-business`, but it is now also a live `singularity-academy` overlay when the operator is using ventures to test whether recursive, self-improving AI can produce durable leverage across real commercial work. Canonical singularity hub: [Singularity Workshop](../../../codex/academy/singularity/workshop/README.md).

**Instance boundary:** All accounting infrastructure, financial data, and venture-specific docs are **grace-mar only**. Nothing in this territory syncs to companion-self. The template provides the *shape* (`work-business.md` stub, seed survey); grace-mar fills it with specific ventures and financial data.

---

## Purpose

| Role | Description |
|------|-------------|
| **Business planning** | Per-venture strategy, roadmaps, competitive positioning, market research. |
| **Accounting** | Real bookkeeping: JSONL transaction ledger, P&L summaries, tax prep. See [accounting/README.md](accounting/README.md). |
| **Marketing** | Per-venture marketing plans, channel strategy, campaign tracking. See [marketing/README.md](marketing/README.md). |
| **Deep research** | Structured analysis on companies, technologies, commercial landscape. |
| **Evidence-linked** | Sources documented; keep ordinary business and singularity work in WORK docs rather than governed-state machinery. |

**Boundaries:** WORK only. No direct SELF/prompt edits. Logging to WORK docs and session notes; optional ACT- only when companion approves a candidate. Discipline is operator/process.
When this lane is being used under `singularity-academy`, do not introduce `candidates` as part of the normal workflow. Stay in WORK unless the operator explicitly asks to route something out to a governed surface.

### Singularity-use contract

When this lane is being used under `singularity-academy`, do not flatten business work into generic futurism. Keep the ordinary operating files, but ask one additional question per project:

- is AI merely assisting the venture, or recursively improving the workflow that runs it?
- where does authority live: human operator, platform, model, market, automation stack, or ledger?
- what part of the business becomes a control-plane issue instead of a task issue?
- what leverage compounds over repeated cycles strongly enough to count as evidence for the thesis?

---

## Contents

| Doc / file | Purpose |
|------------|---------|
| **This README** | Territory scope, purpose, boundaries. |
| **[WORK-LEDGER.md](WORK-LEDGER.md)** | Compounding watches + pointers ([work-template](../work-template/WORK-LEDGER.md) scaffold). |
| **[accounting/](accounting/)** | **Accounting surface** â€” ledger, chart of accounts, tax prep workflow. Entry: [accounting/README.md](accounting/README.md). |
| **[marketing/](marketing/)** | **Marketing surface** â€” per-venture plans, shared principles. Entry: [marketing/README.md](marketing/README.md). |
| **[grace-gems/](grace-gems/)** | **Grace Gems** (Etsy) â€” shop context, roadmap, agent-encoding, message-assist, market research, marketing plan, workflow reminders. Entry: [grace-gems/README.md](grace-gems/README.md). |
| **[grace-gems/monthly-operating-review.md](grace-gems/monthly-operating-review.md)** | Grace Gems monthly review checklist: books, shop health, marketing, and tax/compliance readiness. |
| **[xavier/](xavier/)** | Xavier business intake workspace (WORK-only starter pack). |
| **[worldland-decentralized-ai-mainnet-2026-03.md](worldland-decentralized-ai-mainnet-2026-03.md)** | Deep research: WorldLand / LiberVance (March 2026). |
| **[work-business-history.md](work-business-history.md)** | Append-only operator log. |

### Scripts (instance-specific)

| Script | Purpose |
|--------|---------|
| `scripts/emit_business_transaction.py` | Append one transaction to `business-ledger.jsonl` |
| `scripts/business_ledger_summary.py` | P&L, category breakdown, per-venture rollup, tax summary |

### Data

| File | Purpose |
|------|---------|
| `business-ledger.jsonl` | Append-only transaction log |
| `schema-registry/business-transaction.v1.json` | Transaction schema (instance-specific) |

---

## Cross-references

- [work-grace-gems](../work-grace-gems/README.md) â€” Legacy path; redirects to **grace-gems** above.
- [work-strategy](../work-strategy/) â€” Shared daily horizon, pipeline, [common-inputs](../work-strategy/common-inputs.md).
- [work-dev](../work-dev/) â€” OpenClaw, identity export, handback; potential integration with business research outputs.
- [AGENTS.md](../../../AGENTS.md) â€” Knowledge boundary, gated pipeline, no direct Record writes.

