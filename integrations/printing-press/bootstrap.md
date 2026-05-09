# Printing Press bootstrap

This file records manual operator-reviewed commands for trying Printing Press. It is documentation only; Strategy-Codex does not auto-install Printing Press or its CLIs.

## Prerequisites

- Go 1.23+ when using the factory or generated Go CLIs.
- Node.js / `npx` for Printing Press install commands.
- Operator review before any CLI receives credentials, cookies, write access, or private account context.

## Starter pack

```bash
npx -y @mvanhorn/printing-press install starter-pack
```

Printing Press documentation describes the starter pack as installing example CLIs such as:

- `espn`
- `flight-goat`
- `movie-goat`
- `recipe-goat`

These are not Strategy-Codex priorities; use them only to confirm the toolchain.

## Candidate installs

Install candidates one at a time after admission review. Do not batch install into daily workflow before smoke tests.

```bash
# Pilot 1: already represented by the repo adapter
npx -y @mvanhorn/printing-press install scrape-creators

# Pilot 2: company / competitor research
npx -y @mvanhorn/printing-press install company-goat
```

Later candidates:

```bash
npx -y @mvanhorn/printing-press install hackernews nvd
npx -y @mvanhorn/printing-press install agent-capture linear
npx -y @mvanhorn/printing-press install archive-is ahrefs yahoo-finance firecrawl
```

`agent-capture` and `linear` require extra review because they may touch local UI, account data, or workflow state.

## Verify

```bash
npx -y @mvanhorn/printing-press list
scrape-creators --help
company-goat --help
```

If a generated binary uses a different command name, record the actual command in the relevant pilot dossier before wrapping it.

## Update

```bash
npx -y @mvanhorn/printing-press update all
```

Update only after noting which local pilots depend on the changed CLI. Re-run smoke tests and keep receipts.

## After a successful smoke test

1. Record command, source URL, tool version, output path, and receipt path.
2. Add or update a pilot dossier under `integrations/printing-press/<cli>/`.
3. Create a portable skill draft under `skills-portable/_drafts/<skill>/SKILL.md`.
4. Promote to `skills-portable/manifest.yaml` only after a separate operator decision.
