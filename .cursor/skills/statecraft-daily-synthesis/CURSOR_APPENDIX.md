**strategy-codex instance notes**

- Canonical source day root for this skill: [source-archive/statecraft](/C:/dev/strategy-codex/source-archive/statecraft)
- Canonical synthesis side for daily reports: [statecraft/daily](/C:/dev/strategy-codex/statecraft/daily/README.md)
- Use the day archive inventory first, then write synthesis downstream.
- Do not place synthesis notes in `source-archive/statecraft/`.

**Current local model example**

- Daily synthesis report:
  - [statecraft/daily/2026-05-29.md](/C:/dev/strategy-codex/statecraft/daily/2026-05-29.md)
- Companion comparison note:
  - [statecraft/daily/2026-05-29-pape-vs-freeman-sachs-marandi.md](/C:/dev/strategy-codex/statecraft/daily/2026-05-29-pape-vs-freeman-sachs-marandi.md)

**Repo notes**

- Archive truth stays upstream in `source-archive/statecraft/`.
- This skill begins only after the archive batch is real.
- The default companion mechanism comparison for this repo is:
  - `Pape` = trap logic
  - `Freeman` = strategic backfire
  - `Sachs` = enabling carrier
  - `Marandi` = adversary-side hardening

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill statecraft-daily-synthesis
python scripts/sync_portable_skills.py --verify --skill statecraft-daily-synthesis
python scripts/validate_skills.py
```
