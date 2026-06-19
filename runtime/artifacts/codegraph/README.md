# CodeGraph Artifacts

This folder holds **derived, rebuildable** outputs from the bounded CodeGraph pilot.

Typical contents:

- context export JSON
- Markdown companion reports
- pilot comparison notes or manifests

These files are **WORK-only** and **non-canonical**:

- not governed state
- not recursion-gate input
- not a substitute for reading source code directly

Recommended workflow:

1. Regenerate the export from the current local `.codegraph/` index.
2. Use the export to support code exploration, impact review, or architecture prep.
3. Treat any presentation bundle or Markdown report as a convenience layer, not authority.

The directory contents are gitignored by default except for this README.

