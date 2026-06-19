Grace-mar paths and commands for this repository.

| Topic | Path |
|--------|------|
| Canonical raw-input tree | [codex/](../../codex/) |
| Host quality reports | [runtime/artifacts/host-shelf-quality/](../../../runtime/artifacts/host-shelf-quality/) |
| Materializer / validator | [scripts/materialize_youtube_raw_input.py](../../../scripts/materialize_youtube_raw_input.py) |
| Quality reporter | [scripts/host_shelf_quality.py](../../../scripts/host_shelf_quality.py) |
| Portable skill manifest | [skills/manifest.yaml](../../../skills/manifest.yaml) |
| Sync script | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |

**Local validation pattern**

```powershell
python scripts/materialize_youtube_raw_input.py --raw-input "<raw-input-path>" --notebook-root "codex/<year>" --apply --with-appearances --purpose one-off --run-id "<label>"
```

For check-streams or densification follow-up, preserve the existing `--purpose` and `--tranche-label` from the capture pass.
