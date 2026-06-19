# Printing Press integration

Status: governed bootstrap
Tier posture: candidate Tier-1 tooling layer after two local pilots

Printing Press is a promising WORK-layer source for agent-native CLIs: compact command output, local mirrors, compound commands, and generated skill wrappers. Strategy-Codex should treat it with governed enthusiasm: high upside, but earned adoption.

Printing Press does not replace the Record, the Voice, the gate, or existing transcript/source discipline. It is an external tooling rail that can feed WORK surfaces when admitted through docs, tests, receipts, and operator review.

## Why it matters here

- **Context efficiency:** CLI output can be shorter and cleaner than raw API or MCP dumps. Public benchmark claims remain project claims until Strategy-Codex has local receipts.
- **Portable skills:** PP-generated workflows can become Codex portable skills after the normal draft-to-listed path.
- **Cognition stream intake:** Public discourse and research CLIs can feed work-strategy, transcript analysis, Perceiver, LEARN MODE, and source review.
- **Governance fit:** Every PP tool must stay WORK-layer unless a separate governed process stages and approves Record changes.

## Tier-1 threshold

Printing Press may be described as Tier-1 in repo docs only after two local pilots pass:

1. `scrape-creators` - public YouTube transcript/video metadata intake for the cognition stream.
2. `company-goat` - company and competitor research for strategy intelligence.

Until then, use "candidate Tier-1 tooling layer" or "governed pilot."

## Contents

- [bootstrap.md](bootstrap.md) - manual operator-reviewed install and update commands.
- [priority-clis.md](priority-clis.md) - candidate CLI order and safety notes.
- [codex-skill-template.md](codex-skill-template.md) - wrapper template for PP-derived portable skill drafts.
- [scrape-creators/](scrape-creators/) - implemented pilot 1.
- [examples/](examples/) - example dossiers for future pilots.

## Non-goals

- No automatic `npx`, Go install, or network setup from repo scripts.
- No manifest promotion before a smoke-tested pilot.
- No direct writes to `self.md`, `self-archive.md`, `recursion-gate.md`, `session-log.md`, or `archive/grace-mar-instance/bot/prompt.py`.
- No credentialed scraping or private-account capture by default.
