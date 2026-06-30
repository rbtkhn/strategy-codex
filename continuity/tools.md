# continuity/ — tools
<!-- word_count: 179 -->

Script-maintained utilities and local operator tooling for the continuity layer.

## Word counts

Many markdown files carry `word_count:` in YAML or `<!-- word_count: N -->` after the first heading.

Maintained by:

```bash
python3 scripts/strategy/update_strategy_notebook_word_counts.py
python3 scripts/strategy/update_strategy_notebook_word_counts.py --check
python3 scripts/strategy/update_strategy_notebook_word_counts.py --dry-run
```

Do not hand-edit counts. Large `source-archive/statecraft/YYYY-MM-DD/` captures are skipped.

## Derived session wrapper

Optional: [STRATEGY-RUN-OPERATOR.md](../docs/skill-work/work-strategy/STRATEGY-RUN-OPERATOR.md) — `run_id` + `state.json` under `artifacts/`. Trace contract: [STRATEGY-NOTEBOOK-TRACE-CONTRACT.md](STRATEGY-NOTEBOOK-TRACE-CONTRACT.md).

## Workbench visualizer (WORK-only)

Static structure map: [demo-runs/workbench-visualizer/README.md](demo-runs/workbench-visualizer/README.md). Part of [work-dev Workbench](../docs/skill-work/work-dev/workbench/README.md).

## Derived interface artifacts

Strategy-codex is markdown-canonical with derived orientation surfaces (WORK-only, non-canonical unless promoted). Judgment remains in `strategy-page` blocks and `days.md`.

## Search (`rg`)

Prefer `rg` for file search. On Windows, if WindowsApps `rg.exe` is blocked, use workspace-local [`.codex-tmp/rg.exe`](../.codex-tmp/rg.exe).

## Python runtime

Preferred bundled runtime (operator machine):

`C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`

See also legacy pointer [tools.md](tools.md) if present.

## Validation scripts

| Script | Purpose |
|--------|---------|
| `scripts/check_continuity_status.py` | STATUS.md freshness |
| `scripts/check_text_encoding_hygiene.py --scope continuity --warn` | Mojibake scan |
| `scripts/validate_strategy_pages.py` | strategy-page fences |
| `scripts/validate_strategy_expert_threads.py` | Thread month segments |
| `scripts/validate_expert_predictions.py` | Predictions ledger |

## Continuity report (derived)

```bash
python3 scripts/build_continuity_report.py          # Markdown to stdout
python3 scripts/build_continuity_report.py --json   # JSON to stdout
python3 scripts/build_continuity_report.py --write  # write runtime/artifacts/
```

Default mode is read-only observability. Use `--write` to persist under `runtime/artifacts/` — not authority.
