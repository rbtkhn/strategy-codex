<!-- Example output shape; regenerate via run_diagnostics + render_diagnostics_report -->

# Diagnostics report — grace-mar

Run:

```bash
python scripts/work_dev/run_diagnostics.py --config docs/diagnostics/fixtures/sample_input.yaml --json-out /tmp/d.json
python scripts/work_dev/render_diagnostics_report.py --input /tmp/d.json -o docs/diagnostics/fixtures/sample_report.generated.md
```
