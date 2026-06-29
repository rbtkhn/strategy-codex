# Research-to-evidence stubs (adapter)

**Status:** WORK/runtime tooling only. This path does **not** browse the web, run MCP servers, or merge canonical Record content.

---

## Why this adapter exists

Structured research (claims, sources, confidence, routing hints) should land as **inspectable WORK artifacts** before any gate staging. **Capability is not authority**; neither research JSON nor generated stubs are canonical evidence until reviewed and promoted per [`AGENTS.md`](../../AGENTS.md).

---

## Input format

- **JSON Schema:** [`schemas/research-evidence-input.v1.json`](../../schemas/research-evidence-input.v1.json)
- **Example:** [`docs/mcp/fixtures/research-evidence-input.example.json`](../../docs/mcp/fixtures/research-evidence-input.example.json)

Each source needs a stable **`source_id`**, **`title`**, and **either `url` or `local_path`**. **`short_excerpts`** are capped at **300 characters** each. **`candidate_claims.supporting_sources`** must reference declared **`source_id`** values.

---

## Output format

- **Markdown stub** under [`runtime/artifacts/evidence-stubs/`](../../runtime/artifacts/evidence-stubs/) with YAML front matter and prominent lines: **PRE-CANONICAL Â· WORK ARTIFACT Â· NOT APPROVED RECORD**.
- **MCP execution receipt** under [`runtime/artifacts/mcp-receipts/`](../../runtime/artifacts/mcp-receipts/) using capability **`evidence_stub_operator_template`** by default â€” see [`docs/mcp/mcp-execution-receipts.md`](mcp-execution-receipts.md).

---

## Receipt behavior

Every run emits a **validated** receipt (`schema_version` 1) tying **`resources_read`** to the input JSON and **`resources_written`** to the generated stub. **Receipts are audit metadata, not approval.**

---

## Promotion boundary

| Stage | Role |
|-------|------|
| Research JSON | Operator-structured capture; no Record truth. |
| Evidence stub (this adapter) | Pre-canonical markdown under `runtime/artifacts/`; labeled non-canonical. |
| Candidate proposal | Structured YAML/text for [`recursion-gate.md`](../../archive/grace-mar-instance/recursion-gate.md) â€” separate step. |
| Approved Record evidence | After companion approval / merge scripts â€” **not** automatic from this tool. |

`record_action` and `suggested_gate_action` values are **routing hints** only (`create_candidate_only`, `stage_for_review`, etc.); they **do not** append to EVIDENCE or `self.md`.

---

## Strategy-notebook / history-notebook

This adapter **does not** edit [`strategy-notebook/`](../skill-work/work-strategy/strategy-notebook/) or â€œhistory notebookâ€ spine files. Findings may be **pasted or promoted manually** into lane notebooks after operator reviewâ€”same membrane as other WORKâ†’Record flows.

---

## Command

```bash
python3 scripts/research_to_evidence_stub.py \
  --input docs/mcp/fixtures/research-evidence-input.example.json \
  --output runtime/artifacts/evidence-stubs/my-topic.md
```

