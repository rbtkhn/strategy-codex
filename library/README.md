# Operator library (local)

**Local disk only.** Binaries and bulk text live here; they are **not** committed to git (see repo-root `.gitignore`).

## Layout invariant

**Only** `civilization/` and `science/` may exist as subdirectories at `library/` root.

Flat volume paths such as `library/rome/` are **retired** — use `library/civilization/{volume}/` instead (e.g. `library/civilization/rome/`).

## Namespaces

| Namespace | Purpose | Index |
|-----------|---------|-------|
| `civilization/` | CIV-STATE PD primary text / offline exports | [civilization/README.md](civilization/README.md) |
| `science/` | Singularity-science offline PDFs, ebooks, exports | [science/README.md](science/README.md) |

## Civilization volumes

Witness store aligned with `public/civ-state/volumes/{rome,persia,china,russia,america}/`.

| Subfolder | CIV-STATE volume | Notes |
|-----------|------------------|-------|
| `civilization/rome/` | `public/civ-state/volumes/rome/` | Acquisition manifest: `rome-pd-acquisition-manifest.yaml` |
| `civilization/persia/` | `persia/` | Scaffold until a volume manifest exists |
| `civilization/china/` | `china/` | Scaffold |
| `civilization/russia/` | `russia/` | Scaffold |
| `civilization/america/` | `america/` | Scaffold |

Rome manifest `local_root` is **`library/civilization/rome`** (relative to strategy-codex repo root). Override with env **`ROME_PD_LIBRARY_ROOT`** or operator profile when needed.

## Science streams

Local shelf aligned with [`research/singularity-science/`](../research/singularity-science/README.md).

| Subfolder | Research stream |
|-----------|-----------------|
| `science/innermost-loop/` | `research/singularity-science/innermost-loop/` |
| `science/moonshots/` | `research/singularity-science/moonshots/` |

## Not the same as

- **Operator books** — misc folder homes; see [`continuity/README.md`](../continuity/README.md) § Operator books
- **`source-archive/statecraft/`** — verbatim modern captures in git
- **`source-archive/singularity/`** — verbatim singularity captures in git
- **`public/civ-state/sources/`** — retrieve shelf / bibliography doors (metadata in repo)
- **`research/singularity-science/`** — durable analysis in repo (not local binaries)

Workflow (civilization): [civ-state-primary-text runbook](../skills/runbooks/civ-state-primary-text.runbook.md) · manifest [rome-pd-acquisition-manifest.yaml](../public/civ-state/volumes/rome/rome-pd-acquisition-manifest.yaml).
