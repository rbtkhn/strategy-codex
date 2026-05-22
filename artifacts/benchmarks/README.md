# Benchmarks

**Status:** work-layer artifact bucket. Not Record. Not EVIDENCE.

This folder stores benchmark protocols, fixtures, runs, scores, and closeouts used to calibrate Strategy-codex work.

Current benchmark families:

- [composition](composition/README.md) - strategy-page, chapter, book, civ-mem, and public-writing composition quality
- [code-intelligence](code-intelligence/README.md) - local toolchain benchmark loops for repo code exploration, impact review, and architecture prep
- [speaker-memory](speaker-memory/README.md) - speaker object, speaker arc, helix, and routing-judgment quality; canonical green path is bundle-first, with deeper `pytest`/CI checks as a secondary engineering lane
- `agency/` - session-level agency and flow demonstrations

## Quick Start

Bundle-first validation for the `speaker-memory` family:

```bash
python scripts/validate_speaker_memory_benchmark_family.py
```

Expected green-path headline:

- `speaker-memory benchmark family: OK`

Do not store governed Record changes here. Benchmark artifacts may cite Record-adjacent or WORK surfaces, but they do not merge or approve anything.
