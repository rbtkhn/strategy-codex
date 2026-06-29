WORK only; not Record.

# Jiang Routing

Use this file to decide which Jiang layer to open first.

## Open the Jiang shelf first when

- the task is about Jiang as a speaker object
- the task is asking for total Predictive History counts or corpus scope
- the task is about local statecraft routing, mirror placement, or shelf law
- the task mixes Predictive History with other statecraft speaker or lane work
- the task needs a local path to the official mirror

## Open the embedded mirror first when

- the task is directly about the public Predictive History repo structure
- the task needs `ph-civ`, `ph-apo`, or `ph-mus` chapter paths
- the task is checking source-video indexes, museum manifests, or public repo docs
- the task is about mirror sync, remote identity, or public-repo parity
- the task is about Jiang's lecture pedagogy, rhetoric, spread, or cross-volume analysis notes
- the task is about Volume I **Part** navigation (`civ-01`–`civ-60` doorways), part-boundary tour, or interwoven-spine Part seams

## Open the raw archive first when

- the task is about operator-pasted captures outside the public mirror
- the task is about recent Jiang / PH source residue not yet surfaced publicly
- the task is checking raw local transcript or Substack preservation

## First-open paths

- External interviews: [jiang-index.md](jiang-index.md)
- Count and scope: [jiang-predictive-history-master-index.md](jiang-predictive-history-master-index.md)
- Public mirror: [../../../public/predictive-history/README.md](../../../README.md)
- Volume I interwoven spine: [public/predictive-history/book/volume-i-civilization/interwoven-reader/README.md](../../../singularity/work-cici/README.md)
- Volume I Parts shelf: [public/predictive-history/book/volume-i-civilization/parts/README.md](../../../singularity/work-cici/README.md)
- Jiang analysis notes: [../../../public/predictive-history/docs/jiang-analysis-index.md](../../../public/predictive-history/docs/jiang-analysis-index.md)
- Raw archive bench: [source-archive/statecraft/jiang-predictive-history-index.md](../../../source-archive/statecraft/jiang-predictive-history-index.md)

## Volume I Parts (reading navigation)

Ten **Part doorways** overlay the interwoven civilization spine — navigation only; spine order stays authoritative.

| Surface | Path |
|---------|------|
| Parts index | [public/predictive-history/book/volume-i-civilization/parts/README.md](../../../singularity/work-cici/README.md) |
| Registry (SSOT) | [../../../public/predictive-history/data/parts/volume-i-parts.json](../../../public/predictive-history/data/parts/volume-i-parts.json) |
| Part boundary tour | [../../../public/predictive-history/data/routes/part-boundary-tour.json](../../../public/predictive-history/data/routes/part-boundary-tour.json) |
| LLM `part_tour` mode | [../../../public/predictive-history/data/llm-experience.json](../../../public/predictive-history/data/llm-experience.json) |

**Reading law:** open the [interwoven spine](../../../README.md) for canonical order; use Part doorways for law-discovery questions, companion weave, and corridor links. **Part** here ≠ lecture transcript "Part I / Part II" ≠ CIV-STATE Part 1/2/3.

**Split seams:** VI/VII at `civ-34`/`civ-35` (Dante bookend — opens in VI, returns in VII); IX/X at `civ-53`/`civ-54`.

**Validate (from `ph-civ` root):** `python scripts/validate_volume_i_parts.py` · wired into `ph-civ validate` · tests: `tests/test_volume_i_parts.py`

## Transcript floor (verbatim SSOT)

In the embedded `ph-civ` mirror, **lecture transcript bodies are not commentary**:

- **Frozen by default:** `**/*-transcript.md` under `../../../public/predictive-history/` — no typo fixes, ASR cleanup, or synthesis merges during lattice walks, Layer 3 updates, or corridor work.
- **Edit surfaces:** `*-commentary.md`, cards, corridors, orientation YAML; cite transcript line refs instead of rewriting source text.
- **Legitimate transcript changes** require an explicit operator lane (re-materialize, rights-reviewed re-import from `rbtkhn/predictive-history`, or named cleanup skill) in **`PREDICTIVE_HISTORY_ROOT`**.
- **Check before commit:** `python scripts/validate_ph_civ_transcript_boundary.py --staged` from strategy-codex root (optional pre-commit hook).
- **ASR pilot guard (civ-01–12):** `python scripts/validate_transcript_proper_nouns.py` — blocklist at `../../../public/predictive-history/data/asr-blocklist/volume-ii-pilot.json`; regenerate via `python scripts/generate_ph_civ_asr_blocklist.py` after pilot script edits.

Cursor agents: `.cursor/rules/ph-civ-transcript-immutability.mdc` when paths touch the mirror.

## Routing rule

The Jiang shelf is the canonical statecraft-side front door. Use the shelf for speaker law, count disambiguation, and layer choice; use the mirror for public corpus files; use the raw archive bench for source residue outside the mirror.
