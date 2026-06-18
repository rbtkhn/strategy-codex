# Contributing

Thank you for improving **Civilizational Statecraft**.

## Canonical rule

**Public canonical text lives in this repository (`rbtkhn/civ-state`).**  
Edit ship-bound prose in the workspace staging mirror (`public/civ-state/`) and publish via the explicit publish script — not by silent dual edit elsewhere in the monorepo.

## How to propose changes

1. **Small fixes** (typos, broken links, clarity): open a PR against this repo.
2. **Substantive judgment changes** (essays, comparative claims, shelf structure): open an issue describing the mechanism and counterweight. Maintainers land approved prose in `public/civ-state/` and publish on the next tagged release.

## What we merge here directly

- Link fixes, formatting, and reader-navigation improvements
- Primary-source edition pointers when rights-clear
- Staging-mirror slices that match an approved release

## What we do not merge without maintainer receipt

- Large essay rewrites that bypass the public source-lattice discipline
- Operator routing, transactions, or lane-deploy material
- Cross-references to external lecture corpora (this book is self-contained)

## Publish pipeline

Maintainers validate and publish from the staging mirror:

```bash
validate_civilizational_statecraft_public.py public/civ-state
publish_public_civ_state.py -m "…" --push
```

See [FOUNDING-PROVENANCE.md](FOUNDING-PROVENANCE.md) and [EXPORT-RECEIPT.md](EXPORT-RECEIPT.md).

## Code of conduct

Be precise, cite sources, preserve counterweights, and do not flatten civilizational tension for narrative smoothness.
