# Lane-To-Corpus Promotion Policy
<!-- word_count: 334 -->


## Canonical rule

Strategy-codex now uses a strict split:

- [`statecraft/voices/`](../statecraft/voices) is the canonical home for whole-analyst continuity shelves.
- [`statecraft/channels/`](../statecraft/channels) is the canonical home for host-family continuity (Davis, Napolitano, Nima, …).
- [`source-archive/statecraft/`](../statecraft) is the dated provenance layer.

Legacy **`continuity/speakers/`** is terminated — [codex-speakers-deprecated.md](../docs/archive/codex-speakers-deprecated.md).

Do not treat `continuity/years/2026/<person>/` as a live notebook lane model. That pattern is retired.

## Default model

The default pattern is:

- analyst shelf in `statecraft/voices/<name>/`
- host-family shelf in `statecraft/channels/<host>/` when guest-on-host law applies
- source capture in `source-archive/statecraft/YYYY-MM-DD/`
- host-local guest transformations owned by the channel shelf as flat files (e.g. `davis-<guest>-speaker-arc.md`)

## Promotion question

The promotion decision is no longer "should this person get a year-lane?"

The real question is:

- should the person remain a lightweight speaker shelf over shared archive captures
- or should the person gain a richer speaker-owned corpus inside `statecraft/voices/<name>/`
- or, in rarer cases, should work also justify a dedicated external research corpus outside the speaker shelf

## Promote within `statecraft/voices` when

A speaker should gain richer flat-shelf structure when most of the payoff comes from continuity rather than single captures:

- sustained source volume
- repeated reuse in notebook work
- recurring host transformations worth preserving (route guest arcs as flat files under `statecraft/channels/<host>/`)
- chronology or quote pressure that a thin route map no longer handles well
- clear savings from lane-specific manifests, ledgers, shelves, or cross-host notes

## Do not promote just because

These are not enough by themselves:

- importance or popularity
- one strong week or month
- a burst of archive activity
- the fact that another speaker already has a richer shelf

## External corpus threshold

Move beyond `statecraft/voices/<name>/` only when the work clearly needs a separate research world with its own maintenance burden, such as:

- dedicated source registries
- heavy quote-bank discipline
- prediction tracking
- evidence packs
- project-scale analysis that would clutter the shared strategy shelf

Promotion is a workflow decision, not a prestige decision.
