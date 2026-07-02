# Moonshots Intelligence Pipeline

work only; not Record.

Deterministic **epistemic compiler** for Moonshots archive transcripts → structured intelligence documents with verbatim-grounded evidence and strict validation.

## Layer boundaries

| Layer | Path |
| --- | --- |
| Raw capture (read-only) | [`source-archive/singularity/moonshots/`](../../../source-archive/singularity/moonshots/) |
| Intelligence output | `moonshots-ep-<N>-intelligence.{json,md}` (this folder) |
| Output template | [moonshots-intelligence-template.md](moonshots-intelligence-template.md) |
| Workshop sheets | [`singularity/workshop/sheets/`](../../../singularity/workshop/sheets/) |

## Pipeline stages

1. **Ingest** — read archive; extract `## Verbatim Transcript` only; no rewrite
2. **Segment** — lossless sentence units with line/char offsets
3. **Evidence extract** — accept spans ≥30 words verbatim; assign `E1…En`
4. **Generate** — LLM dual-layer bullets (`claim`, `mechanism`, `implication`) or `--bullets-json` replay
5. **Validate** — fail closed on paraphrase, stitch, missing mechanism, bad `evidence_ref`
6. **Assemble** — schema-checked JSON + markdown render
7. **NST map** (optional `--nst`) — Object/Morphism/Functor projection

## CLI

```bash
python3 scripts/compile_moonshots_intelligence.py \
  --archive source-archive/singularity/moonshots/moonshots-265-spacex-ipo-anthropic-export-control-2026-06-19.md \
  --out research/singularity-science/moonshots/ \
  [--strict] [--nst] [--dry-run] [--bullets-json path]
```

## Output naming

| Archive | Output basename |
| --- | --- |
| `episode_number: 265` | `moonshots-ep-265-intelligence` |
| Unscheduled / no ep # | `moonshots-emerging-<slug>-intelligence` |

## Guarantees (v1)

- Evidence ≥30 words and verbatim in archive body
- No stitched `|||` evidence spans
- Mechanism layer required with causal structure
- CI uses `--bullets-json` fixtures (no live LLM required)
- LLM runs log `prompt_hash` + `model` in provenance

## Related

- Skill: [`.cursor/skills/moonshots-intelligence/SKILL.md`](../../../.cursor/skills/moonshots-intelligence/SKILL.md)
- Loop: [`moonshots-intelligence-compile`](../../../singularity/loops/research/moonshots-intelligence-compile.yaml)
- Schema: [`schemas/singularity/moonshots-intelligence.schema.json`](../../../schemas/singularity/moonshots-intelligence.schema.json)
