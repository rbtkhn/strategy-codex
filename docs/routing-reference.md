# Routing reference — strategy-codex


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

Every route in [`repo-map.yaml`](../repo-map.yaml) **must** declare `category`: `source`, `work`, `generated`, or `archive`. Validation uses path-first rules in `scripts/validate_repo_routing.py` (`expected_route_category`).

| `category` | Meaning | Typical routes |
|---|---|---|
| `source` | Primary or canonical source material | `statecraft-source-capture` → `source-archive/statecraft/YYYY-MM-DD/source-*.md` |
| `work` | Active operator-authored or routing surfaces | `source_index` (analyst indexes), `routing_aid`, essays, host shelves |
| `generated` | Derived, rebuildable outputs | `LLM-ROUTING.md`, thread/day indexes, `runtime/artifacts/library-index.md` |
| `archive` | Frozen historical or compatibility material | `archive/grace-mar-instance/self-library.md` |

**Load-bearing distinction:** `statecraft/voices/*/*-source-index.md` is **`work`** (routing over captures). Verbatim `source-archive/statecraft/YYYY-MM-DD/source-*.md` is **`source`**. Day `day-index.md` files are **`generated`**.

### Path-first rules (validator)

| Condition | `category` |
|---|---|
| `source-archive/statecraft/` + `source-*.md` path_pattern or basename `source-*.md` | `source` |
| `kind: source_capture` | `source` |
| Path under `docs/archive/` or `archive/grace-mar-` | `archive` |
| Path under `runtime/artifacts/` | `generated` |
| `kind` is `generated_inventory` or `generated_dashboard` | `generated` |
| Route id `llm-routing` | `generated` |
| Default | `work` |

### Kind reference (selected)

| `kind` | Typical `category` | Notes |
|---|---|---|
| `source_capture` | `source` | Verbatim transcript/wire body path_pattern |
| `source_index` | `work` | Analyst corpus index — not primary source |
| `local_index_script` | `work` | Script routing entry (e.g. `scripts/index_record.py`) |
| `canonical_reference` under `archive/grace-mar-` | `archive` | Path prefix wins over kind |
| `generated_inventory` | `generated` | Thread index, day-index path_pattern |

Declared `category` must match `expected_route_category()` or validation fails. All four categories must appear at least once in repo-map.

## Index disambiguation (short)

| Query shape | Open first |
|---|---|
| Calendar day **`YYYY-MM-DD`** + day-index / what landed | `source-archive/statecraft/YYYY-MM-DD/day-index.md` only |
| Named analyst / speaker corpus | `statecraft/voices/<speaker>/<speaker>-source-index.md` → [`statecraft/voices/voice-index.md`](../statecraft/voices/voice-index.md) |
| Thread coverage / counts | `source-archive/statecraft/thread-index.md` (inventory, not route map) |
| Reading order / corpus tiers | [`docs/source-lattice-beyond-the-repo.md`](source-lattice-beyond-the-repo.md) |

Full tables live in [`LLM-ROUTING.md`](../LLM-ROUTING.md) (curated prose) and generated registries below the `<!-- GENERATED:sections -->` marker in the template.

## Related

- [`docs/complexity-budget.md`](complexity-budget.md) — routing surface targets
- [`docs/templates/llm-routing-prose.md`](templates/llm-routing-prose.md) — hand-curated prose template
- [`scripts/generate_llm_routing.py`](../scripts/generate_llm_routing.py) — hybrid generator
