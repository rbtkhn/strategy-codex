Cursor-only paths for [ph-interview-transcript-curation/SKILL.md](../../../skills/ph-interview-transcript-curation/SKILL.md).

## Repo layout

| Surface | Path |
|---------|------|
| Canonical PH repo (edit here) | `C:\dev\predictive-history` or operator clone of `rbtkhn/predictive-history` |
| Inbound mirror (do not hand-edit) | `public/predictive-history/` in strategy-codex |
| Frozen workshop (do not edit unless revived) | `codex/predictive-history/` |

## Known interview packets

Catalog: `predictive-history/docs/predictive-history-index.md` · **Provenance** section.

Exemplar pass-2: `interviews/interview-2026-03-20-tucker-carlson/` (vi-11, `d475974`).

Pending curation candidate: `interviews/interview-2026-05-07-diary-of-a-ceo/` (ext-doac-01, promoted `d49d9e9` — raw ASR-style opening).

## Commands (PH repo root)

```bash
PYTHONPATH=src python -m civ_ph.cli validate
python -m pytest -q
git -c user.name="Robert Kuhne" -c user.email="rbtkhn@users.noreply.github.com" commit -m "PH-TRANSCRIPT-EDIT: …"
git push origin main
```

## Mirror (strategy-codex)

```bash
python scripts/sync_predictive_history_mirror.py
# commit message must include [predictive-history-sync]
```

## External intake sibling

Promote **new** external interviews (not pass-2) via PH `scripts/intake_interview_external.py` — separate commit slice from this skill. Exclude sidecar `_land_*` folders from commits.

## Portable plumbing

| Topic | Path |
|-------|------|
| Manifest | [skills/manifest.yaml](../../../skills/manifest.yaml) |
| Backlog | [skills/skill-candidates.md](../../../skills/skill-candidates.md) |
| Sync | `python3 scripts/sync_portable_skills.py --skill ph-interview-transcript-curation --verify` |
| Validate | `python3 scripts/validate_skills.py` |
