# Example: company-goat pilot dossier

Status: example only
CLI: `company-goat`
Purpose: prove Printing Press value for company, competitor, and market research inside work-strategy.

## Candidate use

`company-goat` should help answer questions such as:

- What is this company building?
- Who are its competitors?
- What public signals matter for Strategy-Codex positioning?
- Which claims require corroboration before entering a strategy note?

## Example smoke

```bash
company-goat --help
company-goat research "xAI" --agent
```

Record the real command shape after install; do not assume this example matches the generated binary until verified.

## Expected output handling

- Save compact output under `runtime/artifacts/printing-press/company-goat/`.
- Record command, query, fetched date, tool version, and output path.
- Route useful insights to work-strategy notes or a review packet.
- Do not stage Record candidates unless the operator separately asks for a governed Record update.

## Admission notes

- Treat output as research input, not neutral fact.
- Prefer company websites, filings, docs, and primary sources when strong claims matter.
- Keep public benchmark/token claims labeled as Printing Press project claims until local context-efficiency receipts exist.

## Success criteria

The pilot is useful if it produces a compact company brief that is faster to load than manual web research and clear enough to support a Strategy-Codex decision or positioning note.
