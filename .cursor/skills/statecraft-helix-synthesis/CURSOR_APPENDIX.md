## strategy-codex instance

- Root working area for this skill: [continuity/academy/statecraft](../../../continuity/academy/statecraft) with the main control plane under [civ-state/migration](../../../statecraft/states/migration).
- Preferred source stack for synthesis work:
  - lane helixes such as [America helix](../../../continuity/academy/statecraft/america/helix.md)
  - first-wave strand objects under each lane's `civilization/` and `empire/`
  - migration control-plane notes in [civ-state/migration](../../../statecraft/states/migration)
- Preferred generator command after edits:

```powershell
python scripts/build_civ_emp_migration_inventory.py
```

- Preferred validation commands after listed-skill edits:

```powershell
python scripts/sync_portable_skills.py --skill statecraft-helix-synthesis
python scripts/sync_portable_skills.py --verify --skill statecraft-helix-synthesis
python scripts/validate_skills.py
```

- Keep this skill scoped to the statecraft synthesis layer. Do not let it drift into PH-CIV authoring, raw CIV-MEM backfill, or Record-bearing surfaces unless the operator explicitly asks.
