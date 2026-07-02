---
name: moonshots-intelligence
description: Compile Moonshots archive transcripts into verbatim-grounded intelligence documents (dual-layer bullets, strict validator). Triggers moonshots intelligence, compile moonshots, epistemic compiler moonshots.
---

# Moonshots Intelligence

Compile verbatim Moonshots captures into audit-grade structured intelligence.

## When to use

- Operator lands a new capture under `source-archive/singularity/moonshots/`
- Workshop sheet needs evidence-grounded dual-layer bullets
- Replay or correct compile via `--bullets-json`

## Default execution order

1. Confirm archive path (`source-archive/singularity/moonshots/*.md`) has `## Verbatim Transcript`.
2. Run validator-first dry run:
   ```bash
   python3 scripts/compile_moonshots_intelligence.py --archive <path> --dry-run
   ```
3. Compile (fixture replay in CI; live LLM when `OPENAI_API_KEY` set):
   ```bash
   python3 scripts/compile_moonshots_intelligence.py --archive <path> --out research/singularity-science/moonshots/ --strict
   ```
4. Validate schema:
   ```bash
   python3 scripts/validate_all_schemas.py --scope singularity
   ```
5. Link output from workshop sheet if needed (`moonshots-ep-<N>-intelligence.json`).

## Output shape

SSOT: [research/singularity-science/moonshots/moonshots-intelligence-template.md](../../research/singularity-science/moonshots/moonshots-intelligence-template.md)

## Do not

- Rewrite or summarize archive verbatim body
- Skip validator on promoted claims
- Duplicate full transcript in research output beyond evidence spans

## Related

- [PIPELINE.md](../../research/singularity-science/moonshots/PIPELINE.md)
- [synthesis-research-frame.md](../../research/singularity-science/moonshots/synthesis-research-frame.md)
