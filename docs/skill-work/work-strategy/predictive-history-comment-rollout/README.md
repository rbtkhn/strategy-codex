# Predictive History comment rollout

This work-strategy note documents the two-phase public comment rollout for the Predictive History YouTube channel.

## Phases

- **Phase 1:** one top-level trust-first comment per video, using the chapter-folder doorway packet from `ph-civ`.
- **Phase 2:** one second top-level comment per video, using the corresponding `ph-mus` exhibit route when one exists.

If the route is missing or unpublished, the item is parked instead of inventing a link.

## Canonical sources

- Public source list: [`codex/academy/ph-civ/docs/source-video-index.md`](../../../../academy/ph-civ/docs/source-video-index.md)
- Museum manifest index: [`codex/academy/ph-civ/data/museum/index.json`](../../../../academy/ph-civ/data/museum/index.json)
- Comment doctrine: [`docs/skill-write/predictive-history-youtube-comments.md`](../../../skill-write/predictive-history-youtube-comments.md)

## Queue and commands

The rollout queue is stored at:

- [`queue.json`](queue.json)

Recommended commands:

```bash
python scripts/predictive_history_comment_rollout.py build --write
python scripts/predictive_history_comment_rollout.py report
python scripts/predictive_history_comment_rollout.py draft gt-16 1
python scripts/predictive_history_comment_rollout.py draft gt-16 2
python scripts/predictive_history_comment_rollout.py set-state gt-16 1 --state approved
python scripts/predictive_history_comment_rollout.py post --phase 1 --dry-run
```

## Guardrails

- Keep the rollout review-gated.
- Use `commentThreads.insert` only for approved top-level comments.
- Do not fabricate a `ph-mus` link if no exhibit route exists.
- Preserve the quiet, lecture-first tone from the comment doctrine.
