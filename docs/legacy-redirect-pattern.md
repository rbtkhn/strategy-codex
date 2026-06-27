# Legacy Redirect Pattern

work only; not Record.

Use this pattern when a legacy surface still has inbound link value, but no longer owns the canonical content.

## Core Rule

When a real canonical home exists elsewhere, the legacy surface should degrade into a **thin compatibility layer**, not a shadow owner.

That usually means:

- keep the old path alive
- state clearly that it is no longer canonical
- point directly to the canonical home
- explain the remaining value of the legacy path, if any
- stop extending doctrine there

## What A Good Legacy Redirect Should Do

A good redirect surface should answer four questions quickly:

1. what is this path now?
2. where is the canonical home?
3. why does this old path still exist?
4. what should the operator do next?

If it cannot answer those in a few lines, it is probably still trying to own too much.

## What A Legacy Redirect Should Not Do

Do not let a legacy surface:

- keep restating the full doctrine after ownership has moved
- behave like a second canonical shelf
- accumulate fresh conceptual mass after re-homing
- force the operator to compare two equal-looking owners

## Preferred Shapes

The best shape depends on what remains useful:

- **single-file redirect**
  Use when the old file only needs to preserve links.
- **compatibility README**
  Use when a whole folder still needs re-entry guidance.
- **legacy lane shell**
  Use when a larger surface still contains unmigrated residue, but should no longer be mistaken for the live owner.

## Live Examples

- [docs/skill-work/work-strategy/interpretive-machine-lineage.md](skill-work/work-strategy/interpretive-machine-lineage.md)
- [docs/skill-work/work-strategy/interpretive-machine-corporate-applications.md](skill-work/work-strategy/interpretive-machine-corporate-applications.md)
- [docs/skill-work/work-strategy/interpretive-machine-workflow-manifestations.md](skill-work/work-strategy/interpretive-machine-workflow-manifestations.md)

These work because they no longer pretend to be doctrine owners. They preserve the old path, name the new canonical home, and get out of the way.

## Best Short Rule

Use this compression:

```text
when ownership moves,
the old path should preserve access without preserving ambiguity
```

## Return Path

- Return to [docs/prose-index.md](prose-index.md) for prose-class routing.
- Return to [docs/prose-cluster-placement-comparison.md](prose-cluster-placement-comparison.md) for the live placement comparison.
