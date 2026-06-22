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

## Retirement table

| Key | Category | Canonical | Legacy | Status | Wave | Notes |
|---|---|---|---|---|---|---|
| `app` | `active_canonical` | `platform/app` | `app` | `remove_when_clean` | 2 | Platform app subpath; verify apps first. |
| `apps` | `active_canonical` | `platform/apps` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `artifacts` | `active_canonical` | `runtime/artifacts` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `auto-research` | `active_canonical` | `research/auto-research` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `bin` | `active_canonical` | `platform/bin` | `bin` | `remove_when_clean` | 2 | Platform bin subpath. |
| `bootstrap` | `grace_mar_compat` | `archive/grace-mar-instance/bootstrap` | `bootstrap` | `move_to_grace_mar_compat` | 4 | Archive-only bootstrap fallback. |
| `bot` | `grace_mar_compat` | `archive/grace-mar-instance/bot` | `bot` | `move_to_grace_mar_compat` | 4 | Voice archaeology only; relocate to compat module. |
| `bridges` | `active_canonical` | `research/bridges` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `config` | `active_canonical` | `platform/config` | `config` | `remove_when_clean` | 2 | Platform config subpath. |
| `daily-handoff` | `active_canonical` | `runtime/daily-handoff` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `deployment` | `active_canonical` | `platform/deployment` | `deployment` | `remove_when_clean` | 2 | Platform deployment subpath. |
| `evidence` | `archive_placeholder` | `archive/placeholders/evidence` | `evidence` | `keep_temporarily` | 3 | Archive placeholder until queue usage audited. |
| `extension` | `active_canonical` | `platform/extension` | `extension` | `remove_when_clean` | 2 | Platform extension subpath. |
| `grace-mar-instance` | `grace_mar_compat` | `archive/grace-mar-instance` | `—` | `keep_no_legacy` | — | Single canonical tuple; Record bundle root. |
| `integrations` | `active_canonical` | `platform/integrations` | `integrations` | `remove_when_clean` | 2 | Platform integrations subpath. |
| `miniapp` | `active_canonical` | `platform/miniapp` | `miniapp` | `remove_when_clean` | 2 | Platform miniapp subpath. |
| `prepared-context` | `active_canonical` | `runtime/prepared-context` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `profile` | `active_canonical` | `platform/profile` | `profile` | `remove_when_clean` | 2 | Platform profile subpath. |
| `recursion-gate-staging` | `grace_mar_compat` | `archive/grace-mar-instance/recursion-gate-staging` | `recursion-gate-staging` | `move_to_grace_mar_compat` | 4 | Archive-only gate staging. |
| `reflection-proposals` | `archive_placeholder` | `archive/queues/reflection-proposals` | `reflection-proposals` | `keep_temporarily` | 3 | Archive queue placeholder. |
| `review-queue` | `archive_placeholder` | `archive/queues/review-queue` | `review-queue` | `keep_temporarily` | 3 | Archive queue placeholder. |
| `runtime-bundle` | `active_canonical` | `runtime/bundle` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `schema-registry` | `active_canonical` | `schemas/registry` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `skills` | `active_canonical` | `skills` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `skills-portable` | `active_canonical` | `skills` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `src` | `active_canonical` | `platform/src` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `styles` | `active_canonical` | `templates/styles` | `—` | `keep_no_legacy` | 1 | Wave 1 fallback removed; canonical path only. |
| `template` | `active_canonical` | `platform/template` | `_template` | `remove_when_clean` | 2 | Platform template; legacy _template at repo root. |
| `users` | `active_canonical` | `platform/users` | `users` | `remove_when_clean` | 2 | Platform users profiles root. |

## Removal waves

### Wave 1 — active canonical (retired 2026-06-21)

artifacts, daily-handoff, prepared-context, runtime-bundle, apps, src, skills, skills-portable, schema-registry, styles, auto-research, bridges

### Wave 2 — Platform subpaths (verify apps first)

app, bin, deployment, config, extension, integrations, miniapp, users, template, profile

### Wave 3 — Archive placeholders

evidence, reflection-proposals, review-queue

### Wave 4 — Grace-Mar compatibility relocation

bot, recursion-gate-staging, bootstrap -> future `platform/src/strategy_codex/compat/grace_mar_paths.py` (document only; not moved in this slice).

`grace-mar-instance` has no legacy tuple (`keep_no_legacy`).

## Related

- [`docs/complexity-budget.md`](complexity-budget.md)
- `python scripts/check_repo_path_strict.py`
