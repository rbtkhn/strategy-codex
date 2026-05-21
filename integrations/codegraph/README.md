# CodeGraph Pilot Integration

This directory holds a **bounded CodeGraph pilot** for `strategy-codex`.

## Scope

Use this pilot for:

- code exploration against `src/`, `scripts/`, and integration code
- pre-edit impact review using CodeGraph context and `affected`
- architecture-context export for deck or bundle preparation

Do **not** use this pilot as:

- a recursion-gate path
- a governed-state path
- a replacement for source review on doc-heavy or Record-heavy work

## Pilot Commands

Initialize or refresh the local CodeGraph index:

```bash
npx @colbymchenry/codegraph install --target=codex --location=local --yes
npx @colbymchenry/codegraph status -j
```

Export a bounded context packet plus Markdown report:

```bash
python -m integrations.codegraph.export_code_context \
  --task "presentation service architecture" \
  --symbol "PresentationService" \
  --changed-file "src/grace_mar/presentations/service.py" \
  --output "service-architecture.json" \
  --markdown-output "service-architecture.md"
```

Build a Presenton-oriented architecture bundle from that export:

```bash
python -m integrations.codegraph.generate_architecture_bundle \
  --input artifacts/codegraph/service-architecture.json \
  --output artifacts/presentations/codegraph-service-architecture.bundle.json \
  --title "Strategy-Codex Presentation Service Architecture"
```

## Pilot Success Thresholds

Expand beyond this pilot only if local workflow evidence shows:

- at least **20% lower cost** on code-heavy sessions
- at least **30% faster** code exploration or impact review
- at least **15% lower prep time** for one architecture/deck workflow
- no governance or local-sovereignty regressions

## Notes

- `.codegraph/` stays local and should remain gitignored.
- `artifacts/codegraph/` outputs are rebuildable WORK artifacts, not canonical truth.
- The deck path intentionally reuses the existing `grace_mar.presentations.contract` bundle contract instead of introducing a separate presentation schema.

