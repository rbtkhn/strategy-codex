Grace-mar paths and commands for this repository (from `.cursor/skills/strategy-notebook-guest-canon-note/`).

| Topic | Path |
|--------|------|
| Existing stream-local speaker arcs | [codex/years/2026/diesen/](../../codex/years/2026/diesen/) |
| Lattice speakers roster | [codex/COGNITION-LATTICE-SPEAKERS.md](../../codex/COGNITION-LATTICE-SPEAKERS.md) |
| Thread handle roster | [codex/strategy-commentator-threads.md](../../codex/strategy-commentator-threads.md) |
| Portable skill manifest | [skills-portable/manifest.yaml](../../../skills-portable/manifest.yaml) |
| Sync script | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |
| Skill validator | [scripts/validate_skills.py](../../../scripts/validate_skills.py) |

**Repo notes**

- In this repo, guest speaker arcs belong to the **host stream** unless an existing taxonomy explicitly says otherwise.
- Current reference pattern:
  - [diesen-matlock-speaker-arc.md](../../codex/years/2026/diesen/diesen-matlock-speaker-arc.md)
  - [diesen-jiang-speaker-arc.md](../../codex/years/2026/diesen/diesen-jiang-speaker-arc.md)
- The lattice and `thread:` roster may cite the speaker arc, but the note itself should not invent a new shelf or corpus boundary.

**Common local command pattern**

```powershell
python scripts/sync_portable_skills.py --skill strategy-notebook-guest-canon-note
python scripts/sync_portable_skills.py --verify
python scripts/validate_skills.py
```
