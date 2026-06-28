**strategy-codex instance notes**

- Canonical front-door doctrine surface: [statecraft/states/README.md](../../../statecraft/states/README.md)
- Canonical volume map: [statecraft/states/volumes/README.md](../../../statecraft/states/volumes/README.md)
- Volume surfaces to harden:
  - [Vol I - China](../../../README.md)
  - [Vol II - Persia](../../../README.md)
  - [Vol III - Rome](../../../README.md)
  - [Vol IV - Russia](../../../README.md)
  - [Vol V - America](../../../README.md)
- Use `civilization_memory` only as evidence for this skill; CIV-STATE surfaces remain the operator-facing layer.
- Keep volume passes bounded to CIV-STATE architecture surfaces unless the operator explicitly widens scope into lane, transaction, or source-memory files.

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill civ-state-volume-harden
python scripts/sync_portable_skills.py --verify --skill civ-state-volume-harden
python scripts/validate_skills.py
```
