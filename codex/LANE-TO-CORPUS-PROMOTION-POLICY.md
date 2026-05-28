# Lane-To-Corpus Promotion Policy

WORK only; not Record.

## Canonical rule

Strategy-codex now uses a strict split:

- [`codex/speakers/`](C:/dev/strategy-codex/codex/speakers) is the canonical home for every recurring person lane, including hosts.
- [`source-archive/statecraft/`](C:/dev/strategy-codex/source-archive/statecraft) is the dated provenance layer.

Do not treat `codex/years/2026/<person>/` as a live notebook lane model. That pattern is retired.

## Default model

The default pattern is:

- person shelf in `codex/speakers/<name>/`
- source capture in `source-archive/statecraft/YYYY-MM-DD/`
- host-local guest transformations owned by the host shelf, typically under `codex/speakers/<host>/stream/`

## Promotion question

The promotion decision is no longer "should this person get a year-lane?"

The real question is:

- should the person remain a lightweight speaker shelf over shared raw-input
- or should the person gain a richer speaker-owned corpus inside `codex/speakers/<name>/stream/`
- or, in rarer cases, should work also justify a dedicated external research corpus outside the speaker shelf

## Promote within `codex/speakers` when

A speaker should gain richer `stream/` structure when most of the payoff comes from continuity rather than single captures:

- sustained source volume
- repeated reuse in notebook work
- recurring host transformations worth preserving
- chronology or quote pressure that a thin route map no longer handles well
- clear savings from lane-specific manifests, ledgers, shelves, or cross-host notes

## Do not promote just because

These are not enough by themselves:

- importance or popularity
- one strong week or month
- a burst of raw-input activity
- the fact that another speaker already has a richer shelf

## External corpus threshold

Move beyond `codex/speakers/<name>/` only when the work clearly needs a separate research world with its own maintenance burden, such as:

- dedicated source registries
- heavy quote-bank discipline
- prediction tracking
- evidence packs
- project-scale analysis that would clutter the shared strategy shelf

Promotion is a workflow decision, not a prestige decision.
