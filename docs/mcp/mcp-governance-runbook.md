# MCP governance runbook

**Purpose:** Run the **governed MCP toolchain** in a safe order using **committed examples only** â€” **no live MCP servers**, **no credentials**, **no network**, **no shell beyond `python` invoking repo scripts**. Canonical Record files under **``** are not written by these steps.

**Automation:** From repo root:

```bash
python3 scripts/run_mcp_governance_checks.py
```

Writes an aggregated report to **`runtime/artifacts/mcp-governance-demo-report.md`**, audit outputs under **`runtime/artifacts/mcp-governance-demo/`**, and adapter packets under each scriptâ€™s required bucket using **`governance-demo-*`** filenames (see table below).

**Related:** **[`mcp-stack-overview.md`](mcp-stack-overview.md)**, **[`governed-mcp-layer.md`](governed-mcp-layer.md)**.

---

## Why isolate outputs under `runtime/artifacts/mcp-governance-demo/`

Scripts such as [`scripts/mcp_capability_audit.py`](../../scripts/mcp_capability_audit.py) default to workspace paths like **`runtime/artifacts/mcp-capability-report.md`**. For exploratory or CI demo runs, direct **`--output` / `--markdown` / `--json`** overrides avoid overwriting long-lived derived reports. The orchestrator **`run_mcp_governance_checks.py`** uses the demo prefix consistently.

---

## Recommended sequence (manual)

Use **`python3`** or **`python`** as appropriate on your OS. Commands assume repository root as current working directory.

### 1. Capability audit

```bash
python3 scripts/mcp_capability_audit.py \
  -o runtime/artifacts/mcp-governance-demo/capability-report.md
```

Optional **`--strict`** fails if heuristic danger flags fire after validation.

### 2. Authority binding check

```bash
python3 scripts/mcp_authority_check.py \
  -o runtime/artifacts/mcp-governance-demo/authority-report.md
```

Optional **`--strict`** treats warnings as failure (non-default).

### 3. Risk scan

```bash
python3 scripts/mcp_risk_scan.py \
  --markdown runtime/artifacts/mcp-governance-demo/risk-report.md \
  --json runtime/artifacts/mcp-governance-demo/risk-report.json
```

Exit code **`1`** when the scan reports **`pass=false`** â€” treat as failure for governance gates.

| Adapter / tool | Demo output path |
|----------------|------------------|
| Manifest admission | **`runtime/artifacts/mcp-admission/governance-demo-manifest.md`** |
| Mock harness | **`runtime/artifacts/mcp-mock-runs/governance-demo-mock.md`** |
| Local read | **`runtime/artifacts/mcp-local-read/governance-demo-read.md`** |
| Local index | **`runtime/artifacts/mcp-local-index/governance-demo-index.md`** |
| Research stub | **`runtime/artifacts/evidence-stubs/governance-demo-stub.md`** |
| Patch intake | **`runtime/artifacts/patch-intake/governance-demo-intake.md`** |

### 4. Manifest admission (example)

```bash
python3 scripts/mcp_manifest_admission.py \
  --input docs/mcp/fixtures/mcp-server-manifest.example.yaml \
  --output runtime/artifacts/mcp-admission/governance-demo-manifest.md
```

### 5. Mock execution harness (example)

Uses **shell-blocked** fixture (aligns with â€œno shell executionâ€ messaging):

```bash
python3 scripts/mcp_mock_harness.py \
  --input docs/mcp/fixtures/mcp-mock-run.shell-blocked.example.json \
  --output runtime/artifacts/mcp-mock-runs/governance-demo-mock.md
```

### 6. Local read-only adapter (example)

```bash
python3 scripts/mcp_local_readonly.py \
  --input docs/mcp/fixtures/mcp-local-read-request.example.json \
  --output runtime/artifacts/mcp-local-read/governance-demo-read.md
```

### 7. Local directory index adapter (example)

```bash
python3 scripts/mcp_local_index.py \
  --input docs/mcp/fixtures/mcp-local-index-request.example.json \
  --output runtime/artifacts/mcp-local-index/governance-demo-index.md
```

### 8. Optional â€” research â†’ evidence stub (example)

If [`docs/mcp/fixtures/research-evidence-input.example.json`](../../docs/mcp/fixtures/research-evidence-input.example.json) exists:

```bash
python3 scripts/research_to_evidence_stub.py \
  --input docs/mcp/fixtures/research-evidence-input.example.json \
  --output runtime/artifacts/evidence-stubs/governance-demo-stub.md
```

### 9. Optional â€” coding-agent patch intake (example)

If [`docs/mcp/fixtures/coding-agent-patch-intake.example.json`](../../docs/mcp/fixtures/coding-agent-patch-intake.example.json) exists:

```bash
python3 scripts/coding_agent_patch_intake.py \
  --input docs/mcp/fixtures/coding-agent-patch-intake.example.json \
  --output runtime/artifacts/patch-intake/governance-demo-intake.md
```

---

## Receipts

Adapters and harness steps emit JSON under **`runtime/artifacts/mcp-receipts/`**. The orchestrator aggregates paths into **`runtime/artifacts/mcp-governance-demo-report.md`**. Receipts **do not** approve Record merges or live MCP integration.

---

## Boundaries (all steps)

- **No live MCP server execution** â€” subprocesses invoke **Python scripts** only.
- **No credentials** and **no network** â€” tooling is local repo config + filesystem under policy.
- **No canonical Record mutation** â€” adapters do not merge gate candidates or edit **``** identity surfaces by design (see per-adapter docs).

Passing this runbook **does not** authorize arbitrary MCP integration; live MCP remains a **separate** operator decision.

