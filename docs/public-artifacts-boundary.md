# Public artifacts boundary

Compact law for **parallel public corpora** maintained outside strategy-codex canonical workshop trees.

## ph-civ

**Canonical home:** [`rbtkhn/ph-civ`](https://github.com/rbtkhn/ph-civ)

Predictive History public artifact (lectures, chapters, cards, routes, patterns). strategy-codex **observes only** — see [predictive-history-external-boundary.md](predictive-history-external-boundary.md).

## civ-state

**Canonical home:** [`rbtkhn/civ-state`](https://github.com/rbtkhn/civ-state) (renamed from `civ-emp`)

Civilizational Statecraft comparative book. strategy-codex drafts in `statecraft/states/` and **exports** — see [civilizational-statecraft-external-boundary.md](civilizational-statecraft-external-boundary.md).

## Zero cross-reference (locked)

Public **ph-civ** and public **civ-state** are **distinct**. Published surfaces **must not reference each other** — no URLs, IDs, bridge pages, or shared reader navigation.

Workshop may read both under their respective boundary rules. Export linter enforces ph-civ absence in civ-state public output.

## strategy-codex role

| Artifact | Draft | Publish |
|----------|-------|---------|
| ph-civ | never (observe / critique) | ph-civ repo only |
| civ-state | `statecraft/states/` | export → civ-state repo |
| statecraft ops | lanes, archive, synthesis | never wholesale |

## Export commands

```bash
python scripts/export_civilizational_statecraft_public.py
python scripts/validate_civilizational_statecraft_public.py
```
