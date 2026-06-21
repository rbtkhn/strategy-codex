# Contributor checklist — generated surfaces

1. Authority: **generated** — rebuildable, non-authoritative.
2. Regenerate via documented script; add header comment when introducing new generators.
3. Do not hand-edit drift-prone indexes (`thread-index.md`, hybrid `LLM-ROUTING.md`, etc.) — run generator `--check` in CI.
4. Manifest SSOT: [`generated-manifest.yaml`](../../generated-manifest.yaml) — new committed generated surfaces must be listed there.
5. Preflight: `python3 scripts/check_generated_surfaces.py --check` (or `python3 scripts/check_repo_health.py --quick`).
6. Header convention: see [complexity-budget.md](../complexity-budget.md#generated-surface-header-convention-sprint-6).
