# CIV-STATE Game Substrate

WORK only; not Record.

Machine companion layer for strategy games, sims, and mods. The **five-volume book** stays human-first under `volumes/`; this folder holds **typed extracts**—profiles, pattern schemas, settlement clauses, and future engine adapters.

**Not exported to the public book by default.** See [CIV-STATE → Game Systems Mapping](../civ-state-game-systems-mapping.md) and [external boundary](../../../docs/civilizational-statecraft-external-boundary.md).

## Start here

| Artifact | Purpose |
|----------|---------|
| [Profile schema v0.1](profile-schema-v0.1.md) | Faction package field law + validation rules |
| [Persia.pkg.yaml](profiles/persia.pkg.yaml) | Reference implementation (Vol II) |
| [parity-rival.schema.yaml](schemas/parity-rival.schema.yaml) | Pattern card → state machine |
| [settlement clauses v0.1](settlement/clauses-v0.1.yaml) | Shared clause library |
| [Game systems mapping](../civ-state-game-systems-mapping.md) | One-page engine bridge |

## Layout

```text
game-substrate/
├── README.md
├── profile-schema-v0.1.md
├── schemas/           # pattern + clause shapes
├── profiles/          # volume packages (*.pkg.yaml)
├── settlement/        # clause library
└── adapters/          # engine bindings (future)
```

## Validation (manual v0.1)

Before shipping a profile:

1. Every `book_anchor` path must exist under `statecraft/states/`.
2. At least one `counterweight` per primary pattern.
3. Every `red_line` maps to a settlement `clause_id` veto or `hard_reject`.
4. `continuity_script` must match a known script id in the schema doc.
5. No profile without `governing_pair_default` and `recovery_triggers`.

Future: `scripts/validate_civ_state_game_profiles.py`.

## Related book doors

- [Volume II Persia](../volumes/civ-state-persia/README.md)
- [Parity rival](../framework/patterns/parity-rival.md)
- [Continuity mechanism](../framework/continuity.md)
- [Framework shelf](../framework/README.md)
