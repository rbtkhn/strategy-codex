# Statecraft Source Archive

This tree is the canonical on-disk home of the **Statecraft Source Archive** layer.

For the layer law above it, open [Statecraft Archive and Statecraft Synthesis](../../essays/archive-synthesis-law.md).

This namespace is the canonical dated full-source archive for repo-root `statecraft/`.

It is distinct from root [`archive/`](../../archive/README.md), which preserves frozen legacy holdings rather than live source-truth capture.

Canonical path:

- `source-archive/statecraft/YYYY-MM-DD/source-<slug>.md`
- `source-archive/statecraft/_aired-pending/source-<slug>.md`

**Filename law:** The `source-` prefix marks **archive layer membership** — a full source-truth capture in this tree — not the upstream channel, show, or publication. Shape and identity live in frontmatter (`kind`, `source_form`, `channel_slug`, `show_title`, `host_people`, `guest_people`); the slug after `source-` is topic + date only. Do not use alternate filename prefixes (`transcript-`, `youtube-`, channel names) for new lands. Intake: [statecraft-source-intake SKILL](../../.cursor/skills/statecraft-source-intake/SKILL.md). Deprecated materialize path: [YOUTUBE-MATERIALIZE-DEPRECATED.md](../../docs/skill-work/work-strategy/YOUTUBE-MATERIALIZE-DEPRECATED.md). Queue `file_prefix` vs archive naming: [youtube-transcript-queue § Filename surfaces](../../statecraft/sheets/source-archive-control/youtube-transcript-queue.md#filename-surfaces-file_prefix-vs-source-).

Use this tree for source-bearing captures only. Route control, bridge, continuity, synthesis, and drafting surfaces belong in `statecraft/`, not here.

**Intake queue (derived):** After land, run `python3 scripts/statecraft_intake_queue.py --day YYYY-MM-DD` to see which captures are not yet in daily synthesis. Sidecar metadata lives under `artifacts/statecraft-intake-queue/` — spec: [docs/statecraft-intake-queue.md](../../docs/statecraft-intake-queue.md).

Dated day folders may also contain generated **`day-index.md`** **day archive inventory** notes (channel / writer / other partitions) plus a short **`README.md`** stub pointing at the day-index. These are derived navigation aids, not source captures.
Generated **month archive rollups** live at `source-archive/statecraft/YYYY-MM.md`. Drill down via each day's README ingest register. These are derived navigation aids, not source captures.
Generated year indices now live at `source-archive/statecraft/YYYY.md`. **Thread rollup** and staleness navigation also live at the archive root as derived indices.

After lands, rebuild all archive navigation indices with `python3 scripts/refresh_statecraft_archive_indices.py` (or `post_land_statecraft_batch.py --day YYYY-MM-DD --sync-daily YYYY-MM-DD`). Vocabulary: [Speaker-Shelf Vocabulary — Archive inventory vs voice source bench](../../statecraft/voices/speaker-shelf-vocabulary.md#archive-inventory-vs-voice-source-bench).

Useful indices:

- Year indices: [2025.md](/C:/dev/strategy-codex/source-archive/statecraft/2025.md), [2026.md](/C:/dev/strategy-codex/source-archive/statecraft/2026.md)
- Thread index: [thread-index.md](/C:/dev/strategy-codex/source-archive/statecraft/thread-index.md)
- Channel index: [channel-index.md](/C:/dev/strategy-codex/source-archive/statecraft/channel-index.md)
- Miscellaneous channel index: [channel-index-misc.md](/C:/dev/strategy-codex/source-archive/statecraft/channel-index-misc.md)
- Writer index (Substack roster v1): [writer-index.md](/C:/dev/strategy-codex/source-archive/statecraft/writer-index.md) · [writer-index-spec.md](/C:/dev/strategy-codex/source-archive/statecraft/writer-index-spec.md)
- Day index spec: [day-index-spec.md](/C:/dev/strategy-codex/source-archive/statecraft/day-index-spec.md)
- Stale audit: [stale-index-audit.md](/C:/dev/strategy-codex/source-archive/statecraft/stale-index-audit.md)
- Jiang / Predictive History raw-capture master index: [jiang-predictive-history-index.md](/C:/dev/strategy-codex/source-archive/statecraft/jiang-predictive-history-index.md)
- Public Predictive History lecture index inside the official Jiang mirror: [statecraft/voices/civ-lens-jiang/ph-civ/docs/source-video-index.md](/C:/dev/strategy-codex/statecraft/voices/civ-lens-jiang/ph-civ/docs/source-video-index.md)
- Example month index: [2026-05.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05.md)

When the archive itself is the live problem rather than a source lookup target, open [Archive Truth-Floor Repair Routing](/C:/dev/strategy-codex/statecraft/notes/archive-truth-floor-repair-routing-2026-06-01.md). That note treats the current transcript-integrity seam as a governed machine object with distinct tranches, not as a raw debt pile.
