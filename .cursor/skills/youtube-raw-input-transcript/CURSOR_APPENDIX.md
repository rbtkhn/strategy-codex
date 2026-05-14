Grace-mar paths and commands for this repository (from `.cursor/skills/youtube-raw-input-transcript/`).

| Topic | Path |
|--------|------|
| Canonical raw-input tree | [codex/](../../codex/) |
| Date-bucket target pattern | `codex/YYYY/raw-input/YYYY-MM-DD/` |
| Existing Diesen examples | [codex/2026/raw-input/2026-04-19/](../../codex/2026/raw-input/2026-04-19/) · [codex/2026/raw-input/2026-05-11/](../../codex/2026/raw-input/2026-05-11/) |
| Temp subtitle cache | [\.codex-tmp/yt-dlp/](../../.codex-tmp/yt-dlp/) |
| Portable skill manifest | [skills-portable/manifest.yaml](../../../skills-portable/manifest.yaml) |
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
