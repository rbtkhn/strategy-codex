# Predictive History comment rollout

This work-strategy note documents the single-phase public comment rollout for the Predictive History YouTube channel.

The default model remains the trust-first doorway rollout. A separate local pilot now also exists for `civ-01` through `civ-06`: [Wave One: `civ-01` to `civ-06`](wave-one-civ-01-to-civ-06.md). That pilot treats comments as statecraft proof objects rather than repo doorways.

## Phase

- **Phase 1:** one top-level trust-first comment per video, using the chapter-folder doorway packet from `ph-civ`.

The retired `ph-mus` exhibit follow-up phase was removed from the mirror vision. See [`public/predictive-history/docs/archive/ph-mus-retired.md`](../../../../public/predictive-history/docs/archive/ph-mus-retired.md).

## Canonical sources

- Public source list: [`statecraft/voices/civ-lens-jiang/ph-civ/docs/source-video-index.md`](../../../../statecraft/voices/civ-lens-jiang/ph-civ/docs/source-video-index.md)
- Comment doctrine: [`docs/skill-write/predictive-history-youtube-comments.md`](../../../skill-write/predictive-history-youtube-comments.md)

## Queue and commands

The rollout queue is stored at:

- [`queue.json`](queue.json)

The readable local Phase 1 review drafts are rendered under:

- [`drafts/`](drafts/)

`queue.json` is the canonical workflow ledger for readiness, approval, and posting state. The Markdown files under `drafts/` are local review surfaces only. They are generated from queue state and rollout inputs so comment drafting stays inside `strategy-codex` rather than the public `ph-civ` repo.

Recommended commands:

```bash
python scripts/predictive_history_comment_rollout.py build --write
python scripts/predictive_history_comment_rollout.py report
python scripts/predictive_history_comment_rollout.py draft gt-16 1
python scripts/predictive_history_comment_rollout.py set-state gt-16 1 --state approved
python scripts/predictive_history_comment_rollout.py post --phase 1 --dry-run
```

## Guardrails

- Keep the rollout review-gated.
- Keep draft comments local to `strategy-codex`; do not store them in the public `ph-civ` repo.
- Use `commentThreads.insert` only for approved top-level comments.
- Preserve the quiet, lecture-first tone from the comment doctrine.

For the Wave One pilot:

- comments may omit links entirely
- comments should demonstrate statecraft synthesis in public without exposing internal machinery
- each comment must include at least two concrete historical examples
- those examples should explicitly support the thesis rather than sit as vague references
