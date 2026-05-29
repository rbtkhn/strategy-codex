WORK only; not Record.

# civ-lens migration verification - 2026-05-29

Purpose: seal the namespace migration from `statecraft/speakers/` to `statecraft/civ-lens/` with one compact verification receipt.

## Verified

- Canonical live shelf namespace is `statecraft/civ-lens/`.
- Canonical migrated shelf shape is `statecraft/civ-lens/civ-lens-<speaker>/`.
- `statecraft/speakers/README.md` is a compatibility-only redirect surface, not a parallel authority path.
- Jiang mirror gitlink is live at `statecraft/civ-lens/civ-lens-jiang/ph-civ`.
- `civ-lens-diesen/` is promoted as a truthful first-pass canonical shelf rather than a forced month-ladder shelf.

## Checks run

- Repo grep over live docs, skills, scripts, tests, and statecraft surfaces reduced old `statecraft/speakers` claims to the intentional compatibility stub.
- [tests/test_rehome_path_hygiene_contract.py](/C:/dev/strategy-codex/tests/test_rehome_path_hygiene_contract.py) passed via `.venv\Scripts\python.exe`.
- [tests/test_validate_speaker_state_sets.py](/C:/dev/strategy-codex/tests/test_validate_speaker_state_sets.py) passed via `.venv\Scripts\python.exe`.
- `git ls-files --stage` shows the Jiang gitlink at `statecraft/civ-lens/civ-lens-jiang/ph-civ` and `.gitmodules` points to the same path.

## Intentional exclusions

- Benchmark provenance under `artifacts/benchmarks/` is explicitly excluded by [tests/fixtures/rehome_path_hygiene_contract.json](/C:/dev/strategy-codex/tests/fixtures/rehome_path_hygiene_contract.json).
- Remaining old `codex/2026/...` strings in those benchmark source packs and outputs are historical evaluation residue, not live path authority.

## Boundary

No further action recommended for the namespace migration itself.

If a later pass wants to modernize benchmark fixtures, treat that as separate benchmark-maintenance work rather than as unfinished `civ-lens` migration cleanup.
