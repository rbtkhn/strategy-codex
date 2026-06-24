# Runbooks (composed workflows)

**Purpose:** Runbooks compose multiple portable **skills** into larger workflows with handoff points, stop conditions, and verification requirements.

| Layer | Answers | Example |
|-------|---------|---------|
| **Skill** | What can this agent do? | `statecraft-source-intake` |
| **Runbook** | What can this workflow reliably produce? | `source-to-daily-synthesis.runbook.md` |
| **Wrapper / catalog** | How do humans discover it? | [catalog.md](../catalog.md), [workflow-wrapper-schema.md](../../docs/skills/workflow-wrapper-schema.md) |
| **Coffee / object ritual** | What is the session-scoped pass on one object? | Conductor compression into coffee hub (legacy) |

**Rule:** Runbooks **reference** skill methodology; they do not re-teach it. Edit the portable skill when methodology changes; edit the runbook when step order, gates, or verification change.

## Where composition lives

- **Skill** — portable primitive under `skills/<name>/SKILL.md`
- **Runbook** — multi-skill workflow under `skills/runbooks/*.runbook.md`
- **Wrapper / catalog** — human onboarding; derivative only
- **Conductor / coffee object ritual** — session-scoped object pass (compressed into coffee hub)

## Schema

Full spec: [_schema.md](_schema.md)

Validate with:

```bash
python3 scripts/validate_skills.py
```

## Catalog

| Runbook | Trigger (operator phrase) | Skills chain |
|---------|---------------------------|--------------|
| `source-to-daily-synthesis` | `runbook source to daily` / landed transcript → daily candidate | `statecraft-source-intake` → `state-synthesis` |
| `source-to-transaction-fit` | `runbook transaction fit` / verified source → fit class | `statecraft-source-intake`, `state-synthesis` + transaction router sheet |
| `transcript-to-state-note` | `runbook state note` / transcript wedge → one note | `statecraft-source-intake` → `state-note` |
| `transcript-intake` | `runbook transcript intake` / ASR cleanup chain | `youtube-raw-input-transcript` → `transcript-cleanup` → `transcript-proper-noun-normalization` → `source-clean` |
| `periodic-statecraft-review` | `runbook periodic review` / `runbook last30` | `state-synthesis` · `primary-overhearing-analysis` · optional `statecraft-intelligence-essay` (`last30days` / `monthly-deepening` redirect here) |
| `civ-state-primary-text` | `runbook civ state primary text` | `civ-state` → `civ-state-primary-text-acquisition` |
| `civ-state-volume-hardening` | `runbook civ state harden` | `civ-state` → `civ-state-volume-harden` |
| `venture-ideation` | `runbook venture ideation` | `ideation-engine` → `mtp` → `abundance-native-ventures` |
| `chapter-seeding` | `runbook chapter seed` | `arc-to-chapter-seeds` + PH/book Cursor skills |
| `voice-profile-review` | `runbook voice profile review` | `voice-profile-panel` |
| `mtp-coffee-dream` | `runbook mtp coffee dream` (reference) | → `venture-ideation` cadence table |

## Discovery ladder

Runbooks are not skills. Capture new **skills** via [skill-candidates.md](../skill-candidates.md) → [_drafts/](../_drafts/) → manifest. Capture new **workflows** by adding a runbook here when the same multi-skill chain repeats.

## Cross-host

Portable runbook markdown can be pasted into any agent host. See [docs/skills/cross-host-install.md](../../docs/skills/cross-host-install.md).

## Return paths

- [skills/README.md](../README.md)
- [skills/_schema.md](../_schema.md)
- [docs/skills-map.md](../../docs/skills-map.md)
- [docs/harness-architecture-map.md](../../docs/harness-architecture-map.md)
