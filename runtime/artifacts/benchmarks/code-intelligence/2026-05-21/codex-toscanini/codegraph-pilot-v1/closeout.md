# CodeGraph Pilot Benchmark Closeout

## Verdict

`Open`

## Why

This pass completed enough of the loop to be useful, but not enough to declare `Expand`, `Contain`, or `Retire`.

What held:

- CodeGraph is clearly helpful for **architecture packaging** once an export already exists.
- The Markdown export and bundle path are more compact and more traceable than the ordinary manual route for Task C.

What did not hold:

- The **impact-review** result was worse than the baseline lane because it under-reported likely dependents and tests.
- A **fresh local rerun** on this Windows setup failed twice, first on npm cache permissions and then on a spawned CodeGraph binary `EINVAL`.

That last point matters most. The benchmark protocol explicitly says repeated environment brittleness blocks a confident expansion decision. That is exactly what showed up here on May 21, 2026.

## Scorecard

| Task | Baseline | CodeGraph | Read |
|---|---|---|---|
| A. Architecture exploration | `usable`, about `3` minutes | `usable`, about `1` minute | CodeGraph is faster and easier to scan, but a bit noisier in symbol selection. |
| B. Impact review | `strong`, about `2` minutes | `weak`, about `1` minute | Baseline was more trustworthy because it surfaced the obvious tests and scripts. |
| C. Bundle prep | `weak`, about `4` minutes | `strong`, about `1` minute | CodeGraph bundle path is materially better when an export already exists. |

## Toscanini Read

The pilot currently behaves like a **good second movement attached to an unreliable first movement**.

- The export-to-bundle story is elegant.
- The fresh invocation story is still brittle.
- That makes this a promising toolchain component, but not yet a fully dependable operator path on this workstation.

## Next Action

Patch the Windows CodeGraph invocation so a fresh local export can be regenerated without `npx` spawn failures, then rerun the same three-task loop against the presentation service path.
