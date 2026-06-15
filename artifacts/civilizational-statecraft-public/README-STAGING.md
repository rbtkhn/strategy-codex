# Civilizational Statecraft — export staging bucket

**Derived snapshot — not the canonical public book.**

| Surface | Role |
|---------|------|
| **Canonical public book** | [rbtkhn/civ-state](https://github.com/rbtkhn/civ-state) |
| **Workshop SSOT** | [`statecraft/states/`](../../statecraft/states/) |
| **This folder** | Last exported staging tree before publish |

## Regenerate

From repo root:

```bash
python3 scripts/export_civilizational_statecraft_public.py
python3 scripts/validate_civilizational_statecraft_public.py
```

Publish clone with legacy archive present:

```bash
python3 scripts/export_civilizational_statecraft_public.py --output /path/to/civ-state-clone
python3 scripts/export_civilizational_statecraft_public.py --output /path/to/civ-state-clone --legacy-archive-only
python3 scripts/validate_civilizational_statecraft_public.py --no-default-exclude /path/to/civ-state-clone
```

## Validate

| Check | Command |
|-------|---------|
| Staging book (default) | `python3 scripts/validate_civilizational_statecraft_public.py` |
| Full publish tree | `python3 scripts/validate_civilizational_statecraft_public.py --no-default-exclude /path/to/civ-state-clone` |
| Book only (exclude archive) | `python3 scripts/validate_civilizational_statecraft_public.py --exclude archive /path/to/civ-state-clone` |

Default validator excludes top-level `archive/` per manifest — book corpus lint only.

## Commit policy

Commit this folder when a **public release tag** ships to `rbtkhn/civ-state`, so the workshop retains a diffable receipt aligned to the tag. Do not treat local edits here as updating the public book without export + publish.

Receipt: [EXPORT-RECEIPT.md](EXPORT-RECEIPT.md) · Boundary: [docs/civilizational-statecraft-external-boundary.md](../../docs/civilizational-statecraft-external-boundary.md)
