WORK only; not Record.

# voices/states namespace migration — 2026-06-13

Purpose: seal `statecraft/civ-lens` → `statecraft/voices` and `statecraft/civ-state` → `statecraft/states` hard cutover.

## Verified

- Canonical live synthesis namespace: `statecraft/voices/`
- Canonical source-memory path: `statecraft/states/`
- Profile template: `statecraft/voices/voice-profile-template.md` (legacy `voices-profile-template.md` redirects)
- `statecraft/speakers/README.md` is the **only** compatibility stub → `voices/`
- Submodule gitlink: `statecraft/voices/jiang/ph-civ` (`.gitmodules` + `git ls-files --stage`)
- ph-civ submodule: 48 chapter README bridge URLs updated to `statecraft/states/` (submodule commit `0e3cade`)

## Checks run (2026-06-13)

```
python scripts/rehome_statecraft_namespace.py --check
# check ok: no statecraft/civ-lens or statecraft/civ-state outside exclusions

python scripts/validate_repo_routing.py
# ok: repo routing validation passed

python scripts/validate_ph_civ_transcript_boundary.py --staged
# PH-CIV transcript boundary OK

python scripts/validate_civ_state_eras.py
# CIV-STATE era doctrine valid.

python scripts/validate_civ_state_primary_texts.py
# CIV-STATE primary-text layer valid.

pytest tests/test_rehome_path_hygiene_contract.py tests/test_speaker_orthogonality_contract.py tests/test_validate_ph_civ_transcript_boundary.py tests/test_operator_handoff_check.py -q
# 10 passed; 2 failed (pre-existing Record-frozen gate tests — not rename-related)

python scripts/check_academy_mirror_sync.py
# parent_gitlink_matches_nested: ok (ca7bf04); nested_matches_remote: fail until submodule pushed to rbtkhn/ph-civ
```

Second `--apply` pass added **72** relative-link replacements in **32** files (`../../civ-state/` → `../../states/`, etc.).

## ph-civ submodule commits

- `0e3cade` — 48 chapter README bridge URLs → `statecraft/states/`
- `ca7bf04` — ASR blocklist `source_script` path metadata

Parent gitlink: `ca7bf04d72ec781b7229ff3dfb9db36b583cf0da`

## Windows submodule note

After path move: `git submodule sync --recursive` from repo root. If gitlink desyncs, re-init `statecraft/voices/jiang/ph-civ`.

## Intentional exclusions

- `artifacts/benchmarks/` may retain historical `civ-lens` / `civ-state` path strings
- Inner volume dirs remain `civ-state-america/` etc.
- Skill IDs remain `statecraft-civ-state`, `civ-state-volume-harden`, etc.

## Boundary

No further namespace action required for this cutover.
