# Cursor appendix — `source-section`

Host-specific paths for **strategy-codex**. Portable core: [`skills/source-section/SKILL.md`](../../skills/source-section/SKILL.md).

## Shared library

```text
scripts/transcript_section_curation.py
```

Import (Windows-safe — in-process for batch):

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path("scripts").resolve()))
from transcript_section_curation import (
    insert_sections,
    write_sectioned_capture,
    write_slug_retitle_capture,
    common_asr_cleanup,
    prepend_speaker_at_section_opens,
    strip_speakers_before_section_headings,
)
```

## Body markers (statecraft archive)

| Marker | Typical surface |
| --- | --- |
| `## Transcript\n` | `source-archive/statecraft/**/source-*.md` |
| `## Part I: Full transcript\n` | Long-form provenance packets in sibling repos |

Auto-detect via `detect_body_marker()` unless `--body-marker` is passed.

## Per-source patch scripts

Pin section maps under `scripts/patch_<slug>_sections.py` (pattern from truth-pipeline curation). Each script should only hold:

- `SECTION_TITLES` / `SECTION_ANCHORS`
- optional `asr_cleanup` overrides
- interview `speaker_cleanup` fixes

Call `write_sectioned_capture()` from `main()`.

## Default CLI-shaped one-liner

After map is pinned in a patch script:

```bash
python scripts/patch_<slug>_sections.py
```

No repo-wide batch sectioner — maps stay per capture.

## Pipeline hook (source-intake step 5)

After land (+ optional **`source-clean`**) on **`source_form: solo`** or **`source_form: interview`**, offer **`source-section outline`** first on long captures; **`source-section`** ship only after map approval — not automatic on every intake.

## Related docs

- [`source-archive/statecraft/README.md`](../../source-archive/statecraft/README.md)
- [`skills/source-clean/SKILL.md`](../../skills/source-clean/SKILL.md)
- [`skills/statecraft-source-intake/SKILL.md`](../../skills/statecraft-source-intake/SKILL.md)
