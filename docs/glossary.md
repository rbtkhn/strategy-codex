# Glossary — Grace-Mar

Short definitions for contributors and tooling. **Governed by:** [GRACE-MAR-CORE v2.0](grace-mar-core.md).

**Narrative source of truth for the fork layout:** [architecture.md](architecture.md) § Core Principle. This glossary **locks terminology**; the one-line boundary rule below is **verbatim** from [archive/boundary-museum-knowledge-self-library.md](archive/boundary-museum-knowledge-self-library.md).

| Term | Definition |
|------|------------|
| **Rule (identity vs reference)** | **museum knowledge is identity-facing. removed operator-books symlink is reference-facing.** CIV-MEM is inside removed operator-books symlink, not museum knowledge. |
| **Rule (identity vs capability)** | **SELF is identity-facing. SKILLS is capability-facing.** SELF answers who Grace-Mar is and how she comes across; SKILLS answers what she can reliably do and under what constraints. |
| **Grace-Mar** | Legacy product name for the frozen embedded Record in this repo. **Active product:** strategy-codex governed interpretive machine. See [archive/grace-mar-corpus/README.md](../archive/grace-mar-corpus/README.md). |
| **Interpretive machine** | **Legacy Grace-Mar term** — versioned personal Record branch. **Not** a strategy-codex growth objective; archaeology on **`fork revive`** only. See [legacy-operator-concepts.md](legacy-operator-concepts.md). |
| **companion** | The human whose Record it is; the sovereign in **triadic cognition** (**Mind**, **Record**, **Voice**). |
| **Record** | Companion-owned **canonical data** with **four surfaces**: (1) **SELF** — identity + **museum knowledge** (`self.md`, museum knowledge section A/B/C); (2) **removed operator-books symlink** — **reference-facing** governed library (`self-library.md`), including **CIV-MEM** as a sub-library; (3) **SKILLS** — capability index (`self-skills.md`; legacy `skills.md` still resolved until migrated); (4) **EVIDENCE** — canonical activity log body **`self-archive.md`** (optional `self-evidence.md` pointer only). Identity ≠ library: corpora live in removed operator-books symlink, not in museum knowledge section A. Gate applies to merges into these surfaces. See [archive/boundary-museum-knowledge-self-library.md](archive/boundary-museum-knowledge-self-library.md). |
| **Voice** | The queryable interface that speaks the Record — e.g. the Telegram/WeChat bot. It responds when queried, never unbidden; it renders the Record in conversation (**emulation**). Voice is identity-facing: it should sound like Grace-Mar, not like a capability rubric. |
| **WORK execution layer** | The execution stack on **WORK territories** and **skill-work** docs: operator + tooling + AI assistant that drafts, mirrors, template diffs, and runbooks. It **stages**; it does **not** merge into SELF / EVIDENCE / prompt without companion approval. Distinct from **Voice** (speech from the Record). See [CONCEPTUAL-FRAMEWORK §8](conceptual-framework.md#8-design-lens-triadic-cognition) and [SKILLS-MODULARITY §5a](skills-modularity.md#5a-identity-vs-instrument-record-skills-and-work). |
| **Mirror (pattern)** | A **downstream or tracked copy** of shared layouts/runbooks (e.g. advisor `work-*` ↔ template) kept **aligned on a rhythm** — not a **interpretive machine** and not **Record truth**. Contrast **Git fork** (hosting a separate repository). |
| **triadic cognition** | **Mind** (human) + **Record** + **Voice** — a **triad**: one human part, two digital parts (Record, Voice). The **companion-self** architecture defines the pattern; each **instance** (e.g. **Grace-Mar**) hosts the digital pair. Two-word **companion self** = the conceptual dyad. **WORK execution** is **instrumental**, not a fourth part of the triad. See [CONCEPTUAL-FRAMEWORK §8](conceptual-framework.md#8-design-lens-triadic-cognition). |
| **tricameral mind** | **Synonym** for **triadic cognition** (same Mind + Record + Voice). Still used in some prompts and next to Jaynes; prefer **triadic cognition** in new prose. |
| **companion self** | Two words — **conceptual** shorthand: (1) the companion’s self externalized in the Record (their knowledge/curiosity/personality), and (2) the Record+Voice that accompanies them and speaks when queried. **Not** the same as **companion-self** (hyphenated system name). |
| **companion-self** | **Always hyphenated.** Names the **template** repository and **intelligence-system** product surface (fork blueprint, upgrades, `platform/template/`). Use this spelling for the **system / entity**, never `companion self` or `companionself`. |
| **companion-xavier** | **Always hyphenated.** May name **a** sovereign instance (fork) as a **system entity** when the companion uses that deployment name (typically **not** inside the grace-mar repo). Same rule: hyphenated marks a **named** cognitive-fork deployment, not the two-word **companion self** concept. |
| **recursion-gate** (gate) | The staging surface and concept: candidates sit above `## Processed` in `recursion-gate.md` until the companion approves; on approval they are merged and moved below Processed. |
| **Approval Inbox** (user-facing) | Plain-language name for **pending candidates** in the gate file before merge — same as **recursion-gate** queue; not a separate system. |
| **Governance unbundling** | Splitting **routing** (staging / analyst), **sensemaking** (human Approval Inbox review), and **accountability** (sovereign merge). See [governance-unbundling.md](governance-unbundling.md). |
| **OB1** (informal) | Shorthand for **Open Brain**–style personal knowledge / gateway mental models; not a Grace-Mar product name. |
| **SELF** | Identity surface: `self.md` — narrative, preferences, values, and post-seed **museum knowledge** (museum knowledge section A), curiosity (museum knowledge section B), personality (museum knowledge section C). Not domain corpora. |
| **Personality** | Identity-facing observed traits and expressive patterns in `self.md` museum knowledge section C — behavior, values, speech traits, art style, and the way Grace-Mar tends to come across. Personality is not a skill level. |
| **SELF / SKILLS / EVIDENCE** (modules) | Shorthand; full Record adds **removed operator-books symlink**. On disk: `self.md`, `self-library.md`, `self-skills.md` (EVIDENCE body: `self-archive.md`). |
| **museum knowledge** | Identity-facing knowledge in SELF — what the companion knows *about herself* (museum knowledge section A and related); not domain corpora. See [archive/boundary-museum-knowledge-self-library.md](archive/boundary-museum-knowledge-self-library.md). |
| **removed operator-books symlink** | Reference-facing governed library (`self-library.md`): return-to sources and domain shelves. **Parallel to identity**, not a subset of museum knowledge. |
| **Library / Skills / Evidence (display)** | User-facing labels for **removed operator-books symlink**, **SKILLS**, and **EVIDENCE** in prose and exports; machine keys and stems live in **`scripts/surface_aliases.py`** (`self_library` → Library, `self_skills` → Skills, `self_evidence` → Evidence on `self-archive.md`). |
| **WRITE / self-skill-write** | The writing capability container in SKILLS (`self-skills.md`, `skill-write.md`). It captures demonstrated writing competence, production range, support needs, and growth trajectory. It is capability-facing, not identity-facing. |
| **Linguistic style** | The Voice-facing description of how Grace-Mar tends to sound. It lives on the SELF side as expressive identity, even when it is informed by WRITE evidence. When surfaces disagree, SELF owns style-as-identity and SKILLS owns style-as-capability. |
| **CIV-MEM** | Civilizational-memory **sub-library** inside removed operator-books symlink (LIB scopes + hybrid corpus). Never treated as museum knowledge. |
| **Library Domain Registry** | Canonical index (`docs/self-library-domains.md` + `.json`) of **installed reference domains** (e.g. CIV-MEM, LIB entries): surface, authority, invocation, mutation policy, freshness. Routable domains must be declared here. See [self-library-domains.md](self-library-domains.md). |
| **self-* (standard labels)** | **museum identity knowledge (archive)**, **self-library**, … — lowercase hyphenated labels for Record components; formal surfaces **museum knowledge** / **removed operator-books symlink** when disambiguating. See [id-taxonomy.md — Capitalization and format](id-taxonomy.md#capitalization-and-format). |
| **Skill card** | Small **derived** JSON/Markdown summary of a portable skill for operator context — produced by `scripts/build_skill_cards.py`, validated by `schemas/registry/skill-card.v1.json`. Does **not** replace `skills/` or generated `.cursor/skills/` bodies. See [skill-card-spec.md](skills/skill-card-spec.md). |
| **Active lane compression** | One **WORK** lane (`docs/skill-work/work-*`) squeezed into a short memo with recovery paths — `scripts/compress_active_lane.py`. **Not** the JSON paste caps in `platform/config/context_budgets/`. See [active-lane-compression.md](skill-work/active-lane-compression.md). |
| **Runtime vs Record** | **Runtime** = session paste, harness output, derived artifacts, MEMORY — not canonical truth. **Record** = SELF, removed operator-books symlink, SKILLS, EVIDENCE after gate. See [runtime-vs-record.md](runtime-vs-record.md). |
| **Intelligence harness** | **Product term** — the governed structure around models in **strategy-codex**: source truth, context routing, artifact authority, review, transaction ceilings. Not a specific vendor or model. See [intelligence-harness.md](intelligence-harness.md). |
| **Harness script** | **Tooling term** — operational scripts (`harness_warmup.py`, eval/replay harnesses) that implement parts of the product harness; distinct from the product identity itself. |
| **Intake queue sidecar** | **Derived JSON** under `runtime/artifacts/statecraft-intake-queue/` tracking `synthesis_status` and routing hints for an archive capture; **not** archive SSOT. See [statecraft-intake-queue.md](statecraft-intake-queue.md). |

## Cadence shortcuts (FAQ)

| Phrase | Role |
|--------|------|
| **coffee** | Repeated **orientation** (many per day); read-only planning; ends with **A–G** menu in grace-mar; **not** a session seal. |
| **dream** | **End-of-day** maintenance (MEMORY, integrity, handoff artifact); **not** merge authority. |
| **bridge** | **Session close** → commit/push + **transfer packet** for a **fresh** thread; packet ends with lone **`coffee`**. |
| **harvest** | **Midstream** dense packet for an **already-running** agent; **must not** end with **`coffee`**. See [harvest-packet-contract.md](skill-work/work-cadence/harvest-packet-contract.md). |

**Doc-only loop (habit):** If the same cadence confusion repeats twice, patch the relevant **SKILL** or **work-cadence** doc — not SELF/EVIDENCE. See [work-cadence README](skill-work/work-cadence/README.md) § *Closing the troubleshooting loop*.

For full terminology and invariants, see [conceptual-framework.md](conceptual-framework.md), [archive/boundary-museum-knowledge-self-library.md](archive/boundary-museum-knowledge-self-library.md), and [canonical-paths.md](canonical-paths.md).
