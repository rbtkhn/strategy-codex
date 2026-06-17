# Predictive History external boundary

`rbtkhn/ph-civ` is the canonical public Predictive History repository.

It is the two-volume public artifact containing the `ph-civ`, `ph-apo`, and `ph-mus` surfaces: public lecture transcripts, companion commentaries, cards, routes, patterns, and museum manifests. `rbtkhn/ph-workshop` is legacy workshop/import provenance unless the operator explicitly invokes that archive lane.

Inside `strategy-codex`, Predictive History corpus work uses a **staging mirror → explicit publish** loop:

- **edit** only under [`public/ph-civ/`](../public/ph-civ/) (vendored workspace copy)
- **pull inbound** with `python scripts/sync_public_ph_civ_mirror.py`
- **publish outbound** with `python scripts/publish_public_ph_civ.py -m "…" --push` (no automatic push from strategy-codex commits)

Legacy residue trees remain **frozen** (no canonical edits):

- `codex/predictive-history/`
- `research/external/youtube-channels/predictive-history/`

Observation, critique, review packets, and citation of public `ph-civ` IDs elsewhere in strategy-codex remain allowed.

## Canonical rule

`strategy-codex` must not create, update, regenerate, or maintain Predictive History corpus or manuscript content under:

- `codex/predictive-history/`
- `research/external/youtube-channels/predictive-history/`

Those trees remain in this repo only as **frozen migration residue / historical reference**. The public reader artifact now lives in the external `ph-civ` repo.

## What belongs here

Allowed Predictive History work inside `strategy-codex`:

- **corpus edits** under `public/ph-civ/` only (staging mirror)
- **publish** to [`rbtkhn/ph-civ`](https://github.com/rbtkhn/ph-civ) only via `scripts/publish_public_ph_civ.py --push`
- boundary doctrine and migration notices
- review packet templates and analysis prompts
- source-discipline critique
- structure/editorial feedback
- strategy commentary about externally supplied PH material
- public `ph-civ` ID references, such as `source_id`, `pattern_id`, and route IDs

## What does not belong here

Disallowed Predictive History work inside `strategy-codex` includes:

- editing lecture bodies, book architecture, queues, registries, or corpus metadata **outside** `public/ph-civ/`
- treating a normal strategy-codex commit as having updated the public repo (without `publish_public_ph_civ.py --push`)
- regenerating PH renders or dashboards for canonical use outside the publish loop
- refreshing legacy local PH trees as if this repo still owned the ingest lane
- treating `codex/predictive-history/` as a live work surface
- silently patching `ph-civ` from residue paths other than `public/ph-civ/`

## Feedback loop

```text
edit public/ph-civ/ in strategy-codex
  → commit workspace slice
  → python scripts/publish_public_ph_civ.py -m "…" --push
  → tagged/public main on rbtkhn/ph-civ
```

Review-only feedback (no corpus edit) may still use a **review packet**:

- pasted diff
- pasted excerpt
- file snapshot
- bounded artifact bundle with source links
- public `ph-civ` ID or route reference

`strategy-codex` may then return:

- editorial critique
- structure feedback
- source-discipline notes
- strategy/notebook commentary

It may not patch the external project except through `public/ph-civ/` + `publish_public_ph_civ.py`.

For a compact operator/public handoff summary of the boundary shift, see [predictive-history-boundary-handoff.md](predictive-history-boundary-handoff.md).
