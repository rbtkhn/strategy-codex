# Code-Intelligence Benchmarks

**Status:** work-layer benchmark bucket. Not Record. Not EVIDENCE.

This folder stores benchmark runs for local code-intelligence tools used inside `strategy-codex`.

Current use:

- CodeGraph pilot expand / contain / retire loops

Recommended layout:

```text
runtime/artifacts/benchmarks/code-intelligence/YYYY-MM-DD/<runner>/codegraph-pilot-v1/
```

Typical contents:

- `metadata.json`
- `baseline-notes.md`
- `codegraph-notes.md`
- `closeout.md`

Keep this bucket narrow. It is for local workflow calibration, not broad public benchmark claims and not a substitute for the actual implementation docs.

