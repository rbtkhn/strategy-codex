# Contributor checklist — scripts

1. Use [`scripts/repo_io.py`](../../scripts/repo_io.py) for `REPO_ROOT` and path keys — no new root literals (`check_repo_path_adoption.py`).
2. Resolve paths via `resolve_repo_path()`; legacy fallbacks warn — `STRATEGY_CODEX_STRICT_PATHS=1` fails.
3. Record paths → `profile_dir()` / `archive/grace-mar-instance/` — not repo root.
4. Add tests under `tests/` when behavior is non-obvious.
5. Preflight: `python3 scripts/check_repo_health.py --quick`
