# Public artifacts boundary

Compact law for **parallel public corpora** and their **`public/` mirror folders**.

## predictive-history (Predictive History)

**Canonical home:** [`rbtkhn/predictive-history`](https://github.com/rbtkhn/predictive-history)

Predictive History public artifact (lectures, essays, chapters, cards, routes, patterns).

**strategy-codex mirror:** [`public/predictive-history/`](../public/predictive-history/) — **inbound read-only**.

**Author / ship:** edit and `git push` in **`PREDICTIVE_HISTORY_ROOT`** (canonical clone).

**Refresh mirror:** `python scripts/sync_predictive_history_mirror.py` → commit **`[predictive-history-sync]`**

Full boundary: [predictive-history-external-boundary.md](predictive-history-external-boundary.md) · [predictive-history-operator-workspace.md](predictive-history-operator-workspace.md)

## civ-state

**Canonical home:** [`rbtkhn/civ-state`](https://github.com/rbtkhn/civ-state)

Civilizational Statecraft comparative book (five volumes + appendix).

**Workspace edit surface:** [`public/civ-state/`](../public/civ-state/) — staging mirror + publish loop.

**Pull:** `python scripts/sync_public_civ_state_mirror.py`

**Ship:** `python scripts/publish_public_civ_state.py -m "…" --push`

Full boundary: [civilizational-statecraft-external-boundary.md](civilizational-statecraft-external-boundary.md)

## Membrane at `public/` (predictive-history ⊥ civ-state)

| Rule | Detail |
|------|--------|
| **Orthogonal artifacts** | Two public books, two remotes, two folders |
| **Zero cross-reference (published)** | No URLs, PH IDs, bridge pages, or shared reader navigation in shipped civ-state copy |
| **No folder bridge** | Nothing under `public/predictive-history/` links into `public/civ-state/` (or reverse) in reader-facing ship |
| **Operator bridges stay internal** | `ph-civ-to-civ-state-bridge.md`, promotion ledger — operator routing only |
| **Asymmetric edit law** | PH: direct-edit upstream + inbound sync; civ-state: edit `public/civ-state/` + publish script |

## strategy-codex role

| Artifact | Public surface in strategy-codex | Ship |
|----------|----------------------------------|------|
| Predictive History | `public/predictive-history/` (read-only) | push canonical repo; sync mirror |
| civ-state | `public/civ-state/` (staging) | `publish_public_civ_state.py --push` |
| statecraft operator | `statecraft/states/` (non-ship) | — |

## Commands

**Predictive History**

```powershell
# in PREDICTIVE_HISTORY_ROOT
ph-civ validate
git push origin main

# refresh strategy-codex snapshot
python scripts/sync_predictive_history_mirror.py
python scripts/check_academy_mirror_sync.py --mirror predictive-history
```

**civ-state**

```powershell
python scripts/sync_public_civ_state_mirror.py
python scripts/publish_public_civ_state.py -m "…" --push
python scripts/check_academy_mirror_sync.py --mirror civ-state
```

## Related

- Staging index: [public/README.md](../public/README.md)
- PH operator workspace: [predictive-history-operator-workspace.md](predictive-history-operator-workspace.md)
