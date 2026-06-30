# Voice and avatar tools — layer separation

WORK only; not Record.

---

## Principle

Voice and visual presenter layers are **separate artifacts** until final composite:

```text
narration_script.md  →  voiceover.wav  →  video_edit.mp4
lesson_script.md     →  avatar take (optional)  →  video_edit.mp4
```

Enables re-voice, translation, audio-only podcast, and caption-only updates without full video rebuild.

---

## Voice (narration)

| Use | Tool class | Notes |
| --- | --- | --- |
| Primary narration | TTS (ElevenLabs, etc.) | Consistent voice across lessons |
| Human read | Operator recording | Highest trust for sensitive material |
| Podcast export | Same voiceover track | Feed `distribution/podcast/` |

**Checks:** intelligibility, pacing match to segment plan, rights/commercial terms documented.

---

## Avatar / talking-head (optional)

| Use | Tool class | Notes |
| --- | --- | --- |
| Explainer segments | Synthesia, HeyGen | Can feel generic — use sparingly |
| No avatar | Slides + voiceover | Default for PH until quality bar met |

**Checks:** no unclear likeness; disclosure where platform requires; avatar does not replace source citation on screen.

---

## Related

- [`ai-video-tools.md`](ai-video-tools.md)
- [`rights-and-disclosure.md`](rights-and-disclosure.md)
- [`../media-review/media-quality-gate-template.md`](../media-review/media-quality-gate-template.md)
