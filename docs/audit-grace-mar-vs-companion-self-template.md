# Audit: Grace-Mar vs Companion-Self Template

**Purpose:** Assess how well the grace-mar **instance** aligns with the companion-self **template** specification. Companion-self is the template repo ([github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self)) â€” concept, protocol, seed, structure â€” and the origin for Grace-Mar and future instances. The template is defined in [COMPANION-SELF-BOOTSTRAP](../bootstrap/companion-self-bootstrap.md), [COMPANION-SELF-DEVELOPER-PLAN](companion-self-developer-plan.md), and [MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md). Grace-mar is the reference implementation and the source from which the template was extracted; this audit checks that the instance has the structure, docs, and behavior the template expects. **See also:** [grace-mar vs companion-self](grace-mar-vs-companion-self.md) for a side-by-side instance vs template comparison.

**Scope:** Structure, concept compliance, protocol compliance, schema alignment, governance, and sync readiness. Not a full security or UX audit.

**Date:** March 2026

---

## 1. Template expectations for an instance

From the bootstrap and merge doc, an **instance** (e.g. grace-mar) is expected to:

- Have a **Record** under ``: SELF, SKILLS, EVIDENCE, RECURSION-GATE, and related pipeline/archive files.
- Run a **bot** (or equivalent Voice) and **pipeline** (stage â†’ approve â†’ merge).
- Hold **instance-specific config** (e.g. Telegram, domain, PRP output) that is never overwritten by template sync.
- Maintain **copies of template docs** (concept, protocol, schema templates, AGENTS) that can be updated when the template is updated.
- Follow the **Identity Fork Protocol** (stage only; no merge without approval; evidence linkage).
- Enforce the **knowledge boundary** and **operating modes** in AGENTS.md.

---

## 2. Structure audit

| Expectation | Grace-mar | Status |
|-------------|-----------|--------|
| `` with one companion | `` present | âœ… |
| self.md | Present | âœ… |
| skills.md | Present | âœ… |
| self-archive.md | Present â€” canonical **EVIDENCE** (activity spine + Â§ VIII gated approved log per [canonical-paths.md](canonical-paths.md)) | âœ… |
| self-evidence.md | Optional compatibility pointer only; tooling prefers `self-archive.md` ([AGENTS.md](../AGENTS.md)) | âœ… (if present) |
| recursion-gate.md | Present | âœ… |
| self-memory.md (template: `_template/self-memory.md`) | Optional; present | âœ… |
| session-transcript.md / SESSION-LOG | Present | âœ… |
| pipeline-events.jsonl | Present | âœ… |
| self-library.md | Present | âœ… |
| Artifacts (CREATE-*, WRITE-* evidence) | `artifacts/` | âœ… |
| Bot code | `bot/` (Telegram, WeChat, core, prompt) | âœ… |
| Merge script | `scripts/process_approved_candidates.py` | âœ… |
| PRP export | `scripts/export_prp.py`; output e.g. `grace-mar-llm.txt` | âœ… |
| Validation | `scripts/validate-integrity.py` | âœ… |
| Governance check | `scripts/governance_checker.py` | âœ… |

**Verdict:** Structure is complete. All template-expected instance components exist.

---

## 3. Concept compliance

The template concept (Mind + Record + Voice; cognitive fork; sovereign merge; knowledge boundary) must be reflected in the instanceâ€™s design and docs.

| Concept | Where in grace-mar | Status |
|---------|--------------------|--------|
| Record = documented self; Voice = speaks Record | CONCEPTUAL-FRAMEWORK, AGENTS, ARCHITECTURE | âœ… |
| Triadic cognition (Mind, Record, Voice); tricameral mind synonym | AGENTS, CONCEPTUAL-FRAMEWORK, prompt/PRP | âœ… |
| Fork, not twin | CONCEPTUAL-FRAMEWORK, AGENTS | âœ… |
| Knowledge boundary (no LLM leak) | AGENTS Â§1, KNOWLEDGE-BOUNDARY-FRAMEWORK, prompt | âœ… |
| Sovereign merge (companion gates) | AGENTS Â§2, IDENTITY-FORK-PROTOCOL | âœ… |
| Evidence linkage | IDENTITY-FORK-PROTOCOL, EVIDENCE-TEMPLATE, File Update Protocol | âœ… |

**Verdict:** Concept is implemented and documented. Instance is suitable as the source for generalizing the template concept doc.

---

## 4. Protocol compliance (Identity Fork Protocol)

| Rule | Implementation | Status |
|------|----------------|--------|
| Agent may stage, may not merge | Analyst stages to RECURSION-GATE; merge only via `process_approved_candidates.py` after human approval | âœ… |
| No direct merge into SELF/EVIDENCE/prompt without staging and approval | AGENTS Â§2; no code path merges without approval | âœ… |
| Evidence linkage (claims traceable) | EVIDENCE entries, ACT-*, CREATE-*, WRITE-*; provenance in SELF IX entries | âœ… |
| Manual gate only (no autonomous merge) | Documented in AGENTS and IDENTITY-FORK-PROTOCOL; no autonomous merge path | âœ… |

**Verdict:** Protocol is followed. Grace-mar is a valid reference implementation for the template protocol doc.

---

## 5. Schema alignment (template paths)

Template alignment is now best understood in **two layers**:

1. **Concept / protocol alignment** â€” does grace-mar implement the same governing model?
2. **Manifest / path alignment** â€” does grace-mar mirror or explicitly account for the live template's current file surface?

Grace-mar remains strongly aligned on the first layer. The second layer is now **partial**, because the live companion-self repo has added template files and path names that are not yet fully reflected in grace-mar's local sync docs.

| Template path | In grace-mar | Notes |
|---------------|--------------|--------|
| `docs/identity-fork-protocol.md` | âœ… | Present, but differs from template copy |
| `docs/concept.md` | âš ï¸ | No same-name file; concept is covered across `docs/conceptual-framework.md` and `docs/architecture.md` |
| `docs/seed-phase.md` | âš ï¸ | No same-name file; seed phase is covered in ARCHITECTURE and operator docs |
| `docs/long-term-objective.md` | âŒ | Template-only path; not yet mirrored or explicitly mapped in grace-mar |
| `docs/two-hour-screentime-target.md` | âŒ | Template-only path; not yet mirrored or explicitly mapped in grace-mar |
| `docs/instance-patterns.md` | âŒ | Template-only path; not yet mirrored or explicitly mapped in grace-mar |
| `_template/` | Reference only | Correctly absent as a live instance path; should remain template-side |
| `template-manifest.json` / `template-version.json` | âš ï¸ | Not tracked locally as sync anchors; no recorded baseline yet |
| Grace-mar schema mirrors (`docs/self-template.md`, `docs/skills-template.md`, `docs/evidence-template.md`, `docs/memory-template.md`, `AGENTS.md`) | âœ… | Present and still valid instance-side mirrors / elaborations |

**Verdict:** Grace-mar is **conceptually aligned** with the companion-self template, but **path / manifest alignment is partial**. The local instance still matches the template's governing model, yet the sync contract and audit docs lag the live template surface.

---

## 6. Governance and operating modes

| Item | Status |
|------|--------|
| Operating modes (Session, Pipeline, Query) defined in AGENTS | âœ… |
| Session: no merge; pipeline only on "we [did X]" or explicit processing | âœ… |
| Pipeline: stage to RECURSION-GATE; process approved via script | âœ… |
| Query: read-only | âœ… |
| Knowledge boundary rule (no undocumented facts in Record) | âœ… |
| Lexile / WRITE-derived voice (skill-write) | âœ… (prompt, SKILLS-MODULARITY) |
| No "parent" language; companion terminology | âœ… |

**Verdict:** Governance and operating modes match the templateâ€™s expectations.

---

## 7. Gaps and recommendations

### 7.1 Audit drift to fix

- **Local audit verdict is too strong:** Earlier wording said all template paths exist in grace-mar. That is no longer accurate against the live template manifest.
- **Template sync log / manifest diff:** [MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md) Â§3 now records governance merges and manifest-diff refreshes; [work-companion-self/audit-report-manifest.md](skill-work/work-companion-self/audit-report-manifest.md) is regenerated with `template_diff.py --use-manifest`. Governance baseline remains pinned in [TEMPLATE-BASELINE.md](skill-work/work-companion-self/TEMPLATE-BASELINE.md) (`288b438`) while `main` may move â€” re-run the diff after pulls.
- **Manifest-first sync contract not yet fully internalized:** Grace-mar now acknowledges manifest-driven sync, but operator habit should treat `template-manifest.json` + diff report as the first stop on each sync.
- **_template/ in template repo:** Correctly absent in grace-mar as a live instance path. This is not a defect, but the audit should distinguish template-only scaffolds from missing instance mirrors.

### 7.2 Instance-only vs template

- Grace-mar contains **instance-only** docs (PROFILE-DEPLOY, NAMECHEAP-GUIDE, OPERATOR-WEEKLY-REVIEW, instance/operator workflows, etc.). This is correct: they stay in the instance and are not overwritten by template sync. No change needed.
- **`bootstrap/companion-self-bootstrap.md`** in grace-mar is the reference copy for the companion-self template. Thatâ€™s intentional per Â§6: â€œThis file can live in grace-mar; the companion-self repo now exists at https://github.com/rbtkhn/companion-self.â€ No change needed.

### 7.3 Naming and consistency

- **WORK vs BUILD:** Prose and standard labels use WORK; internal IDs (BUILD container, CREATE-nnn, ACT-nnn) unchanged. Aligns with the deliberate design; template, when extracted, should use the same convention (WORK in prose, BUILD as internal identifier where relevant).
- **SKILLS-MODULARITY:** Formal module set (including self-knowledge, self-personality, self-curiosity, self-library, self-skill-*) is documented. Template concept doc could reference this structure when generalizing.

### 7.4 Seed phase

- Seed phase is **defined** in ARCHITECTURE (Fork Lifecycle, Seeding) and **operationalized** in OPERATOR-BRIEF and in grace-marâ€™s SEED-PHASE-2-SURVEY, SEED-PHASE-3-SURVEY. The templateâ€™s seed-phase doc can be derived from these. No gap.

### 7.5 Template promotion â€” doc-only loop

When grace-mar proves a **repeatable** pattern that belongs upstream, use companion-self `.cursor/skills/promote-from-grace-mar/SKILL.md` (checklist, strip instance data). After a successful promote, add **one line** to [instance-patterns.md](instance-patterns.md) or refresh [MERGING-FROM-COMPANION-SELF.md](merging-from-companion-self.md) / manifest diff notes so the next sync does not rediscover the same delta. This loop does **not** merge into the Record.

---

## 8. Summary

| Area | Result |
|------|--------|
| Structure | âœ… Complete |
| Concept compliance | âœ… Aligned |
| Protocol compliance | âœ… Aligned |
| Schema / template paths | âš ï¸ Partial |
| Governance & operating modes | âœ… Aligned |
| Gaps | Path-level parity with template `main` remains partial; manifest diff report is refreshed on a schedule or after template pulls |

**Conclusion:** Grace-mar remains a valid **reference implementation** of the companion-self model, and it is still aligned on concept, protocol, and governance. **Path-level** alignment is partial by design (instance WORK tree is much larger than the template). The operator refreshes [audit-report-manifest.md](skill-work/work-companion-self/audit-report-manifest.md) against companion-self `main` to see drift; governance merges stay pinned per [TEMPLATE-BASELINE.md](skill-work/work-companion-self/TEMPLATE-BASELINE.md) until a new merge is recorded.

---

*Audit performed per COMPANION-SELF-BOOTSTRAP and COMPANION-SELF-DEVELOPER-PLAN. Re-run after material changes to structure, protocol, or template expectations.*

