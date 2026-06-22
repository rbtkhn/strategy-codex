**strategy-codex instance notes**

- Canonical daily shelf for downstream statecraft essays: [statecraft/synthesis](../../statecraft/synthesis/README.md)
- Canonical archive substrate for these essays: [source-archive/statecraft](/C:/dev/strategy-codex/source-archive/statecraft)
- Use archive-grounded notes and day/month synthesis surfaces as substrate, but do not leave speaker-shelf scaffolding visible in the essay prose.

**Current local model examples**

- Parent day with linked essay pair:
  - [statecraft/synthesis/day/2026-06-01.md](/C:/dev/strategy-codex/statecraft/synthesis/day/2026-06-01.md)
- Paired intelligence essays:
  - [statecraft/notes/2026-06-01-persia-hormuz-lebanon-strategic-memory.md](/C:/dev/strategy-codex/statecraft/notes/2026-06-01-persia-hormuz-lebanon-strategic-memory.md)
  - [statecraft/notes/2026-06-01-america-hormuz-lebanon-strategic-memory.md](/C:/dev/strategy-codex/statecraft/notes/2026-06-01-america-hormuz-lebanon-strategic-memory.md)

**Repo notes**

- Daily and monthly synthesis documents remain the quote-bearing, speaker-shelf-based surfaces.
- Intelligence essays remain synthetic, authored, and non-speaker-led.
- Use the archive as substrate rather than visible frame.

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill statecraft-intelligence-essay
python scripts/sync_portable_skills.py --verify --skill statecraft-intelligence-essay
python scripts/validate_skills.py
```
