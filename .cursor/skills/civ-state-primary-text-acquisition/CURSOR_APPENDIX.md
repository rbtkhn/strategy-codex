**strategy-codex instance notes**

- Canonical doctrine note for this skill: [statecraft/states/primary-text-architecture.md](/C:/dev/strategy-codex/statecraft/states/primary-text-architecture.md)
- Canonical structured layers:
  - [source-records](/C:/dev/strategy-codex/statecraft/states/source-records/README.md)
  - [source-excerpts](/C:/dev/strategy-codex/statecraft/states/source-excerpts/README.md)
  - [source-sidecar](/C:/dev/strategy-codex/statecraft/states/source-sidecar/README.md)
- Current pilot records live under:
  - [statecraft/states/source-records/pilot](/C:/dev/strategy-codex/statecraft/states/source-records/pilot)

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill civ-state-primary-text-acquisition
python scripts/sync_portable_skills.py --verify --skill civ-state-primary-text-acquisition
python scripts/validate_skills.py
```
