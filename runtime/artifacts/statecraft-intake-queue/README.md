# Statecraft intake queue (derived sidecars)

Non-canonical **runtime / derived** queue metadata for statecraft archive captures. Sidecars sit between verbatim archive and daily synthesis.

**Spec:** [docs/statecraft-intake-queue.md](../../docs/statecraft-intake-queue.md)

**Schema:** [schemas/registry/statecraft-intake-sidecar.v1.json](../../schemas/registry/statecraft-intake-sidecar.v1.json)

## Layout

```text
runtime/artifacts/statecraft-intake-queue/<pub_date>/<source-stem>.v1.json
```

Optional committed digests: `digest-YYYY-MM-DD.md` when the digest supports a ship decision.

## Rebuild

```bash
python3 scripts/statecraft_intake_queue.py --day YYYY-MM-DD --emit-sidecars
python3 scripts/statecraft_intake_queue.py --day YYYY-MM-DD --write-digest --digest-out runtime/artifacts/statecraft-intake-queue/digest-YYYY-MM-DD.md
```

Default: `*.json` sidecars are **gitignored**. They are rebuildable from archive frontmatter + daily sync — not Record truth.
