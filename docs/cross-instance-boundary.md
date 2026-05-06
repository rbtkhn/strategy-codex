# Cross-instance boundary (grace-mar and external companions)

**Purpose:** One-page contract for **collaboration without merging Records** â€” especially when one operator works in grace-mar and a peer companion has a **separate instance repository** created from [companion-self](https://github.com/rbtkhn/companion-self).

**Authority:** Complements [fork-isolation-and-multi-tenant.md](fork-isolation-and-multi-tenant.md), [identity-fork-protocol.md](identity-fork-protocol.md), and [MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md).

---

## 1. Two repositories, two roles

| Repository | Holds |
|------------|--------|
| **grace-mar** (mentor / operator) | `` Record, work territories (e.g. collaborative **work-cici** module), template sync tooling. |
| **Peer instance** (e.g. employeeâ€™s repo) | **Her** `<fork_id>/` tree, **her** gate, **her** merge script â€” not a subtree inside grace-mar. |

â€œSimilar companion-self type agentsâ€ here means: **same protocol**, **different forks**, **different repos** unless you explicitly choose otherwise.

---

## 2. What must not cross without the peerâ€™s gate

- **Mentor Record facts** (SELF, EVIDENCE, prompt) must not appear in the peerâ€™s **canonical** profile files as if they were hers without **her** recursion-gate and `process_approved_candidates.py --apply` (or equivalent).
- **Undocumented LLM knowledge** â€” same [knowledge boundary](knowledge-boundary-framework.md) as grace-mar; nothing becomes her Record without write + approval.

**Collaborative work modules** (advisor runbooks, mirrors, client WORK docs) live in **mentor** or **shared docs** by agreement; they are **not** her `self.md`.

---

## 3. What may cross

- **Template upgrades** from companion-self into **each** repo on its own schedule.
- **Workflow patterns** (checklists, mirror contracts) as **WORK** artifacts.
- **Pointers** (â€œsee mentor repo PR #â€¦â€) without pasting mentor identity blocks.

---

## 4. Mechanical backstop (optional)

Run this **only in the peerâ€™s instance repository**, not in grace-mar. Under `` in grace-mar, the mentor fork id appears legitimately everywhere; the same scan would raise noise.

To catch accidental paste of the **mentor fork path** into **her** tree, run from **her** repo root:

```bash
python3 scripts/check_forbidden_path_strings.py --preset isolate-external-instance --under users
```

Script: [scripts/check_forbidden_path_strings.py](../scripts/check_forbidden_path_strings.py). The preset forbids the literal substring `` anywhere in scanned files â€” appropriate when **no** file under **her** `` should reference the mentorâ€™s profile directory.

Scans **``** by default when `--under` is omitted and `` exists. Add `--under docs` only with `--exclude` patterns for docs that must quote paths literally.

grace-mar can keep the script so operators copy it into her repo or pull from template; **do not** wire CI on grace-mar `main` with this preset across the whole `` tree without a different scope.

---

## 5. Two-person scale

With **one other person**, prefer **explicit habits** over heavy automation: who runs merges on her fork, where Session 0 capture lives, and one recurring leakage check (Â§4) if she uses CI or pre-commit.

---

**Related:** [audit-boundary-grace-mar-companion-self.md](audit-boundary-grace-mar-companion-self.md), [skill-work/work-cici/README.md](skill-work/work-cici/README.md), [inter-fork-collaboration.md](inter-fork-collaboration.md).

