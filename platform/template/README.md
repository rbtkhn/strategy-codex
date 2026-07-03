# Work domain template

- **[DOMAIN.md](DOMAIN.md)** â€” scaffold for a **`work-<slug>/`** directory with an uppercase **`<SLUG>.md`** wisdom surface (e.g. `politics` â†’ `work-politics/POLITICS.md`).
- **Create an instance:** from repo root, `python3 scripts/create-domain.py <name>`.
- **Migrate existing `docs/archive/skill-work-legacy/work-*` lanes:** dry-run first, then `python3 scripts/migrate-to-domain-surface.py --execute` (see script docstring). Backups go under `backups/domain-migration/` (gitignored).
- **work-strategy canonical ledger** in-repo: `docs/archive/skill-work-legacy/work-strategy/STRATEGY.md` (not `civilizational-strategy-surface.md`; a stub may redirect).

Placeholders in the template (`{{DOMAIN}}`, `{{DOMAIN_TITLE}}`, `{{DOMAIN_LOWER}}`) are filled by the script. Do not use a bare substring replace for `DOMAIN` in prose (it would corrupt words like â€œcross-domainâ€). Link targets `../AGENTS.md` and `../self.md` are rebased by `scripts/_domain_surface_links.py` when generating files under `docs/archive/skill-work-legacy/`.

