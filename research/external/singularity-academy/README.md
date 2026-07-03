# Singularity Academy - external research

Upstream WORK research for `singularity-academy`. These artifacts are not workshop truth, not Record truth, and not automatic gate inputs.

## Purpose

Use this surface for bounded external research captures that may later support:

- singularity workshop interpretation
- source-bound academy briefs
- work-business offer memos
- explicit, rare self-proposal drafts when a durable Record-adjacent claim truly exists

Normal flow:

`external research capture -> research/external/singularity-academy/queries -> optional brief or memo -> explicit curation elsewhere`

## Layout

| Path | Role |
|------|------|
| `queries/` | Validated lane-scoped research artifacts, usually from paste ingest. |
| `briefs/` | Source-bound academy briefs derived from query artifacts. These are still upstream WORK notes, not workshop sheets. |

## Typical workflow

1. Paste a Sci-Bot answer into a local text file.
2. Ingest it into a validated singularity-academy artifact under `queries/`.
   The script enforces validation locally and uses `jsonschema` when available.
3. Optionally emit:
   - an academy brief under `briefs/`
   - an offer memo under `docs/archive/skill-work-legacy/work-business/singularity-academy-research-memos/`
   - a derived self-proposal draft only when a durable self-facing claim truly exists
4. Curate any durable workshop or work-business reuse explicitly elsewhere.

Example:

```powershell
Get-Content .\sample-scibot.txt | .\.venv\Scripts\python.exe scripts\ingest_external_research.py `
  --lane singularity-academy `
  --topic "AI workflow authority" `
  --query "How should review-gated AI workflow research be applied to singularity academy?" `
  --input - `
  --emit-workshop-brief `
  --emit-offer-memo `
  --academy-surface workshop
```

Expected outputs:

- `research/external/singularity-academy/queries/<date>-<topic>.json`
- `research/external/singularity-academy/briefs/<date>-<topic>-academy-brief.md`
- optionally a work-business memo and derived self-proposal draft when requested

Stable examples for this workflow live under `research/external/singularity-academy/fixtures/external-research/`.

## Boundaries

- Do not treat these files as workshop sheet replacements.
- Do not write directly into `singularity/workshop/sheets/` from raw ingest.
- Do not send these artifacts into `recursion-gate.md` by default.
- If a self-facing claim matters, export a derived draft deliberately and route it through the existing `research/auto-research/self-proposals` review flow.
