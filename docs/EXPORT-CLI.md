# Unified export CLI (`scripts/export.py`)

**Purpose:** One entrypoint that **dispatches** to existing `scripts/export_*.py` modules via subprocess (v1). Does not reimplement fork loading.

**Default profile (M1):** If the child invocation has no `-u` / `--user`, `export.py` injects `-u` using, in order: explicit `export.py -u`, then the configured root profile id, then repo heuristic (`strategy-codex` when `self.md` exists, else `platform/template`).

**Forwarding (M2):** Use `--` to pass flags to the target script verbatim:

```bash
python3 scripts/export.py fork -- -o fork-export.json
python3 scripts/export.py fork -- --format json-ld -o out.jsonld
```

Omitting `--` still forwards any tokens after the subcommand (e.g. `export.py fork -o out.json`).

**G1 â€” `all`:** Same as `bundle` (forwards to `export_runtime_bundle.py`).

**Non-goals:** `export_view`, `export_gate_to_review_queue`, â€¦ â€” run those scripts directly.

**Template repo:** [companion-self](https://github.com/rbtkhn/companion-self) may not yet ship every `export_*.py`; `export.py` errors clearly if a target script is missing. Promote scripts from the instance repo per [MERGING-FROM-COMPANION-SELF.md](MERGING-FROM-COMPANION-SELF.md).

**Migration:**

| Before | After |
|--------|--------|
| `python scripts/export_fork.py` | `python scripts/export.py fork -- -o x.json` |
| `python scripts/export_prp.py` | `python scripts/export.py prp --` (or add `-o` after `--`) |
| `python scripts/export_runtime_bundle.py` | `python scripts/export.py bundle --` or `python scripts/export.py all --` |
| `python scripts/export_emulation_bundle.py` | `python scripts/export.py emulation --` |

Legacy scripts remain; they may emit `DeprecationWarning` when run as `__main__`.

