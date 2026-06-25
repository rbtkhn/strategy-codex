# Public mirrors

Repo-root folders for **parallel public book artifacts**.

| Mirror | Remote | strategy-codex path | Model |
|--------|--------|-------------------|--------|
| Predictive History | [`rbtkhn/predictive-history`](https://github.com/rbtkhn/predictive-history) | [predictive-history/](predictive-history/) | **Direct-edit upstream**; inbound snapshot here |
| Civilizational Statecraft | [`rbtkhn/civ-state`](https://github.com/rbtkhn/civ-state) | [civ-state/](civ-state/) | Staging mirror + publish script |

Boundary law: [docs/public-artifacts-boundary.md](../docs/public-artifacts-boundary.md)

## Membrane (predictive-history ⊥ civ-state)

- **Sibling folders only** — no cross-links or shared navigation between the two trees.
- **Workshop promotion** (`statecraft/states/ph-civ-to-civ-state-bridge.md`) is internal operator routing — not a public-tree pipe.

## Predictive History (inbound snapshot)

**Do not edit corpus under `public/predictive-history/`.** See [DO-NOT-EDIT.md](predictive-history/DO-NOT-EDIT.md).

```powershell
# Author in canonical clone (PREDICTIVE_HISTORY_ROOT), then:
python scripts/sync_predictive_history_mirror.py
git commit -m "[predictive-history-sync] inbound mirror refresh"
```

Operator guide: [docs/predictive-history-operator-workspace.md](../docs/predictive-history-operator-workspace.md)

Sync check: `python scripts/check_academy_mirror_sync.py --mirror predictive-history`

## civ-state (staging mirror)

```powershell
python scripts/sync_public_civ_state_mirror.py
python scripts/publish_public_civ_state.py -m "your message" --push
```

Default publish clone: `C:\dev\civ-state` (`CIV_STATE_PUBLISH_CLONE`).

Full boundary: [docs/civilizational-statecraft-external-boundary.md](../docs/civilizational-statecraft-external-boundary.md)
