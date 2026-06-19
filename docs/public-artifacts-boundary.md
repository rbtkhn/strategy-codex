# Public artifacts boundary

Compact law for **parallel public corpora** and their **`public/` staging mirrors**.

Both mirrors use the same workspace loop: **edit in `public/<artifact>/` → commit in strategy-codex → explicit publish script → public GitHub repo**.

## ph-civ

**Canonical home:** [`rbtkhn/ph-civ`](https://github.com/rbtkhn/ph-civ)

Predictive History public artifact (lectures, chapters, cards, routes, patterns).

**Workspace edit surface:** [`public/ph-civ/`](../public/ph-civ/) only.

**Pull:** `python scripts/sync_public_ph_civ_mirror.py`

**Ship:** `python scripts/publish_public_ph_civ.py -m "…" --push`

Full boundary: [predictive-history-external-boundary.md](predictive-history-external-boundary.md)

## civ-state

**Canonical home:** [`rbtkhn/civ-state`](https://github.com/rbtkhn/civ-state) (renamed from `civ-emp`)

Civilizational Statecraft comparative book (five volumes + appendix).

**Workspace edit surface:** [`public/civ-state/`](../public/civ-state/) only — same role as `public/ph-civ/`.

**Pull:** `python scripts/sync_public_civ_state_mirror.py`

**Ship:** `python scripts/publish_public_civ_state.py -m "…" --push`

**Not the public edit surface:** anything outside `public/civ-state/` for ship-bound prose — including `statecraft/states/`, which is operator statecraft substrate, **not** an upstream or workshop layer for the public book.

Full boundary: [civilizational-statecraft-external-boundary.md](civilizational-statecraft-external-boundary.md)

## Membrane at `public/` (ph-civ ⊥ civ-state)

| Rule | Detail |
|------|--------|
| **Orthogonal artifacts** | Two public books, two remotes, two staging folders |
| **Zero cross-reference (published)** | No URLs, PH IDs, bridge pages, or shared reader navigation in shipped civ-state copy |
| **No folder bridge** | Nothing under `public/ph-civ/` links into `public/civ-state/` (or reverse) in reader-facing ship |
| **Operator bridges stay internal** | `ph-civ-to-civ-state-bridge.md`, promotion ledger — operator routing only; **not** a public-tree pipe |
| **Symmetric edit law** | Each corpus edited only in its own `public/<artifact>/` tree |

## strategy-codex role

| Artifact | Public edit surface | Publish |
|----------|---------------------|---------|
| ph-civ | `public/ph-civ/` | `publish_public_ph_civ.py --push` |
| civ-state | `public/civ-state/` | `publish_public_civ_state.py --push` |
| statecraft operator | `statecraft/states/` (non-ship; separate from public civ-state) | — |
| statecraft ops | lanes, archive, synthesis | never wholesale |

## Commands

**ph-civ (live)**

```powershell
python scripts/sync_public_ph_civ_mirror.py
python scripts/publish_public_ph_civ.py -m "…" --push
python scripts/check_academy_mirror_sync.py
```

**civ-state (live)**

```powershell
python scripts/sync_public_civ_state_mirror.py
python scripts/validate_civilizational_statecraft_public.py public/civ-state
python scripts/publish_public_civ_state.py -m "…" --push
python scripts/check_academy_mirror_sync.py --mirror civ-state
```

Legacy `export_civilizational_statecraft_public.py` is migration/reshape residue only — not daily edit. Legacy bucket `runtime/artifacts/civilizational-statecraft-public/` is retired — see [README-STAGING.md](../runtime/artifacts/civilizational-statecraft-public/README-STAGING.md).

## Related

- Staging index: [public/README.md](../public/README.md)
- PH boundary: [predictive-history-external-boundary.md](predictive-history-external-boundary.md)
- CIV-STATE boundary: [civilizational-statecraft-external-boundary.md](civilizational-statecraft-external-boundary.md)
