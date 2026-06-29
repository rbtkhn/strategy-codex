# Agent deep rules — strategy-codex

**Work only; not Record.**

Extended guardrails moved from root [AGENTS.md](../../AGENTS.md) during Sprint 5 slimming. **Always-on contract:** slim AGENTS + [instance-doctrine.md](../../instance-doctrine.md). Fork / gate / triadic cognition detail lives here.

**Archive fork (frozen):** [docs/archive/grace-mar.md](../archive/grace-mar.md)

---

**For conceptual clarity (legacy instance):** Read `docs/conceptual-framework.md` â€” Record vs. fork, Voice vs. bot, fork vs. twin, terminology. Applies when operator explicitly invokes **`fork revive`** or **`grace-mar archive`**.

**For system design:** Read `docs/architecture.md` (includes forced-absorption risk pattern and convenience-path defenses). For the formal skill modularity model (THINK/WRITE boundaries, separate work/execution layer, Voice and profile as functions of skill-write, invariants), see `docs/skills-modularity.md`. For the typed non-Record membrane and the lane overlays for `statecraft` and `singularity`, see `docs/work-membrane-v2.md`, `statecraft/work-membrane.md`, and `singularity/work-membrane.md`.
For the normal operator routing model, see `docs/operator-two-channel-architecture.md`.

**For local-first sovereignty:** Read `docs/sovereignty.md` â€” memory and governance stay local; cloud/frontier models are helpers, not owners of the Record.

**For chat/UI design:** Read `docs/chat-first-design.md` â€” principles for delivering the full experience within Telegram/chat (bounded sessions, one-tap, Record felt not seen).

**Design alignment:** This repo still carries legacy Grace-Mar / 5000 Days framing in some embedded materials - abundance, identity beyond productivity, conductor workflow, symbiosis (human holds the reins), interregnum fortification (Part 14). For active strategy-codex work, treat that as historical or embedded context unless the operator invokes it directly.

**Operator model (default):** **Mind** (operator) + **work execution layer** (assistant, scripts, `statecraft/`, `singularity/`). Two primary channels per [`docs/operator-two-channel-architecture.md`](../operator-two-channel-architecture.md). **Legacy — triadic cognition (frozen Grace-Mar instance):** Mind + Record + Voice — historical instance doctrine only; Voice/bot deprecated. See CONCEPTUAL-FRAMEWORK §8 when reviving archive work.

**SKILLS (Record-bound):** Use **self-skill-think**, **self-skill-write**, **self-skill-work**, and **self-skill-steward** as the **conceptual labels** for Record-bound capabilities. In this repo's active root layout, the concrete split skill files are **`skill-think.md`**, **`skill-write.md`**, and **`skill-steward.md`**, while **`self-skills.md`** remains the canonical capability index. Treat any future **`self-skill-*.md`** filenames here as migration-only or template-specific unless doctrine explicitly promotes them. See [id-taxonomy.md](../id-taxonomy.md), [skills-modularity.md](../skills-modularity.md), and [canonical-paths.md](../canonical-paths.md). **THINK doctrine (intake vs identity vs work):** [docs/skill-think/README.md](../skill-think/README.md). **Skill lifecycle (discovery ladder):** `skills/README.md` â€” pointer â†’ draft â†’ listed. **Skill validation:** `python3 scripts/validate_skills.py`.

**Agent vocabulary (onboarding):** Many new AI users already use **agent** for â€œa tool-using runner.â€ **Work agent** and **skill-work agent** are **onboarding-friendly** names for that pattern on work surfaces: they **utilize** the Record (read; propose via the gate only) and may support the Voice (e.g. harnesses, PRP, prompt work) under **operator** control â€” they are **not** Mind, **not** the companion-facing Voice in chat, and **not** a fourth triad seat. **Skill-work agent** stresses the same idea scoped to **`docs/skill-work/`** and **work territories**, including **replicated / parallel** lanes. Precision term for the stack: **work execution layer**; beginner gloss: `singularity/work-cici/GLOSSARY-FOR-BEGINNERS.md`.

## Agent role boundaries â€” unbundled management functions

Assistants and automation in this repo are limited to the **routing** layer unless a human explicitly runs a merge:

- **Allowed (routing):** Statecraft/singularity WORK routing, archive→synthesis promotion, integrity/boundary/git stewardship. **Fork revive only:** detect signals; stage museum knowledge section A/B/C in `recursion-gate.md` when operator says **`fork revive`**, **`grace-mar archive`**, or equivalent (see boundary doc).
- **Prohibited without human gate (sensemaking and accountability):** Auto-approve, auto-merge, or silently resolve conflicting candidates; substitute deep personal or ethical judgment for companion review; overwrite user intent.

When uncertain, stage with an explicit note that **human sensemaking** may be requiredâ€”never merge without companion approval. Full framing: [`docs/governance-unbundling.md`](../governance-unbundling.md).

---

## What This System Is

A **governed interpretive machine** — verbatim sources land in archive; bounded synthesis and **notes** carry judgment under **statecraft** and **singularity**. Durable operator work ends at **governed adjacent** surfaces unless the operator explicitly revives the Grace-Mar fork lane. See [`docs/product-identity.md`](../product-identity.md) and [`essays/from-accumulation-to-governed-interpretive-machine.md`](../../essays/from-accumulation-to-governed-interpretive-machine.md).

**Legacy — Grace-Mar interpretive machine (frozen sidecar):** A versioned personal Record (`archive/grace-mar-instance/self.md`, `self-archive.md`, …) and deprecated Voice (`archive/grace-mar-instance/bot/`) remain for archaeology and explicit revive only. Do not treat fork growth as the product objective. [`docs/archive/grace-mar.md`](../archive/grace-mar.md) · [`docs/grace-mar-instance-boundary.md`](../grace-mar-instance-boundary.md).

**Legacy conceptual distinctions** (Grace-Mar instance; fork revive only — see conceptual-framework.md):
- **Companion** â€” The person whose Record it is (the human in **triadic cognition** â€” Mind in the triad). Preferred term over "user" in conceptual prose; affectionate and relatable. **Framing:** The human is Grace-Mar's companion â€” the Record and Voice are accompanied by the human, who holds authority and meaning. Grace-Mar serves the companion; the companion serves Grace-Mar.
- **Record and Voice** â€” The Record is the documented self; the Voice speaks the Record when queried. Self = Record + Voice (the thing you can talk to).
- **Companion self** â€” One phrase for both sides of the dyad: the companion's self (the human's self, externalized in the Record) and the self that companions (the Record and Voice that accompany the human). The ambiguity is intentional; see CONCEPTUAL-FRAMEWORK (companion self). **Companion self contains:** **museum identity knowledge (archive)** (**museum knowledge**, museum knowledge section A), **self-curiosity** (museum knowledge section B), **self-personality** (museum knowledge section C), **self-skill-think**, **self-skill-write**, **self-skill-work**, **self-skill-steward** (optional STEWARD split), **self-archive**, **self-library** (**removed operator-books symlink**; CIV-MEM subdomain), **memory**, **self-voice** (see [ID-TAXONOMY â€” Capitalization and format](../id-taxonomy.md#capitalization-and-format), [archive/boundary-self-knowledge-self-library.md](../archive/boundary-self-knowledge-self-library.md)). Work territories are adjacent execution surfaces, not self-skills.
- **companion-self** / **companion-xavier** â€” **Always hyphenated** when naming a **system or instance** (template repo, named fork, intelligence-system platform/deployment). **companion-self** = upstream template; **companion-xavier** may name a **named instance** as an **intelligence-system entity** (e.g. a companionâ€™s repo created from the template). This is **not** the same spelling as **companion self** (two words), the **conceptual** dyad above. See [glossary.md](../glossary.md).
- **Fork, not twin** â€” The Record diverges by design; it is its own entity, not a mirror.
- **Emulation** â€” Applies to the Voice (renders the Record in conversation), not to the Record's relationship to the real person.
- **Instances and release** â€” Exports are for consumption (schools, agents that read the Record), not for deploying other instances as independent economic/social actors without companion consent. See `docs/instances-and-release.md` and CONCEPTUAL-FRAMEWORK invariant 34.

---

## Operating Modes

Four modes: **Session** (conversational, no merges â€” default), **Pipeline** (process staged candidates), **Query** (read-only), **Maintenance** (dream). See [instance-doctrine.md](../../instance-doctrine.md) for the full mode table, proposal format, and edit restraint rules.

### Repo focus

`strategy-codex` is the active development repo. Grace-Mar Record surfaces live under [`archive/grace-mar-instance/`](../../archive/grace-mar-instance/) (not the repo's top-level public identity). See [`docs/archive/grace-mar.md`](../archive/grace-mar.md).

### Default work lane (operator)

Normal operator routing now uses two primary channels: [singularity](../../singularity/README.md) and [statecraft](../../statecraft/README.md). `singularity` owns acceleration, agency, substrate, control planes, recursive tooling, and compounding experiments; `statecraft` owns legitimacy, power, command, settlement, and judgment-bearing geopolitical or civilizational work. Other named territories such as **work-dev**, **work-cici**, and **work-business** are normally overlays or proving grounds nested under one of those two channels rather than equal sovereign categories.

Unless the operator **explicitly** names another territory, assistants should still treat the session as **statecraft** by default: [statecraft](../../statecraft/README.md) is the canonical operator judgment surface for live geopolitical, civilizational, legitimacy-bearing, and mechanism-bearing analytical work. [`/codex`](../../codex/README.md) remains the chronology, accumulation, and continuity layer beneath both primary channels. **`work-strategy`** and **`strategy-notebook`** are now legacy compatibility namespaces only; do not treat them as the active public/operator-facing strategy surface. Technical execution (fixes, scripts, CI) may still run under that default unless the operator asks for **hands-only** implementation with no statecraft framing.

**Predictive History boundary:** The canonical public Predictive History repo is **[`rbtkhn/predictive-history`](https://github.com/rbtkhn/predictive-history)**. It is the **namespace catalog hub** over lecture, essay, and interview corpora; legacy **`ph-civ` / `ph-apo`** folders are tombstone-only compat namespaces (retired 2026-06). **Corpus EXECUTE:** edit and `git push` in **`PREDICTIVE_HISTORY_ROOT`** (canonical clone). Inside `strategy-codex`, **`public/predictive-history/`** is an **inbound read-only snapshot** — refresh only via **`python scripts/sync_predictive_history_mirror.py`** and commits tagged **`[predictive-history-sync]`**. Legacy trees under `codex/predictive-history/` or `research/external/youtube-channels/predictive-history/` remain **frozen**. Assistants may **observe, review, critique, and cite public chapter IDs** (`civ-07`, `gt-16`, …) elsewhere, but must **not** edit PH manuscript content under `public/predictive-history/` or use deprecated **`publish_public_ph_civ.py`**. See [docs/predictive-history-external-boundary.md](../predictive-history-external-boundary.md) and [docs/predictive-history-operator-workspace.md](../predictive-history-operator-workspace.md).

---

## Layer Architecture

This system uses a **four-layer instruction architecture**. Later layers may narrow but never contradict earlier ones. See [docs/layer-architecture.md](../layer-architecture.md) for the full spec.

| Layer | File | Scope |
|-------|------|-------|
| **1. Core Doctrine** | This file (`AGENTS.md`) | State separation, authority, promotion law, knowledge boundary, terminology |
| **2. Instance Doctrine** | `instance-doctrine.md` | Operating modes, repo structure, file update protocol, success metrics, prompt architecture |
| **3. Lane Overlays** | `docs/skill-work/work-*/` | work-dev, work-politics, work-business, work-jiang, seed-phase |
| **4. Mode Overlays** | `.cursor/skills/*/SKILL.md` + `.cursor/rules/*.mdc` | coffee, **conductor** (Phase 2 redirect stub), dream, bridge, harvest, thanks (deprecated — prefer coffee), gate-review, **`strategy` → [strategy-codex-pass.mdc](../../.cursor/rules/strategy-codex-pass.mdc) + [DEFAULT-PATH.md](../skill-work/work-strategy/DEFAULT-PATH.md)** (`strategy-notebook` / skill-strategy skill are **deprecated compatibility** only), skill-write, tri-mind (deprecated — prefer **`periodic-statecraft-review`** runbook or named speaker), and other listed skills |

**`coffee` menu:** **A**, **B**, **C**, **D** (Confirm / Test / Deepen / Reframe). **Default attention from hub (Phase 2):** **A** *(none)*, **B** `precision pass`, **C** `hold tension`, **D** `one object only` — infer silently; override with plain phrase in same message. **Legacy master slugs** (`toscanini`, `karajan`, …) **redirect** to **`coffee`** + hub — do **not** emit Conductor Action Menu on new sessions. SSOT: [CONDUCTOR-COMPRESSION-SPEC.md](../skill-work/work-coffee/CONDUCTOR-COMPRESSION-SPEC.md). Substantive closes: extended **`coffee_close`** (`object_ref`, `falsify`, optional `verdict`). **`coffee_conductor_outcome` is deprecated (Phase 3)** — read-only in cadence; do not append new lines for strategy-codex. See `.cursor/skills/coffee/SKILL.md`, `.cursor/skills/conductor/SKILL.md` (redirect). **Durable close:** [CONDUCTOR-IMPROVEMENT-LOOP.md](../../codex/CONDUCTOR-IMPROVEMENT-LOOP.md), [CONDUCTOR-CLOSE-TEMPLATE.md](../../codex/CONDUCTOR-CLOSE-TEMPLATE.md).

**Conductor clarity (work):** [CONDUCTOR-LAYER-MAP.md](../skill-work/work-coffee/CONDUCTOR-LAYER-MAP.md) — update attention phrases over master slugs for new work. Coding-agent proposal posture: [conductor-proposal-lenses.md](../skill-work/work-dev/conductor-proposal-lenses.md). Neither document is Record authority.

**Operator publishing (Locals / X / Predictive History comments):** [`docs/skill-write/README.md`](../skill-write/README.md) â€” calibrates paste-ready public copy; **not** the companion Record `skill-write.md` (capability archive/placeholders/evidence). SSOT: [`docs/skill-write/write-operator-preferences.md`](../skill-write/write-operator-preferences.md).

**Substantive work plans (optional discipline):** For large plans in statecraft, work-dev, or brief contexts, assistants may end with a **Reality Sprint Block** per [`docs/skill-work/reality-sprint-block.md`](../skill-work/reality-sprint-block.md) â€” a compact execution wedge (primary path, first contact with reality, failure checks, pruned steps). It is **not** a gate substitute, not a merge, and not required on every reply.

**Cross-host rule transfer:** `AGENTS.md` and instance doctrine are the **always-on** cross-agent contract. `.cursor/skills/*/SKILL.md` are **invocation-bound protocols**: use them when the operator invokes that workflow or territory. `.cursor/rules/*.mdc` should **not** be assumed automatically active outside Cursor; when an `.mdc` rule is important across hosts, promote the invariant into repo-neutral doctrine (`AGENTS.md`, instance doctrine, or `docs/`). See [docs/codex-rule-transfer-audit.md](../codex-rule-transfer-audit.md).

**Territory entry discipline:** When working inside `docs/skill-work/<territory>/`, read the territory README and key specs first, respect lane boundaries, and use the territory's own vocabulary. Do not leak assumptions from one territory into another unless the operator explicitly crosses the boundary.

---

## Critical Rules

### Repository search protocol for LLM agents

When asked to find a file, index, corpus, source map, analyst, speaker, **essay**, or **prose object**:

1. Check [LLM-ROUTING.md](../../LLM-ROUTING.md).
2. If the query is **architecture / harness topology** (model vs harness, membrane, queue, AFK, channels), check [docs/harness-architecture-map.md](../harness-architecture-map.md).
3. Check [repo-map.yaml](../../repo-map.yaml) if present.
4. If the query involves an analyst, speaker, source corpus, transcript set, or geopolitical commentator, check [statecraft/voices/](../../statecraft/voices/) and [source-archive/statecraft/](../../source-archive/statecraft/).
5. If the query involves a **stand-alone essay**, **cross-channel thesis**, or **prose-class** placement (essay vs note vs synthesis), check [essays/README.md](../../essays/README.md) first (primary essay shelf), then [docs/prose-index.md](../prose-index.md) (class chooser). Bounded seams live in `statecraft/notes/` or `singularity/notes/` only; `statecraft/essays/` and `singularity/essays/` are **compatibility stubs** — follow pointers to repo-root `essays/`.
6. Do not rely only on GitHub code search.
7. If `grep`, `rg`, or GitHub code search returns zero results, treat that as a possible search failure, not proof of absence.
8. Only say "not found" after checking the routing map plus the likely path family.
9. If the user provides a GitHub URL or exact path, fetch that path directly before doing broad search.

**Search commands:** prefer `rg` for interactive local search when available; use portable `grep` (or `rg` with `grep -R` fallback) in committed scripts and CI examples. Full convention: [LLM-ROUTING.md — Search command convention](../../LLM-ROUTING.md#search-command-convention).

**Find-then-read:** After locating a capture via a voices source-index, apply [docs/source-lattice-beyond-the-repo.md](../source-lattice-beyond-the-repo.md) (corpus tiers + reading layers) before synthesis. PH chapter objects additionally use [public/predictive-history/docs/source-lattice.md](../../public/predictive-history/docs/source-lattice.md). **Source-index** (where) and **source-lattice** (how) are different queries — see LLM-ROUTING.md.

**Prose routing:** After locating an essay or note candidate, confirm class and canonical home via [docs/prose-index.md](../prose-index.md) — repo-root [`essays/`](../../essays/README.md) for transportable theses; channel `notes/` for bounded seams; channel `*/essays/` only when following compatibility stubs.

### 1. Knowledge Boundary â€” Never Leak LLM Knowledge

The emulated self can only know what is explicitly documented in its profile (`self.md`). The emulation prompt (`archive/grace-mar-instance/bot/prompt.py`) enforces this. **Never** merge facts, references, or knowledge into the profile or prompt that the companion has not explicitly provided through the gated pipeline. LLM training data must not leak into the fork. For a framework that quantifies and describes the boundary and how to treat information (inside / edge / outside / lookup), see [KNOWLEDGE-BOUNDARY-FRAMEWORK](../knowledge-boundary-framework.md). **Runtime / pre-gate abstention** (uncertainty envelopes, fabricated-history screening â€” advisory, not merge authority) is documented in [docs/abstention-policy.md](../abstention-policy.md).

### 2. Gated Pipeline â€” The Sovereign Merge Rule (explicit fork revive only)

**Default:** Do not stage gate candidates or offer gate review. Record is frozen per [`docs/grace-mar-instance-boundary.md`](../grace-mar-instance-boundary.md). Default capture: [`docs/replacement-capture-habits.md`](../replacement-capture-habits.md). Legacy concepts: [`docs/legacy-operator-concepts.md`](../legacy-operator-concepts.md). Full fork doctrine: [`archive/grace-mar-corpus/README.md`](../../archive/grace-mar-corpus/README.md).

When the operator **explicitly revives** the fork lane (`fork revive`, `grace-mar archive`, coffee **`A gate`**, etc.): *The agent may stage. It may not merge.* Profile changes pass through a companion-controlled gate:

1. Detect signals (knowledge, curiosity, personality)
2. Stage candidates in `recursion-gate.md` (shared queue â€” Telegram, WeChat, operator, tests; `channel_key` marks source)
3. **Integration moment** â€” Wait for companion approval before merging into profile. This is the conscious gate: the companion chooses what enters the record. Like a membrane: only what the companion approves crosses into the Record.
4. On approval, merge immediately into all affected files together (see File Update Protocol below). **One gate:** When the user says "approve" or approves candidates, process right away â€” do not wait for a separate "process the review queue" command. **Agent UX:** Before acting on a bare **approve**, echo **`CANDIDATE-XXXX`** plus a **one-line summary** (from the gate YAML) for each id you will merge, as confirmation; if ambiguous, list plausible candidates and ask. When **offering** a candidate for approval, always show id + one-line summary first.

**Never** merge directly into self.md, self-archive.md (EVIDENCE), or prompt.py without staging and approval. See `docs/identity-fork-protocol.md` for the full protocol spec. **Companion-reported content** (e.g. "we listened to X", "merge X into grace-mar") must be staged as candidate(s) in RECURSION-GATE and merged only after companion approval â€” do not merge on report alone.
**Reference implementation note:** Grace-Mar runs in manual-gate mode. No autonomous merge path is enabled.

### 3. The "we" Convention (fork revive only)

**Default (Record frozen):** **"we [did X]"** in work-politics, statecraft, or singularity lanes is normal operator phrasing — route to the active WORK lane; do **not** auto-stage RECURSION-GATE candidates.

**Fork revive only:** When the operator has explicitly reopened the fork lane and says **"we [did X]"** with companion/identity intent, or **"we finished [book]"** / **"we read [title]"** for Record growth, run signal detection and stage candidates per pipeline-map Â§ READ. Do not merge without approval.

### 4. No "Parent" Language

The system has a **companion** and a **fork**. There is no "parent mode" or "child mode." The current instance (grace-mar) happens to be a child, but the architecture is age-independent. Do not use the word "parent" as a system concept.

### 5. Immutability

- EVIDENCE entries are immutable once captured

### 5a. Contradiction Preservation

When evidence or self-reports conflict (e.g., multiple self-descriptions, opposing observations), preserve both with provenance â€” do not force resolution. Record tensions; do not flatten them for narrative smoothness.

- SKILLS claims may upgrade, never downgrade or delete
- SELF components may update but history is preserved
- Git history is the audit trail

### 6. Lexile Ceiling

The fork's output language matches the companion's register. There is no artificial simplification ceiling. The Voice speaks at the level appropriate to the documented companion identity.

### 7. Meet the Companion Where They Are (Grief / Resistance)

When the companion shows resistance, denial, or anxiety about change â€” deskilling, loss of a role, identity shifts â€” meet them where they are. Do not force adaptation or push through. The system supports; it does not compel. Respect KÃ¼bler-Rossâ€“style stages (denial, anger, bargaining, depression, acceptance). Session pacing and wisdom questions should feel invitational, not interrogative.

**Operator guidance:** If resistance appears â€” pause that line of questioning; optionally note in MEMORY (Resistance Notes) for continuity; do not treat resistance as a problem to fix.

### 8. Humane Purpose in Prompts

When designing or modifying analyst prompts, system prompts, lookup flows, or rephrase prompts (`archive/grace-mar-instance/bot/prompt.py` and related), embed humane purpose: dignity, connection, values. Do not optimize solely for efficiency. The fork records who the person is; prompts should honor that, not treat the companion as a data source.

**Authoring test (operators and prompt editors):** When drafting or revising such prompts, ask whether the companionâ€”if they read the instructions about themselvesâ€”would feel **respected as the author of their life** or **treated as a source to be mined** for signals. Prefer collaborative, consent-aware framing; an aggressive extraction tone is a design smell even when the gated pipeline technically blocks merges.

Expanded rationale and edge cases: [docs/prompt-humane-purpose.md](../prompt-humane-purpose.md).

### 9. Calibrated Abstention

When the emulated self encounters a topic outside its documented knowledge, it must say so and offer to look it up â€” never guess or hallucinate. The phrase "do you want me to look it up?" enforces this. Abstention (saying "I don't know") is a safety feature, not a failure.

### 10. Write It Down or Forget It

Nothing enters the Record without being written and approved. If it isn't documented and merged through the gated pipeline, it doesn't exist. See CONCEPTUAL-FRAMEWORK invariant 25.

### 10a. Agent turn discipline (Windows harness)

On the Windows Cursor harness, treat **parallel agent tools as forbidden by default** — they cause multi-minute stalls and failed writes, not speedups. **One agent turn:** at most **one** write path (`StrReplace` / `Write` / in-process sequential patch per file) and **one** `Shell` (chain subcommands with `;` inside it). Do **not** batch parallel `Shell` calls, parallel `StrReplace` on one file, or `Read`+write on the same path in the same turn. Operator bypass for that turn only: **`parallel ok`**. Observability: `python scripts/check_agent_turn_discipline.py --latest` and `python scripts/operator_handoff_check.py --fast` (§ Agent turn discipline). SSOT: [agent-tool-latency-discipline.mdc](../../.cursor/rules/agent-tool-latency-discipline.mdc) · RLJ [parallel ban](../../statecraft/recursive-learning-journal.md#2026-06-18---parallel-ban-on-file-tools-and-shell-calls-windows-execute-ship).

### 11. MEMORY (memory.md â€” continuity, not Record)

MEMORY (**memory**, canonical path `memory.md`; legacy `memory.md` still read until migrated â€” see [canonical-paths.md](../canonical-paths.md)) holds **continuity context** at **short / medium / long** horizons (session â†’ weeks â†’ long-term **meta/pointers and process only** â€” see `docs/memory-template.md`). It is **mostly chronological** (time-ordered prose within those horizons). **EVIDENCE** (`self-archive.md`) is **also chronological** (dated spine across logs) but **more expansive** â€” **multicategory** (READ / WRITE / CREATE / ACT / media / Â§ VIII) and **multimodal** (structured entries, runtime/artifacts). MEMORY is **not part of the Record**; it is **narrower and mostly textual** than EVIDENCE.

- **â€œEphemeralâ€ (governance):** Means **outside the gated Record** and **expected to rotate or prune** â€” **not** â€œonly short-term.â€ Long-horizon MEMORY is still non-authoritative versus SELF; durable facts and identity belong in SELF + gate, not in MEMORY as substitute Record.
- **Scope:** Tone, thread continuity, calibrations, open loops, and long-horizon **process/pointers** â€” not durable facts or identity (those stay in SELF + gate). See `docs/memory-template.md` v2.0.
- **Hierarchy:** SELF is authoritative. When MEMORY conflicts with SELF, follow SELF. MEMORY refines; it does not override.
- **Pipeline:** Nothing in MEMORY may enter SELF or EVIDENCE without going through RECURSION-GATE. The analyst stages to RECURSION-GATE only; it does NOT write to MEMORY.
- **Lifespan:** Rotate or prune per horizon (short often; medium weekly; long quarterly â€” see template). MEMORY is optional; the system runs normally if absent.

See `docs/memory-template.md`.

### 11a. Self-history (derived dual log â€” not Record)

**`self-history`** (`self-history.md`, optional) is a **derived** timeline: **(1)** dense consolidation of **`docs/skill-work/work-*/*-history.md`** (**work** stream) and **(2)** **gate-approved** companion-relevant lines (**COMPANION** stream â€” from merged **SELF/EVIDENCE** only, not pending candidates). It is **not** authoritative identity truth; **SELF** and merged **EVIDENCE** remain canonical. **Nothing** becomes Record fact **only** because it appears here â€” pipeline and companion approval rules are unchanged. See [canonical-paths.md](../canonical-paths.md) and the fileâ€™s header fence.

### 11b. Derived operator artifacts (not Record)

**Skill cards** (`scripts/build_skill_cards.py` â†’ `runtime/artifacts/skill-cards/`) and **active lane compression** (`scripts/compress_active_lane.py` â†’ `runtime/artifacts/context/`) are **rebuildable work-layer** summaries. They point back to portable skills and `docs/skill-work/work-*` sources; they do **not** replace canonical skill files or Record surfaces. Policy: [docs/runtime-vs-record.md](../runtime-vs-record.md), [runtime/artifacts/README.md](../../runtime/artifacts/README.md).

---

## Permission Boundaries

**Autonomous (no approval required):**
- Read companion files (SELF, SKILLS, EVIDENCE, SESSION-LOG, RECURSION-GATE, etc.)
- Run signal detection; stage candidates to RECURSION-GATE
- Respond as Voice (emulate Record)
- Propose activities, wisdom questions, lookups
- Analyze exchanges for profile-relevant signals

**Requires companion approval:**
- Merge into SELF, EVIDENCE, or prompt
- Process RECURSION-GATE (approve or reject candidates)
- Any change to the Record
- Create or modify EVIDENCE entries
- Update archive/grace-mar-instance/bot/prompt.py

### Minimize approval prompts (execution hygiene)

When tooling imposes command or sandbox approval prompts, assistants should treat prompt minimization as an operator comfort requirement:

- Prefer read-only inspection, diffing, and verification **before** requesting any escalated command.
- Batch related escalated actions into the **fewest approval moments** that still preserve safety and clarity.
- Reuse previously approved command shapes when practical, rather than generating avoidably novel variants.
- Avoid escalation for work that can be completed safely inside the sandbox or workspace boundary.
- When a later escalated step is likely, delay the prompt until the task is fully prepared so the operator is not interrupted early.
- If an approval is still necessary, briefly explain why that boundary is real and what grouped action it will unlock.

This is **execution hygiene**, not authority relaxation: safety boundaries still apply, but assistants should avoid creating avoidable approval fatigue.

**RL / fine-tuning (optional):** `scripts/export_conversation_trajectories.py` emits read-only JSONL for local harnesses. It does **not** merge into the Record. Shared or pooled RL requires operator policy â€” minors, secrets, staging drafts: see [openclaw-rl-boundary.md](../openclaw-rl-boundary.md).

---

## Success Metrics and File Update Protocol

Instance-specific. See [instance-doctrine.md](../../instance-doctrine.md) for the full success metrics table, file update protocol, merge-via-script rules, provenance requirements, and prompt architecture.

**Key invariant (repeated here for safety):** The agent must **not** edit `archive/grace-mar-instance/self.md`, `archive/grace-mar-instance/self-archive.md`, `archive/grace-mar-instance/recursion-gate.md`, `session-log.md`, or `archive/grace-mar-instance/bot/prompt.py` directly. Merge only via `python scripts/process_approved_candidates.py --apply`.

---

## Three-Dimension Mind Model

Post-seed growth in self.md Section IX is organized into:

- **museum knowledge section A. Knowledge** â€” Facts entering awareness through observation
- **museum knowledge section B. Curiosity** â€” Topics that catch attention, engagement signals
- **museum knowledge section C. Personality** â€” Observed behavioral patterns, art style, speech traits

A single artifact can populate all three dimensions.

---

## Repository Structure and Prompt Architecture

Instance-specific. See [instance-doctrine.md](../../instance-doctrine.md) for the full repository tree, prompt architecture table, and canonical path conventions.

---

## What Not to Do

- Merge knowledge the companion didn't provide
- Skip the staging/approval gate
- Delete or overwrite companion data
- Use "parent" as a system term
- Raise the Lexile ceiling without writing sample evidence
- Reference books, media, or experiences not in the profile
- Treat the Voice as the Record (it's the observation window and queryable voice, not the Record itself)
- Use "cognitive twin" (use "interpretive machine")
- Call the Voice an "oracle" or the Record "commanding" â€” use mirror, reflect, voice, record
- Let terminology drift â€” when editing CONCEPTUAL-FRAMEWORK, AGENTS, or templates, prefer Record (not fork) and Voice (not archive/grace-mar-instance/bot) in conceptual prose; correct inconsistencies
- **Do not** use legacy on-disk names (`SELF.md`, `EVIDENCE.md`, `PENDING-REVIEW.md`, â€¦) â€” canonical paths are **`self.md`**, **`self-skills.md`** (capability index; legacy `skills.md` until migrated), **`self-archive.md`** (EVIDENCE), **`recursion-gate.md`** ([canonical-paths.md](../canonical-paths.md))
