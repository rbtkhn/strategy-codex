**strategy-codex instance notes**

- Canonical front-door doctrine surface: [statecraft/civ-state/README.md](/C:/dev/strategy-codex/statecraft/civ-state/README.md)
- Canonical volume map: [statecraft/civ-state/volumes/README.md](/C:/dev/strategy-codex/statecraft/civ-state/volumes/README.md)
- Volume surfaces to harden:
  - [Vol I - China](/C:/dev/strategy-codex/statecraft/civ-state/volumes/vol-i-china/README.md)
  - [Vol II - Persia](/C:/dev/strategy-codex/statecraft/civ-state/volumes/vol-ii-persia/README.md)
  - [Vol III - Rome](/C:/dev/strategy-codex/statecraft/civ-state/volumes/vol-iii-rome/README.md)
  - [Vol IV - Russia](/C:/dev/strategy-codex/statecraft/civ-state/volumes/vol-iv-russia/README.md)
  - [Vol V - America](/C:/dev/strategy-codex/statecraft/civ-state/volumes/vol-v-america/README.md)
- Use `civilization_memory` only as evidence for this skill; CIV-STATE surfaces remain the operator-facing layer.
- Keep volume passes bounded to CIV-STATE architecture surfaces unless the operator explicitly widens scope into lane, transaction, or source-memory files.

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill civ-state-volume-harden
python scripts/sync_portable_skills.py --verify --skill civ-state-volume-harden
python scripts/validate_skills.py
```
