# Grace-Mar compatibility

**Archive / compatibility only — not active product identity.**

Grace-Mar was the prior frozen fork identity for the embedded Record under [`archive/grace-mar-instance/`](../../archive/grace-mar-instance/). It is retained for archived material and backward-compatible command aliases.

**Active work belongs to strategy-codex.**

## CLI

| Command | Status |
|---------|--------|
| `strategy-codex` | **Active** — preferred entrypoint (`platform/src/strategy_codex/`) |
| `grace-mar` | **Deprecated** — prints a one-line warning, then delegates to the same commands |
| `predictive-history` | Unchanged short term (`grace_mar.predictive_history`) |

Install:

```bash
pip install -e .
strategy-codex warmup -u strategy-codex --compact
```

## Python package layout (Stage A+B)

- **Active package name:** `strategy-codex` ([`pyproject.toml`](../../pyproject.toml))
- **Internal module:** `grace_mar` under [`platform/src/grace_mar/`](../../platform/src/grace_mar/) — not renamed in Sprint 1
- **Wrapper:** `strategy_codex` re-exports repo helpers and owns the primary CLI

## When to use Grace-Mar paths

- Explicit **`fork revive`**, **`grace-mar archive`**, or coffee **`A gate`**
- Archaeology under [`archive/grace-mar-corpus/`](../../archive/grace-mar-corpus/)

Default operator capture: [`docs/replacement-capture-habits.md`](../replacement-capture-habits.md).

## Canonical archive doctrine

See [`grace-mar.md`](grace-mar.md) (Sprint 2) and [`../grace-mar-instance-boundary.md`](../grace-mar-instance-boundary.md).
