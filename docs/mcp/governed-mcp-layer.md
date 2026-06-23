# Governed MCP layer (Grace-Mar)

**Status:** Planning and policy surface only. This document does **not** connect MCP servers or execute external tools.

**Related:** Read-only export adapter â€” [`platform/integrations/mcp-adapter.md`](../platform/integrations/mcp-adapter.md). Internal worker trust (different domain) â€” [`schemas/worker-trust-registry.v1.schema.json`](../../schemas/worker-trust-registry.v1.schema.json). Capability registry â€” [`platform/config/mcp-capabilities.yaml`](../../platform/config/mcp-capabilities.yaml), schema [`schemas/mcp-capability.v1.json`](../../schemas/mcp-capability.v1.json). Lane â†” authority bindings â€” [`platform/config/mcp-authority-bindings.yaml`](../../platform/config/mcp-authority-bindings.yaml), [`mcp-authority-bindings.md`](mcp-authority-bindings.md). Execution receipts â€” [`schemas/mcp-execution-receipt.v1.json`](../../schemas/mcp-execution-receipt.v1.json), [`mcp-execution-receipts.md`](mcp-execution-receipts.md). MCP stack overview â€” [`mcp-stack-overview.md`](mcp-stack-overview.md). Governance runbook â€” [`mcp-governance-runbook.md`](mcp-governance-runbook.md).

---

## What MCP is

**Model Context Protocol (MCP)** is a hostâ€“tool protocol: clients (IDEs, assistants) discover tools and exchange structured requests/responses. It is **not** merge authority and **not** Grace-Marâ€™s Record.

---

## Why MCP must stay governed

Grace-Mar separates **interface/runtime assistance** from **canonical durable state**. MCP tools may speed retrieval, drafting, and WORK-layer coordination; they must **not** become a silent path into `self.md`, EVIDENCE, `archive/grace-mar-instance/bot/prompt.py`, or other gated surfaces. Merge authority stays with the companion and the governed pipeline ([`AGENTS.md`](../../AGENTS.md)).

---

## Runtime vs Record

| Side | Role |
|------|------|
| **Runtime / WORK** | Sessions, scripts, exports, assistant drafts, receipts, scratch patches â€” visible and inspectable. |
| **Record (canonical)** | Approved identity and evidence â€” merged only via [`recursion-gate.md`](../../recursion-gate.md) and [`process_approved_candidates.py`](../../scripts/process_approved_candidates.py) (human gate). |

MCP outputs belong on the **runtime / WORK** side until promoted through the gate.

---

## MCP authority ladder (informal)

1. **Read-only retrieval** â€” governed exports, public URLs, read-only DB/GH views (receipts encouraged).
2. **Work artifacts** â€” Markdown/JSON under WORK lanes, logs, operator-visible drafts.
3. **Evidence stubs / prepared context** â€” pre-canonical material feeding review.
4. **Candidate proposals** â€” YAML/text staged for [`recursion-gate.md`](../../recursion-gate.md).
5. **Canonical merge** â€” companion-approved apply only.

Skipping steps 4â€“5 for â€œdurable identity truthâ€ is an anti-pattern.

---

## Allowed vs prohibited (examples)

Illustrative capability **classes** live in [`platform/config/mcp-capabilities.yaml`](../../platform/config/mcp-capabilities.yaml). Examples:

| Intent | Allowed posture | Prohibited |
|--------|-----------------|------------|
| Browse repo / docs | Read-only paths, export views | Writing into `self.md` without gate |
| SCM | Read issues/PRs; draft branches as **proposals** | Merge to default branch as Record truth |
| Web | Fetch/summarize with citations | Treating fetched text as merged museum knowledge section A |
| Shell | **Policy default:** not enabled for governed MCP (`shell_execution_prohibited` class) | Arbitrary subprocess on operator machine |
| External memory | Policy class rejects silent sync | Implying retrieval = gate approval |

---

## How MCP outputs become stubs, artifacts, or candidates

- **Evidence stubs / prepared context:** Operator tooling may emit structured drafts; they remain **non-canonical** until merged.
- **Work artifacts:** Logs, dashboards, lane files â€” rebuildable, non-Record ([`runtime/artifacts/README.md`](../../runtime/artifacts/README.md)).
- **Gate candidates:** YAML blocks or drafts appended via staging conventions â€” **never** auto-merge.

---

## Why durable mutation requires review

Durable changes encode **identity and accountability**. Tooling cannot substitute for companion consent; â€œthe model wrote itâ€ or â€œMCP returned successâ€ is **not** approval. Review preserves auditability and aligns with [`authority-values.md`](../authority-values.md) and source-of-truth rules.

---

## Authority binding (lanes â†” `authority-map.json`)

Each **`output_lane`** in [`platform/config/mcp-capabilities.yaml`](../../platform/config/mcp-capabilities.yaml) must map to exactly one row in [`platform/config/mcp-authority-bindings.yaml`](../../platform/config/mcp-authority-bindings.yaml). Bindings pin lanes to **`authority_surface`** keys from [`platform/config/authority-map.json`](../../platform/config/authority-map.json) so capability posture cannot drift into wider write classes without an explicit policy edit.

Cross-check (writes [`runtime/artifacts/mcp-authority-report.md`](../../runtime/artifacts/mcp-authority-report.md)):

```bash
python3 scripts/mcp_authority_check.py
```

Use **`--strict`** to fail when informational warnings fire (e.g. unused binding lanes). Full rationale and mapping table: **[`mcp-authority-bindings.md`](mcp-authority-bindings.md)**.

---

## Execution receipts

Every capability class that may emit tool-shaped work should produce **execution receipts** ([`schemas/mcp-execution-receipt.v1.json`](../../schemas/mcp-execution-receipt.v1.json)): structured audit metadata linking **`capability.id`**, **`output_lane`**, and **authority** resolved from bindings. Receipts live under **[`runtime/artifacts/mcp-receipts/`](../../runtime/artifacts/mcp-receipts/)** â€” **WORK/runtime artifacts**, not canonical Record. **Receipts do not grant approval**; durable Record change still requires recursion-gate review and companion-approved merge.

Before enabling **live MCP integration**, receipt generation and validation (`scripts/mcp_receipt.py`, `scripts/mcp_receipt_audit.py`) should be part of the operator workflow so posture cannot drift unseen. Full semantics: **[`mcp-execution-receipts.md`](mcp-execution-receipts.md)**.

---

## Research-to-evidence stubs

Structured research JSON ([`schemas/research-evidence-input.v1.json`](../../schemas/research-evidence-input.v1.json)) can be turned into **pre-canonical** Markdown under **[`runtime/artifacts/evidence-stubs/`](../../runtime/artifacts/evidence-stubs/)** via **`scripts/research_to_evidence_stub.py`**. Each run also emits an **MCP execution receipt** in **`runtime/artifacts/mcp-receipts/`**. Stubs are **not** canonical evidence; promotion follows the ordinary **`recursion-gate.md`** / review path â€” **[`research-to-evidence-stubs.md`](research-to-evidence-stubs.md)**.

---

## Coding-agent patch intake

Structured intake JSON ([`schemas/coding-agent-patch-intake.v1.json`](../../schemas/coding-agent-patch-intake.v1.json)) can be turned into a **patch-review Markdown packet** under **[`runtime/artifacts/patch-intake/`](../../runtime/artifacts/patch-intake/)** via **`scripts/coding_agent_patch_intake.py`**. Each run emits an **MCP execution receipt** under **`runtime/artifacts/mcp-receipts/`**. Packets are **candidate proposals**, not merges or approvals â€” merge authority stays outside the adapter â€” **[`coding-agent-patch-intake.md`](coding-agent-patch-intake.md)**.

---

## Manifest admission

Declared MCP server manifests ([`schemas/mcp-server-manifest.v1.json`](../../schemas/mcp-server-manifest.v1.json)) can be validated and classified **without executing MCP** via **`scripts/mcp_manifest_admission.py`**. Output lands under **`runtime/artifacts/mcp-admission/`** with an **`mcp_manifest_admission`** receipt in **`runtime/artifacts/mcp-receipts/`** (`work_artifact` lane). This step is **admission review**, not live integration approval â€” **[`mcp-manifest-admission.md`](mcp-manifest-admission.md)**.

---

## Mock execution harness

Fixture JSON ([`schemas/mcp-mock-run.v1.json`](../../schemas/mcp-mock-run.v1.json)) can exercise **MCP-shaped tool calls** against registry classes **without launching MCP servers** via **`scripts/mcp_mock_harness.py`**. Output lands under **`runtime/artifacts/mcp-mock-runs/`** with an **`mcp_mock_harness`** receipt in **`runtime/artifacts/mcp-receipts/`**. Every mock run produces a receipt; **live integration remains a separate future decision** â€” **[`mcp-mock-execution-harness.md`](mcp-mock-execution-harness.md)**.

---

## Local read-only adapter

Bounded UTF-8 file reads against **[`platform/config/mcp-local-read-allowlist.yaml`](../../platform/config/mcp-local-read-allowlist.yaml)** via **`scripts/mcp_local_readonly.py`** produce Markdown under **`runtime/artifacts/mcp-local-read/`** plus MCP receipts with **`filesystem_readonly`**. **Local repo-scoped read-only runs are allowed only through this allowlisted adapter**, **every run gets a receipt**, **no general MCP integration is enabled**, and **Record promotion remains gated** â€” **[`mcp-local-readonly-adapter.md`](mcp-local-readonly-adapter.md)**.

---

## Local directory index adapter

Repo-scoped **directory metadata** listings (paths, kinds, sizes; optional line counts and hashes â€” **no file bodies**) against **[`platform/config/mcp-local-read-allowlist.yaml`](../../platform/config/mcp-local-read-allowlist.yaml)** via **`scripts/mcp_local_index.py`** produce Markdown under **`runtime/artifacts/mcp-local-index/`** plus MCP receipts with **`filesystem_readonly`**. **Local indexing runs are allowed only through this adapter**, **every run gets a receipt**, **no file contents are emitted**, **no general MCP integration is enabled**, and **Record promotion remains gated** â€” **[`mcp-local-index-adapter.md`](mcp-local-index-adapter.md)**.

---

## Risk / permission scanning

New capability classes should be **risk-scanned** before admission using **`scripts/mcp_risk_scan.py`** against [`platform/config/mcp-risk-policy.yaml`](../../platform/config/mcp-risk-policy.yaml) â€” see **[`mcp-risk-permission-scanner.md`](mcp-risk-permission-scanner.md)**. The scanner **does not execute MCP servers**; it classifies **permission risk**, not factual truth. **Passing the scan does not approve live integration** â€” it only clears structured blocker rules on registry policy text.

---

## Audit

Regenerate the Markdown report after editing the registry:

```bash
python3 scripts/mcp_capability_audit.py
```

Output: [`runtime/artifacts/mcp-capability-report.md`](../../runtime/artifacts/mcp-capability-report.md). Use `--strict` in CI if you want the process to fail when heuristics flag risk.

After changing bindings or `authority-map.json`, run **`mcp_authority_check.py`** as well (see **Authority binding** above).

---

## Governance consolidation

The **[`mcp-stack-overview.md`](mcp-stack-overview.md)** table summarizes the full MCP substrate (registry, bindings, receipts, risk, adapters). **[`mcp-governance-runbook.md`](mcp-governance-runbook.md)** documents the operator sequence; **`scripts/run_mcp_governance_checks.py`** runs that sequence against committed examples and writes **`runtime/artifacts/mcp-governance-demo-report.md`** (no live MCP servers, **`subprocess`** without shell).

Passing the consolidation run **does not** approve arbitrary **live MCP** integration or canonical Record merges â€” **live MCP remains a separate operator decision**; merge authority stays with the companion and **[`recursion-gate.md`](../../recursion-gate.md)** / **`process_approved_candidates.py`** per **[`AGENTS.md`](../../AGENTS.md)**.

