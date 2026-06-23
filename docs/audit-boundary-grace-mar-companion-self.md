# Audit: Boundaries â€” grace-mar Â· companion-self

**Purpose:** State **proper** boundaries between the **grace-mar** repository (reference instance) and the **companion-self** template â€” what **must** stay separate, what **may** cross under contract, and **how** enforcement works. Complements [audit-structural-alignment-grace-mar-companion-self.md](audit-structural-alignment-grace-mar-companion-self.md) (paths and formatting). **Governed by:** [AGENTS.md](../AGENTS.md), [identity-fork-protocol.md](identity-fork-protocol.md), [fork-isolation-and-multi-tenant.md](fork-isolation-and-multi-tenant.md), [archive/boundary-museum-knowledge-self-library.md](archive/boundary-museum-knowledge-self-library.md).

**As of:** 2026-03-27 (updated: no second instance tree in this repo).

---

## 1. The two surfaces (what they *are*)

| Surface | What it is | Holds a live companion Record? |
|---------|------------|--------------------------------|
| **grace-mar** | This **repository** â€” reference **instance** ``, full stack, operator tooling | **Yes** â€” the companionâ€™s fork hosted here |
| **companion-self** | **Upstream template** repo â€” `platform/template/`, protocol docs, reusable scaffolds | **No** â€” no `<real-id>/` Record; template only |

**Other instances** (e.g. a companion who clones the template into **their own** repo) are **outside** this repo. Their boundaries are the same **Identity Fork Protocol** and fork isolation rules in their workspace.

**Boundary mistake to avoid:** Treating **companion-self** as â€œanother forkâ€ like grace-mar. It is **blueprint**, not identity.

---

## 2. Boundary matrix (normative)

| Boundary | grace-mar | companion-self |
|----------|-----------|----------------|
| **Fork namespace** | `` only | `platform/template/` only (scaffold, not a person) |
| **Template â†’ instance** | Merges via [MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md); **never** overwrite live Record wholesale | Source of **structure** and **protocol** |
| **Instance â†’ template** | Structural / instance-agnostic improvements may **propose** upstream PRs | Accepts PRs; remains **generic** |
| **museum knowledge vs removed operator-books symlink** | IX vs `self-library.md` rows â€” [boundary doc](archive/boundary-museum-knowledge-self-library.md) | Template teaches the same rule |
| **WORK vs Record** | `docs/skill-work/work-*`, `self-work.md` coordination â€” not IX | N/A (docs) |
| **Gated merge** | `process_approved_candidates.py` â€” companion approves | N/A |
| **Workspace (multi-root)** | Instance edits live **here**; template read-only when diffing ([MERGING-FROM Â§0](merging-from-companion-self.md)) | Template edits in **companion-self** repo |

---

## 3. What **may** cross (allowed flows)

| Flow | Rule |
|------|------|
| **Protocol & docs** | IFP, glossary, architecture concepts â€” sync **companion-self â†’ grace-mar** per merge doc. |
| **removed operator-books symlink governance** | Same **instance-agnostic** `self-library.md` **shape** (governance + empty `entries:`) on template; grace-mar retains **live** LIB rows with boundary discipline. |
| **Scripts / exports** | `GRACE_MAR_USER_ID` resolves ``: in this repo the primary instance is **grace-mar**. |

---

## 4. What **must not** cross (hard lines)

| Prohibited | Why |
|------------|-----|
| **Undocumented facts** into `` without pipeline | Sovereign merge rule; [AGENTS.md](../AGENTS.md). |
| **Template treated as Record** | No approvals or IX in companion-self `platform/template/` as if it were a companion. |
| **LLM / training knowledge** into profile without pipeline | Knowledge boundary. |

---

## 5. Audit checklist (operator)

- [ ] **Namespace:** `` is the only live Record root in this repo for the pilot instance.
- [ ] **Template pin:** [TEMPLATE-BASELINE](skill-work/work-companion-self/TEMPLATE-BASELINE.md) reflects **companion-self `main`** commit used for governance alignment when recorded.
- [ ] **Gate:** No hand-merge into `self.md` without staging and approval.

---

## 6. Verdict

**Proper boundaries** are defined in repo policy: **fork isolation**, **template upstream** (companion-self without live Record), and **IFP** (stage â†’ approve â†’ merge). **Drift risk** is operational: copying prose or conflating **WORK** client copy with **Record** â€” countered by **gated pipeline** and boundary docs.

**Related:** [audit-structural-alignment-grace-mar-companion-self.md](audit-structural-alignment-grace-mar-companion-self.md) Â· [audit-companion-self.md](audit-companion-self.md) Â· [conceptual-framework.md](conceptual-framework.md).

