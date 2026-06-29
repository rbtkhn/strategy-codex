# `codex/speakers/` — deprecated (terminated)

**Status:** The legacy tree **`codex/speakers/`** was **removed** in the statecraft voices migration (2026-06). Do not recreate it or add redirect stubs under `codex/`.

## Canonical homes

| Role | Path |
|------|------|
| Analyst / guest speaker shelves | [`statecraft/voices/`](../../statecraft/voices/README.md) |
| Host-family continuity (Davis, Napolitano, Nima / Dialogue Works) | [`statecraft/channels/`](../../statecraft/channels/README.md) |
| Full-source captures | [`source-archive/statecraft/`](../../source-archive/statecraft/README.md) |

## Migration receipt

Mechanical path map: [`runtime/artifacts/statecraft/codex-speakers-migration-receipt.json`](../../runtime/artifacts/statecraft/codex-speakers-migration-receipt.json).

Script: `python scripts/migrate_codex_speakers_to_statecraft.py --plan` (historical; tree already deleted).

## Link repair

Replace **`codex/speakers/<slug>/`** with:

- **`statecraft/voices/<slug>/`** for analyst shelves
- **`statecraft/channels/<slug>/`** for **`davis`**, **`napolitano`**, **`nima`**

Shared tooling moved to **`statecraft/templates/`** (speaker scaffolds). Cross-speaker compare notes → **`statecraft/notes/`**.
