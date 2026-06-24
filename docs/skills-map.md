# Skills map — strategy-codex

Operator-facing index for the skill system. Pipeline detail: [skills/README.md](../skills/README.md). Field spec: [skills/_schema.md](../skills/_schema.md).

## Where things live

| Surface | Path | Role |
|---------|------|------|
| **Portable core** | `skills/<name>/SKILL.md` | Hand-edited methodology; SSOT for manifest-listed skills |
| **Cursor target** | `.cursor/skills/<name>/SKILL.md` | Generated — run `python3 scripts/sync_portable_skills.py` after portable edits |
| **Appendix** | `.cursor/skills/<name>/CURSOR_APPENDIX.md` | Host-only paths and commands |
| **Manifest** | `skills/manifest.yaml` | Promoted portable inventory + sync mapping |
| **Runbooks** | `skills/runbooks/*.runbook.md` | Multi-skill composed workflows |
| **Drafts** | `skills/_drafts/<name>/SKILL.md` | Experimental; not manifest-listed |
| **Inventory** | `runtime/artifacts/skill-inventory.md` | Generated — `python3 scripts/generate_skill_inventory.py` |
| **Domain-pack triage** | `runtime/artifacts/domain-pack-triage.md` | Generated — `python3 scripts/generate_domain_pack_triage.py` (disposition SSOT during consolidation) |
| **External cadence** | `~/.codex/skills/coffee/` | Host-installed; not in repo manifest |

## Six categories

| Category | Purpose | Examples |
|----------|---------|----------|
| `truth-pipeline` | Source accuracy, intake, verification, synthesis | `statecraft-source-intake`, `check-sources`, `news-verify`, `state-synthesis` |
| `operator-coherence` | Cadence, memory, repo hygiene | `coffee` (external), `dream`, `bridge`, `memory`, `recursive-learn` |
| `judgment-enhancement` | Interpretation quality (not intake) | `primary-overhearing-analysis`, `statecraft-intelligence-essay`, `tufte-data-viz` |
| `domain-pack` | Lane-specific when domain is active | `civ-state`, `politics-massie`, `state-america` (cursor) |
| `product-narrative` | Commercial, book, voice product | `product-strategy`, `skill-narrative`, `arc-to-chapter-seeds` |
| `legacy-redirect` | Thin compatibility alias only | `wire-verify` → `news-verify`, `tri-mind` → `periodic-statecraft-review`, `last30days` → runbook |

## Skill vs runbook

- **Skill** — single reusable primitive (`skills/<name>/SKILL.md`).
- **Runbook** — sequences skills with gates and verification (`skills/runbooks/*.runbook.md`).

Use a runbook when the workflow mainly chains multiple skills (e.g. **`runbook transcript intake`**, **`runbook venture ideation`**). Do not add a new top-level skill for every repeated chain.

Runbook catalog: [skills/runbooks/README.md](../skills/runbooks/README.md).

## Domain packs

- **CIV-STATE:** [skills/civ-state/SKILL.md](../skills/civ-state/SKILL.md) — entry skill; sub-skills and runbooks listed in **Domain pack** section.
- **Statecraft openers:** [docs/skills/statecraft-opener-pack.md](statecraft-opener-pack.md) — `state-america`, `state-china`, etc. (cursor-only).
- **Product:** [skills/product-strategy/SKILL.md](../skills/product-strategy/SKILL.md) — umbrella for ideation / MTP / ventures (legacy: `ideation-engine`, `mtp`, `abundance-native-ventures`).

## Promotion path

```text
session pattern
  → skills/skill-candidates.md (one row)
  → skills/_drafts/<name>/SKILL.md
  → tested in ≥2 real uses + ## Verification / Proof Standard
  → skills/<name>/SKILL.md + manifest.yaml entry
  → python3 scripts/sync_portable_skills.py
```

**Draft expiration:** drafts older than **30 days** must be promoted, merged, archived, or explicitly renewed (validator info warning).

## Validation

```bash
python3 scripts/validate_skills.py
python3 scripts/validate_skills.py --strict-metadata
python3 scripts/validate_skills.py --strict-verification   # migration gate
python3 scripts/generate_skill_inventory.py
```

## Recommended active surface (post-consolidation)

Rough promoted set (~45 manifest skills including redirects):

- **Truth:** intake, clean, check-sources, news-verify, state-note, state-synthesis, packet-before-synthesis
- **Operator:** memory, recursive-learn, repo-hygiene-pass, portable-skills-sync, extract-skill-from-session
- **Judgment:** primary-overhearing-analysis, statecraft-intelligence-essay, tufte-data-viz; periodic review via **`periodic-statecraft-review`** runbook
- **Domain:** civ-state, politics-massie, jurisdiction-campaign-history, work-jiang-ingest-fallback
- **Product:** product-strategy, voice-profile-panel, skill-narrative
- **Legacy redirects:** wire-verify, check-streams, cognition-streams, strategy-notebook-*, ideation-engine, mtp, abundance-native-ventures, last30days, monthly-deepening

Full inventory: `runtime/artifacts/skill-inventory.md`.
