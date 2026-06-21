# Routing reference — strategy-codex

**Work only; not Record.**

Machine-readable SSOT for route entries: [`repo-map.yaml`](../repo-map.yaml). Human/agent front door: [`LLM-ROUTING.md`](../LLM-ROUTING.md) (hybrid generated + curated prose).

## Routing hierarchy

```text
README.md → docs/start-here.md → repo-map.yaml → domain README
```

| Layer | Role |
|---|---|
| [`README.md`](../README.md) | Public orientation and choose-your-path |
| [`docs/start-here.md`](start-here.md) | Operator loop and default lanes |
| [`repo-map.yaml`](../repo-map.yaml) | Machine-readable route registry (ids, paths, kinds, search hints) |
| Domain README | e.g. [`statecraft/README.md`](../statecraft/README.md), [`singularity/README.md`](../singularity/README.md) |

Regenerate routing doc: `python3 scripts/generate_llm_routing.py`

Validate: `python3 scripts/validate_repo_routing.py --strict`

## Authority categories (four-way model)

Sprint 3 adds optional `category` on repo-map routes. Until migration completes, infer from `kind` + `authority`:

| `category` | Meaning | Typical `kind` / `authority` |
|---|---|---|
| `source` | Primary or canonical source material | (reserved — archive captures use path patterns, not repo-map rows today) |
| `work` | Active operator-authored or routing surfaces | `source_index` + `work_only`; `routing_aid`; `reading_discipline`; `directory_index` + `routing_aid` |
| `generated` | Derived, rebuildable outputs | `generated_inventory` + `derived`; `generated_dashboard` + `derived`; `local_index_script` + `derived_local` |
| `archive` | Frozen historical or compatibility material | Grace-Mar corpus pointers; legacy compatibility stubs |

### Inference table (validator default)

| `kind` | `authority` | Inferred `category` |
|---|---|---|
| `source_index` | `work_only` | `work` |
| `routing_aid` | `routing_aid` or `work_only` | `work` |
| `directory_index` | `routing_aid` | `work` |
| `reading_discipline` | `work_only` | `work` |
| `canonical_reference` | `canonical_self_library` | `work` |
| `generated_inventory` | `derived` | `generated` |
| `generated_dashboard` | `derived` | `generated` |
| `local_index_script` | `derived_local` | `generated` |

When `category` is present on a route, it must match the inferred value or validation warns (Sprint 3) / fails (Sprint 6+).

## Index disambiguation (short)

| Query shape | Open first |
|---|---|
| Calendar day **`YYYY-MM-DD`** + day-index / what landed | `source-archive/statecraft/YYYY-MM-DD/day-index.md` only |
| Named analyst / speaker corpus | `statecraft/voices/<speaker>/<speaker>-source-index.md` → [`statecraft/voices/INDEX.md`](../statecraft/voices/INDEX.md) |
| Thread coverage / counts | `source-archive/statecraft/thread-index.md` (inventory, not route map) |
| Reading order / corpus tiers | [`docs/source-lattice-beyond-the-repo.md`](source-lattice-beyond-the-repo.md) |

Full tables live in [`LLM-ROUTING.md`](../LLM-ROUTING.md) (curated prose) and generated registries below the `<!-- GENERATED:sections -->` marker in the template.

## Related

- [`docs/complexity-budget.md`](complexity-budget.md) — routing surface targets
- [`docs/templates/llm-routing-prose.md`](templates/llm-routing-prose.md) — hand-curated prose template
- [`scripts/generate_llm_routing.py`](../scripts/generate_llm_routing.py) — hybrid generator
