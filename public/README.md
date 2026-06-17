# Public mirrors

Repo-root staging for **parallel public book mirrors**. Corpus that ships to GitHub is edited **only** under these paths; each mirror has its own publish gate.

| Mirror | Remote | Workspace path | Inbound (pull) | Outbound (publish) |
|--------|--------|----------------|----------------|---------------------|
| Predictive History (`ph-civ`) | [`rbtkhn/ph-civ`](https://github.com/rbtkhn/ph-civ) | [ph-civ/](ph-civ/) | `python scripts/sync_public_ph_civ_mirror.py` | `python scripts/publish_public_ph_civ.py -m "…" --push` |
| Civilizational Statecraft (`civ-state`) | [`rbtkhn/civ-state`](https://github.com/rbtkhn/civ-state) | [civ-state/](civ-state/) | `python scripts/sync_public_civ_state_mirror.py` | `python scripts/publish_public_civ_state.py -m "…" --push` |

Sync check: `python scripts/check_academy_mirror_sync.py --mirror ph-civ` · `python scripts/check_academy_mirror_sync.py --mirror civ-state`

Boundary law: [docs/public-artifacts-boundary.md](../docs/public-artifacts-boundary.md)

## Membrane (ph-civ ⊥ civ-state)

- **Sibling folders only** — no cross-links, bridge pages, or shared navigation between `public/ph-civ/` and `public/civ-state/`.
- **Published copy** on GitHub must stay orthogonal (civ-state ship path must not embed `ph-civ` URLs or IDs).
- **Workshop promotion** (`statecraft/states/ph-civ-to-civ-state-bridge.md`) is one-way mechanism transfer into operator memory — not a substitute for editing either public tree.

## Shared discipline (both mirrors)

1. **Edit** public corpus only under `public/ph-civ/` or `public/civ-state/` — not legacy residue trees, not scattered workshop paths for ship-bound prose.
2. **Commit** the workspace slice in strategy-codex when ready.
3. **Publish** upstream only via that mirror’s explicit publish script with `--push` (no automatic push from a normal commit).
4. **Pull** upstream with that mirror’s sync script when reconciling against remote `main`.

### ph-civ (live)

```powershell
python scripts/sync_public_ph_civ_mirror.py
python scripts/publish_public_ph_civ.py -m "your message" --push
```

Default publish clone: `C:\dev\ph-civ` (`PH_CIV_PUBLISH_CLONE` / `--clone-dir`).

### civ-state

```powershell
python scripts/sync_public_civ_state_mirror.py
python scripts/publish_public_civ_state.py -m "your message" --push
```

Default publish clone: `C:\dev\civ-state` (`CIV_STATE_PUBLISH_CLONE` / `--clone-dir`).

Full boundary: [docs/civilizational-statecraft-external-boundary.md](../docs/civilizational-statecraft-external-boundary.md)
