# work-cici â€” advisor / project module (grace-mar)

## Purpose

**Cici AI** is the active singularity-native and human-facing name for this lane; the live folder now sits at `singularity/work-cici/`, while `docs/skill-work/work-cici/` remains a compatibility pointer.

`work-cici` is a WORK territory in the grace-mar repo for coordinating advisor/project work with Cici, formerly tracked as Xavier. It preserves the prior Xavier / BrewMind / SMM materials while normalizing the active workspace name to Cici.

**Singularity-academy consolidation:** This lane remains canonically `work-cici` as an internal path, but it is now also a live `singularity-academy` overlay when the operator is using Cici AI, cohort onboarding, or advisor tooling to test whether recursive AI systems can help people learn, coordinate, and accomplish real work faster. Canonical singularity hub: [Singularity Workshop](../../../singularity/workshop/README.md).

Under that overlay, keep the work in WORK artifacts. `singularity-academy` is not a `candidates` workflow and should not inherit governed-state overhead during ordinary Cici-singularity passes.

This folder is the **operator/advisor layer:** contracts, mirrors, runbooks, content plans, operator navigation, work profile, capability rubric, handoffs, evidence pointers, and BrewMind pilot materials.

It is not Ciciâ€™s sovereign Record repository and not a canonical Record surface.

### Singularity-use contract

When this lane is being used under `singularity-academy`, the live question is not only "how do we support Cici?" but also "does recursive AI actually help beginners or distributed teams compound capability in the wild?"

Keep the advisor boundary intact and ask:

- what part of the learning or coordination loop is being recursively improved?
- what human gate still matters for trust, judgment, and durable progress?
- which results generalize beyond one person or one prompt?
- where does the control plane live: repo doctrine, runbook, Telegram group, cohort artifact, model behavior, or operator review?

### Why `cici-ai` matters to the singularity thesis

`work-cici` is valuable to `singularity-academy` because it tests a different claim than pure operator productivity.

- `work-business` asks whether AI can compress expert or founder work.
- `work-cici` asks whether AI can raise the floor for newer people, cohorts, or distributed teams.
- If both work, the thesis starts to look broader than "the operator got faster."

Treat Cici AI as evidence for the thesis only when the gains are durable and reusable:

- onboarding gets easier without collapsing quality
- people complete real tasks they would otherwise stall on
- support patterns become reusable runbooks instead of heroic one-off coaching
- progress survives beyond a single session, prompt, or human rescuer

Failure modes to watch:

- the operator is secretly doing the hard part while AI gets credit
- the system creates enthusiasm without durable competence
- outputs depend on one unusually motivated person and do not generalize
- coordination overhead grows faster than capability

## Rename note

This lane was previously named `work-xavier`. It has been renamed to `work-cici`. Older files may retain **Xavier** in filenames or historical notes when they refer to prior artifacts, continuity records, or legacy naming. **Active** references should prefer **Cici AI** in user-facing copy and **Cici** in general prose unless the historical filename, artifact title, or **archived note** requires **Xavier**.

**Legacy note: formerly Xavier. Active display name: Cici AI.**

## Naming and continuity

- **Cici AI** is the active singularity-facing and human-facing lane name.
- **Xavier** may appear in legacy filenames, historical notes, and older artifacts.
- **`work-cici`** is the canonical internal workspace path and Grace-Mar advisor/project territory for the Cici AI program.
- Ciciâ€™s **actual governed instance**, if any, lives in **her own repository** (companion / template fork â€” see the section *Her instance repository* below).
- **This folder must not host Ciciâ€™s Record.** Her cognitive-fork Record lives only under `` in **her** instance repo, behind **her** gate and merge script.
- Legacy script names such as `build_xavier_handbook_bundle.py` may remain until a separate compatibility-safe rename PR.

## Legacy-reference policy check

Legacy mentions are allowed only in:
- rename continuity sections
- explicit legacy alias tables
- revision/history logs
- immutable evidence records and source titles

Active onboarding, coordination, and daily operating text should remain Cici-first.

## Legacy filename aliases

| Legacy / historical artifact | Current interpretation |
|------------------------------|------------------------|
| [cici-work-profile.md](cici-work-profile.md) | Cici work profile (was `xavier-work-profile.md`) |
| [cici-progress-log.md](cici-progress-log.md) | Operator progress + evidence index (coaching notes) |
| [TERMS-XAVIER.md](TERMS-XAVIER.md) | Cici terms / legacy Xavier filename |
| [xavier-instance-two-step.md](xavier-instance-two-step.md) | Cici instance two-step / legacy Xavier filename |
| [xavier-smm-capability-rubric.md](xavier-smm-capability-rubric.md) | Cici SMM capability rubric / legacy Xavier filename |
| `COMPANION-XAVIER-*` ([e.g. DELETION-READINESS](COMPANION-XAVIER-DELETION-READINESS.md)) | Cici companion-instance planning / legacy Xavier filename pattern |

### Machine-readable manifest

- **[legacy-aliases.yml](legacy-aliases.yml)** â€” Advisory YAML for audits and future rename-safe tooling: enumerates the **repo-root paths** in this table that stay **Xavier-**named for compatibility (three docs, two SMM scripts), plus `allowed_legacy_contexts` and `prohibited_contexts`. The human **table** above is the full picture (renames like `cici-work-profile` / `cici-progress-log`, and filename **patterns** such as `COMPANION-XAVIER-*`, are not duplicated in the YAML; pattern-level rows may get a later schema if tooling needs them).

**Read first:** [INDEX.md](INDEX.md) Â· [ALIGNMENT.md](ALIGNMENT.md) Â· [LANES.md](LANES.md) Â· [TERMS-XAVIER.md](TERMS-XAVIER.md) Â· [legacy-aliases.yml](legacy-aliases.yml).

Template baseline (canonical): [work-companion-self/TEMPLATE-BASELINE.md](../../docs/skill-work/work-companion-self/TEMPLATE-BASELINE.md).  
Boundaries: [audit-boundary-grace-mar-companion-self.md](../../docs/audit-boundary-grace-mar-companion-self.md) (grace-mar Â· template); her instance follows the same rules **in her repo**.

**Never copy** `**` into another companionâ€™s instance tree. See [LEAKAGE-CHECKLIST.md](LEAKAGE-CHECKLIST.md).

## Her instance repository (Ciciâ€™s companion / template fork)

Ciciâ€™s **companion** or **chosen instance** repository (Identity Fork Protocol paths under ``, gate, seed survey, Voice), when created from [companion-self](https://github.com/rbtkhn/companion-self), lives in **her own GitHub repository**. The default or historical repo name is often still **`companion-xavier`** on GitHub; she may choose another name. That code and **her** Record **do not** need to be copied into grace-mar. This folder documents how grace-mar interfaces with that work **without** hosting her fork.

**Session 0 / seed survey:** Lives **in her repository** (paths such as `docs/seed-survey/` or `xavier/` per her layout from the template) â€” not under `singularity/work-cici/` here. Operator docs: [GOOD-MORNING.md](GOOD-MORNING.md), [SESSION-0-OPERATOR.md](SESSION-0-OPERATOR.md). **Instance checklist (template â†’ clone â†’ Claude Code â†’ Seed Phase):** [xavier-instance-two-step.md](xavier-instance-two-step.md) â€” send before first Good Morning if she does not have her repo yet; day-one steps are items 1â€“6.

**Daily sync surface (advisor view):** [SYNC-DAILY.md](SYNC-DAILY.md). **Mirrors:** [work-dev-mirror/README.md](work-dev-mirror/README.md), [work-politics-mirror/README.md](work-politics-mirror/README.md).

**Operator observations (progress / evidence):** [cici-progress-log.md](cici-progress-log.md) â€” qualitative notes, hypotheses, coaching hooks; artifacts in [evidence/](evidence/). **Milestones + dated pointers:** [work-cici-history.md](work-cici-history.md).  
**Beginner daily journal:** [daily-journal/README.md](daily-journal/README.md) â€” the uniform semi-automated daily journal pattern for OB1 members.

**BrewMind (Philippines pilot):** [brewmind-philippines-onboarding-guide.md](brewmind-philippines-onboarding-guide.md) â€” bundle hub for strategy, brand, field script, and PH market notes ([INDEX.md](INDEX.md) lists all BrewMind WORK files).

**Community measurement:** [cici-ai-community-dashboard.md](cici-ai-community-dashboard.md), [cici-ai-first-task-proof-packet.md](cici-ai-first-task-proof-packet.md), and [cici-ai-weekly-governance-review-template.md](cici-ai-weekly-governance-review-template.md). **Weekly review instances** live in [reviews/](reviews/).
**Daily team/group brief:** [cici-ai-daily-telegram-brief.md](cici-ai-daily-telegram-brief.md) defines the Telegram-ready daily operating brief, source hierarchy, confidence rules, and automation path for `cici-ai`.
**Daily brief quickstart:** [cici-ai-daily-brief-quickstart.md](cici-ai-daily-brief-quickstart.md) is the beginner-facing wrapper for proof reply, re-entry, and boundary clarity.
**Daily brief control-plane pilot:** [cici-ai-daily-brief-control-plane-pilot.md](cici-ai-daily-brief-control-plane-pilot.md) defines the first live test for whether a partially automated brief can improve routing and proof without blurring authority.

**Apprentice Studio pilot:** [apprentice-studio-pilot-ops.md](apprentice-studio-pilot-ops.md) is the month-one operating layer for using Grace Gems as a real-work substrate, `cici-ai` as the onboarding/progress surface, and `singularity-academy` as the evaluation lens.

**Active `cici-ai` work lanes:** [cici-ai-lanes.md](cici-ai-lanes.md) splits the current operator surface into [cici-ai-telegram](cici-ai-telegram/README.md), [cici-ai-core](cici-ai-core/README.md), and [cici-ai-progress](cici-ai-progress/README.md). These lanes route action for the `cici-ai` team; they do not replace evidence, governed-state, or Cici's own repo.

**Portability:** Patterns in this module are intended to be **mirrored or adapted** for other companion-self operator/agent workspaces; the instance Record stays in each companionâ€™s repo. Reusable pattern: see [docs/skill-work/work-template/external-companion-workspace-template.md](../../docs/skill-work/work-template/external-companion-workspace-template.md) (generic advisor-lane template; this folder remains not Ciciâ€™s Record).

**Template alignment:** [work-cici-sources.md](work-cici-sources.md) (feeds / pointers), [LANE-CI.md](LANE-CI.md) (PR labels), [WORK-LEDGER.md](WORK-LEDGER.md) (watches + compounding). Concept map: [work-template/MAPPING.md](../../docs/skill-work/work-template/MAPPING.md) (section *work-cici (advisor module)*).

## Path-status close note

After the `work-cici` shelf move, treat path residue in three classes:

- **Live authority:** `singularity/work-cici/` is the only live shelf for this lane inside strategy-codex, and Cici AI should be treated as singularity-native by default when discussing the program.
- **Compatibility only:** `docs/skill-work/work-cici/` remains a pointer surface during cutover, not a second authority.
- **Historical only:** legacy `work-xavier`, `companion-xavier`, and older path strings may remain when they identify real historical artifacts, filename compatibility, or past repo structure.

Regression rule: if a runbook, source list, script constant, workshop link, or operator prompt treats `docs/skill-work/work-cici/` as the live execution shelf again, that is stale continuity and should be corrected rather than preserved.

## Scripts (repo)

**Naming** â€” for when legacy SMM entrypoints may be renamed, see **Naming and continuity** (legacy script bullet) above.

**SMM handbooks (work-politics outputs):**

- [scripts/build_xavier_handbook_bundle.py](../../../scripts/build_xavier_handbook_bundle.py) â€” assembles `smm-xavier-handbook-bundle.md` for print/PDF inputs.
- [scripts/generate_smm_xavier_pdf.sh](../../../scripts/generate_smm_xavier_pdf.sh) â€” regenerates print HTML + PDF via headless Chrome (run on a normal macOS host if CI/sandbox blocks).

**Legacy script names:** these filenames and the `smm-xavier-*` bundle paths are **historical SMM lane naming** and remain stable so downstream invocations and docs do not break. They are still the supported entrypoints for regenerating the **work-politics** SMM bundle from current sources; they are not a separate architecture lane.

## Record, Voice, and WORK execution (this folder)

- **Record** â€” Lived identity under `` in **her** instance repo; durable truth enters only through **her** recursion-gate and merge script.
- **Voice** â€” Speaks the Record when queried; bounded by what is merged and by prompt rules.
- **WORK execution** â€” Operator, AI assistant, and scripts running **WORK modules** (this folder, mirrors, Cursor workflows): drafts, plans, and **optional ongoing sync** of pattern docs with a source tree. This layer does **not** own the Record; anything that changes identity or Voice obligations must surface as **candidates** in **her** `recursion-gate.md` (or explicit companion-approved policy), not as silent edits to `self.md` in her repo or grace-marâ€™s companion tree.

## Words we use (avoid confusion)

- **Interpretive machine / Record** â€” The governed self (Identity Fork Protocol). Not â€œa copy of someone elseâ€™s markdown tree.â€
- **Git repository / instance repo** â€” Where that Record lives: **Ciciâ€™s companion or chosen instance repo** (on GitHub it is **often** still the literal name `companion-xavier`). â€œForkâ€ on GitHub is **hosting**; it is not the same word as **interpretive machine**.
- **Mirror / track / sync** â€” Use for `work-*` **advisor** layouts you keep **aligned over time** with a golden source. Prefer this over **â€œfork onceâ€** when you mean **ongoing** alignment.

**External Open Brain / instance repo:** the [**Cici**](https://github.com/Xavier-x01/Cici) repo (OB1 **instance** layer on GitHub â€” config, docs, governed state) is Ciciâ€™s public instance (**@Xavier-x01** on GitHub); digest and cross-links: [cici-notebook](cici-notebook/README.md), [work-cici-history](work-cici-history.md) `### 2026-04-10`. That is distinct from the **companion-self** `companion-*` Record repo and from **this** advisor folder.

---

## Governance contract (compact)

1. **Primary output (grace-mar):** `work-cici` = advisor project + operator artifacts; **not** Ciciâ€™s gated Record files in **her** repo.
2. **Primary output (her repo):** Ciciâ€™s companion or chosen instance repository (when the literal name is `companion-xavier`, that is a legacy defaultâ€”she may use another name) = her instance; durable identity truth enters only through **her** gate and merge script.
3. **Mirror scope:** Mirror workflow docs and ops artifacts **here** for your advisory cadence; do **not** mirror identity Record prose across repos without her pipeline.
4. **Directionality:** Approved patterns flow from grace-mar skill-work into mirrors; conflicts require human resolution.
5. **Ownership (RACI):** operator / AI assistant drafts; Cici (legal name **Xavier**) / operator review; companion approves gated merges **in her repo** for identity; you approve public ship for your content.
6. **Promotion path (her repo):** candidate â†’ `recursion-gate.md` â†’ approval â†’ `process_approved_candidates.py --apply`.
7. **Security boundary:** no secrets in shared mirror docs.

---

## Risk mitigation (template â€” Tier 1+)

Per [work-template/README.md](../../docs/skill-work/work-template/README.md) Â§ *Risk-mitigation checklist*. Filled for **advisor module** obligations (mirrors, sync cadence, leakage boundary).

### 1. Quantitative success criteria

| Metric | Target | How to measure |
|--------|--------|----------------|
| Daily sync surface used | â‰¥1 operator touch / week when the Cici advisory loop is active | [SYNC-DAILY.md](SYNC-DAILY.md) checkboxes or [cici-progress-log.md](cici-progress-log.md) dated lines |
| Mirror drift | No silent staleness >30d on labeled â€œliveâ€ mirror paths | Spot-check [work-dev-mirror](work-dev-mirror/README.md) / [work-politics-mirror](work-politics-mirror/README.md) headers + `git log` on mirrored sources when in doubt |
| Leakage discipline | Zero grace-mar Record paths in outbound advisor bundles | Run [LEAKAGE-CHECKLIST.md](LEAKAGE-CHECKLIST.md) before ship; CI label per [LANE-CI.md](LANE-CI.md) when applicable |

### 2. Sustainment table

| Task | Cadence | What to check |
|------|---------|----------------|
| SYNC-DAILY / Good Morning loop | Weekly when engaged | [SYNC-DAILY.md](SYNC-DAILY.md) still matches actual chat/repo rhythm |
| Handbook / bundle outputs | On change to SMM or operator handbook sources | [build_xavier_handbook_bundle.py](../../../scripts/build_xavier_handbook_bundle.py) + [generate_smm_xavier_pdf.sh](../../../scripts/generate_smm_xavier_pdf.sh) still run clean |
| Mirror alignment | Monthly light pass | Mirror README â€œlast reviewedâ€ vs upstream doc movement |

### 3. Deprecation / retirement path

1. Stop active advisory cadence (explicit operator decision).
2. Close open items in [WORK-LEDGER.md](WORK-LEDGER.md) with status notes.
3. Archive lane-specific experiments under a dated `archive/` note in this folder (README pointer), not by deleting her instance repo.
4. Remove or downgrade automation only after no operator relies on the path; **never** delete her `` tree from **her** repo from grace-mar tooling.

### 4. Scope creep guardrail

> Any workflow that copies **gated Record** prose (`self.md`, `self-archive.md`, `recursion-gate.md` merges) from **grace-mar** into **Cici** / her companion instance (`companion-xavier` or her chosen repo name) **without** her gate requires a **new plan** and explicit consent â€” not an incremental doc edit. This laneâ€™s charter is **advisor + WORK execution**, not hosting her fork.

**Member profiles:** [member-profiles/README.md](member-profiles/README.md) for the standardized profile form and Xavier's filled profile.
