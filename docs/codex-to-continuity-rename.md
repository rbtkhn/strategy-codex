---
audience: operator
authority: doctrine
record_status: none
---

# codex/ → continuity/ rename decision

**Status:** Active migration — path rename in progress. Public project name remains **strategy-codex**.

## Why rename `codex/`?

The folder `codex/` already functions as the repo's **chronology, accumulation, and notebook continuity layer**, but the name is opaque, brand-like, and historically overloaded (strategy-notebook alias, expert mind files, compiled views). Renaming to **`continuity/`** makes the role plain without renaming the project.

## Why not `memory/`?

| Surface | Role |
|---------|------|
| [`memory.md`](../memory.md) | Rotatable **session** continuity buffer |
| **`continuity/`** | Durable chronology, accumulation, and notebook continuity |
| [`source-archive/`](../source-archive/README.md) | Evidence and source truth |
| [`statecraft/`](../statecraft/README.md) | Live judgment and first-class geopolitical work |
| [`singularity/`](../singularity/README.md) | Live acceleration / agency / recursive tooling |
| [`archive/`](../archive/README.md) | Frozen or non-live holdings |

Collapsing session memory, durable continuity, evidence, and judgment into one word would increase entropy, not reduce it.

## Target state

```text
strategy-codex     — project / public name (unchanged)
continuity/        — durable chronology and notebook continuity (canonical path)
codex/             — legacy redirect only (README pointer after move)
memory.md          — rotatable session continuity buffer
```

## Core doctrine

```text
The repo owns context. Models borrow context.
continuity/ owns durable chronology and notebook continuity.
memory.md remains a rotatable session continuity buffer.
source-archive/ remains source truth.
statecraft/ remains live judgment.
```

## Compatibility period

After the folder move:

- **`continuity/`** holds all live notebook corpus files.
- **`codex/`** may contain only [`codex/README.md`](../codex/README.md) (redirect) and optionally `.gitkeep`.
- Routing docs, repo maps, and agent rules point operators to **`continuity/`**.
- **`strategy-codex`**, **`strategy-notebook`**, **`strategy-expert`**, and **`strategy-author`** remain where they are parser, fixture, or public-name contracts — do not bulk-replace.

Related prior migration: [`scripts/validate_strategy_codex_transition.py`](../scripts/validate_strategy_codex_transition.py) (strategy-notebook → strategy-codex prose). This rename is a separate path migration.

**Different concept:** [`scripts/continuity_preflight.py`](../scripts/continuity_preflight.py) hashes Record session contract files — not the notebook continuity layer.

## What must not be renamed yet

- Repository name **strategy-codex**
- Python package / product config **`strategy_codex`**
- Parser and marker contracts: **`strategy-expert-*`**, **`strategy-page`**, thread markers
- Generated artifacts until explicitly regenerated
- Museum Record under **`archive/grace-mar-instance/`**

## Migration tooling

| Tool | Purpose |
|------|---------|
| [`scripts/audit_continuity_rename.py`](../scripts/audit_continuity_rename.py) | Classify references; strict mode before/after move |
| [`scripts/continuity_paths.py`](../scripts/continuity_paths.py) | Resolve canonical continuity root (dual-path) |
| [`scripts/check_continuity_status.py`](../scripts/check_continuity_status.py) | STATUS.md freshness |
| [`scripts/check_text_encoding_hygiene.py`](../scripts/check_text_encoding_hygiene.py) | Mojibake detection |

## Approved legacy references (post-move)

Path references to **`codex/`** are allowed only in:

| Bucket | Examples |
|--------|----------|
| Redirect pointer | `codex/README.md` |
| Rename doctrine | This file, migration PR descriptions |
| Audit allowlist | `scripts/audit_continuity_rename.py` `APPROVED_LEGACY_PATH_PREFIXES` |
| Historical archive | `docs/archive/`, `archive/` (frozen) |
| Compatibility prose | Explicit "formerly codex/" phrasing in routing docs |

Public project name **`strategy-codex`** and legacy tokens **`strategy-notebook`**, **`strategy-expert`**, **`strategy-author`** remain valid in prose and contracts per [STRATEGY-NOTEBOOK-DEPRECATED.md](skill-work/work-strategy/STRATEGY-NOTEBOOK-DEPRECATED.md).

## Cross-links

- [Context layer](context-layer.md)
- [AGENTS.md](../AGENTS.md)
- [memory.md](../memory.md)
- [codex/README.md](../codex/README.md) (legacy redirect) → [continuity/README.md](../continuity/README.md) (post-move)
