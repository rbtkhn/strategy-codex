---
name: monthly-deepening
description: Deprecated legacy judgment-review skill. Use the periodic-statecraft-review runbook for new work.
preferred_activation: monthly deepening
activation: monthly deepening
portable: true
version: 0.2.0
category: legacy-redirect
status: deprecated
replacement: periodic-statecraft-review
scope_class: repo-governed
review_date: 2026-12-31
tags:
- operator
- deprecated
- statecraft
portable_source: skills/monthly-deepening/SKILL.md
synced_by: sync_portable_skills.py
---
# Deprecated — monthly-deepening

**Status:** Deprecated. Do not use this skill for new work.

**Use instead:** [`skills/runbooks/periodic-statecraft-review.runbook.md`](../../../skills/runbooks/periodic-statecraft-review.runbook.md).

This file remains only for legacy trigger compatibility.

## Legacy activation

When the operator says `monthly deepening`, route to the `periodic-statecraft-review` runbook if a time-window review is still intended.

## No independent methodology

This file must not contain independent judgment-review doctrine. Put workflow composition in the runbook and current methodology in active skills.


## Cursor / strategy-codex instance

Grace-mar paths and commands for this repository (from `.cursor/skills/monthly-deepening/`).

| Topic | Path |
|--------|------|
| Canonical archive root | [source-archive/statecraft/](../../../source-archive/statecraft/) |
| Local observability receipts | [runtime/artifacts/cognition-streams/](../../../runtime/artifacts/cognition-streams/) |
| Deprecated raw-input (archaeology) | [RAW-INPUT-DEPRECATED.md](../../../docs/skill-work/work-strategy/RAW-INPUT-DEPRECATED.md) · [codex/raw-input/README.md](../../../codex/raw-input/README.md) |
| Mercouris local index cache | [\.codex-tmp/youtube-alex-mercouris-index/](../../../.codex-tmp/youtube-alex-mercouris-index/) |
| Day README generator | [scripts/build_statecraft_day_indices.py](../../../scripts/build_statecraft_day_indices.py) |
| Day dashboard generator | [scripts/build_statecraft_day_dashboard.py](../../../scripts/build_statecraft_day_dashboard.py) |
| Speaker dashboard generator | [scripts/build_statecraft_speaker_dashboard.py](../../../scripts/build_statecraft_speaker_dashboard.py) |
| Portable skill manifest | [skills/manifest.yaml](../../../skills/manifest.yaml) |
| Sync script | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |
| Skill validator | [scripts/validate_skills.py](../../../scripts/validate_skills.py) |

**Repo notes**

- In this repo, monthly deepening often sits on top of statecraft archive recovery work, not just reporting.
- The operator transcript convention is load-bearing here: full transcript pastes should be materialized by default unless the operator explicitly limits the turn to reporting-only.
- `speaker-only`, `speaker-adjacent`, and `mixed` are not interchangeable categories. Keep the split explicit in Mercouris and related monthly passes.
- The Mercouris month index commonly depends on:
  - canonical `source-archive/statecraft/YYYY-MM-DD/` files
  - local channel index caches in `.codex-tmp/`
  - repair receipts in `runtime/artifacts/cognition-streams/`
- Materialization is archive work, not shelf-building. Do not wait for an extra `please materialize` step after the operator has already pasted the transcript.

**Common local command pattern**

```powershell
python scripts/sync_portable_skills.py --skill monthly-deepening
python scripts/sync_portable_skills.py --verify --skill monthly-deepening
python scripts/validate_skills.py
python scripts/build_statecraft_day_indices.py --day YYYY-MM-DD
python scripts/build_statecraft_day_dashboard.py --thread mercouris --slug mercouris-thread
```


## Cursor / strategy-codex instance

Grace-mar paths and commands for this repository (from `.cursor/skills/monthly-deepening/`).

| Topic | Path |
|--------|------|
| Canonical archive root | [source-archive/statecraft/](../../../source-archive/statecraft/) |
| Local observability receipts | [runtime/artifacts/cognition-streams/](../../../runtime/artifacts/cognition-streams/) |
| Legacy raw-input fallback | [codex/years/2026/raw-input/](../../../codex/years/2026/raw-input/) |
| Mercouris local index cache | [\.codex-tmp/youtube-alex-mercouris-index/](../../../.codex-tmp/youtube-alex-mercouris-index/) |
| Day README generator | [scripts/build_statecraft_day_indices.py](../../../scripts/build_statecraft_day_indices.py) |
| Day dashboard generator | [scripts/build_statecraft_day_dashboard.py](../../../scripts/build_statecraft_day_dashboard.py) |
| Speaker dashboard generator | [scripts/build_statecraft_speaker_dashboard.py](../../../scripts/build_statecraft_speaker_dashboard.py) |
| Portable skill manifest | [skills/manifest.yaml](../../../skills/manifest.yaml) |
| Sync script | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |
| Skill validator | [scripts/validate_skills.py](../../../scripts/validate_skills.py) |

**Repo notes**

- In this repo, monthly deepening often sits on top of statecraft archive recovery work, not just reporting.
- The operator transcript convention is load-bearing here: full transcript pastes should be materialized by default unless the operator explicitly limits the turn to reporting-only.
- `speaker-only`, `speaker-adjacent`, and `mixed` are not interchangeable categories. Keep the split explicit in Mercouris and related monthly passes.
- The Mercouris month index commonly depends on:
  - canonical `source-archive/statecraft/YYYY-MM-DD/` files
  - local channel index caches in `.codex-tmp/`
  - repair receipts in `runtime/artifacts/cognition-streams/`
- Materialization is archive work, not shelf-building. Do not wait for an extra `please materialize` step after the operator has already pasted the transcript.

**Common local command pattern**

```powershell
python scripts/sync_portable_skills.py --skill monthly-deepening
python scripts/sync_portable_skills.py --verify --skill monthly-deepening
python scripts/validate_skills.py
python scripts/build_statecraft_day_indices.py --day YYYY-MM-DD
python scripts/build_statecraft_day_dashboard.py --thread mercouris --slug mercouris-thread
```
