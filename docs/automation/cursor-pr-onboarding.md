# Cursor PR Onboarding Comment

**Status:** **WORK** documentation. This page does **not** enable a [Cursor Automation](https://cursor.com/docs/cloud-agent/automations) in the repo. It describes a **read-only** PR **briefing** for the **operator**. **Doctrine:** [AGENTS.md](../../AGENTS.md) (routing, no merge) Â· [cursor-safe-automation-contract.md](cursor-safe-automation-contract.md).

---

## Purpose

A **PR onboarding** automation posts a **short** â€œoperator briefingâ€ when a **pull request** is **opened** or **updated** (e.g. synchronized / reopened). It **summarizes** **PR shape**, **likely** [lane](https://github.com/rbtkhn/strategy-codex/blob/main/lanes.yaml), **sensitive** paths, and **which** **checks** to watch â€” it does **not** **review** code, **apply** **labels**, **fix** the branch, or **replace** a human **review**.

**Core line:** **Lane workflows decide enforcement; Cursor Automation explains the PR shape before the operator spends attention.**

**Paste prompt (procedure + identity):** [prompts/cursor-pr-onboarding.md](prompts/cursor-pr-onboarding.md) â€” the **single** place for the model instruction; this guide holds **operator** setup, **inference** tables, and the **canonical** [output comment format](#output-comment-format).

## Relationship to existing GitHub Actions (complement, not replace)

| Workflow | Role |
|----------|------|
| [lane-pr-hint.yml](https://github.com/rbtkhn/strategy-codex/blob/main/.github/workflows/lane-pr-hint.yml) | May **comment** a **suggested** `lane/*` **label** from paths â€” **deterministic** script. |
| [lane-scope.yml](https://github.com/rbtkhn/strategy-codex/blob/main/.github/workflows/lane-scope.yml) | **Enforces** that changed files **fit** the **declared** PR lane. |
| [governance.yml](https://github.com/rbtkhn/strategy-codex/blob/main/.github/workflows/governance.yml) | **Governance** and **integrity** jobs on `push`/`PR`. |
| [test.yml](https://github.com/rbtkhn/strategy-codex/blob/main/.github/workflows/test.yml) | **Tests** and many **validations** in one job. |

This automation **narrates** and **orients** the operator. It is **not** a second **lane** engine and does **not** set labels or merge.

---

## Recommended trigger (Cursor product)

| Setting | Suggestion |
|---------|------------|
| **Event** | GitHub Â· **PR opened** Â· **synchronized** Â· optional **reopened** |
| **Destination** | **Comment** on the **PR** (not a new issue, unless you add that later) |
| **Duplication** | **Update** a **prior** automation **comment** on the same PR if Cursor **supports** it; otherwise **one** new comment per run (avoid comment spam) |

**Ideal output:** a short **operator briefing**, not a code review. **Not** a **review** of individual lines unless you scope that in a **future** policy.

---

## Allowed behavior

- Read **PR** title, body, **labels**, **base/head** branch names, **changed-files** list, and any **summary** the automation API provides.
- **Infer** a **likely** lane or category from **labels**, **branch**, and **paths** â€” mark **uncertain** when mixed.
- **Flag** if **Record**- / **gate**- / **prompt**-sensitive files appear in the **diff**.
- **Name** which **workflows** or **check** names are **likely** to run (from path â†’ workflow heuristics; do **not** re-run CI).
- Note whether **gated Record** [commit message](https://github.com/rbtkhn/strategy-codex/blob/main/.github/workflows/governance.yml) **discipline** may **apply** (for **human** commits â€” not this archive/grace-mar-instance/bot).
- **Suggest** a **single** **operator** next step (e.g. *wait for CI*, *confirm `lane/*` label*, *re-read `recursion-gate` if touched*).
- **State** when classification is **uncertain**.

## Prohibited behavior

- No `git` **commits** or **pushes**; no **edits** to the repo, **PR** branch, or **protected** paths.
- No **adding**, **removing**, or **changing** **issue** or **PR** **labels** in this v1 (unless a **later** explicit policy allows a narrow exception).
- No **approvals**, **request changes**, or other **review** **state** changes.
- No edits to `self.md`, `self-archive.md`, `recursion-gate.md`, `session-log.md`, or `archive/grace-mar-instance/bot/prompt.py` â€” the automation does **not** write those files.
- No `process_approved_candidates.py` â€” any mode.
- No **staging**, **approving**, **rejecting**, or **editing** **`CANDIDATE-*`**.
- No **memory** (product feature) for **PR** text, **logs**, **diffs**, or **untrusted** **issue** content (see [contract](cursor-safe-automation-contract.md) Â§ 10).
- No **ritual** language: do **not** call the output `coffee`, `dream`, `bridge`, **Steward**, or **gate** **review** **completion**.

---

## Lane inference guide (heuristics, not labels)

| Signal | Likely lane / category | Note |
| --- | --- | --- |
| `docs/skill-work/work-dev/**` | work-dev | Technical execution / architecture / work-dev **control** plane. |
| `docs/skill-work/work-strategy/**` | work-strategy | Strategy notebook, geopolitical **WORK** |
| `docs/skill-work/work-cici/**` | work-cici | Cici-related **WORK** |
| `codex/predictive-history/**` or `codex/predictive-history/**` | work-jiang | Jiang / Predictive History lane; [work-jiang](https://github.com/rbtkhn/strategy-codex/blob/main/.github/workflows/work-jiang.yml) may path-filter |
| `**` | **Record-sensitive** | Treat as **protected**; **companion** / gate **governance** applies to merges |
| `archive/grace-mar-instance/bot/prompt.py` | **prompt-sensitive** | High caution; often **gated** commit expectations |
| `scripts/**` | tooling / runtime | [test.yml](https://github.com/rbtkhn/strategy-codex/blob/main/.github/workflows/test.yml) and **governance** / **harness** may apply |
| `.github/workflows/**` | **CI** / **governance** **infrastructure** | **Meta**; watch **governance** + **lane** + **all** default checks |
| `runtime/artifacts/**` | **derived** **artifact** | Confirm whether **intentional** check-in or **generated**; **library-index** and others may care |

**Explicit** `lane/*` **label** on the PR, when present, **outranks** path inference â€” still **narrate**; do **not** **re-label**.

---

## Sensitive path guide (highlight only; do not edit)

**Flag** (but **do not** **modify** or **suggest** **auto-fixes** in-repo) if the **change** **set** **touches**:

- `self.md` â€” **Record** (SELF) surface
- `self-archive.md` â€” **EVIDENCE** surface
- `recursion-gate.md` â€” **gate** queue
- `session-log.md` â€” **session** log
- `archive/grace-mar-instance/bot/prompt.py` â€” **Voice** / prompt

**More broadly:** any path under `` is an **instance** **Record** or **operational** **surface** â€” treat as **companion-** and **merge-** **sensitive**. For **gated** **merge** and **[gated-merge]** **commit** rules, see [instance-doctrine.md](../../instance-doctrine.md) and the **Gated Record** **job** in [governance.yml](https://github.com/rbtkhn/strategy-codex/blob/main/.github/workflows/governance.yml) on **PRs**.

---

<a id="output-comment-format"></a>

## Output comment format (canonical template)

The automationâ€™s **PR comment** should follow this **shape**. The paste prompt in [prompts/cursor-pr-onboarding.md](prompts/cursor-pr-onboarding.md) requires **this** section **exactly** (headings/labels only; no alternate titles).

```markdown
### PR onboarding

**PR shape:**
**Likely lane:**
**Sensitive paths:**
**Checks to watch:**
**Possible gated-record concern:**
**Operator next step:**

**Boundary note:** This is an onboarding comment only. It did not approve, merge, edit files, change labels, process the gate, or run mutating commands.
```

*Fill the fields from evidence; use `uncertain` in prose where needed.*

## Operator setup

1. Read [cursor-safe-automation-contract.md](cursor-safe-automation-contract.md) (paste at top of the Cursor prompt or link + **short** summary).
2. Copy the full text of [prompts/cursor-pr-onboarding.md](prompts/cursor-pr-onboarding.md) into the [Cursor Automations](https://cursor.com/docs/cloud-agent/automations) **PR**-triggered automation.
3. Configure: **PR opened** / **synchronized** ( / **reopened** optional); **comment** on **PR**; **not** â€œopen a PRâ€ or **not** run **mutating** tools in the automation.
4. Keep **label** and **merge** **authority** with the **operator** and **GitHub**; this automation is **narration** only.

**See also:** [README â€” PR onboarding comment](README.md#pr-onboarding-comment) Â· [cursor-automations.md](cursor-automations.md)

**Maintenance:** Reconcile the **lane** table and workflow names with [lanes.yaml](https://github.com/rbtkhn/strategy-codex/blob/main/lanes.yaml) and [`.github/workflows/`](https://github.com/rbtkhn/strategy-codex/tree/main/.github/workflows) when they change. *Last reviewed: 2026-04.*
