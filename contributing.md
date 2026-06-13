# Contributing

This repository is **strategy-codex** — a **governed interpretive machine** for statecraft and singularity operator work. External contributions are welcome for **code and docs**.

The embedded Grace-Mar **Record** at repo root is **frozen archaeology**; merges into identity/evidence/prompt run only on explicit **`fork revive`** via the gated pipeline ([grace-mar-instance-boundary.md](docs/grace-mar-instance-boundary.md)).

**Filename conventions:** [docs/naming-convention.md](docs/naming-convention.md) (lowercase docs, reserved `AGENTS.md`, OpenClaw export path).

## Before you start

1. Read [docs/start-here.md](docs/start-here.md) and [AGENTS.md](AGENTS.md) — active operator surface, knowledge boundary, merge law when fork is revived.
2. Legacy fork doctrine (archived): [archive/grace-mar-corpus/README.md](archive/grace-mar-corpus/README.md).
3. Canonical on-disk paths: [docs/canonical-paths.md](docs/canonical-paths.md).
4. **Public-facing tone:** [docs/contributing-public-copy.md](docs/contributing-public-copy.md).

## Record and pipeline (fork revive only)

- **Default:** capture via WORK lanes — see [docs/replacement-capture-habits.md](docs/replacement-capture-habits.md).
- **Do not** edit `self.md`, `self-evidence.md`, `recursion-gate.md`, `bot/prompt.py`, or PRP outputs by hand for merges. Stage candidates; companion approves; merge via `python scripts/process_approved_candidates.py --apply`.
- Gated-path commits should include **`[gated-merge]`** when the commit-msg hook is installed.

## Code layout (after repo refactor)

- Flask apps: [apps/](apps/) (`miniapp_server.py`, `gate-review-app.py`, `metrics-dashboard.py`).
- Run from repository root so `REPO_ROOT` resolves to the checkout.
- Optional: [deployment/README.md](deployment/README.md) for Docker / Render / Procfile notes.

## Python package (optional)

The repo includes a minimal installable package under [src/grace_mar/](src/grace_mar/) ([pyproject.toml](pyproject.toml)):

```bash
pip install -e .
grace-mar warmup -u strategy-codex --compact
```

Mini App / bot dependencies are optional: `pip install -e ".[miniapp]"`. Most scripts run with `python scripts/...` without an editable install.

**Reflection cycle (fork revive / archaeology):** `pip install -e ".[reflect]"` — see [docs/reflection-cycle.md](docs/reflection-cycle.md). Use `-u grace-mar` only when explicitly reviving the frozen Record.

## Performance

- Budgets: [docs/perf-budgets.md](docs/perf-budgets.md).
- Local check: `python scripts/run_perf_suite.py --tier 1 -u strategy-codex --check-baseline`.

## Questions

Open a discussion or issue on [GitHub](https://github.com/rbtkhn/grace-mar) for tooling and docs; instance-specific Record content is not something to “fix” without the companion’s fork-revive process.
