# Canonical record paths

**Purpose:** Single source of truth for sole-operator Record paths. All tooling and docs should use these **lowercase** paths. No uppercase filenames (e.g. `SELF.md`, `EVIDENCE.md`) are canonical.

**See also:** [Date and time formats](date-time-conventions.md) â€” `YYYY-MM-DD` for dated artifacts and CLI vs compact ids (`YYYYMMDD`, directory sharding).

**Governed by:** [GRACE-MAR-CORE v2.0](grace-mar-core.md), [Identity Fork Protocol](identity-fork-protocol.md)

---

## Paths

| Concept | Canonical path |
|--------|-----------------|
| Identity shell + three-dimension mind overview | `self.md` |
| Durable IX-A knowledge surface | `self-knowledge.md` |
| Durable identity commitments (optional split surface) | `self-identity.md` |
| Activity log (ACT-*, READ-*, WRITE-*, CREATE-*) + gated approved log Â§ VIII | **`self-archive.md`** â€” single canonical **EVIDENCE** file |
| `self-evidence.md` | **Optional compatibility pointer** for old bookmarks; tooling reads **`self-archive.md`**. Do not rely on this path for new instances. |
| Gated approved activity (voice + non-voice) | **`self-archive.md` Â§ `## VIII. GATED APPROVED LOG (SELF-ARCHIVE)`** â€” appended only by `process_approved_candidates.py` |
| Pipeline staging (candidates above `## Processed`) | `recursion-gate.md` |
| Session / interaction history | `session-log.md` |
| Capability index (THINK, WRITE, etc.) | **`self-skills.md`** â€” legacy `skills.md` is still read if present (see `scripts/repo_io.py` `resolve_surface_markdown_path`). **Root skill naming contract for this repo:** use **self-skill-\*** labels in doctrine, but the active split root files are **`skill-think.md`**, **`skill-write.md`**, and **`skill-steward.md`**. Template or migration layouts may also carry `self-skill-think.md`, `self-skill-write.md`, `self-skill-work.md`, or `self-skill-steward.md`; do not create those here unless doctrine explicitly promotes a migration. See [id-taxonomy.md](id-taxonomy.md). **THINK operator doctrine:** [skill-think/README.md](skill-think/README.md). |
| Curated references, canon | `self-library.md` |
| Self-memory (continuity â€” short/medium/long; not Record) | **`self-memory.md`** â€” standard label **self-memory**. Legacy layouts may still have **`memory.md`**; readers resolve **self-memory first**, then **memory.md**, via `scripts/repo_io.py` `resolve_self_memory_path`. |
| Self-history (derived dual log â€” not Record) | **`self-history.md`** â€” optional **systematic** timeline: **WORK** aggregate from **`docs/skill-work/work-*/*-history.md`** plus **gate-approved** **COMPANION** thread (pointers/summaries from merged **SELF/EVIDENCE** only). **Derived gazette**; not a merge bypass. See file header fence. |
| Intent (goals, tradeoffs â€” YAML in fenced block; see [intent-template.md](intent-template.md)) | `intent.md` |
| **Moonshot staging** (PMOS â€” pre-gate programs; **not** authoritative SELF until promoted) | **`self-moonshots.md`** â€” see [moonshot-operating-model.md](moonshot-operating-model.md) |

All paths are **lowercase** with hyphens where used (e.g. `self-archive.md`, `recursion-gate.md`).

**Alias:** `knowledge-gate` is a human-friendly synonym for `recursion-gate`; both names refer to the same approval membrane and same canonical file path.

**`self-*` labels in prose:** Standard companion-self component names (**self-knowledge**, **self-identity**, **self-library**, …) and formal surfaces (**SELF-KNOWLEDGE**, **SELF-LIBRARY**) are defined in [id-taxonomy.md — Capitalization and format](id-taxonomy.md#capitalization-and-format). `self-knowledge.md` is the canonical IX-A knowledge file; `self.md` now keeps the overview shell.

**`intent.md`:** Not required by `assert_canonical_record_layout()` for minimal bot startup; when present it is the canonical source for `export_intent_snapshot` / manifest policy and clears export **degraded** mode when valid.

---

## Startup and tooling

Scripts and the bot resolve paths at the repository root using these names. If the expected files are missing, tooling should fail loudly. See `scripts/assert_canonical_paths.py` and env `GRACE_MAR_SKIP_PATH_CHECK` for optional skip.

**Legacy (do not create new):** `SELF.md`, `EVIDENCE.md`, `ARCHIVE.md`, `PENDING-REVIEW.md`, `SKILLS.md` (uppercase), **`skills.md`** (old capability index name), and **`memory.md`** (old self-memory filename) are **not** canonical for new work â€” use **`self-skills.md`** and **`self-memory.md`**. The migration script renames `skills.md` â†’ `self-skills.md` and **`memory.md` â†’ `self-memory.md`** when the canonical file is absent.

**Surface registry:** Internal keys and display labels (`self_skills` â†’ Skills, `self_evidence` â†’ Evidence, etc.) live in **`scripts/surface_aliases.py`**.

**Migration:** `python scripts/migrate_legacy_user_filenames.py --dry-run` then `--apply`. If both `PENDING-REVIEW.md` and `recursion-gate.md` exist, use `--merge-pending-review` to append or resolve manually.

**Startup:** Telegram bot, WeChat bot, `apps/miniapp_server.py`, and `apps/gate-review-app.py` call `assert_canonical_record_layout()` and **exit with an error** if any required file is missing. Override only for special environments: `GRACE_MAR_SKIP_PATH_CHECK=1`.
