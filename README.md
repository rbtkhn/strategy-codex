# strategy-codex

**strategy-codex** - The active development repo for strategy-first companion systems, notebook tooling, and governed cognitive-fork infrastructure. It currently carries the **Grace-Mar** reference instance plus related strategy and civ-mem surfaces. **Terminology:** [docs/glossary.md](docs/glossary.md).

**Repo identity:** `strategy-codex` is now the development home. The Grace-Mar reference surfaces now live at the repository root (`self.md`, `self-archive.md`, `recursion-gate.md`, `session-log.md`, `self-skills.md`, `self-library.md`, and `grace-mar-llm.txt`) rather than under a nested instance directory.

**Strategy-codex corpus:** [`codex/`](codex/README.md) is the first-class home for the polyphonic cognition streams, raw inputs, chapters, compiled views, and strategy-codex artifacts. The old `docs/skill-work/work-strategy/strategy-notebook/` path is deprecated compatibility only.

**New here?** Plain-language orientation and audience paths: [docs/start-here.md](docs/start-here.md) â€” quick pick [Choose your path](docs/start-here.md#choose-your-path) (Aâ€“F).

If you come from **OB1-style** memory systems (dashboard, recipes, imports, review queue), the quickest mental model is: the repo has a **Library**, **Skills**, **Evidence** log, **workflow** lanes, and an **Approval Inbox** (`recursion-gate.md`). Durable Record changes are **gated**, not auto-merged. **[Coming from OB1? Start here â†’](docs/start-here-ob1-users.md)**

## Claude Code surfaces

If you come from **Claude Code** workflows, the fastest mental model is:

- **Skills** â†’ the repo has portable skills plus skill-adjacent runtime helpers and operator doctrine.
- **Commands / workflows** â†’ the repo has explicit operator flows for retrieval, compression, prepared context, review, and export.
- **Memory** â†’ the repo separates **runtime memory** from the **canonical Record**; runtime recall can assist, but durable truth stays gated.
- **Rules / boundaries** â†’ the repo uses explicit boundary docs, source-of-truth order, authority mapping, and no-merge-without-approval constraints.
- **Review queue** â†’ durable changes flow through the **Approval Inbox** (`recursion-gate.md`) and related review artifacts, not silent mutation.
- **Reference state** â†’ the forkâ€™s canonical surfaces are **SELF**, **SELF-LIBRARY**, **SKILLS**, and **EVIDENCE**.

A simple Claude Code-style translation is:

| Claude Code mental model | strategy-codex equivalent |
|---|---|
| Skills | `docs/skills/`, skill-card artifacts, capability doctrine |
| Commands / orchestrations | retrieval, compression, export, and review scripts under `scripts/` |
| Memory | `runtime/`, `prepared-context/`, and runtime observation flows |
| Rules / instructions | boundary docs, authority map, source-of-truth order, runtime-vs-Record rules |
| Review / approval | `recursion-gate.md`, review queue artifacts, gate-review workflow |
| Durable state | **SELF**, **SELF-LIBRARY**, **SKILLS**, **EVIDENCE** |

Start here:

- **Architecture overview** â†’ [docs/architecture.md](docs/architecture.md)
- **Runtime vs Record** â†’ [docs/runtime-vs-record.md](docs/runtime-vs-record.md)
- **Start-here guide** â†’ [docs/start-here.md](docs/start-here.md)
- **OB1-style translation** â†’ [docs/start-here-ob1-users.md](docs/start-here-ob1-users.md)
- Want to see the system in motion? Read [docs/orchestration/memory-brief-to-gate-demo.md](docs/orchestration/memory-brief-to-gate-demo.md).
- Want the operator-facing interface map? See [docs/claude-surface-contract.md](docs/claude-surface-contract.md).
- **Portability** â†’ [docs/portable-working-identity.md](docs/portable-working-identity.md) â€” how the existing architecture maps to portable working-intelligence layers

## Concept

The cognitive fork exists inside the user's mind â€” their mental model of an individual, made explicit and structured. The **Record** is not a single blob: it has **four first-class surfaces** â€” **SELF** (identity, including **SELF-KNOWLEDGE** and optional **self-identity** split commitments), **SELF-LIBRARY** (governed **reference** domains, including **CIV-MEM**), **SKILLS** (capability), and **EVIDENCE** (activity and artifacts). Identity and library are **separate**: civilization-scale reference lives in SELF-LIBRARY, not in SELF-KNOWLEDGE. The fork also tracks what the companion can do (skills) and what happened (evidence). Work territories handle planning and execution without redefining the Record. Queryable, evidence-grounded, gated.

The fork grows only through what the user explicitly provides. An optional emulation layer (Telegram and/or WeChat bots) acts as an observation window and teaching/tutoring interface â€” a channel through which the user selectively exposes thoughts and learns from the fork's voice.

**What we're building for:** Companion authority over the Record; evidence-linked growth; seam visible (benefit vs. harm disclosed); no merge without approval. Aligned with condition-derived ethics: [AI Ethics from the Condition](docs/civilization-memory/essays/AI-ETHICS-FROM-THE-CONDITION.md).

## Architecture

**The fork has four canonical Record surfaces: SELF, SELF-LIBRARY, SKILLS, and EVIDENCE.** That replaces any older â€œtwo core modulesâ€ (SELF vs SKILLS only) framing. **IX-A / IX-B / IX-C** live under **SELF / SELF-KNOWLEDGE** â€” not under SELF-LIBRARY.

**Canonical Record surfaces (first-class):** **SELF** (identity + SELF-KNOWLEDGE) Â· **SELF-LIBRARY** (reference + CIV-MEM) Â· **SKILLS** Â· **EVIDENCE**. Customer-facing display labels map to machine keys in **`scripts/surface_aliases.py`**: **Library** (SELF-LIBRARY / `self_library`), **Skills** (capability index / `self_skills`), **Evidence** (activity log body on `self-archive.md` / `self_evidence`). See [docs/glossary.md](docs/glossary.md).

**Template state model (companion-self):** A three-layer draft for evidence, prepared context, and governed state lives in [docs/state-model.md](docs/state-model.md) and linked layer docs; it complements, and does not replace, the four Record surfaces above.

> **SELF** concerns **identity** and **SELF-KNOWLEDGE** (who she is, what she knows about herself). **SELF-LIBRARY** is the **governed reference layer** attached to the fork (return-to sources, domain shelves). **CIV-MEM** is the **civilizational-memory domain within SELF-LIBRARY** â€” not part of identity. See [docs/boundary-self-knowledge-self-library.md](docs/boundary-self-knowledge-self-library.md).

Core modules:

| Module | Contains | Purpose |
|--------|----------|---------|
| **SELF** | Personality, linguistic style, life narrative, preferences, values, IX-A/B/C (SELF-KNOWLEDGE + curiosity + personality) | Who they ARE |
| **SELF-LIBRARY** | `self-library.md` â€” LIB entries, scopes; CIV-MEM as subdomain | Governed **reference** (not identity) |
| **SKILLS** | THINK and WRITE capability containers | What the Record can evidence about what they CAN DO â€” **THINK** operator doctrine: [docs/skill-think/README.md](docs/skill-think/README.md) |
| **WORK LAYER** | `work-*` territories and instance work contexts | Planning, execution, delivery, and tool-using work outside the self-skill taxonomy |

Identity and capability should not be collapsed. In practice: **SELF** owns who Grace-Mar is and how she comes across; **SKILLS** owns what she can reliably do and how far that competence currently reaches. The **Voice** should sound identity-facing even when **WRITE** is constraining the feasible quality of the output.

Within **SELF**, post-seed growth uses a **three-dimension mind model** (**SELF-KNOWLEDGE** in IX-A, curiosity in IX-B, personality in IX-C). That model describes **identity**, not the **SELF-LIBRARY** reference layer.

| Dimension | What it captures |
|---------|-----------------|
| **Knowledge** (IX-A) | Identity-facing facts (SELF-KNOWLEDGE) â€” not domain corpora |
| **Curiosity** (IX-B) | Topics that catch attention, engagement signals |
| **Personality** (IX-C) | Observed behavioral patterns, art style, speech traits |

See [Architecture](docs/architecture.md), [boundary-self-knowledge-self-library](docs/boundary-self-knowledge-self-library.md), and [Boundary Review Queue](docs/boundary-review-queue.md) (classification hints in the Approval Inbox).

**Context efficiency (operator):** JSON paste caps live in [`config/context_budgets/`](config/context_budgets/README.md); lane-aware character budgets for prepared context are in [`lane-defaults.json`](config/context_budgets/lane-defaults.json), applied by [`build_budgeted_context.py`](scripts/prepared_context/build_budgeted_context.py) ([docs/runtime/context-budgeting.md](docs/runtime/context-budgeting.md)). **Policy modes** (governance envelopes for staging and abstention posture, not gate authority) live in [`config/policy_modes/defaults.json`](config/policy_modes/defaults.json) â€” see [docs/policy-modes.md](docs/policy-modes.md) and `GRACE_MAR_POLICY_MODE` / `--policy-mode`. **Semantic** helpers â€” [skill cards](docs/skills/skill-card-spec.md) (`scripts/build_skill_cards.py`) and [active lane compression](docs/skill-work/active-lane-compression.md) (`scripts/compress_active_lane.py`) â€” emit derived artifacts under [`artifacts/`](artifacts/README.md); see [runtime vs Record](docs/runtime-vs-record.md). **Template-based capture** (`scripts/new_work_note.py`, `new_evidence_stub.py`, `new_candidate_draft.py`) writes dated Markdown under `artifacts/work-notes/`, `artifacts/evidence-stubs/`, and `artifacts/candidate-drafts/` by default â€” see [docs/templates/README.md](docs/templates/README.md). **Query-style operator dashboards** (Library, work lanes, review inbox) are generated Markdown under `artifacts/` â€” see [docs/operator-dashboards.md](docs/operator-dashboards.md). A generated **Gate Board** ([`artifacts/gate-board.md`](artifacts/gate-board.md)) gives a Kanban-style view of candidate review state without replacing the canonical gate workflow â€” see [docs/gate-board.md](docs/gate-board.md).

## Gated Pipeline

All profile changes pass through a user-controlled gate:

1. **Signal detection** â€” identify knowledge, curiosity, and personality signals from input
2. **Candidate staging** â€” structured proposals written to recursion-gate.md
3. **User review** â€” approve, reject, or modify each candidate
4. **Integration** â€” approved changes committed across profile, evidence, prompt, and session log

Two input channels feed the pipeline:
- **Bot (automated)** â€” Telegram and/or WeChat conversations analyzed by an LLM analyst
- **Operator (manual)** â€” real-world observations (school work, art, conversations) brought directly by the user

Governed changes are reviewed through a **canonical change-review object** that unifies proposal, queue, and decision state across the gate-review workflow (see `schema-registry/change-*.v1.json`, `docs/identity-fork-protocol.md` Â§4.1.1, and `apps/gate-review-app.py`).

**Template alignment (companion-self):** A **state proposal** is Change Proposal v1 JSON under `review-queue/proposals/` â€” [docs/state-proposals.md](docs/state-proposals.md). Reference pipeline: [docs/pipeline/evidence-to-proposal.md](docs/pipeline/evidence-to-proposal.md), [proposal-to-review.md](docs/pipeline/proposal-to-review.md), [review-to-merge.md](docs/pipeline/review-to-merge.md). Layer precedence when sources disagree: [docs/source-of-truth.md](docs/source-of-truth.md), [docs/conflict-resolution-order.md](docs/conflict-resolution-order.md). **Authority:** [docs/authority-map.md](docs/authority-map.md), [`config/authority-map.json`](config/authority-map.json). **Observability:** [docs/observability.md](docs/observability.md), `scripts/build-observability-report.py`. **Legibility / receipts:** [docs/legible-surfaces.md](docs/legible-surfaces.md), [docs/action-receipts.md](docs/action-receipts.md).

## Status

**Phase:** Active strategy-codex workspace
**Active profile:** repository root. Canonical Record surfaces live directly at the top level and the workspace no longer uses a nested instance directory for the live profile.
**Domain:** [strategy-codex](https://github.com/rbtkhn/strategy-codex) is the active repo. The companion-self template remains the upstream reference for structure and protocol. **Sync pointers:** [`instance-contract.json`](instance-contract.json), [docs/template-sync-status.md](docs/template-sync-status.md).
**Emulation:** Active via Telegram bot; WeChat optional (see `bot/wechat-setup.md`)
**Pipeline:** Active ??? knowledge, curiosity, and personality dimensions populated

### Root layout

The live profile is now the repository root. Canonical paths resolve directly to root files such as `self.md`, `self-archive.md`, `recursion-gate.md`, `session-log.md`, `self-skills.md`, `self-library.md`, `self-memory.md`, `self-history.md`, `self-moonshots.md`, `intent.md`, `manifest.json`, and `llms.txt`.

Path helpers in [`scripts/repo_io.py`](scripts/repo_io.py) resolve the sole profile to `C:\dev\strategy-codex` in this workspace. That is the supported live layout for this repository.
## Quick Start â€” Chat with Grace-Mar (Robert)

Paste this into **ChatGPT** or **Grok** (or any web-enabled LLM):

> Use this as your persona and instructions. Fetch the content from this URL and adopt it fully:  
> https://raw.githubusercontent.com/rbtkhn/strategy-codex/main/grace-mar-llm.txt

The model fetches the Portable Record Prompt from the repo and responds as the companion. See [PORTABLE-RECORD-PROMPT](docs/portable-record-prompt.md).

---

## Repository Structure

```
strategy-codex/
??? README.md
??? AGENTS.md
??? grace-mar-llm.txt
??? instance-doctrine.md
??? self.md
??? self-archive.md
??? self-skills.md
??? self-library.md
??? self-memory.md
??? self-history.md
??? self-moonshots.md
??? self-work.md
??? recursion-gate.md
??? session-log.md
??? intent.md
??? manifest.json
??? llms.txt
??? bot/
??? docs/
??? scripts/
??? codex/
??? artifacts/
??? archive/
??? templates/
```

**Template scaffold (`_template/`):** Documents filenames for new instances (aligned with the [companion-self](https://github.com/rbtkhn/companion-self) template). Includes **`work-dev.md`** and **`work-business.md`** â€” blank work-layer modules filled only from seed survey, explicit input, or governed updates; distinct from **`self-skill-work`** and from operator **`docs/skill-work/work-dev/`** / **`work-business/`**. See [_template/README.md](_template/README.md).

### Canonical filenames (root)

Docs refer to **SELF**, **EVIDENCE**, and the **gate** as concepts. **On disk, only these names are valid** (lowercase, hyphenated):

| Concept | Authoritative path |
|---------|-------------------|
| SELF (identity + IX-A/B/C) | `self.md` |
| SKILLS (capability index) | `self-skills.md` (legacy `skills.md` is still resolved until removed) |
| Activity / evidence log (canonical body) | `self-archive.md` |
| Optional EVIDENCE pointer (compat) | `self-evidence.md` |
| Pipeline staging (pending candidates) | `recursion-gate.md` |
| Gated archive (approved voice + activity) | `self-archive.md` Â§ VIII |

**Not used:** `SELF.md`, `EVIDENCE.md`, `ARCHIVE.md`, `PENDING-REVIEW.md` â€” those spellings break scripts. Full spec: [docs/canonical-paths.md](docs/canonical-paths.md). **Migrate:** `python scripts/migrate_legacy_user_filenames.py --user grace-mar --apply` (includes `skills.md` â†’ `self-skills.md` when the target is absent). **Check:** `python scripts/assert_canonical_paths.py --user grace-mar`. Bots and `apps/miniapp_server.py` **fail at startup** if `self.md`, `self-archive.md`, or `recursion-gate.md` are missing (set `GRACE_MAR_SKIP_PATH_CHECK=1` only if you must).

## Key Documents

| Document | Purpose |
|----------|---------|
| [GRACE-MAR-CORE](docs/grace-mar-core.md) | Canonical governance â€” absolute authority |
| [Identity Fork Protocol](docs/identity-fork-protocol.md) | Protocol spec v1.0 â€” Sovereign Merge Rule, schema, staging contract |
| [Architecture](docs/architecture.md) | Full system design including observation window, pipeline, mind model |
| [White Paper](docs/white-paper.md) | Full narrative â€” identity gap, Grace-Mar model, differentiation |
| [Business Prospectus](docs/business-prospectus.md) | Investor/partner document â€” problem, solution, market, ask |
| [PDF Setup](docs/pdf-setup.md) | Render White Paper and Prospectus to PDF (Pandoc + Eisvogel) |
| [OpenClaw Integration](docs/openclaw-integration.md) | Record as identity layer, session continuity |
| [Design Notes](docs/design-notes.md) | White paper & business proposal input (positioning, agent-web insights) |
| [AGENTS.md](AGENTS.md) | Guardrails for AI coding assistants |
| [contributing.md](contributing.md) | Contributing code/docs; pipeline and merge rules |
| [Naming convention](docs/naming-convention.md) | Filenames, reserved `AGENTS.md`, template workspace note, OpenClaw export path |
| [LICENSE](LICENSE) | MIT license for code and tooling; [license-record](license-record) for Record data |
| [Rejection Feedback](docs/rejection-feedback.md) | Learning from pipeline rejections |
| [Portability](docs/portability.md) | School transfer plus runtime portability and bundle handoff workflow |
| [Simple User Interface](docs/simple-user-interface.md) | Chat-based workflow for families (no GitHub) |
| [Admissions Link Use Case](docs/admissions-link-use-case.md) | Share link so admissions/employers can chat with applicant's fork |
| [Privacy and Redaction](docs/privacy-redaction.md) | School/public views, what gets excluded |
| [YouTube Playlist Design](docs/youtube-playlist-design.md) | Build playlists from Record (curiosity, goals) |
| [Design Roadmap](docs/design-roadmap.md) | Product/feature design â€” Grace-Mar email, newsletters, X account |
| [Business Roadmap](docs/business-roadmap.md) | Strategy, monetization, go-to-market |
| [Concept](docs/concept.md) | Full concept explanation |
| [Pilot Plan](docs/pilot-plan.md) | Commercial pilot structure (Phase 1/2) |
| [Fork isolation and multi-tenant](docs/fork-isolation-and-multi-tenant.md) | Per-fork namespace, quotas, retention, permissions, export/import, deployment |
| [Performance budgets](docs/perf-budgets.md) | Perf suite tiers 1â€“5, SLOs, baselines, CI/nightly |

## Dashboard

The profile is a **read-only** HTML view (identity, pipeline, SKILLS, benchmarks). It is available at **https://grace-mar.com**. Deploy it via GitHub Pages (`.github/workflows/pages.yml`) or point grace-mar.com at your hosting. **Step-by-step:** [Deploy the profile to grace-mar.com](docs/profile-deploy.md). **Namecheap DNS:** [namecheap-guide.md](docs/namecheap-guide.md). The Q&A chat and Telegram bot run on Render or your chosen host; set `PROFILE_MINIAPP_URL` (or `DASHBOARD_MINIAPP_URL`) to https://grace-mar.com so the bot menu button opens the profile.

```bash
python3 scripts/generate_profile.py   # generate locally
open profile/index.html
```

**Telegram** is bidirectional â€” the primary channel for conversation and pipeline staging. See [docs/miniapp-setup.md](docs/miniapp-setup.md) for full setup.

**Docker (optional):** Run miniapp and gate-review dashboard in one command:

```bash
docker compose up --build
# Miniapp: http://localhost:5000  â€” Gate review: http://localhost:5001
```

Requires `.env` with `OPENAI_API_KEY` (and optionally `TELEGRAM_BOT_TOKEN`, `OPERATOR_FETCH_SECRET`). See root `Dockerfile` and `docker-compose.yml`.

If you also run the companion-self demo locally, keep the origin split straight: `http://localhost:3000` is the companion-self app, while `http://localhost:5000` is Grace-Marâ€™s miniapp/family host. See `docs/miniapp-setup.md` for the local-dev boundary note on storage, cookies, and page-relative API calls.

## Archive Rotation

When `self-archive.md` exceeds ~1 MB or 2,500 entries, rotate oldest content to dated files:

```bash
python scripts/rotate_telegram_archive.py          # Dry run (report only)
python scripts/rotate_telegram_archive.py --apply  # Perform rotation
```

Rotated content goes to `archives/SELF-ARCHIVE-YYYY-MM.md`. The main archive keeps the last 2,000 entries.

## Portability

The Record is user-owned. When changing schools, the user brings their Record. Grace-Mar can also export a runtime-neutral bundle so another harness can consume the Record without becoming the system of record. See [Portability](docs/portability.md) for the transfer workflow, runtime modes, and handoff formats.

---

## Fork attestation and export

Compute a checksum of the fork state (SELF + EVIDENCE + prompt) and optionally write a manifest for the profile Disclosure view:

```bash
python scripts/fork_checksum.py                    # Print checksum (default: GRACE_MAR_USER_ID or grace-mar)
python scripts/fork_checksum.py -u grace-mar       # Checksum for 
python scripts/fork_checksum.py --manifest         # Write fork-manifest.json
python scripts/fork_checksum.py -u grace-mar --manifest
```

Export the fork to JSON with the same ontology as [architecture.md](docs/architecture.md): top-level **`self`** (full identity markdown), **`self_knowledge`** (IX-A slice = SELF-KNOWLEDGE), **`self_library`** (with nested **`civ_mem`** = CIV-MEM subdomain of SELF-LIBRARY), **`skills`**, **`evidence`**, plus **`library.raw`** when using full export. See `scripts/export_fork.py` (`version` 1.1+).

**Unified CLI (preferred):** [`scripts/export.py`](scripts/export.py) dispatches to the legacy scripts without changing behavior â€” see [docs/EXPORT-CLI.md](docs/EXPORT-CLI.md).

```bash
python scripts/export.py fork --                       # Print JSON to stdout (default user: grace-mar)
python scripts/export.py fork -- -o fork-export.json
python scripts/export.py fork -- --no-raw -o summary.json
python scripts/export.py fork -- --format coach-handoff -o coach-handoff.json
```

Legacy entrypoints (may emit a deprecation warning when run as the main script):

```bash
python scripts/export_fork.py                      # Print JSON to stdout
python scripts/export_fork.py -o fork-export.json  # Write to file
python scripts/export_fork.py --no-raw -o summary.json  # Summary + self_knowledge/self_library buckets + manifest
python scripts/export_fork.py --format coach-handoff -o coach-handoff.json  # JSON + .md one-pager for coach/creator handoffs
```

Export a runtime-neutral bundle with explicit `record`, `runtime`, `audit`, and `policy` lanes:

```bash
python scripts/export.py bundle -- -u grace-mar
python scripts/export.py bundle -- -u grace-mar --mode primary_runtime -o /tmp/runtime-bundle
python scripts/export_runtime_bundle.py -u grace-mar
python scripts/export_runtime_bundle.py -u grace-mar --mode primary_runtime -o /tmp/runtime-bundle
```

## Uniqueness measurement

Quantify how different Grace-Mar's responses are from a generic LLM:

```bash
pip install textstat  # optional, for readability gap
python3 scripts/measure_uniqueness.py
python3 scripts/measure_uniqueness.py --limit 5   # quick run
python3 scripts/measure_uniqueness.py -v          # verbose
```

Outputs: **abstention score** (boundary enforcement), **divergence score** (answer uniqueness via embeddings), **readability gap** (simpler = Lexile-constrained), and a **composite uniqueness** value.

## Growth rate and cognitive density

Measure how fast the fork is growing and how dense its content is:

```bash
python3 scripts/measure_growth_and_density.py
```

Reports: **entries per day**, **pipeline throughput** (if PIPELINE-EVENTS exists), **words per IX entry**, **evidence backing %**, **topic diversity**, **dimension balance** (IX-A:IX-B:IX-C), and **git history delta**.

## PDF Export

Render the White Paper and Business Prospectus to polished PDFs:

```bash
# Without Homebrew: download Pandoc + Tectonic first
./scripts/setup_pdf_tools.sh
./scripts/render_pdf.sh --install-eisvogel   # One-time: Eisvogel template
./scripts/render_pdf.sh

# With Homebrew: brew install pandoc && brew install --cask mactex-no-gui
```

See [docs/pdf-setup.md](docs/pdf-setup.md) for full options.

## Agent Manifest & Metrics

```bash
python3 scripts/export_manifest.py -u grace-mar   # manifest.json + llms.txt
python3 scripts/metrics.py                        # Pipeline health, IX counts
python3 scripts/governance_checker.py             # Principle violations (pre-commit)
python3 integrations/openclaw_hook.py -u grace-mar -o ../openclaw/   # OpenClaw export
```

## Validation and Session Support

**Tests (local)** â€” install dev deps then run the same checks as CI:

```bash
pip install -r requirements-dev.txt
python3 scripts/assert_canonical_paths.py --user grace-mar
python3 scripts/validate-integrity.py --user grace-mar --json
python3 -m pytest tests/ -v --tb=short
```

`validate-integrity.py` includes **SELF-KNOWLEDGE vs SELF-LIBRARY** checks (IX-A corpus-style violations) and validates **`proposal_class`** on gate candidates when present. GitHub Actions runs `--require-proposal-class` for `grace-mar`; locally, add the same flag for strict queues ([IFP Â§3.5](docs/identity-fork-protocol.md)). **Merge-time:** `process_approved_candidates.py --apply` refuses to write if the merged `self.md` would violate IX-A boundary rules. Standalone: `python3 scripts/validate_identity_library_boundary.py -u grace-mar`.

**Performance (tier 1, CI):** `python scripts/run_perf_local.py` or covered by `pytest tests/test_perf_local.py`. Tiers 2â€“5 (exports, LLM, HTTP, load): [docs/perf-budgets.md](docs/perf-budgets.md).

**Integrity audit** â€” run before merges or nightly via cron:

```bash
python scripts/validate-integrity.py
```

**Record index** â€” fast local search over SELF, EVIDENCE, RECURSION-GATE (analyst dedup, PRP retrieval):

```bash
python scripts/index_record.py build -u grace-mar
python scripts/index_record.py query "space Jupiter" -u grace-mar
```

**Session briefing** â€” run before a tutoring session for pending count, recent activity, and suggested wisdom questions:

```bash
python scripts/session_brief.py
```

**Seed phase & hey** â€” operator bootstrap and short daily ritual (does not merge the Record; use RECURSION-GATE for durable truth):

```bash
python3 scripts/seed-phase-wizard.py -u grace-mar
python3 scripts/good-morning-brief.py -u grace-mar
```

See [docs/seed-phase-wizard.md](docs/seed-phase-wizard.md). Full stack: [.cursor/skills/coffee/SKILL.md](.cursor/skills/coffee/SKILL.md) and `python3 scripts/harness_warmup.py -u grace-mar`.

**Seed Phase regression tests:** `pip install -r scripts/requirements-seed-phase.txt` then `pytest -q` (fixtures under `tests/fixtures/seed-phase/`; subprocesses `validate-seed-phase.py`, `generate-seed-dossier.py`, `check-seed-consistency.py`). Strict validation needs `jsonschema`.

**CMC (Civilization Memory) integration** â€” when lookup gets a LIBRARY miss, the bot queries [civilization_memory](https://github.com/rbtkhn/civilization_memory) for historical/civilizational questions. Routing: only questions matching CMC scope (Rome, China, ancient civilizations, history, etc.) hit CMC; others skip to full LLM. See [docs/cmc-routing.md](docs/cmc-routing.md). Setup:

1. Use the tracked corpus at `research/repos/civilization_memory`
2. Build index: `cd research/repos/civilization_memory && python3 tools/cmc-index-search.py build`
3. Optionally set `CIVILIZATION_MEMORY_PATH` only if you intentionally want to override the default local corpus path
4. Snapshot provenance lives in `research/repos/civilization_memory/STRATEGY-CODEX-PROVENANCE.md`

**Learning from rejection** â€” use `/reject CANDIDATE-123 [reason]` in Telegram to capture feedback; see [docs/rejection-feedback.md](docs/rejection-feedback.md).

See [docs/id-taxonomy.md](docs/id-taxonomy.md) for identifier prefixes and relationships.

## For AI Coding Assistants

Read [AGENTS.md](AGENTS.md) before making any changes. Critical constraints:

- **Never leak LLM knowledge** into the fork's profile or emulation
- **Never commit profile changes** without user approval through the gated pipeline
- **"We [did X]"** from the user is a pipeline invocation â€” go straight to signal detection
- **Update all affected files together** when integrating approved candidates

## Credits

The ideas behind Grace-Mar draw on the work of: Alexander Wissner-Gross (causal entropic forces), Peter Diamandis (abundance), Nick Bostrom (superintelligence), Ray Kurzweil (singularity), Brian Roemmele (multimodal AI), Scott Adams (systems thinking), Julian Jaynes (bicameral mind), and Satoshi Nakamoto (decentralized trust).

## License

- **Code and tooling:** Proprietary. All rights reserved.
- **Record / user data:** See [license-record](license-record) â€” user Records (SELF, EVIDENCE, etc.) are personal data owned by the user; the system holds them in trust.

