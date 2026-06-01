**strategy-codex instance notes**

- Canonical synthesis shelf: [singularity/synthesis](/C:/dev/strategy-codex/singularity/synthesis)
- Canonical support-note shelf: [singularity/synthesis/support](/C:/dev/strategy-codex/singularity/synthesis/support)
- Canonical month example: [2026-05.md](/C:/dev/strategy-codex/singularity/synthesis/2026-05.md)
- Deterministic spine: [singularity/workshop/longitudinal/innermost-loop.md](/C:/dev/strategy-codex/singularity/workshop/longitudinal/innermost-loop.md)
- Structured spine index: [innermost-loop-signals.json](/C:/dev/strategy-codex/singularity/workshop/longitudinal/innermost-loop-signals.json)
- Source-sheet anchors: [singularity/workshop/sheets](/C:/dev/strategy-codex/singularity/workshop/sheets)
- Raw archive: [source-archive/singularity/innermost-loop](/C:/dev/strategy-codex/source-archive/singularity/innermost-loop)
- Generator: [scripts/build_innermost_loop_synthesis.py](/C:/dev/strategy-codex/scripts/build_innermost_loop_synthesis.py)

**Repo notes**

- In this repo, Innermost Loop monthly work is explicitly **synthesis-first**, not commentary-first.
- The month memo is the primary object; support notes should stay scarce and typed.
- The current support-note rule for this shelf is intentionally narrow: first-front anchors, chronology anomalies, or source-sheet-backed action wedges.
- Promotion targets live at [singularity/notes](/C:/dev/strategy-codex/singularity/notes) and [singularity/essays](/C:/dev/strategy-codex/singularity/essays).

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill singularity-monthly-synthesis
python scripts/sync_portable_skills.py --verify --skill singularity-monthly-synthesis
python scripts/validate_skills.py
python scripts/build_innermost_loop_synthesis.py
```

