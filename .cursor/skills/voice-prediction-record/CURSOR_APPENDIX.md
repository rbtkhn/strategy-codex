Strategy-codex paths and scripts for **voice-prediction-record**. Replace `<speaker>` with the voice slug (e.g. `freeman`).

## Triggers

- **`voice prediction record`**, **`prediction record`**, **`capture map recurate`**, **`rebuild predictions`**
- With speaker: **`voice prediction record freeman`**

## Path conventions

| Surface | Path |
|---------|------|
| Public map | `statecraft/data/<speaker>-prediction-public-map.json` |
| Capture map | `statecraft/data/<speaker>-prediction-capture-map.json` |
| Thesis map (optional) | `statecraft/data/<speaker>-prediction-thesis-map.json` |
| Auto-file config (optional) | `statecraft/data/<speaker>-prediction-auto-file.json` |
| Generated shelf | `statecraft/voices/<speaker>/<speaker>-predictions.json` · `.md` |
| Wire-events index | `statecraft/voices/<speaker>/<speaker>-prediction-wire-events.md` |
| Shared events | `statecraft/data/event-registry.json` |
| Event doctrine | `docs/statecraft/event-system.md` |
| Runtime registry | `runtime/artifacts/prediction-registry.json` |

## Freeman reference (production today)

Scripts are Freeman-named; **same rules apply to all voices** — clone pattern until generic `--speaker` scripts land.

| Role | Script |
|------|--------|
| Shared validation + registry | `scripts/voice_prediction_pilot.py` |
| Bootstrap / validate capture map | `scripts/bootstrap_voice_capture_map.py --speaker <slug> --check` |
| Build shelf | `scripts/build_voice_predictions.py --speaker <slug>` |
| Shape checker | `scripts/check_voice_predictions.py --speaker <slug>` |
| Auto-materialize (optional) | `scripts/auto_materialize_freeman_predictions.py --prune` |
| Auto-file calibration | `scripts/calibrate_auto_file.py --all-events` |

**Pilot constants** (in `voice_prediction_pilot.py`): `MIN_ANCHOR_WORDS=40`, `MIN_APPEARANCE_WORDS=30`, `MAX_PUBLIC_EXCERPT_WORDS=80`, `ALLOWED_PUBLIC_EXCEPTIONS={short_decisive_sentence}`, `ASR_REPAIR_VALUES` (five tiers), `quote_speaker` ∈ `{guest, host, mixed, operator_summary}`.

**Freeman schema:** `freeman-predictions-v3` — capture map v3 adds `public_excerpt_raw`, `asr_repair`, `quote_speaker`, `host_setup`, `public_display`. Recuration helper: `scripts/recurate_freeman_capture_excerpts.py`.

**Source trail MD** (in `build_voice_predictions.py`): `SOURCE_TRAIL_HEADER = | Date | Channel | Episode | Stance | Excerpt |`; episode column links via `citation.title` + `citation.youtube_url`. Legacy `Appearance` / `Exact words` headers are checker failures. Freeman tests: `test_freeman_source_trail_*` in `tests/test_freeman_predictions.py`.

**Freeman wire-events SSOT:** [statecraft/voices/freeman/freeman-prediction-wire-events.md](../../../statecraft/voices/freeman/freeman-prediction-wire-events.md)

**Freeman wrappers:** `build_freeman_predictions.py`, `check_freeman_predictions.py`, `bootstrap_freeman_capture_map.py` (v1 rebuild + `--check`).

## Validation chain (Freeman)

```bash
python3 scripts/bootstrap_voice_capture_map.py --speaker freeman --check
python3 scripts/build_voice_predictions.py --speaker freeman
python3 scripts/build_voice_predictions.py --speaker freeman --check
python3 scripts/check_voice_predictions.py --speaker freeman
python3 -m pytest tests/test_freeman_predictions.py tests/test_voice_predictions.py -q
```

**Full closure / auto-file chain** (when hooks or registry change):

```bash
python3 scripts/auto_materialize_freeman_predictions.py --prune
python3 scripts/build_prediction_registry.py
python3 scripts/build_prediction_timeline.py
python3 scripts/build_freeman_predictions.py
python3 scripts/calibrate_auto_file.py --all-events
python3 scripts/check_freeman_predictions.py
```

## Generated-manifest enrollment

When a voice has a curated capture map gate, add to [generated-manifest.yaml](../../../generated-manifest.yaml):

```yaml
  - id: <speaker>-prediction-capture-map
    path: statecraft/data/<speaker>-prediction-capture-map.json
    category: work
    generator: scripts/bootstrap_<speaker>_capture_map.py
    check_args: ["--check"]
    drift_group: <speaker>-capture-map
```

Shelf JSON/MD entries mirror Freeman (`freeman-predictions-md` / `freeman-predictions-json` pattern).

## Tests

| Voice | Test module |
|-------|-------------|
| Freeman | `tests/test_freeman_predictions.py` |
| Manifest gate | `tests/test_check_generated_surfaces.py` (capture-map id present) |

## New voice checklist

1. Add `VoiceConfig` entry to `VOICE_REGISTRY` in `scripts/voice_prediction_pilot.py`.
2. Copy Freeman data file naming → `<speaker>-prediction-*.json`
3. Add `tests/test_<speaker>_predictions.py` mirroring Freeman shape tests
4. Author `<speaker>-prediction-wire-events.md`
5. Enroll `generated-manifest.yaml` + pytest manifest assertion
6. Run validation chain; commit as a single voice slice when operator asks

## Registry (SSOT)

Speaker list: `python3 -c "from voice_prediction_pilot import list_voice_speakers; print(list_voice_speakers())"`

Add voices by extending `VOICE_REGISTRY` — paths follow `statecraft/data/<speaker>-prediction-*.json` and `statecraft/voices/<speaker>/<speaker>-predictions.*`.

## Boundary

- non-authoritative; not Record merge
- Do not hand-edit generated `<speaker>-predictions.*`
- Kiev / Kharkov normalization applies in operator-facing MD, not inside verbatim `public_excerpt`
