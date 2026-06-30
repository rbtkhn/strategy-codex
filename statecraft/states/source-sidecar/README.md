# Source Sidecar

This surface is non-authoritative and subject to revision.

This folder holds lawful sidecar full-text payloads and small sidecar manifests keyed by `source_id`.

The sidecar exists so CIV-STATE can keep:

- source records in the main structured registry
- excerpts in bounded readable form
- full texts in a deeper payload layer

Use full-text sidecar storage only for sources whose rights class safely permits it, such as:

- `public_domain`
- `official_government_text`
- `operator_authored_transcription`

This folder should stay deterministic and file-backed. The first pass is intentionally simple and does not attempt a database architecture.
