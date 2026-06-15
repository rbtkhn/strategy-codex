# Civilizational Statecraft external boundary

`rbtkhn/civ-state` is the canonical **public Civilizational Statecraft** book.

It is the standalone comparative artifact: two-volume whole work, five civilization-state volumes, source-lattice per volume, framework, comparative sheets, and sacred-grammar library. Inside `strategy-codex`, Civilizational Statecraft is an **external published book** after cutover:

- observation allowed
- critique allowed
- review packets allowed
- citation of **civ-state** public chapter slugs allowed
- mutation of the public book from local workshop residue **disallowed** without export

## Canonical rule

After cutover, `strategy-codex` must not treat `statecraft/states/` as the canonical public book. Public canonical text lives in **`rbtkhn/civ-state`** only.

Workshop drafting in `statecraft/states/` continues. Publishing happens only through:

```text
local draft → export script → public repo PR → tagged release
```

## ph-civ ⊥ civ-state (locked)

**`ph-civ` and `civ-state` are distinct public artifacts.** They **must not reference each other** in published civ-state copy:

- no cross-repo URLs or footnotes
- no bridge pages or shared navigation
- no PH chapter / pattern IDs in public shelves or apparatus

strategy-codex **observes** [`rbtkhn/ph-civ`](https://github.com/rbtkhn/ph-civ) per [predictive-history-external-boundary.md](predictive-history-external-boundary.md). Internal workshop files such as [`ph-civ-promotion-ledger.md`](../statecraft/states/ph-civ-promotion-ledger.md) and [`ph-civ-to-civ-state-bridge.md`](../statecraft/states/ph-civ-to-civ-state-bridge.md) are **not exported**.

## What belongs in strategy-codex

Allowed Civilizational Statecraft work inside `strategy-codex`:

- draft and deepen `statecraft/states/` (volumes, lattice, framework, comparative)
- run `scripts/export_civilizational_statecraft_public.py`
- run `scripts/validate_civilizational_statecraft_public.py`
- critique public `civ-state` PRs and issues
- cite public civ-state slugs in review packets and operator copy

## What does not belong in strategy-codex (as public canonical)

Disallowed after cutover:

- treating local `statecraft/states/` edits as silently updating the public book
- patching `rbtkhn/civ-state` from local residue without export receipt
- embedding ph-civ links in export output (export linter fails)

## Export surfaces

| Asset | Path |
|-------|------|
| Export manifest | [`config/civilizational_statecraft_public_export.yaml`](../config/civilizational_statecraft_public_export.yaml) |
| Export script | [`scripts/export_civilizational_statecraft_public.py`](../scripts/export_civilizational_statecraft_public.py) |
| Validator | [`scripts/validate_civilizational_statecraft_public.py`](../scripts/validate_civilizational_statecraft_public.py) |
| Staging output | [`artifacts/civilizational-statecraft-public/`](../artifacts/civilizational-statecraft-public/) |

## Feedback loop

```text
public issue / PR on rbtkhn/civ-state
  → strategy-codex review packet
  → local draft in statecraft/states/
  → export + validate
  → public PR + tag (e.g. v0.1.1)
```

## Related

- Unified public-artifact law: [public-artifacts-boundary.md](public-artifacts-boundary.md)
- PH boundary: [predictive-history-external-boundary.md](predictive-history-external-boundary.md)
- GitHub rename procedure: [civilizational-statecraft/GITHUB-RENAME-CIV-STATE.md](civilizational-statecraft/GITHUB-RENAME-CIV-STATE.md)
- Helix salvage: [civilizational-statecraft/helix-salvage-matrix.md](civilizational-statecraft/helix-salvage-matrix.md)
