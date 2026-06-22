# Prose Forge

WORK only; not Record.

**Surface type** — workflow / helper  
**Primary purpose** — Improve draft prose so it becomes specific, repo-native, and reviewable — not “humanizer” evasion.  
**When to use** — Promoting model output or draft essays/notes toward durable prose surfaces; before shipping new `essays/` files.  
**Inputs** — Markdown path(s), optional `--diff base...head`, optional `--mode essay|skill-write|note`.  
**Outputs** — lint findings (`prose-forge.report.json`), staged `candidate.md`, `review-note.md`, diff via `compare`.  
**Mutation scope** — runtime-only; may stage under `runtime/artifacts/prose-forge/`; **never** silent canonical edits.  
**Canonical Record access** — none.  
**Typical next step** — operator review, manual merge.  
**Do not use for** — source archives, review-queue Record paths, detector evasion, laundering unsupported claims.

## Voice SSOT (do not duplicate here)

| Prose class | Voice / lint SSOT |
|-------------|-------------------|
| `essays/` | [essay-voice.md](essay-voice.md) |
| Public copy | [skill-write/write-operator-preferences.md](skill-write/write-operator-preferences.md) |
| Placement | [prose-index.md](prose-index.md) |

## Commands

```bash
# Phase 0 — template slop (stdlib; always available)
python3 scripts/prose_slop_lint.py essays/draft.md
python3 scripts/prose_slop_lint.py --diff origin/main...HEAD essays/

# Phase 1+ — wrapper (slop + optional Vale)
python3 scripts/prose_forge.py lint essays/draft.md
python3 scripts/prose_forge.py lint --diff origin/main...HEAD essays/
python3 scripts/prose_forge.py lint --strict essays/leo-barnes-jiang-on-ai.md

# Phase 3 — stage candidate (no LLM call in-repo)
python3 scripts/prose_forge.py rewrite essays/draft.md --mode essay
python3 scripts/prose_forge.py compare essays/draft.md runtime/artifacts/prose-forge/draft/candidate.md
python3 scripts/prose_forge.py gate runtime/artifacts/prose-forge/draft/candidate.md
```

## Class router

| Path prefix | Class | Slop rules | Vale packs |
|-------------|-------|------------|------------|
| `essays/` | essay | SLOP-01..08 | EssaySlop, AITexture |
| `docs/skill-write/` | skill-write | extended optional | SkillWriteResidue, AITexture |
| `*/notes/` | note | minimal | AITexture |
| `docs/` | doctrine | lint only | AITexture |
| `source-archive/`, `archive/queues/review-queue/`, `statecraft/synthesis/day/` | **denied** | — | — |

## Legacy shelf

The script **`LEGACY_ALLOWLIST`** is empty — all repo-root essays are linted in default full scan. Retrofitted exemplar: [`essays/leo-barnes-jiang-on-ai.md`](../essays/leo-barnes-jiang-on-ai.md) (Band A lede + voice sections; passes `--strict --full`).

New essays may set frontmatter `voice_profile: tri-blend-band-a` (future strict gate).

## Optional Vale

Install [Vale](https://vale.sh/) locally for generic AI-texture checks. CI and scripts skip Vale gracefully if not installed.

Config: [`.vale.ini`](../.vale.ini), [`templates/styles/StrategyCodex/`](../templates/styles/StrategyCodex/).

## Staging layout

```
runtime/artifacts/prose-forge/<slug>/
  candidate.md
  prose-forge.report.json
  review-note.md
```

Not `archive/queues/review-queue/` — that path is Grace-Mar material change-review.

## Related

- [claude-surface-contract.md](claude-surface-contract.md)
- [essay-voice.md](essay-voice.md) — SLOP-01..08 SSOT
