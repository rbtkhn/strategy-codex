## strategy-codex instance

- Root working areas for this skill:
  - [codex/speakers](/C:/dev/strategy-codex/codex/speakers)
  - [codex/academy/statecraft](/C:/dev/strategy-codex/codex/academy/statecraft)
- Preferred source stack for China- or statecraft-facing seed extraction:
  - canonical speaker or host arc notes under [codex/speakers](/C:/dev/strategy-codex/codex/speakers)
  - strongest supporting raw-input transcript files under [codex/years/2026/raw-input](/C:/dev/strategy-codex/codex/years/2026/raw-input)
  - lane destination or upstream seed files such as [China volume seeds](/C:/dev/strategy-codex/codex/academy/statecraft/china/china-volume-seeds.md)
- Preferred validation commands after listed-skill edits:

```powershell
python scripts/sync_portable_skills.py --skill arc-to-chapter-seeds
python scripts/sync_portable_skills.py --verify --skill arc-to-chapter-seeds
python scripts/validate_skills.py
```

- Keep this skill upstream. Do not let it write destination-corpus doctrine or imply that a seed list has already become a chapter architecture.
