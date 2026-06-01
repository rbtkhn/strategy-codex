**strategy-codex instance notes**

- Parent synthesis shelf: [singularity/synthesis](/C:/dev/strategy-codex/singularity/synthesis)
- Notes shelf: [singularity/notes](/C:/dev/strategy-codex/singularity/notes/README.md)
- Current promoted example: [compute-political-currency-control-plane-substrate.md](/C:/dev/strategy-codex/singularity/notes/compute-political-currency-control-plane-substrate.md)
- Parent month example: [2026-05.md](/C:/dev/strategy-codex/singularity/synthesis/2026-05.md)
- Notes index: [singularity/notes/README.md](/C:/dev/strategy-codex/singularity/notes/README.md)

**Repo notes**

- Promotion in this repo should be bidirectional: the new note links back to the month, and the month records the completed `promote_to_note` route.
- Use source sheets and a few raw checkpoints as anchors; do not restate the entire month.
- If the argument starts absorbing too many fronts at once, stop and keep it in synthesis.

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill singularity-note-promotion
python scripts/sync_portable_skills.py --verify --skill singularity-note-promotion
python scripts/validate_skills.py
```

