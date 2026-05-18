# Predictive History external boundary

`rbtkhn/ph-civ` is the canonical public Predictive History repository.

It is the two-volume public artifact containing the `ph-civ`, `ph-apo`, and `ph-mus` surfaces: public lecture transcripts, companion commentaries, cards, routes, patterns, and museum manifests. `rbtkhn/ph-workshop` is legacy workshop/import provenance unless the operator explicitly invokes that archive lane.

Inside `strategy-codex`, Predictive History is now an **external observed public project**:

- observation allowed
- critique allowed
- review packets allowed
- citation of public `ph-civ` IDs allowed
- mutation disallowed

## Canonical rule

`strategy-codex` must not create, update, regenerate, or maintain Predictive History corpus or manuscript content under:

- `codex/predictive-history/`
- `research/external/youtube-channels/predictive-history/`

Those trees remain in this repo only as **frozen migration residue / historical reference**. The public reader artifact now lives in the external `ph-civ` repo.

## What belongs here

Allowed Predictive History work inside `strategy-codex` is limited to:

- boundary doctrine and migration notices
- review packet templates and analysis prompts
- source-discipline critique
- structure/editorial feedback
- strategy commentary about externally supplied PH material
- public `ph-civ` ID references, such as `source_id`, `pattern_id`, and route IDs

## What does not belong here

Disallowed Predictive History work inside `strategy-codex` includes:

- editing lecture bodies, book architecture, queues, registries, or corpus metadata as canonical work
- regenerating PH renders or dashboards for canonical use
- refreshing the local PH transcript snapshot as if this repo still owned the ingest lane
- treating `codex/predictive-history/` as a live work surface
- silently patching `ph-civ` from local residue paths

## Feedback loop

The standard interface from Predictive History into `strategy-codex` is a **review packet**:

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

It may not patch the external project from here.

For a compact operator/public handoff summary of the boundary shift, see [predictive-history-boundary-handoff.md](predictive-history-boundary-handoff.md).
