Grace-mar paths and commands for this repository (from `.cursor/skills/cognition-streams/`).

| Topic | Path |
|--------|------|
| Canonical raw-input tree | [codex/](../../codex/) |
| Date-bucket target pattern | `codex/YYYY/raw-input/YYYY-MM-DD/` |
| Existing lower-layer ingest skill | [skills-portable/youtube-raw-input-transcript/SKILL.md](../../../skills-portable/youtube-raw-input-transcript/SKILL.md) |
| Generated lower-layer Cursor skill | [\.cursor/skills/youtube-raw-input-transcript/SKILL.md](../youtube-raw-input-transcript/SKILL.md) |
| Temp daily discovery cache | [\.codex-tmp/](../../.codex-tmp/) |
| Temp subtitle cache | [\.codex-tmp/yt-dlp/](../../.codex-tmp/yt-dlp/) |
| Portable skill manifest | [skills-portable/manifest.yaml](../../../skills-portable/manifest.yaml) |
| Sync script | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |
| Skill validator | [scripts/validate_skills.py](../../../scripts/validate_skills.py) |

**Repo notes**

- This skill is the **daily wrapper** over the single-URL YouTube transcript workflow.
- In v1, the fixed default watchlist is:
  - Glenn Diesen
  - Daniel Davis
  - Alexander Mercouris
  - Dialogue Works
- The operator-facing rule is:
  - `cognition streams` for daily roster checks
  - `youtube transcript` for one-off URLs
- Default output class should remain conservative:
  - `auto_subtitles_vtt`
- When the operator asks for stronger cleanup later, follow the lower-layer transcript skill rather than inventing a second transcript doctrine here.

**Common local command pattern**

```powershell
python scripts/sync_portable_skills.py --skill cognition-streams
python scripts/sync_portable_skills.py --verify --skill cognition-streams
python scripts/validate_skills.py
```
