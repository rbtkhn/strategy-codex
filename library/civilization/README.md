# Operator library — civilization (local)

**Local disk only.** PD primary text and bulk exports live here; they are **not** committed to git (see repo-root `.gitignore`).

## Purpose

Witness store for **third-party primary-source text** used in CIV-STATE volume work — aligned with [`public/civ-state/volumes/`](../../public/civ-state/volumes/).

| Subfolder | CIV-STATE volume | Notes |
|-----------|------------------|-------|
| `rome/` | [`public/civ-state/volumes/rome/`](../../public/civ-state/volumes/rome/) | Acquisition manifest: [`rome-pd-acquisition-manifest.yaml`](../../public/civ-state/volumes/rome/rome-pd-acquisition-manifest.yaml) |
| `persia/` | [`persia/`](../../public/civ-state/volumes/persia/) | Scaffold until a volume manifest exists |
| `china/` | [`china/`](../../public/civ-state/volumes/china/) | Scaffold |
| `russia/` | [`russia/`](../../public/civ-state/volumes/russia/) | Scaffold |
| `america/` | [`america/`](../../public/civ-state/volumes/america/) | Scaffold |

## Rome default path

Manifest `local_root` is **`library/civilization/rome`** (relative to strategy-codex repo root). Override with env **`ROME_PD_LIBRARY_ROOT`** or operator profile when needed.

Workflow: [civ-state-primary-text runbook](../../skills/runbooks/civ-state-primary-text.runbook.md) · manifest [rome-pd-acquisition-manifest.yaml](../../public/civ-state/volumes/rome/rome-pd-acquisition-manifest.yaml).

## Migration from flat `library/rome/`

If you already downloaded Rome PD files to the legacy flat path `library/rome/`:

```powershell
# from repo root, only if old flat folder exists and has content
New-Item -ItemType Directory -Force library/civilization/rome
Move-Item library/rome/* library/civilization/rome/ -ErrorAction SilentlyContinue
```

Or keep a custom absolute path via **`ROME_PD_LIBRARY_ROOT`**.

## Not the same as

- **Operator books** — misc folder homes; see [`continuity/README.md`](../../continuity/README.md) § Operator books
- **`source-archive/statecraft/`** — verbatim modern captures in git
- **`public/civ-state/sources/`** — retrieve shelf / bibliography doors (metadata in repo)

Parent index: [`library/README.md`](../README.md).
