Grace-mar paths and commands for this repository (from `.cursor/skills/check-streams/`).

| Topic | Path |
|--------|------|
| Canonical source archive | [source-archive/statecraft/](../../source-archive/statecraft/) |
| Archive land skill | [statecraft-source-intake/SKILL.md](../statecraft-source-intake/SKILL.md) |
| Deprecated materialize path | [YOUTUBE-MATERIALIZE-DEPRECATED.md](../../../docs/skill-work/work-strategy/YOUTUBE-MATERIALIZE-DEPRECATED.md) |
| Legacy raw-input tree (staging) | [docs/skill-work/work-strategy/strategy-notebook/raw-input/](../../../docs/skill-work/work-strategy/strategy-notebook/raw-input/) |
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

- This skill is the **daily roster wrapper**; approved captures close with **`source-intake`**, not `materialize_youtube_raw_input.py --apply`.
- `check streams` is the canonical activation; `cognition streams` remains a legacy compatibility alias.
- After archive land, speaker folders are the durable routing layer. Lattice/cognition-streams surfaces are secondary lookup views, not the first update target.
- In v1, the fixed default watchlist is:
  - Glenn Diesen
  - Daniel Davis
  - Alexander Mercouris
  - Dialogue Works
  - Judge Napolitano / Judging Freedom
  - Redacted News (sixth channel on discovery config)
- The operator-facing rule is:
  - `check streams` for daily roster checks
  - `cognition streams` as a legacy alias
  - `source-intake` for canonical archive land (paste or post-fetch body)
- Default transcript provenance on subtitle fetch should remain conservative (`auto_subtitles_vtt`).

**Common local command pattern**

```powershell
python scripts/sync_portable_skills.py --skill check-streams
python scripts/sync_portable_skills.py --verify --skill check-streams
python scripts/build_speaker_routing_queue.py --start YYYY-MM-DD --end YYYY-MM-DD
python scripts/validate_skills.py
```
