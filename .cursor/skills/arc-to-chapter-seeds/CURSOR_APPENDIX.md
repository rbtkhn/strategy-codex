## strategy-codex instance

- Root working areas for this skill:
  - [statecraft/voices](../../../statecraft/voices/)
  - [statecraft/channels](../../../statecraft/channels/)
  - [codex/academy/statecraft](../../../codex/academy/statecraft)
- Preferred source stack for China- or statecraft-facing seed extraction:
  - canonical analyst arc notes under [statecraft/voices/](../../../statecraft/voices/) and host guest arcs under [statecraft/channels/](../../../statecraft/channels/)
  - strongest supporting raw-input transcript files under [codex/years/2026/raw-input](../../../codex/years/2026/raw-input) (archaeology only)
  - lane destination or upstream seed files such as [China volume seeds](../../../codex/academy/statecraft/china/chapter-seeds.md)
- Preferred validation commands after listed-skill edits:

```powershell
python scripts/sync_portable_skills.py --skill arc-to-chapter-seeds
python scripts/sync_portable_skills.py --verify --skill arc-to-chapter-seeds
python scripts/validate_skills.py
```

- Keep this skill upstream. Do not let it write destination-corpus doctrine or imply that a seed list has already become a chapter architecture.
