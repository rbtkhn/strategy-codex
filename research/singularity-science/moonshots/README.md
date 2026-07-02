# Moonshots — analysis

Analysis workspace for the **Moonshots** podcast stream — structured research, consequence-mapping, and synthesis notes built **on top of** episode captures.

**Seed:** [synthesis-research-frame.md](synthesis-research-frame.md)

## Intelligence pipeline

Compile archive transcripts → structured intelligence documents:

| Artifact | Path |
| --- | --- |
| Pipeline spec | [PIPELINE.md](PIPELINE.md) |
| Output template | [moonshots-intelligence-template.md](moonshots-intelligence-template.md) |
| Compiler CLI | `python3 scripts/compile_moonshots_intelligence.py` |

**Output naming:** `moonshots-ep-<N>-intelligence.{json,md}` when `episode_number` exists in archive frontmatter; else `moonshots-emerging-<slug>-intelligence.*`.

## Raw capture SSOT

Verbatim transcripts live under [`source-archive/singularity/moonshots/`](../../../source-archive/singularity/moonshots/). Do not mirror full transcript text here.

Intake protocol: [`source-archive/singularity/README.md`](../../../source-archive/singularity/README.md)

## Related surfaces

| Surface | Path |
| --- | --- |
| Parent shelf | [../README.md](../README.md) |
| Innermost Loop (helix pair) | [../innermost-loop/README.md](../innermost-loop/README.md) |
| Workshop sheets | [`singularity/workshop/sheets/`](../../../singularity/workshop/sheets/) |
| Keystone helix | [`singularity/workshop/keystone-helix.md`](../../../singularity/workshop/keystone-helix.md) |

## Classification

`research/singularity-science/moonshots/`
