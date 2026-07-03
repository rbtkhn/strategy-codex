# continuity/ — compatibility naming
<!-- word_count: 215 -->

Public project name remains **strategy-codex**. This folder is **`continuity/`** (formerly `codex/`). See [docs/codex-to-continuity-rename.md](../docs/codex-to-continuity-rename.md).

## Naming split

| Token | Role |
|-------|------|
| **strategy-codex** | Public name for the notebook/workspace |
| **strategy-notebook** | Legacy compatibility name in some tooling paths |
| **strategy-author** | Public name for the human analytical lane |
| **strategy-expert** | Legacy parser, marker, and filename contract |
| **continuity/** | Canonical path for this tree |
| **codex/** | Legacy redirect only |

## Practical rules

- In **prose, menus, rules, and operator guidance**, prefer **strategy-codex** and **strategy-author**.
- In **paths, filenames, parser regexes, HTML markers, fixtures, and generated artifacts**, keep legacy forms until a coordinated migration updates machinery.

When both names appear:

- `strategy-codex (legacy path: strategy-notebook)`
- `strategy-author (legacy filename contract: strategy-expert-*)`

## Operator books (misc homes)

| Operator phrase | Canonical path |
|-----------------|----------------|
| `strategy-codex` | `continuity/` (this tree) |
| `strategy-notebook` (legacy) | `continuity/` — [STRATEGY-NOTEBOOK-DEPRECATED.md](../docs/archive/skill-work-legacy/work-strategy/STRATEGY-NOTEBOOK-DEPRECATED.md) |
| `predictive-history` | `continuity/predictive-history/` |
| cici notebook | `singularity/work-cici/cici-notebook/` |
| dev journal | `docs/archive/skill-work-legacy/work-dev/dev-notebook/work-dev/journal/` |
| history notebook | `docs/archive/skill-work-legacy/work-strategy/history-notebook/` |
| theology notebook | `docs/archive/skill-work-legacy/work-strategy/theology-notebook/` |

Routing rule: [`.cursor/rules/operator-books-routing.mdc`](../.cursor/rules/operator-books-routing.mdc).

## Primary 2026 volume pointers

Full-source capture: [`source-archive/statecraft/`](../source-archive/statecraft/README.md). People shelves: [`statecraft/voices/`](../statecraft/voices/README.md). Host continuity: [`statecraft/channels/`](../statecraft/channels/README.md). Legacy `continuity/speakers/` terminated — [codex-speakers-deprecated.md](../docs/archive/codex-speakers-deprecated.md). Channel profiles: [`profiles/`](profiles/).
