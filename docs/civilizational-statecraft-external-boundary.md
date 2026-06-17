# Civilizational Statecraft external boundary

`rbtkhn/civ-state` is the canonical **public Civilizational Statecraft** book (repo slug only — not a reader-facing title).

It is the standalone comparative artifact: **Civilization and Empire** (whole-work opening essay), **five case volumes** (China, Persia, Rome, Russia, America) each with a **thematic volume introduction**, then **Civilization** and **Empire** essay chapters, source-lattice, plus a **whole-work appendix** (framework, sacred grammar, hybrid references, index, comparative continuity, pattern library).

Title layers are locked in workshop [Names and titles](../statecraft/states/reader-guide.md#names-and-titles) and [Glossary](../statecraft/states/glossary.md).

Inside `strategy-codex`, Civilizational Statecraft uses a **staging mirror → explicit publish** loop (same shape as Predictive History):

- **edit** only under [`public/civ-state/`](../public/civ-state/)
- **pull inbound** with `python scripts/sync_public_civ_state_mirror.py`
- **publish outbound** with `python scripts/publish_public_civ_state.py -m "…" --push`

Operator workshop under `statecraft/states/` continues for analysis, promotion, and review — **not** as the public book edit surface. Public canonical text lives in **`rbtkhn/civ-state`**; workspace edits live in **`public/civ-state/`** until publish.

## Canonical rule

After cutover, strategy-codex must not treat `statecraft/states/` as silently updating the public book. Public canonical text lives in **`rbtkhn/civ-state`**; workspace edits live in **`public/civ-state/`** until publish.

Publishing happens only through:

```text
edit public/civ-state/ → commit workspace slice → publish script --push → tagged release on rbtkhn/civ-state
```

## ph-civ ⊥ civ-state (locked)

**`ph-civ` and `civ-state` are distinct public artifacts.** They **must not reference each other** in published civ-state copy:

- no cross-repo URLs or footnotes
- no bridge pages or shared navigation
- no PH chapter / pattern IDs in public shelves or apparatus

strategy-codex **observes** [`rbtkhn/ph-civ`](https://github.com/rbtkhn/ph-civ) per [predictive-history-external-boundary.md](predictive-history-external-boundary.md). Internal workshop files such as [`ph-civ-promotion-ledger.md`](../statecraft/states/ph-civ-promotion-ledger.md) and [`ph-civ-to-civ-state-bridge.md`](../statecraft/states/ph-civ-to-civ-state-bridge.md) are **not exported**.

## What belongs in strategy-codex

Allowed Civilizational Statecraft work inside `strategy-codex`:

- **corpus edits** under `public/civ-state/` only (staging mirror)
- **publish** to [`rbtkhn/civ-state`](https://github.com/rbtkhn/civ-state) only via `scripts/publish_public_civ_state.py --push`
- deepen operator workshop in `statecraft/states/` (analysis, promotion, game-substrate — non-ship until landed in `public/civ-state/`)
- optional **workshop promotion:** `export_civilizational_statecraft_public.py` → `public/civ-state/` (bulk transform, not daily edit)
- run `scripts/validate_civilizational_statecraft_public.py` on `public/civ-state/`
- critique public `civ-state` PRs and issues
- cite public civ-state slugs in review packets and operator copy

## What does not belong in strategy-codex (as public canonical)

Disallowed after cutover:

- editing ship-bound civ-state prose outside `public/civ-state/`
- treating a normal strategy-codex commit as having updated the public repo (without `publish_public_civ_state.py --push`)
- treating local `statecraft/states/` edits as silently updating the public book
- patching `rbtkhn/civ-state` from residue paths other than `public/civ-state/`
- embedding ph-civ links in civ-state public output (export/publish linter)

## Export surfaces

| Asset | Path |
|-------|------|
| Export manifest | [`config/civilizational_statecraft_public_export.yaml`](../config/civilizational_statecraft_public_export.yaml) |
| Export script | [`scripts/export_civilizational_statecraft_public.py`](../scripts/export_civilizational_statecraft_public.py) |
| Validator | [`scripts/validate_civilizational_statecraft_public.py`](../scripts/validate_civilizational_statecraft_public.py) |
| Staging output | [`public/civ-state/`](../public/civ-state/) |
| Legacy residue | [`artifacts/civilizational-statecraft-public/`](../artifacts/civilizational-statecraft-public/) — retired; do not refresh |

## Feedback loop

```text
edit public/civ-state/ in strategy-codex
  → commit workspace slice
  → python scripts/publish_public_civ_state.py -m "…" --push
  → tagged/public main on rbtkhn/civ-state
```

Review-only or workshop promotion may still use `statecraft/states/` and review packets; ship requires landing prose in `public/civ-state/` first. Optional bulk promotion: `export_civilizational_statecraft_public.py` writes transformed workshop copy into `public/civ-state/` (preserves `MIRROR-RECEIPT.md`).

## Merge triggers (hold until explicit — v0.1.3+)

These are **decision gates**, not automatic pipeline steps. See also [Unresolved tensions](../statecraft/states/volumes/README.md#unresolved-tensions-2026-06-15--hold-before-next-merge) in the volume map.

### When `statecraft-<civ>.md` prose may merge into Empire / introduction

Proceed **only when all** are true:

1. **Per-volume plan** — operator names target file(s) (`empire-*.md`, `introduction.md`, or both) for each civ; no repo-wide bulk merge in one commit.
2. **No third reader part** — merged prose does not reintroduce Part 3 / `statecraft-*` as a coequal chapter in [table-of-contents.md](../statecraft/states/table-of-contents.md), [reader-guide.md](../statecraft/states/reader-guide.md), or export `volume_essay_globs`.
3. **Shelf alignment** — volume shelf-readers and secondary-sources already route upward to empire/introduction (no `statecraft-*.md` links).
4. **Export gate unchanged** — `statecraft-*.md` stays **out** of public export and validator required essays unless manifest + boundary doc are updated in the **same** tagged release.
5. **Retire workshop file** — after merge, remove or archive `statecraft-<civ>.md` with a one-line pointer in the volume README (workshop residue labeled honestly).

**Do not merge** while ledes under volume introduction H1s are still thin placeholders and the operator has not chosen whether present-carrier judgment lives in **introduction** or **Empire**.

### When `archive/helix-lane-v1/legacy-cut/` may return to the public book

Proceed **only when all** are true:

1. **Operator intent** — explicit choice to restore helix-lane v1 cut for **external** readers (not only workshop salvage in [helix-salvage-matrix.md](civilizational-statecraft/helix-salvage-matrix.md)).
2. **Source path** — export manifest gains a documented copy source (e.g. import from civ-state tag **v0.1.2** `legacy-cut/`, or a workshop archive tree checked into strategy-codex); sanitize-only-on-existing-output is insufficient alone.
3. **Sanitize receipt** — `sanitize_legacy_archive` run recorded; forbidden-pattern lint PASS on restored tree.
4. **Stub README updated** — [archive/helix-lane-v1/README.md](../statecraft/states/export-templates/archive-helix-lane-v1-README.md) template reflects restore vs redirect policy.
5. **Tagged release** — public restore ships as a **minor** tag bump (e.g. v0.1.4), not silent drift inside a patch narrative.

**Default after v0.1.3:** keep **book-only** archive stub (`archive/helix-lane-v1/README.md` only). Absence of `legacy-cut` in export staging is export-source law, not accidental deletion.

## Related

- Unified public-artifact law: [public-artifacts-boundary.md](public-artifacts-boundary.md)
- PH boundary: [predictive-history-external-boundary.md](predictive-history-external-boundary.md)
- GitHub rename procedure: [civilizational-statecraft/GITHUB-RENAME-CIV-STATE.md](civilizational-statecraft/GITHUB-RENAME-CIV-STATE.md)
- Helix salvage: [civilizational-statecraft/helix-salvage-matrix.md](civilizational-statecraft/helix-salvage-matrix.md)
