# Contributing

This repository is **strategy-codex** — a **governed interpretive machine** for statecraft and singularity operator work. External contributions are welcome for **code and docs**.

Grace-Mar is archived/frozen. Active strategy-codex work does not grow the fork. See [docs/archive/grace-mar.md](docs/archive/grace-mar.md).

**Filename conventions:** [docs/naming-convention.md](docs/naming-convention.md) (lowercase docs, reserved `AGENTS.md`, OpenClaw export path).

## Before you start

1. Read [docs/start-here.md](docs/start-here.md) and [AGENTS.md](AGENTS.md) — slim always-on contract; extended rules in [docs/agent-rules/deep-rules.md](docs/agent-rules/deep-rules.md).
2. Canonical on-disk paths: [docs/canonical-paths.md](docs/canonical-paths.md).
3. **Public-facing tone:** [docs/contributing-public-copy.md](docs/contributing-public-copy.md).

## Choose your change type

| If you are changing… | Checklist |
|---|---|
| Docs / doctrine | [docs/contributors/docs.md](docs/contributors/docs.md) |
| Python scripts | [docs/contributors/scripts.md](docs/contributors/scripts.md) |
| Source archive captures | [docs/contributors/source-archive.md](docs/contributors/source-archive.md) |
| Essays / notes / prose | [docs/contributors/essays.md](docs/contributors/essays.md) |
| Generated indexes / routing output | [docs/contributors/generated.md](docs/contributors/generated.md) |
| Archive / Grace-Mar / fork | [docs/contributors/archive.md](docs/contributors/archive.md) |
| Unsure | `python3 scripts/check_repo_health.py --quick` |

## Preflight

```bash
python3 scripts/check_repo_health.py --quick
python3 scripts/check_repo_health.py --full   # before large PRs
```

CI equivalent: [`.github/workflows/repo-health.yml`](.github/workflows/repo-health.yml).

## Record and pipeline (fork revive only)

- **Default:** capture via WORK lanes — see [docs/replacement-capture-habits.md](docs/replacement-capture-habits.md).
- **Do not** edit `self.md`, `self-evidence.md`, `recursion-gate.md`, `archive/grace-mar-instance/bot/prompt.py`, or PRP outputs by hand for merges. Stage candidates; companion approves; merge via `python scripts/process_approved_candidates.py --apply`.
- Gated-path commits should include **`[gated-merge]`** when the commit-msg hook is installed.

## Code layout (after repo refactor)

- Flask apps: [platform/apps/](platform/apps/) (`miniapp_server.py`, `gate-review-app.py`, `metrics-dashboard.py`).
- Run from repository root so `REPO_ROOT` resolves to the checkout.
- Optional: [platform/deployment/README.md](platform/deployment/README.md) for Docker / Render / Procfile notes.
- **Root layout:** [docs/root-directory-map.md](docs/root-directory-map.md) — operator ledgers live under `runtime/operator-events/`; dream handoff under `runtime/daily-handoff/`.

## Local dev hygiene

Pytest and Codex may leave temp dirs at the repository root (`pytest-cache-files-*`, `.tmp-pytest-*`, `.codex-tmp`, `.codex-bin`). They are gitignored. Optional cleanup:

```bash
python3 scripts/cleanup_dev_temp_dirs.py --dry-run
python3 scripts/cleanup_dev_temp_dirs.py --apply
```

## Python package (optional)

The repo includes an installable package ([pyproject.toml](pyproject.toml)) — active identity **`strategy-codex`**, wrapper under [platform/src/strategy_codex/](platform/src/strategy_codex/), internal module [platform/src/grace_mar/](platform/src/grace_mar/):

```bash
pip install -e .
strategy-codex warmup -u strategy-codex --compact
```

Deprecated alias: `grace-mar` (warns once). See [docs/archive/grace-mar-compatibility.md](docs/archive/grace-mar-compatibility.md).

Mini App / bot dependencies are optional: `pip install -e ".[miniapp]"`. Most scripts run with `python scripts/...` without an editable install.

**Reflection cycle (fork revive / archaeology):** `pip install -e ".[reflect]"` — see [docs/reflection-cycle.md](docs/reflection-cycle.md). Use `-u grace-mar` only when explicitly reviving the frozen Record.

## Performance

- Budgets: [docs/perf-budgets.md](docs/perf-budgets.md).
- Local check: `python scripts/run_perf_suite.py --tier 1 -u strategy-codex --check-baseline`.

## Questions

Open a discussion or issue on [GitHub](https://github.com/rbtkhn/grace-mar) for tooling and docs; instance-specific Record content is not something to “fix” without the companion’s fork-revive process.
