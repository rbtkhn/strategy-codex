WORK only; not Record.

# Voice Index Registry

Front door for **voice index** health (per-analyst `{slug}-index.md` files). Not the voices router.

## Terminology

| Term | File / role |
| --- | --- |
| **Voices router** | [`voice-index.md`](voice-index.md) — catalog of all analyst/channel indexes |
| **Voice index** | `{slug}/{slug}-index.md` — exhaustive archive capture route map for one analyst |
| **Voice index registry** | Generated parity dashboard (below) |

Do not use “shelf index” in operator prose — it collided with “voice index” and speaker-shelf folders.

## Generated dashboard

- [`runtime/artifacts/voice-index-parity.md`](../../runtime/artifacts/voice-index-parity.md)
- [`runtime/artifacts/voice-index-parity.json`](../../runtime/artifacts/voice-index-parity.json)

Regenerate:

```bash
python3 scripts/build_voice_index_registry.py
```

## Canonical checks

```bash
# Preflight (quick tier — artifact drift + embedded parity)
python3 scripts/build_voice_index_registry.py --check

# Full health / closeout (live rollup)
python3 scripts/audit_statecraft_archive_index.py --all-voice-indexes
```

Repo health: `check_repo_health --quick` runs registry `--check` only; `--full` adds `--all-voice-indexes`.

## Exception metadata

Central config: [`voice-index-registry.yml`](voice-index-registry.yml) — builder, status, curated overlays, documented exclusions.

Matching code SSOT: `scripts/shelf_index_utils.py` → `shelf_capture_excluded()`. Every slug in `CODE_EXCLUSION_SLUGS` must have a non-empty YAML `exclusions` list or checks fail.

## Rules

1. Every primary voice index must be listed in the **voices router** (`voice-index.md`).
2. Every canonical voice should have `{slug}-index.md`.
3. Every eligible archive capture must be cited or excluded in code + documented in YAML when code excludes.
4. Generated rebuilds should preserve curated overlays (v2: HTML marker blocks).
5. After intake or index edits, regen registry artifacts before push.

**Spelling:** display name **Alkhorshid**; voice slug **`alkhorshid`**. Legacy capture filenames and `title_slug` tokens may still contain `alkorshid` (filename alias in `shelf_index_utils`).

Per-voice audit (`--shelf-index` = legacy CLI flag for one **voice index**):

```bash
python3 scripts/audit_statecraft_archive_index.py --shelf-index johnson
```

**Preflight vs closeout:** `--check` verifies artifact drift + YAML exception registry (warnings for parity fail rows). `--all-voice-indexes` fails on parity regressions — use for full health / closeout.
