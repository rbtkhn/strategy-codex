# Instance Doctrine Ã¢â‚¬” single operator

> Instance-specific operating rules for the single-operator companion fork. This file is **Layer 2** in the [four-layer instruction architecture](../../docs/layer-architecture.md). Core doctrine lives in [AGENTS.md](../../AGENTS.md); this file may narrow but never contradict it.

---

## Operating Modes

Distinct modes govern what the agent may do. Avoid mixing them.

**Active identity:** Default all operator work to `strategy-codex` as a **governed interpretive machine** ([`docs/product-identity.md`](docs/product-identity.md)). **Grace-Mar cognitive fork is frozen** — not a growth objective ([`docs/grace-mar-instance-boundary.md`](docs/grace-mar-instance-boundary.md), `platform/platform/config/strategy_codex.yaml`). Fork/gate/pipeline modes apply only on explicit **`fork revive`**. Mentions of `grace-mar` or `companion-self` in older docs are legacy unless the operator names that archive lane.

**Shared membrane:** For the typed `Record` / `governed adjacent` / `instrumental work` / `runtime / derived` / `external complements` model, see [docs/work-membrane-v2.md](docs/work-membrane-v2.md). Use [statecraft/work-membrane.md](statecraft/work-membrane.md) and [singularity/work-membrane.md](singularity/work-membrane.md) when the session is lane-specific.

| Mode | Purpose | Agent behavior |
|------|---------|----------------|
| **Session** | Interactive conversation | Default: statecraft/singularity WORK. Voice emulation **fork revive only**. Do not merge unless operator revives fork and says "we [did X]". |
| **Pipeline** | Process staged candidates | **Fork revive only.** Detect signals, stage to RECURSION-GATE; merge via `process_approved_candidates.py --apply`. Default capture: [replacement-capture-habits.md](docs/replacement-capture-habits.md). |
| **Query** | Browse or answer questions about the Record | Read-only. Report what is documented. Do not edit. |
| **Maintenance** | End-of-day consolidation (`dream`) | Run `scripts/auto_dream.py` Ã¢â‚¬” normalize self-memory, check integrity and governance, refresh contradiction digest, emit pipeline event. Read-only with respect to the Record; may write to self-memory and derived artifacts. No merge authority. See `.cursor/skills/dream/SKILL.md`. |

When in doubt, default to Session (conversational, no merges).

**Message-lane prefixes are cross-host doctrine:** When the operator prefixes a turn with `PLAN`, `EXECUTE`, `DOCSYNC`, or `EXECUTE_LOCAL`, treat that as a host-neutral scope signal governing edits, commits, and push behavior for the turn. Canonical spec: [docs/operator-agent-lanes.md](../../docs/operator-agent-lanes.md).

**Implementation preference:** The operator prefers to see a short proposal (scope, approach, files to touch) before the agent implements. Propose first; implement after approval.

**Proposal format:** One paragraph with: (1) Scope Ã¢â‚¬” what's in, what's out; (2) Approach Ã¢â‚¬” high-level steps or method; (3) Files Ã¢â‚¬” paths to create or modify. Trivial fixes (typos, obvious corrections) may skip proposal.

**Edit restraint:** When the operator asks to "think about", "consider", or explores conceptually Ã¢â‚¬” answer in prose. **Perhaps** / **maybe** (or clear equivalent) means they want **opinion and tradeoffs first**, not an implicit implement. Do not edit files unless implementation is clearly requested ("do it", "implement", "add this"). If unclear, prefer answer over edit.

**Short prompts are intentional:** Treat minimal operator prompts as a preference, not a lack of effort. Infer reasonable scope from context, produce fuller output from brief input, and ask for more specification only when the ambiguity is materially risky.

---

## Success Metrics (frozen Record — archaeology)

Fork-era Voice/pipeline metrics below apply only on **`fork revive`**. Active strategy-codex health: statecraft archive coverage, synthesis cadence, integrity scripts, ship receipts.

| Metric | Target | How to verify |
|--------|--------|---------------|
| **Language register** | Matches companion's register | Manual spot-check of bot responses |
| **Knowledge boundary** | No undocumented references | Bot never cites facts not in profile |
| **Pipeline health** | Candidates processed, not stale | RECURSION-GATE queue doesn't grow unbounded |
| **Profile growth** | IX entries increase over time | IX-A, IX-B, IX-C counts in profile |
| **Calibrated abstention** | "I don't know" when outside knowledge | Bot says "do you want me to look it up?" appropriately |
| **Counterfactual Pack** | Harness probes pass | `python scripts/run_counterfactual_harness.py` Ã¢â‚¬” run before prompt changes |
| **self-voice** (linguistic authenticity) | In-character, fingerprint markers | `python scripts/test_voice_linguistic_authenticity.py` Ã¢â‚¬” no AI disclosure, in-character |
| **Voice benchmark suite** | Voice stability and boundary compliance across model/prompt updates | `python scripts/run_voice_benchmark.py` Ã¢â‚¬” tone, age realism, abstention, bilingual, recall fidelity, overreach; use `-o results.json` for CI/trending |
| **Continuity fidelity** | Bridge round-trip >= 80% | `python scripts/test_bridge_continuity.py` or `pytest tests/test_bridge_continuity.py` Ã¢â‚¬” no LLM needed; run before bridge format changes |
| **Performance suite** | Local micro-benchmarks + optional I/O/LLM/HTTP tiers | `python scripts/run_perf_local.py` or `pytest tests/test_perf_local.py` (tier 1 in CI); full: `python scripts/run_perf_suite.py --tier 1 2 3`; see [perf-budgets.md](../../docs/perf-budgets.md) |
| **Judgment probes** | Voice makes value-aligned choices under ambiguity, reflects IX-C tensions | `python scripts/run_judgment_probes.py` Ã¢â‚¬” 8 probes targeting documented personality tensions; committed/trait_aligned/tension_preserved/age_appropriate scoring; use `-o results.json` for trending |
| **Identity delta** | Profile changes do not degrade Voice quality | `python scripts/eval_identity_delta.py` Ã¢â‚¬” runs judgment + voice benchmarks, computes deltas against saved baseline; run after gate merges |

---

## File Update Protocol

When pipeline candidates are approved, **merge** into all of these together. **Merge only via script:** The agent must **not** edit `self.md`, `self-archive.md`, `recursion-gate.md`, `session-log.md`, or `archive/grace-mar-instance/archive/grace-mar-instance/bot/prompt.py` directly. It must instruct the operator to run `python scripts/process_approved_candidates.py --apply` (or the receipt flow: `--generate-receipt` then `--apply --receipt`). This prevents five-file drift and preserves the audit trail. Only the script performs the atomic update across all files.

**Optional orchestration:** `scripts/atomic_integrate.py` runs the same merge (`--quick` / receipt-based semantics) with extra disk backups and a JSON receipt; it does not replace `process_approved_candidates.py`.

**Derived exports before merge:** `process_approved_candidates.py` runs `scripts/refresh_derived_exports.py` for the target user immediately before integrity preflight, so a stale `manifest.json` / PRP / runtime bundle cannot block merges after prior Record or prompt edits (operators need not run refresh by hand first).

| File | What to update |
|------|---------------|
| `self.md` | New entries merged into IX-A (Knowledge), IX-B (Curiosity), and/or IX-C (Personality) |
| `self-archive.md` | Canonical **EVIDENCE**: new activity log entry (ACT-XXXX) **and** append **Ã‚§ VIII. GATED APPROVED LOG** per merged candidate (gated; only `scripts/process_approved_candidates.py` writes Ã‚§ VIII) |
| `recursion-gate.md` | Move candidates from Candidates to Processed |
| `session-log.md` | New session record; pipeline merges append lines under `## Pipeline merge (automated)` |
| `archive/grace-mar-instance/archive/grace-mar-instance/bot/prompt.py` | Update relevant prompt sections + analyst dedup list |
| `pipeline-events.jsonl` | Append `applied` event per candidate: `python scripts/emit_pipeline_event.py applied CANDIDATE-XXXX evidence_id=ACT-YYYY` |
| **PRP** | Regenerate: `python scripts/export_prp.py -o self-llm.txt` (or repo default). Commit if changed. Keeps anchor in sync with Record. |

**Real-time log vs gated approved log:** The bot and Mini App append to `session-transcript.md` (raw conversation log for operator continuity). The **gated approved log** is **not** written in real time; it is appended only when candidates are merged Ã¢â‚¬” as **`self-archive.md` Ã‚§ VIII** (same gate as SELF/EVIDENCE). It holds voice-related approved summaries and other merge-line activity. Optional **`self-evidence.md`** is a **compatibility pointer** only; see [canonical-paths.md](../../docs/canonical-paths.md).

The bot emits `staged` events automatically. Emit `applied` (or `rejected`) when processing the queue.

**Post-merge PRP refresh:** After merging into SELF, EVIDENCE, or prompt, run the export script. If the output differs from the committed PRP file, commit the update.

**Gated commit hook (optional):** If pre-commit is installed with `pre-commit install --hook-type commit-msg`, commits that stage `self.md`, `self-skills.md`, `skills.md`, `self-evidence.md`, `self-archive.md`, `merge-receipts.jsonl`, `archive/grace-mar-instance/archive/grace-mar-instance/bot/prompt.py`, or PRP `*-llm.txt` must include **`[gated-merge]`** in the commit message (or mention `process_approved_candidates`). Emergency bypass: `ALLOW_GATED_RECORD_EDIT=1`. See `scripts/check_gated_record_commit_msg.py`.

**Provenance on IX entries:** When merging new entries into IX-A, IX-B, or IX-C, include `provenance: human_approved` (content passed the gated pipeline). Existing entries may use `curated_by: companion` as equivalent. Optionally record `source:` (e.g. `bot lookup`, `bot conversation`, `operator`) to indicate origin. Optionally add `scope:` or `constraint:` when the candidate implies a boundary. Optionally add `warrant:` Ã¢â‚¬” the unstated assumption that, if changed, would mean this entry should be revisited (e.g. "holds while limited self-regulation strategies are in use"). Omit for straightforward facts or stable preferences with no expiration condition. Do not backfill old entries unless the companion requests it.

---

## Prompt Architecture (archive/grace-mar-instance/bot/prompt.py)

Four prompts, each with a distinct role:

| Prompt | Purpose |
|--------|---------|
| `SYSTEM_PROMPT` | Emulation persona Ã¢â‚¬” defines who the self is, what they know, how they speak |
| `ANALYST_PROMPT` | Signal detection Ã¢â‚¬” analyzes exchanges for profile-relevant signals |
| `LOOKUP_PROMPT` | Knowledge lookup Ã¢â‚¬” factual research for the companion |
| `REPHRASE_PROMPT` | Answer rephrasing Ã¢â‚¬” converts search results into the self's voice and vocabulary |

The `SYSTEM_PROMPT` contains the self's knowledge, curiosity, and personality inline. It grows as content is merged into the fork. Apply summarization tiers to manage token count.

**IX parity (operator):** `SYSTEM_PROMPT` and `ANALYST_PROMPT` both embed IX-shaped text; either can drift from `self.md` if not updated with merges. Full checklist, `rebuild_ix` behavior, and root **`## RECORD STATE`** vs rebuild headers: [**docs/prompt-ix-sync.md**](../../docs/prompt-ix-sync.md).

**Summarization tiers (when IX lists grow):** Compress by category; preserve **warrants** and **IX-C tensions** where probes depend on them; keep **ANALYST** IX blocks accurate enough for **dedup** even if **SYSTEM_PROMPT** is tighter prose.

---

## Repository Structure

**Canonical user paths** (lowercase filenames): [docs/canonical-paths.md](../../docs/canonical-paths.md). **Dated filenames and CLI dates:** [docs/date-time-conventions.md](../../docs/date-time-conventions.md).

```
repo-root/
Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ AGENTS.md                    # Core doctrine (Layer 1)
Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ README.md                    # Project overview
Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ archive/grace-mar-instance/bootstrap/grace-mar-bootstrap.md  # Session bootstrap for Cursor
Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ docs/
Ã¢”â€š   Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ grace-mar-instance-boundary.md  # Live freeze SSOT
Ã¢”â€š   Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ legacy-operator-concepts.md   # Redirect table
Ã¢”â€š   Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ replacement-capture-habits.md # Default capture when frozen
Ã¢”â€š   Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ architecture.md         # Stub → archive/grace-mar-corpus/doctrine/
Ã¢”â€š   Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ conceptual-framework.md # Stub → archive/grace-mar-corpus/doctrine/
Ã¢”â€š   Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ layer-architecture.md   # Four-layer instruction model
Ã¢”â€š   Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ self-template.md        # SELF module template
Ã¢”â€š   Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ skills-template.md      # SKILLS module template
Ã¢”â€š   Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ evidence-template.md    # EVIDENCE module template
Ã¢”â€š   Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ wisdom-questions.md     # Child-tier wisdom elicitation questions (Save Wisdom inspired)
Ã¢”â€š   Ã¢””Ã¢”â‚¬Ã¢”â‚¬ ...                     # Supporting docs
Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ archive/grace-mar-instance/bot/
Ã¢”â€š   Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ core.py                 # Shared emulation logic (used by Telegram + WeChat)
Ã¢”â€š   Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ bot.py                  # Telegram bot
Ã¢”â€š   Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ wechat_bot.py           # WeChat Official Account bot (webhook server)
Ã¢”â€š   Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ prompt.py               # All LLM prompts (SYSTEM, ANALYST, LOOKUP, REPHRASE)
Ã¢”â€š   Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ wechat-setup.md         # WeChat integration setup guide
Ã¢”â€š   Ã¢””Ã¢”â‚¬Ã¢”â‚¬ requirements.txt        # Python dependencies
Ã¢””Ã¢”â‚¬Ã¢”â‚¬ 
    Ã¢””Ã¢”â‚¬Ã¢”â‚¬ repo-root/              # Active instance root (single operator)
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ instance-doctrine.md  # Instance-specific operating rules (Layer 2)
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ self.md             # Identity + three-dimension mind
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ self-skills.md      # Capability index (Claims, Gaps, Struggles, Milestones); legacy `skills.md` resolved until migrated
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ skill-think.md      # THINK container (repo-specific root filename; conceptual label: self-skill-think)
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ skill-write.md      # WRITE container (repo-specific root filename; conceptual label: self-skill-write)
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ codex/predictive-history/README-operator.md        # work Ã¢â‚¬” Jiang project
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ self-archive.md          # EVIDENCE Ã¢â‚¬” activity log + Ã‚§ VIII gated approved
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ self-evidence.md         # optional compatibility pointer (canonical body is self-archive.md)
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ self-library.md     # SELF-LIBRARY Ã¢â‚¬” reference-facing governed domains; CIV-MEM subdomain; not SELF-KNOWLEDGE
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ SELF-LIBRARY/       # Navigator: INDEX.md, CIV-MEM.md (optional; points at self-library + corpus)
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ self-memory.md      # self-memory Ã¢â‚¬” short/medium/long continuity (optional; not part of Record; rotatable)
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ self-history.md     # Derived dual log: work aggregate + gate-approved companion thread (optional; not Record)
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ session-log.md      # Interaction history
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ recursion-gate.md   # Pipeline staging
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ archive/queues/reflection-proposals/  # Operator reflection cycle outputs (REFLECT-*.md); not canonical Record
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ pipeline-events.jsonl  # Append-only pipeline audit log
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ harness-events.jsonl    # Optional harness audit (merge/export); see docs/harness-inventory.md
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ compute-ledger.jsonl   # Token usage (energy ledger)
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ journal.md                # Daily highlights Ã¢â‚¬” public-suitable, shareable
        Ã¢”Å“Ã¢”â‚¬Ã¢”â‚¬ archives/             # Rotated chunks (SELF-ARCHIVE-YYYY-MM.md)
        Ã¢””Ã¢”â‚¬Ã¢”â‚¬ runtime/artifacts/          # Raw files (writing, artwork)
```

---

## Repository search protocol (agents)

Cross-host mirror of [AGENTS.md — Repository search protocol for LLM agents](AGENTS.md#repository-search-protocol-for-llm-agents). Full step list lives in AGENTS; prose-specific routing:

1. Check [LLM-ROUTING.md](LLM-ROUTING.md) and [repo-map.yaml](repo-map.yaml) when locating files, indexes, or routing surfaces.
2. **Stand-alone / cross-channel essays** → [essays/README.md](essays/README.md) (primary shelf). Channel `statecraft/essays/` and `singularity/essays/` hold **compatibility stubs** only — follow pointers to repo-root `essays/`.
3. **Prose class** (note vs essay vs synthesis) → [docs/prose-index.md](docs/prose-index.md).
4. **Bounded interpretive objects** → `statecraft/notes/` or `singularity/notes/` only (channel-scoped; do not split at note layer).
5. **Prose routing after locate:** Confirm canonical home via prose-index before citing, editing, or promoting essay-class material.

Active operator channels: [statecraft/](statecraft/README.md), [singularity/](singularity/README.md). Product essay: [essays/from-accumulation-to-governed-interpretive-machine.md](essays/from-accumulation-to-governed-interpretive-machine.md).

---

## Instance-specific terminology

- **Do not** use legacy on-disk names (`SELF.md`, `EVIDENCE.md`, `PENDING-REVIEW.md`, …) Ã¢â‚¬” canonical paths are **`self.md`**, **`self-skills.md`** (capability index; legacy `skills.md` until migrated), **`self-archive.md`** (EVIDENCE), **`recursion-gate.md`** ([canonical-paths.md](../../docs/canonical-paths.md))
