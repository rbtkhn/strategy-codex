Grace-mar paths and commands for this repository (from `.cursor/skills/check-sources/`).

| Topic | Path |
|--------|------|
| Canonical source archive | [source-archive/statecraft/](../../source-archive/statecraft/) |
| Check-sources roster (machine) | [channel-index.json](../../source-archive/statecraft/channel-index.json) |
| Check-sources roster (human) | [channel-index.md](../../source-archive/statecraft/channel-index.md) |
| Roster loader | [statecraft_youtube_discovery.py](../../scripts/statecraft_youtube_discovery.py) (`load_check_sources_roster`) |
| Archive land skill | [statecraft-source-intake/SKILL.md](../statecraft-source-intake/SKILL.md) |
| Deprecated materialize path | [YOUTUBE-MATERIALIZE-DEPRECATED.md](../../../docs/skill-work/work-strategy/YOUTUBE-MATERIALIZE-DEPRECATED.md) |
| Legacy check-streams stub | [check-streams/SKILL.md](../check-streams/SKILL.md) |
| Legacy raw-input tree (staging) | [docs/skill-work/work-strategy/strategy-notebook/raw-input/](../../../docs/skill-work/work-strategy/strategy-notebook/raw-input/) |
| Analyst shelves | [statecraft/voices/](../../../statecraft/voices/) |
| Channel shelves | [statecraft/channels/](../../../statecraft/channels/) |
| Philosophical gloss | [docs/skill-work/work-strategy/cognition-streams-daily-aperture.md](../../../docs/skill-work/work-strategy/cognition-streams-daily-aperture.md) |
| Temp daily discovery cache | [\.codex-tmp/](../../.codex-tmp/) |
| Portable skill manifest | [skills/manifest.yaml](../../../skills/manifest.yaml) |
| Sync script | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |

**Repo notes**

- **`check sources`** is canonical; **`check streams`** and **`cognition streams`** are legacy aliases.
- Roster SSOT: **`channel-index.json`** (main only; misc excluded). Watchlist fast pass = six `daily_watchlist` channels.
- Approved captures close with **`source-intake`**, not `materialize_youtube_raw_input.py --apply`.

**Common local command pattern**

```powershell
python scripts/sync_portable_skills.py --skill check-sources
python scripts/sync_portable_skills.py --verify --skill check-sources
python -c "from pathlib import Path; import sys; sys.path.insert(0,'scripts'); from statecraft_youtube_discovery import load_check_sources_roster; print(len(load_check_sources_roster()))"
python scripts/refresh_statecraft_archive_indices.py
python scripts/build_speaker_routing_queue.py --start YYYY-MM-DD --end YYYY-MM-DD
python scripts/validate_skills.py
```
