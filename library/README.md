# Operator library — civilization primary shelf (local)

**Local disk only.** Binaries and bulk PD text live here; they are **not** committed to git (see repo-root `.gitignore`).

## Purpose

Witness store for **third-party primary-source text** used in CIV-STATE volume work — aligned with `public/civ-state/volumes/{rome,persia,china,russia,america}/`.

| Subfolder | CIV-STATE volume | Notes |
|-----------|------------------|-------|
| `rome/` | `public/civ-state/volumes/rome/` | Acquisition manifest: `rome-pd-acquisition-manifest.yaml` |
| `persia/` | `persia/` | Scaffold until a volume manifest exists |
| `china/` | `china/` | Scaffold |
| `russia/` | `russia/` | Scaffold |
| `america/` | `america/` | Scaffold |

## Not the same as

- **Operator books** — misc folder homes; see [`codex/README.md`](../codex/README.md) § Operator books
- **`source-archive/statecraft/`** — verbatim modern captures in git
- **`public/civ-state/sources/`** — retrieve shelf / bibliography doors (metadata in repo)

## Rome default path

Manifest `local_root` is **`library/rome`** (relative to strategy-codex repo root). Override with env **`ROME_PD_LIBRARY_ROOT`** or operator profile when needed.

Workflow: [civ-state-primary-text-acquisition](../../.cursor/skills/civ-state-primary-text-acquisition/SKILL.md) · manifest [rome-pd-acquisition-manifest.yaml](../public/civ-state/volumes/rome/rome-pd-acquisition-manifest.yaml).
