Grace-mar paths and commands for this repository (from `.cursor/skills/check-streams/`).

| Topic | Path |
|--------|------|
| Canonical raw-input tree | [codex/](../../codex/) |
| Date-bucket target pattern | `codex/YYYY/raw-input/YYYY-MM-DD/` |
| Existing lower-layer ingest skill | [skills/youtube-raw-input-transcript/SKILL.md](../../../skills/youtube-raw-input-transcript/SKILL.md) |
| Generated lower-layer Cursor skill | [\.cursor/skills/youtube-raw-input-transcript/SKILL.md](../youtube-raw-input-transcript/SKILL.md) |
| Speaker folder shelf | [codex/speakers/](../../../codex/speakers/) |
| Speaker arc boundary | [docs/skill-work/work-strategy/speaker-arc-thread-lattice-boundaries.md](../../../docs/skill-work/work-strategy/speaker-arc-thread-lattice-boundaries.md) |
| Raw-input vs speaker arc boundary | [docs/skill-work/work-strategy/raw-input-ownership-vs-speaker-arc.md](../../../docs/skill-work/work-strategy/raw-input-ownership-vs-speaker-arc.md) |
| Philosophical gloss | [docs/skill-work/work-strategy/cognition-streams-daily-aperture.md](../../../docs/skill-work/work-strategy/cognition-streams-daily-aperture.md) |
| Temp daily discovery cache | [\.codex-tmp/](../../.codex-tmp/) |
| Temp subtitle cache | [\.codex-tmp/yt-dlp/](../../.codex-tmp/yt-dlp/) |
| Portable skill manifest | [skills/manifest.yaml](../../../skills/manifest.yaml) |
| Sync script | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |
| Skill validator | [scripts/validate_skills.py](../../../scripts/validate_skills.py) |

**Repo notes**

- This skill is the **daily wrapper** over the single-URL YouTube transcript workflow.
- `check streams` is the canonical activation; `cognition streams` remains a legacy compatibility alias.
- After raw-input materialization, speaker folders are the durable routing layer. Lattice/cognition-streams surfaces are secondary lookup views, not the first update target.
- In v1, the fixed default watchlist is:
  - Glenn Diesen
  - Daniel Davis
  - Alexander Mercouris
  - Dialogue Works
- The operator-facing rule is:
  - `check streams` for daily roster checks
  - `cognition streams` as a legacy alias
  - `youtube transcript` for one-off URLs
- Default output class should remain conservative:
  - `auto_subtitles_vtt`
- When the operator asks for stronger cleanup later, follow the lower-layer transcript skill rather than inventing a second transcript doctrine here.

**Common local command pattern**

```powershell
python scripts/sync_portable_skills.py --skill check-streams
python scripts/sync_portable_skills.py --verify --skill check-streams
python scripts/build_speaker_routing_queue.py --start YYYY-MM-DD --end YYYY-MM-DD
python scripts/validate_skills.py
```
