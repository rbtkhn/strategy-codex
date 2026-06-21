---
name: transcript-proper-noun-normalization
preferred_activation: proper noun normalization
description: DEPRECATED 2026-06-21. Redirect to source-clean for statecraft archive captures. Legacy alias for post-land ASR/proper-noun normalization.
portable: true
version: 0.2.0
deprecated: 2026-06-21
see: skills/source-clean/SKILL.md
tags:
- transcript
- raw-input
- quality
- cleanup
- deprecated
portable_source: skills/transcript-proper-noun-normalization/SKILL.md
synced_by: sync_portable_skills.py
---
# DEPRECATED — Transcript proper-noun normalization

**Status:** Deprecated **2026-06-21**. For landed **`source-archive/statecraft/**/source-*.md`** captures, use **[`source-clean`](../source-clean/SKILL.md)** instead.

## Use instead

| Task | Skill / CLI |
|------|-------------|
| Post-land ASR + proper-noun cleanup on archive captures | **`source-clean`** → `python scripts/source_clean_statecraft.py --path <capture>` |
| ASR-only (no scaffold) | `python scripts/normalize_statecraft_source_asr.py <path> --write` |
| First-pass land | **`source-intake`** ([`statecraft-source-intake`](../statecraft-source-intake/SKILL.md)) |

## Legacy activation

When the operator says **`proper noun normalization`** on a **statecraft archive** file, say you are following **`source-clean`** and execute [source-clean/SKILL.md](../source-clean/SKILL.md).

For **raw-input** files under `strategy-notebook/raw-input/` only (not yet archived), apply the same **conservative proper-noun** contract manually or land via intake first, then **`source-clean`**.


## Cursor / strategy-codex instance

Grace-mar paths and commands for this repository.

| Topic | Path |
|--------|------|
| Canonical raw-input tree | [codex/](../../codex/) |
| Host quality reports | [runtime/artifacts/host-shelf-quality/](../../../runtime/artifacts/host-shelf-quality/) |
| Materializer / validator | [scripts/materialize_youtube_raw_input.py](../../../scripts/materialize_youtube_raw_input.py) |
| Quality reporter | [scripts/host_shelf_quality.py](../../../scripts/host_shelf_quality.py) |
| Portable skill manifest | [skills/manifest.yaml](../../../skills/manifest.yaml) |
| Sync script | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |

**Local validation pattern**

```powershell
python scripts/materialize_youtube_raw_input.py --raw-input "<raw-input-path>" --notebook-root "codex/<year>" --apply --with-appearances --purpose one-off --run-id "<label>"
```

For check-streams or densification follow-up, preserve the existing `--purpose` and `--tranche-label` from the capture pass.
