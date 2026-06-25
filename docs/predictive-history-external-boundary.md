# Predictive History external boundary

**Canonical public repo:** [`rbtkhn/predictive-history`](https://github.com/rbtkhn/predictive-history) (formerly `ph-civ`).

It is the two-volume public artifact containing the `ph-civ` and `ph-apo` surfaces: public lecture transcripts, companion commentaries, cards, routes, and patterns. `rbtkhn/ph-workshop` is legacy workshop/import provenance unless the operator explicitly invokes that archive lane.

## Direct-edit model (current)

| Layer | Role |
|-------|------|
| **`rbtkhn/predictive-history`** | Author, validate, `git push` — sole corpus EXECUTE surface |
| **`public/predictive-history/`** in strategy-codex | **Inbound read-only snapshot** — refresh via `sync_predictive_history_mirror.py` + `[predictive-history-sync]` commit |
| **`codex/predictive-history/`** | Frozen workshop residue — read for intake only |

Operator workspace: [predictive-history-operator-workspace.md](predictive-history-operator-workspace.md).

**Deprecated:** staging mirror → `publish_public_ph_civ.py --push`. That script now exits with an error.

[`MIRROR-RECEIPT.md`](../public/predictive-history/MIRROR-RECEIPT.md) pins the last **synced** upstream SHA.

## Canonical rule

`strategy-codex` must not create, update, regenerate, or maintain Predictive History corpus or manuscript content under:

- `codex/predictive-history/`
- `research/external/youtube-channels/predictive-history/`
- **`public/predictive-history/`** except inbound sync (see [DO-NOT-EDIT.md](../public/predictive-history/DO-NOT-EDIT.md))

Those residue trees remain **frozen migration / historical reference** or **read-only mirror**.

## What belongs here

Allowed Predictive History work inside `strategy-codex`:

- **inbound sync** of `public/predictive-history/` from upstream
- boundary doctrine and migration notices
- review packet templates and analysis prompts
- source-discipline critique
- structure/editorial feedback
- strategy commentary about externally supplied PH material
- public `ph-civ` ID references (`source_id`, `pattern_id`, route IDs, `essay-NN`)

## What does not belong here

Disallowed:

- editing lecture bodies, essays, book architecture, queues, registries, or corpus metadata under **`public/predictive-history/`**
- treating a normal strategy-codex commit as having updated the public repo
- using **`publish_public_ph_civ.py`**
- silently patching PH from residue paths

## Feedback loop

```text
edit rbtkhn/predictive-history (PREDICTIVE_HISTORY_ROOT)
  → git commit + git push
  → python scripts/sync_predictive_history_mirror.py
  → strategy-codex commit [predictive-history-sync]
```

Review-only feedback may use pasted diff, excerpt, or public ID reference — strategy-codex returns critique only; it does not patch the external project except via inbound sync.

Handoff summary: [predictive-history-boundary-handoff.md](predictive-history-boundary-handoff.md).
