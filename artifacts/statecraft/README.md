# Statecraft artifacts

This directory holds **derived, rebuildable, non-canonical** statecraft observability outputs.

- `day-dashboard.md` and `day-dashboard.json` are generated from the dated `source-archive/statecraft/YYYY-MM-DD/README.md` day indices, with direct folder parsing as fallback when a local day index is missing.
- Rebuild with `python scripts/build_statecraft_day_dashboard.py`.
- These files are navigation and observability surfaces only; they do not replace the underlying archive captures or day indices.
