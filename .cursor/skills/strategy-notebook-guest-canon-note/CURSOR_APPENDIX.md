Grace-mar paths and commands for this repository (from `.cursor/skills/strategy-notebook-guest-canon-note/`).

| Topic | Path |
|--------|------|
| Existing stream-local canon notes | [codex/2026/diesen/](../../codex/2026/diesen/) |
| Lattice speakers roster | [codex/COGNITION-LATTICE-SPEAKERS.md](../../codex/COGNITION-LATTICE-SPEAKERS.md) |
| Thread handle roster | [codex/strategy-commentator-threads.md](../../codex/strategy-commentator-threads.md) |
| Portable skill manifest | [skills-portable/manifest.yaml](../../../skills-portable/manifest.yaml) |
| Sync script | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |
| Skill validator | [scripts/validate_skills.py](../../../scripts/validate_skills.py) |

**Repo notes**

- In this repo, guest canon notes belong to the **host stream** unless an existing taxonomy explicitly says otherwise.
- Current reference pattern:
  - [diesen-matlock-canon-note.md](../../codex/2026/diesen/diesen-matlock-canon-note.md)
  - [diesen-jiang-canon-note.md](../../codex/2026/diesen/diesen-jiang-canon-note.md)
- The lattice and `thread:` roster may cite the canon note, but the note itself should not invent a new shelf or corpus boundary.

**Common local command pattern**

```powershell
python scripts/sync_portable_skills.py --skill strategy-notebook-guest-canon-note
python scripts/sync_portable_skills.py --verify
python scripts/validate_skills.py
```
