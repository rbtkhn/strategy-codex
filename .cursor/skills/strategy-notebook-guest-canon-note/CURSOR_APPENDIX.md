Grace-mar paths and commands for this repository (from `.cursor/skills/strategy-notebook-guest-canon-note/`).

| Topic | Path |
|--------|------|
| Existing stream-local speaker arcs | [statecraft/voices/diesen/](../../../statecraft/voices/diesen) |
| Lattice speakers roster | [continuity/speaker-lattice.md](../../../continuity/speaker-lattice.md) |
| Thread handle roster | [continuity/strategy-commentator-threads.md](../../../continuity/strategy-commentator-threads.md) |
| Portable skill manifest | [skills/manifest.yaml](../../../skills/manifest.yaml) |
| Sync script | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |
| Skill validator | [scripts/validate_skills.py](../../../scripts/validate_skills.py) |

**Repo notes**

- In this repo, guest speaker arcs belong to the **host stream** unless an existing taxonomy explicitly says otherwise.
- Current reference pattern:
  - [arc-matlock-diesen-host.md](../../../statecraft/notes/arc-matlock-diesen-host.md)
  - [arc-jiang-diesen-host.md](../../../statecraft/notes/arc-jiang-diesen-host.md)
- The lattice and `thread:` roster may cite the speaker arc, but the note itself should not invent a new shelf or corpus boundary.

**Common local command pattern**

```powershell
python scripts/sync_portable_skills.py --skill strategy-notebook-guest-canon-note
python scripts/sync_portable_skills.py --verify
python scripts/validate_skills.py
```
