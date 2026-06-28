# Contributing

Thank you for improving **Civilizational Statecraft**.

## Canonical rule

**Public canonical text lives in this repository (`rbtkhn/civ-state`).**  
The upstream workshop drafts source memory and publishes via export — not by silent dual edit.

## How to propose changes

1. **Small fixes** (typos, broken links, clarity): open a PR against this repo.
2. **Substantive judgment changes** (essays, comparative claims, shelf structure): open an issue describing the mechanism and counterweight. Maintainers may replay through the workshop export pipeline for the next tagged release.

## What we merge here directly

- Link fixes, formatting, and reader-navigation improvements
- Primary-source edition pointers when rights-clear
- Export-regenerated slices that match an approved workshop release

## What we do not merge without export receipt

- Large essay rewrites that bypass the workshop source-lattice
- Operator routing, transactions, or lane-deploy material
- Cross-references to external lecture corpora (this book is self-contained)

## Export pipeline

Maintainers regenerate from the upstream workshop export pipeline:

```bash
export_civilizational_statecraft_public.py
validate_civilizational_statecraft_public.py
```

See [FOUNDING-PROVENANCE.md](FOUNDING-PROVENANCE.md) and [EXPORT-RECEIPT.md](FOUNDING-PROVENANCE.md).

## Code of conduct

Be precise, cite sources, preserve counterweights, and do not flatten civilizational tension for narrative smoothness.
