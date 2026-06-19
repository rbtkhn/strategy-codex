# Polyphonic Cognition Streams

WORK-only notebook artifact produced by [`scripts/build_two_pillar_notebook_graph.py`](../../../../scripts/build_two_pillar_notebook_graph.py).
The script keeps a legacy name for compatibility, but it now emits a count-neutral polyphonic cognition-stream graph.

The current lattice has eight streams, but the file names and schema language avoid baking in the count because the stream set may change later.

## Outputs

| Artifact | Path |
|----------|------|
| JSON graph | `runtime/artifacts/skill-work/work-strategy/interview-graph/cognition-streams-graph.json` |
| Markdown companion | `runtime/artifacts/skill-work/work-strategy/interview-graph/cognition-streams-graph.md` |

## Scope

- Current cognition streams:
  - `Alkorshid` (`alkorshid`) -> `Synthesis`
  - `Diesen` (`diesen`) -> `Order`
  - `Davis` (`davis`) -> `Conflict`
  - `Mercouris` (`mercouris_duran`) -> `Statecraft`
  - `Crooke` (`crooke`) -> `Process`
  - `Parsi` (`parsi`) -> `Scope`
  - `Pape` (`pape`) -> `Escalation`
  - `Ritter` (`ritter`) -> `Mechanics`
- Public labels use last names; source/channel provenance stays in source notes and JSON metadata.
- Default analytical posture is contrapuntal comparison: harmonies, tensions, bridges, and differences without forced synthesis.
- One-year window first: `2025-05-01` through `2026-05-01`.
- Canonical episode node: YouTube URL.
- Conservative guest normalization with aliases preserved separately.
- Cross-stream bridges only for shared guests.
- Themes stay at episode level in the first pass.
- The Mercouris stream keeps `Alex Christoforou` as a cohost node, not a guest.
- Some Mercouris items fall back to deterministic provisional source URLs when the raw-input corpus does not expose a canonical link.
- Future daily stream input automation is a target, but this artifact does not implement schedulers, crawlers, or automatic notebook mutation.

## Deprecated Compatibility

Legacy `four-pillar-notebook-graph.*` artifact names are deprecated. Keep them only as compatibility aliases if an older notebook path still depends on them.

## Rebuild

```bash
python3 scripts/build_two_pillar_notebook_graph.py
```

## Corpus Path

The graph reads shared raw input from `codex/years/2026/raw-input/` by default. First-class stream shelves live under `codex/years/2026/<author>/`; `codex/experts/` is a deprecated compatibility pointer.

