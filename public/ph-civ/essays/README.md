# Essays

**Canonical public home** for Predictive History **Substack and long-form essay** chapters.

Repo path: **`essays/`** at the ph-civ root (sibling to [`ph-civ/`](ph-civ/README.md), [`ph-apo/`](ph-apo/README.md), [`book/`](book/), [`sources/`](sources/)).

## Recategorization (operator policy)

Essays are **explicitly recategorized** out of the Apocalypse-only lane:

- **Before:** essays treated mainly as Volume VII / `ph-apo` / `world-war` (legacy `book/volume-vii/`, `sub-*` on Apocalypse surface).
- **After:** essays are **medium-first** on **`essays/<source_id>/`** with catalog surface **`ph-civ`** / part **`civilization`**.

Reader rollup under [`book/volume-ii-apocalypse/sub/`](book/volume-ii-apocalypse/sub/) may remain as **cross-links or mirrors** during migration; **`essays/<source_id>/`** is the target direct namespace for new and moved essay packets.

## Corpus scope

- **Public today:** five `sub-*` chapter packets (promoted from Substack; paths migrating here).
- **Workshop residue (intake backlog):** ~35 curated files in frozen `codex/predictive-history/substack/essays/` — promote through `public/ph-civ/` intake, not by editing the frozen tree.

## Packet shape

Each essay chapter:

- `*-transcript.md` — verbatim essay body
- `*-commentary.md` — open commentary canvas
- `README.md` — public study doorway
- optional `*-orientation.yaml`

Registry: [`data/cards.jsonl`](data/cards.jsonl) · catalog: [`docs/ph-civ-index.md`](docs/ph-civ-index.md).

## Catalog fields (target after migration)

| Field | Value |
|-------|--------|
| `series` | `essays` |
| `part` | `civilization` |
| `surface` | `ph-civ` |
| `source_paths.*` | under `essays/<source_id>/` |

Legacy Apocalypse routing for `sub-*` is **deprecated** once a chapter is migrated and the index is regenerated.
