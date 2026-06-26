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
| `## Transcript\n` | Default `source-archive/statecraft/**/source-*.md` |
| `## Part I: Full transcript\n` | Long-form provenance packets in sibling repos |
| `## Cleaned Transcript\n` | Post-**`source-clean`** / ASR-normalized captures (Dialogue Works clean wrapper, etc.) |

Auto-detect via `detect_body_marker()` unless `--body-marker` is passed. **Do not** rename `## Cleaned Transcript` → `## Transcript` before sectioning — detection handles both; ship preserves the marker in use.

## Per-source patch scripts

Pin section maps under `scripts/patch_<slug>_sections.py` (pattern from truth-pipeline curation). **Day-batch pins** are OK when curating a compose day — e.g. `scripts/patch_2026_06_25_day_sections.py` holding multiple capture entries.

Each script entry should only hold:

- `titles` / `anchors` (or `SECTION_TITLES` / `SECTION_ANCHORS`)
- optional `asr_cleanup` overrides
- interview `speaker_cleanup` fixes

Call `write_sectioned_capture()` from `main()` for flat bodies; use `write_slug_retitle_capture()` for bootstrap slug → thematic retitle only.

## Navigation quant receipt

After ship or before daily synthesis on a multi-capture day:

```bash
python scripts/quantify_section_nav.py --day YYYY-MM-DD
```

Reports per-capture chunk min/med/max, flat vs sectioned, slug-title warnings, and day-level scan reduction estimate. Wire into **`source-section`** ship receipt when operator asks for metrics.

## Default CLI-shaped one-liner

After map is pinned in a patch script:

```bash
python scripts/patch_<slug>_sections.py
```

No repo-wide batch sectioner — maps stay per capture.

## Pipeline hook (source-intake step 5)

After land (+ optional **`source-clean`**) on **`source_form: solo`** or **`source_form: interview`**, apply **`source-section` § Post-land nudge** when body is flat (≥ ~4k words) or slug-only — state the one-line payoff explicitly; offer **`source-section outline`** first; ship only after map approval. Not automatic on every intake.

## Related docs

- [`source-archive/statecraft/README.md`](../../source-archive/statecraft/README.md)
- [`skills/source-clean/SKILL.md`](../../skills/source-clean/SKILL.md)
- [`skills/statecraft-source-intake/SKILL.md`](../../skills/statecraft-source-intake/SKILL.md)
