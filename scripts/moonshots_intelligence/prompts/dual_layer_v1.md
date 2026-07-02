# Dual-layer bullet generation (v1)

You compile Moonshots podcast transcript evidence into structured intelligence.

## Rules

- Each bullet MUST reference exactly one `evidence_ref` (E1, E2, …) from the provided evidence list.
- The `evidence` field in each bullet MUST be copied **verbatim** from the matching evidence block — no paraphrase, no edit, no stitch.
- `mechanism` must explain **causal structure** (because / therefore / drives / when / if …).
- `claim` is interpretation; `implication` is system-level consequence.
- Output **only** valid JSON matching the schema below.

## Output JSON schema

```json
{
  "core_thesis": "string — system-level episode abstraction",
  "bullets": [
    {
      "claim": "string",
      "mechanism": "string — causal explanation",
      "implication": "string",
      "evidence_ref": "E1",
      "evidence": "verbatim text from evidence block E1"
    }
  ],
  "concept_primitives": ["reusable abstraction", "..."],
  "feedback_loops": {
    "reinforcing": ["..."],
    "balancing": ["..."]
  },
  "meta_insight": "string — cross-system structural interpretation"
}
```

Produce at least {{min_bullets}} bullets when enough evidence blocks exist.

## Evidence blocks

{{evidence_json}}
