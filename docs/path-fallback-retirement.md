# Path fallback retirement

**Work only; not Record.**

Machine SSOT: [`path-fallback-retirement.yaml`](../path-fallback-retirement.yaml).
Resolver: [`scripts/repo_io.py`](../scripts/repo_io.py) (`REPO_PATH_MIGRATIONS`, `REPO_PATH_CLASSIFICATION`).

## Policy

No new fallback tuple may be added without:

1. Classification in `REPO_PATH_CLASSIFICATION`
2. Entry in `path-fallback-retirement.yaml`
3. Test coverage in `tests/test_repo_path_strict.py`

## Retired fallbacks

### Wave 1 — completed 2026-06-21

The following active canonical fallbacks have been removed from `REPO_PATH_MIGRATIONS`:

artifacts, daily-handoff, prepared-context, runtime-bundle, apps, src, skills, skills-portable, schema-registry, styles, auto-research, bridges.

### Wave 2 — completed 2026-06-21

The following platform subpath fallbacks have been removed from `REPO_PATH_MIGRATIONS`:

app, bin, deployment, config, extension, integrations, miniapp, users, template, profile.

Readiness audit receipt: [`runtime/artifacts/complexity-audit/wave-2-platform-readiness-2026-06-21.md`](../runtime/artifacts/complexity-audit/wave-2-platform-readiness-2026-06-21.md).

### Wave 3 — completed 2026-06-21

The following archive placeholder fallbacks have been removed from `REPO_PATH_MIGRATIONS`:

evidence, reflection-proposals, review-queue.

Readiness audit receipt: [`runtime/artifacts/complexity-audit/wave-3-archive-placeholder-readiness-2026-06-21.md`](../runtime/artifacts/complexity-audit/wave-3-archive-placeholder-readiness-2026-06-21.md).

## Retirement table

| Key | Category | Canonical | Legacy | Status | Wave | Notes |
|---|---|---|---|---|---|---|
| `app` | `active_canonical` | `platform/app` | `—` | `keep_no_legacy` | 2 | Wave 2 fallback removed; canonical path only. |
| `apps` | `active_canonical` | `platform/apps` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `artifacts` | `active_canonical` | `runtime/artifacts` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `auto-research` | `active_canonical` | `research/auto-research` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `bin` | `active_canonical` | `platform/bin` | `—` | `keep_no_legacy` | 2 | Wave 2 fallback removed; canonical path only. |
| `bootstrap` | `grace_mar_compat` | `archive/grace-mar-instance/bootstrap` | `bootstrap` | `move_to_grace_mar_compat` | 4 | Archive-only bootstrap fallback. |
| `bot` | `grace_mar_compat` | `archive/grace-mar-instance/bot` | `bot` | `move_to_grace_mar_compat` | 4 | Voice archaeology only; relocate to compat module. |
| `bridges` | `active_canonical` | `research/bridges` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `config` | `active_canonical` | `platform/config` | `—` | `keep_no_legacy` | 2 | Wave 2 fallback removed; canonical path only. |
| `daily-handoff` | `active_canonical` | `runtime/daily-handoff` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `deployment` | `active_canonical` | `platform/deployment` | `—` | `keep_no_legacy` | 2 | Wave 2 fallback removed; canonical path only. |
| `evidence` | `archive_placeholder` | `archive/placeholders/evidence` | `—` | `keep_no_legacy` | 3 | Wave 3 fallback removed; canonical path only. |
| `extension` | `active_canonical` | `platform/extension` | `—` | `keep_no_legacy` | 2 | Wave 2 fallback removed; canonical path only. |
| `grace-mar-instance` | `grace_mar_compat` | `archive/grace-mar-instance` | `—` | `keep_no_legacy` | — | Single canonical tuple; Record bundle root. |
| `integrations` | `active_canonical` | `platform/integrations` | `—` | `keep_no_legacy` | 2 | Wave 2 fallback removed; canonical path only. |
| `miniapp` | `active_canonical` | `platform/miniapp` | `—` | `keep_no_legacy` | 2 | Wave 2 fallback removed; canonical path only. |
| `prepared-context` | `active_canonical` | `runtime/prepared-context` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `profile` | `active_canonical` | `platform/profile` | `—` | `keep_no_legacy` | 2 | Wave 2 fallback removed; canonical path only. |
| `recursion-gate-staging` | `grace_mar_compat` | `archive/grace-mar-instance/recursion-gate-staging` | `recursion-gate-staging` | `move_to_grace_mar_compat` | 4 | Archive-only gate staging. |
| `reflection-proposals` | `archive_placeholder` | `archive/queues/reflection-proposals` | `—` | `keep_no_legacy` | 3 | Wave 3 fallback removed; canonical path only. |
| `review-queue` | `archive_placeholder` | `archive/queues/review-queue` | `—` | `keep_no_legacy` | 3 | Wave 3 fallback removed; canonical path only. |
| `runtime-bundle` | `active_canonical` | `runtime/bundle` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `schema-registry` | `active_canonical` | `schemas/registry` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `skills` | `active_canonical` | `skills` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `skills-portable` | `active_canonical` | `skills` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `src` | `active_canonical` | `platform/src` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `styles` | `active_canonical` | `templates/styles` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `template` | `active_canonical` | `platform/template` | `—` | `keep_no_legacy` | 2 | Wave 2 fallback removed; canonical path only. |
| `users` | `active_canonical` | `platform/users` | `—` | `keep_no_legacy` | 2 | Wave 2 fallback removed; canonical path only. |

## Removal waves

### Wave 1 — active canonical (retired 2026-06-21)

artifacts, daily-handoff, prepared-context, runtime-bundle, apps, src, skills, skills-portable, schema-registry, styles, auto-research, bridges

### Wave 2 — Platform subpaths (retired 2026-06-21)

app, bin, deployment, config, extension, integrations, miniapp, users, template, profile

Readiness verified before removal — see [`wave-2-platform-readiness-2026-06-21.md`](../runtime/artifacts/complexity-audit/wave-2-platform-readiness-2026-06-21.md).

### Wave 3 — Archive placeholders (retired 2026-06-21)

evidence, reflection-proposals, review-queue

Readiness verified before removal — see [`wave-3-archive-placeholder-readiness-2026-06-21.md`](../runtime/artifacts/complexity-audit/wave-3-archive-placeholder-readiness-2026-06-21.md).

### Wave 4 — Grace-Mar compatibility relocation

bot, recursion-gate-staging, bootstrap -> future `platform/src/strategy_codex/compat/grace_mar_paths.py` (document only; not moved in this slice).

`grace-mar-instance` has no legacy tuple (`keep_no_legacy`).

## Related

- [`docs/complexity-budget.md`](complexity-budget.md)
- `python scripts/check_repo_path_strict.py`
- `python scripts/check_repo_path_strict.py --wave 2`
- `python scripts/check_repo_path_strict.py --wave 3`
