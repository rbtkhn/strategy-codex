---
name: youtube-raw-input-transcript
preferred_activation: youtube transcript
description: 'DEPRECATED 2026-06-20. Do not use for new strategy-codex capture. Redirect: source-intake for archive land; check streams for daily roster. See YOUTUBE-MATERIALIZE-DEPRECATED.md.'
portable: true
version: 0.2.0
deprecated: 2026-06-20
see: docs/skill-work/work-strategy/YOUTUBE-MATERIALIZE-DEPRECATED.md
tags:
- operator
- deprecated
- youtube
portable_source: skills/youtube-raw-input-transcript/SKILL.md
synced_by: sync_portable_skills.py
---
# DEPRECATED — YouTube raw-input / materialize skill

**Status:** Deprecated **2026-06-20**. Do not invoke **`youtube transcript`** or **`materialize_youtube_raw_input.py --apply`** for new work in strategy-codex.

Full spec: [YOUTUBE-MATERIALIZE-DEPRECATED.md](../../docs/skill-work/work-strategy/YOUTUBE-MATERIALIZE-DEPRECATED.md)

## Use instead

| Task | Skill / path |
|------|----------------|
| Land pasted or fetched transcript to canonical archive | **`source-intake`** ([`statecraft-source-intake`](../statecraft-source-intake/SKILL.md)) |
| Daily Davis / Diesen / Dialogue Works / Napolitano / Mercouris roster | **`check streams`** ([`check-streams`](../check-streams/SKILL.md)) → approved URLs → **`source-intake`** |
| Channel inventory | [`source-archive/statecraft/channel-index.md`](../../source-archive/statecraft/channel-index.md) |

## Legacy script (no new archive writes)

`python scripts/materialize_youtube_raw_input.py` remains on disk for archaeology and receipt replay only. New captures must use **`source-*`** filenames under `source-archive/statecraft/`.


## Cursor / strategy-codex instance

Grace-mar paths and commands for this repository (from `.cursor/skills/youtube-raw-input-transcript/`).

| Topic | Path |
|--------|------|
| Canonical raw-input tree | [codex/](../../codex/) |
| Date-bucket target pattern | `codex/YYYY/raw-input/YYYY-MM-DD/` |
| Existing Diesen examples | [codex/years/2026/raw-input/2026-04-19/](../../codex/years/2026/raw-input/2026-04-19/) · [codex/years/2026/raw-input/2026-05-11/](../../codex/years/2026/raw-input/2026-05-11/) |
| Temp subtitle cache | [\.codex-tmp/yt-dlp/](../../.codex-tmp/yt-dlp/) |
| Portable skill manifest | [skills/manifest.yaml](../../../skills/manifest.yaml) |
| Sync script | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |
| Skill validator | [scripts/validate_skills.py](../../../scripts/validate_skills.py) |

**Repo notes**

- In this repo, `thread` is usually the host lane such as `diesen`, `mercouris`, or `davis`.
- Prefer `python -m yt_dlp` if `yt-dlp` is not on `PATH`.
- Preserve explicit `editorial_note` language:
  - `Operator-pasted cleaned transcript.`
  - `Auto-captions extracted with yt_dlp from YouTube VTT (en-orig).`
  - `Best-effort speaker normalization and sentence polishing from YouTube auto-captions extracted with yt_dlp (en-orig). Not human-verified verbatim.`

**Common local command pattern**

```powershell
python -m yt_dlp --skip-download --print "%(id)s`n%(title)s`n%(upload_date)s`n%(channel)s" "<youtube-url>"

python -m yt_dlp --skip-download --write-auto-sub --sub-langs "en.*" --sub-format vtt -o "C:\dev\strategy-codex\.codex-tmp\yt-dlp\%(id)s.%(ext)s" "<youtube-url>"
```
