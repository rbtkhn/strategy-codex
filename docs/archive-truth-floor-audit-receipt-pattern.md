# Archive Truth-Floor Audit Receipt Pattern

work only; not Record.

Use this when a bounded archive repair family needs a receipt shape that proves
what changed without pretending to solve the whole archive at once.

## Pattern

The clean shape is:

```text
before -> repair -> after -> remainder
```

## What Each Step Does

### 1. `before`

Show the pre-repair audit artifact.

Its job is to answer:

```text
what was actually wrong,
how large was the family,
and what evidence justified opening the pass?
```

### 2. `repair`

Apply only the bounded fix family that the audit actually proved.

Do not widen the pass just because adjacent noise becomes visible.

### 3. `after`

Show the post-repair audit artifact.

Its job is to answer:

```text
did the family actually collapse,
or did the repair only reduce noise without resolving the object?
```

### 4. `remainder`

Name what is still left and what kind of thing it is.

The remainder should resolve into one of three outcomes:

- zero remainder
- explicitly reviewed exception
- next tranche opening

## Hormuz Example

The `Hormuz` pass now provides the canonical example:

- before: [statecraft-hormuz-audit-current.md](/C:/dev/strategy-codex/runtime/artifacts/transcript-audits/statecraft-hormuz-audit-current.md)
- after: [statecraft-hormuz-audit-postfix-reviewed.md](/C:/dev/strategy-codex/runtime/artifacts/transcript-audits/statecraft-hormuz-audit-postfix-reviewed.md)
- remainder: zero actionable findings after one reviewed title-body divergence was localized and closed

## Stopping Rule

```text
if the remainder is zero or explicitly reviewed,
close the family and advance the tranche boundary
```

## Anti-Pattern

Do not end a bounded archive repair pass with:

- a vague claim that things are cleaner now
- no post-repair artifact
- an unnamed remainder
- a silent slide into the next repair family

That turns a governed repair pass back into accumulation-shaped cleanup.

## Best Sentence

```text
prove one repair family closed, then let the remainder decide the next opening
```
