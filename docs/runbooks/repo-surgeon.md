# Repo Surgeon runbook


Reference-integrity closure for `strategy-codex`: markdown links, local path leaks, path adoption, generated-surface drift, archive boundaries, and authority markers.

**Artifacts:** `runtime/artifacts/repo-surgeon/` (gitignored). Regenerate on demand.

---

## Quick commands

### Baseline / ledger (Phase 0)

```bash
python3 scripts/repo_surgeon.py \
  --scope all \
  --max-link-errors 0 \
  --verify-portable-skills \
  --run-existing-checks \
  --json-out runtime/artifacts/repo-surgeon/pass0-baseline.json \
  --out runtime/artifacts/repo-surgeon/pass0-baseline.md \
  --ledger-out runtime/artifacts/repo-surgeon/pass0-ledger.json
```

Supplement (orchestrated health not fully duplicated in Surgeon):

```bash
python3 scripts/check_repo_health.py --quick 2>&1 | tee runtime/artifacts/repo-surgeon/pass0-health.txt
python3 scripts/check_repo_path_adoption.py 2>&1 | tee runtime/artifacts/repo-surgeon/pass0-paths.txt
python3 scripts/validate_skills.py --strict-metadata 2>&1 | tee runtime/artifacts/repo-surgeon/pass0-skills-metadata.txt
python3 scripts/validate_skills.py --strict-verification 2>&1 | tee runtime/artifacts/repo-surgeon/pass0-skills-verify.txt
python3 scripts/check_archive_boundary.py 2>&1 | tee runtime/artifacts/repo-surgeon/pass0-archive-boundary.txt
```

### Scoped slices

| Scope | Use |
| --- | --- |
| `routing-ssot` | LLM-ROUTING, repo-map, voice `*-index` — must stay **green** |
| `docs` | Operator docs tree |
| `statecraft` | Active synthesis + voices |
| `skills` | `skills/` + `.cursor/skills/` |
| `all` | Full gate (definition of done) |

### Fix passes (mechanical)

```bash
# Pass 4 — bulk link hygiene
python3 scripts/fix_repo_surgeon_link_batch.py --scope all --apply

# Residual basename resolution (when target file exists elsewhere)
python3 scripts/fix_repo_surgeon_resolve_missing.py --scope all --apply

# Pass 6 — path literals (CI already strict on scripts/)
python3 scripts/check_repo_path_adoption.py --max-literals 0
python3 scripts/adopt_repo_path_constants.py --apply  # when safe

# Pass 7 — regenerate derived surfaces
python3 scripts/generate_llm_routing.py --check
python3 scripts/generate_skill_inventory.py
python3 scripts/generate_domain_pack_triage.py
python3 scripts/sync_portable_skills.py --verify
python3 scripts/refresh_statecraft_archive_indices.py --check
```

### Strict gate (Pass 8b)

Exit **1** when `warning_count > 0` or any **blocking** finding:

```bash
python3 scripts/repo_surgeon.py \
  --scope all \
  --strict \
  --verify-portable-skills \
  --max-link-errors 0
```

Strict mode also runs: `check_repo_health --quick`, `generate_llm_routing --check`, `refresh_statecraft_archive_indices --check`, `check_archive_boundary`, `check_doc_authority_markers`.

---

## Ledger taxonomy

`--ledger-out PATH` writes grouped JSON:

| Surgeon category | Ledger category |
| --- | --- |
| `broken_link` | `broken_link` |
| `local_path` | `absolute_path` |
| `path_adoption` | `stale_path` |
| `root_layout` | `root_layout` |
| `skill_drift` | `skill_metadata` |
| `archive_boundary` | `archive_boundary` |
| `generated_drift` | `generated_drift` |
| `deprecated_surface` | `deprecated_surface` |

Header fields: `blocking_count`, `warning_count`, `status`, `categories[]`.

---

## Warning ledger workflow

1. **Measure** — full `--scope all` scan + `--ledger-out` before edits.
2. **Fix highest-count categories first** — `broken_link`, then `absolute_path`, then orchestrated checks.
3. **Re-measure** — same command; compare ledger counts.
4. **Snapshot** — optional count-only history in [repo-surgeon-baseline-snapshot.md](repo-surgeon-baseline-snapshot.md).

**Waiver policy (v1):** `main` target = **0 warnings**. Migration branches may add `runtime/artifacts/repo-surgeon/waivers.yaml` (max 5 entries + expiry) — not enabled on `main` until explicitly adopted.

---

## Fix rules (Pass 4–5)

| Bad | Replace |
| --- | --- |
| `../../...`, Windows absolute paths under `dev` | repo-relative path |
| `codex/years/.../provenance/` | `source-archive/statecraft/YYYY-MM-DD/` |
| `strategy-notebook/` docs paths | `codex/` or [STRATEGY-NOTEBOOK-DEPRECATED.md](../skill-work/work-strategy/STRATEGY-NOTEBOOK-DEPRECATED.md) |
| `../../AGENTS.md` from `docs/skill-work/**` | correct depth to repo root `AGENTS.md` |
| Live workflow into Record without framing | `archive/grace-mar-instance/...` + **fork revive only** |

---

## Authority markers (Pass 8a)

High-traffic docs must carry YAML frontmatter (or HTML comment block) with:

| Field | Values |
| --- | --- |
| `audience` | `public` \| `operator` \| `archive` \| `generated` |
| `authority` | `source` \| `synthesis` \| `transaction` \| `routing_aid` \| `archive` \| `doctrine` |
| `record_status` | `none` \| `frozen` \| `fork_revive_only` |

Validator: `python3 scripts/check_doc_authority_markers.py`

---

## Definition of done

All pass:

```bash
python3 scripts/repo_surgeon.py --scope all --strict --verify-portable-skills --max-link-errors 0
python3 scripts/check_repo_health.py --quick
python3 scripts/assert_root_folder_layout.py
python3 scripts/assert_root_profile_exports.py
python3 scripts/check_repo_path_adoption.py --max-literals 0
python3 scripts/validate_skills.py --strict-metadata
python3 scripts/validate_skills.py --strict-verification
python3 scripts/generate_llm_routing.py --check
python3 scripts/refresh_statecraft_archive_indices.py --check
python3 -m pytest tests/test_repo_surgeon.py tests/test_check_archive_boundary.py -q
```

**Routing SSOT slice** must stay green independently:

```bash
python3 scripts/repo_surgeon.py --scope routing-ssot --max-link-errors 0 --no-existing-checks
```

---

## Related

- [runtime/artifacts/repo-surgeon/README.md](../../runtime/artifacts/repo-surgeon/README.md)
- [operator-dashboard-consolidation-phase0.md](../skill-work/work-dev/operator-dashboard-consolidation-phase0.md)
- [grace-mar-instance-boundary.md](../grace-mar-instance-boundary.md)
