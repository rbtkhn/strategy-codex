# Civilizational Statecraft external boundary

`rbtkhn/civ-state` is the canonical **public Civilizational Statecraft** book (repo slug only — not a reader-facing title).

It is the standalone comparative artifact: **Civilization and Empire** (whole-work opening essay), **five case volumes** (China, Persia, Rome, Russia, America) each with a **thematic volume introduction**, then **Civilization** and **Empire** essay chapters, source-lattice, plus a **whole-work appendix** (theory, sacred grammar, hybrid references, index, comparative essays).

Title layers are locked in [`public/civ-state/docs/`](../public/civ-state/docs/names-and-titles.md) — [Names and titles](../public/civ-state/docs/names-and-titles.md) and [Glossary](../public/civ-state/docs/glossary.md).

Inside `strategy-codex`, Civilizational Statecraft uses a **staging mirror → explicit publish** loop (same shape as Predictive History):

- **edit** only under [`public/civ-state/`](../public/civ-state/)
- **pull inbound** with `python scripts/sync_public_civ_state_mirror.py`
- **publish outbound** with `python scripts/publish_public_civ_state.py -m "…" --push`

## Canonical rule

**Public canonical text lives in `rbtkhn/civ-state`.** Workspace edits live in **`public/civ-state/`** until publish.

Publishing happens only through:

```text
edit public/civ-state/ → commit workspace slice → publish script --push → tagged release on rbtkhn/civ-state
```

## statecraft/states ⊥ public/civ-state (locked)

**`statecraft/states/` is not a workshop, upstream, or draft layer for the public book.**

| Surface | Role |
|---------|------|
| [`public/civ-state/`](../public/civ-state/) | Sole workspace edit surface for ship-bound Civilizational Statecraft prose |
| [`rbtkhn/civ-state`](https://github.com/rbtkhn/civ-state) | Canonical public repository |
| [`statecraft/states/`](../statecraft/states/) | Operator statecraft substrate — lane memory, live drafting, deployment routing (`civ-state remembers → statecraft drafts`) |

These trees are **orthogonal**. Edits under `statecraft/states/` do **not** update the public book. The public book does **not** draft upstream in `statecraft/states/`.

Do not treat `statecraft/states/` as silently updating `public/civ-state/` or `rbtkhn/civ-state`. Ship-bound prose changes belong in `public/civ-state/` directly.

## ph-civ ⊥ civ-state (locked)

**`ph-civ` and `civ-state` are distinct public artifacts.** They **must not reference each other** in published civ-state copy:

- no cross-repo URLs or footnotes
- no bridge pages or shared navigation
- no PH chapter / pattern IDs in public shelves or apparatus

strategy-codex **observes** [`rbtkhn/predictive-history`](https://github.com/rbtkhn/predictive-history) per [predictive-history-external-boundary.md](predictive-history-external-boundary.md). Internal operator files such as [`ph-civ-promotion-ledger.md`](../statecraft/states/ph-civ-promotion-ledger.md) and [`ph-civ-to-civ-state-bridge.md`](../statecraft/states/ph-civ-to-civ-state-bridge.md) are **not exported** and are **not** a public-book pipe.

## What belongs in strategy-codex

Allowed Civilizational Statecraft work inside `strategy-codex`:

- **corpus edits** under `public/civ-state/` only (staging mirror)
- **publish** to [`rbtkhn/civ-state`](https://github.com/rbtkhn/civ-state) only via `scripts/publish_public_civ_state.py --push`
- **operator statecraft** under `statecraft/states/` — live drafting, lanes, synthesis (separate from public book SSOT)
- run `scripts/validate_civilizational_statecraft_public.py` on `public/civ-state/`
- critique public `civ-state` PRs and issues
- cite public civ-state slugs in operator copy when routing readers to the book

## What does not belong in strategy-codex (as public canonical)

Disallowed after cutover:

- editing ship-bound civ-state prose outside `public/civ-state/`
- treating a normal strategy-codex commit as having updated the public repo (without `publish_public_civ_state.py --push`)
- treating `statecraft/states/` edits as updating the public book
- patching `rbtkhn/civ-state` from residue paths other than `public/civ-state/`
- embedding ph-civ links in civ-state public output (export/publish linter)
- framing `statecraft/states/` as upstream workshop or dual SSOT for `public/civ-state/`

## Legacy export script

[`scripts/export_civilizational_statecraft_public.py`](../scripts/export_civilizational_statecraft_public.py) remains for **historical migration and bulk reshape receipts** only — not daily edit, not promotion from `statecraft/states/` as normal workflow. Daily ship-bound edits belong in `public/civ-state/` directly.

| Asset | Path |
|-------|------|
| Export manifest | [`platform/config/civilizational_statecraft_public_export.yaml`](../platform/config/civilizational_statecraft_public_export.yaml) |
| Export script | [`scripts/export_civilizational_statecraft_public.py`](../scripts/export_civilizational_statecraft_public.py) |
| Validator | [`scripts/validate_civilizational_statecraft_public.py`](../scripts/validate_civilizational_statecraft_public.py) |
| Staging output | [`public/civ-state/`](../public/civ-state/) |
| Legacy residue | [`runtime/artifacts/civilizational-statecraft-public/`](../runtime/artifacts/civilizational-statecraft-public/) — retired; do not refresh |

## Feedback loop

```text
edit public/civ-state/ in strategy-codex
  → commit workspace slice
  → python scripts/publish_public_civ_state.py -m "…" --push
  → tagged/public main on rbtkhn/civ-state
```

## Related

- Unified public-artifact law: [public-artifacts-boundary.md](public-artifacts-boundary.md)
- PH boundary: [predictive-history-external-boundary.md](predictive-history-external-boundary.md)
- GitHub rename procedure: [civilizational-statecraft/GITHUB-RENAME-CIV-STATE.md](civilizational-statecraft/GITHUB-RENAME-CIV-STATE.md)
