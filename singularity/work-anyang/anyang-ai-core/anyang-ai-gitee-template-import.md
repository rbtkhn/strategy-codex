# anyang-ai — Gitee template import (from Cici upstream)

**Audience:** Anyang mentor (one-time setup) + operator advisor. **Students** use [§4 Student fork flow](#4-student-fork-flow-tier-a) only — they do **not** import from GitHub themselves.

**Upstream:** [github.com/Xavier-x01/Cici](https://github.com/Xavier-x01/Cici) (OB1 instance reference; international golden path).  
**China stack context:** [anyang-ai-cn-software-stack.md](../anyang-ai-cn-software-stack.md)

**Template slot (fill when live):**

```text
Gitee mentor template URL: https://gitee.com/<MENTOR_GITEE_USER>/anyang-ai-template
Imported-from SHA (GitHub): <record after import>
Import date: YYYY-MM-DD
```

---

## 1. Why mentor imports once

Students in China should **not** depend on GitHub to obtain the template. The mentor:

1. Imports **Cici** into **one** Gitee repo under mentor control.
2. Applies **Anyang Tier A overlays** (China quickstart, Supabase deferred).
3. Publishes a stable URL for students to **fork on Gitee**.

This mirrors cici-ai’s “fork Xavier-x01/Cici” step with a **domestic-stable** remote.

---

## 2. One-time import — Gitee web UI (recommended)

**Prerequisites:** Mentor Gitee account; browser access to Gitee; one-time ability to reach GitHub for import (mentor machine only — not student prerequisite).

### Step A — Create import repo

1. Log in to [gitee.com](https://gitee.com).
2. **+** → **新建仓库** / **从 GitHub 导入** (wording may vary: **导入已有仓库**).
3. **源仓库地址:** `https://github.com/Xavier-x01/Cici`
4. **目标仓库名称:** `anyang-ai-template` (or `安阳-ai-模板` — pick one slug; keep stable).
5. **可见性:** 公开 (students fork without extra permission) unless cohort is private by design.
6. Start import; wait until Gitee shows import complete.

### Step B — Record provenance

In mentor notes or `singularity/work-anyang/evidence/`:

- Import date
- Gitee repo URL
- GitHub `main` SHA at import time (from Gitee commit list or `git log -1`)

### Step C — Verify on mentor machine

```bash
git clone https://gitee.com/<MENTOR_GITEE_USER>/anyang-ai-template.git
cd anyang-ai-template
git log -1 --oneline
# Open README.md — confirm Cici layout present
```

**Preflight pass:** push a test commit from mentor machine; confirm it appears on Gitee web UI.

---

## 3. One-time import — git mirror (fallback)

Use if the Gitee GitHub importer fails or is slow.

**On mentor machine with GitHub access:**

```bash
git clone --mirror https://github.com/Xavier-x01/Cici.git cici-mirror.git
cd cici-mirror.git
git remote set-url --push origin https://gitee.com/<MENTOR_GITEE_USER>/anyang-ai-template.git
git push --mirror
```

Then on Gitee: confirm branches/tags; set **默认分支** to `main`.

**Warning:** `--mirror` overwrites remote; use only on **empty** new Gitee repo.

---

## 4. Anyang Tier A overlays (mentor commits after import)

Add China-specific front door **without** deleting upstream Cici docs (keeps future Tier B parity).

### Required files (suggested)

| File | Purpose |
|---|---|
| `docs/anyang-ai/README.zh-CN.md` | Mandarin student quickstart (Tier A) |
| `docs/anyang-ai/TIER-A-NOTICE.md` | English + 中文: Supabase/Claude **not** week-one requirements |
| `ANYANG-AI.md` (repo root) | Pointer: “安阳 cohort — start here” → `docs/anyang-ai/README.zh-CN.md` |

### Suggested `TIER-A-NOTICE.md` content (stub)

- Phase 1 = Gitee + local git + domestic AI + markdown memory files.
- Ignore Supabase deploy sections until mentor announces phase 2.
- Post Gitee repo URL + done/stuck in WeChat `anyang-ai`.

### Optional trim (phase 1 only)

- Do **not** delete `supabase/` or edge-function folders — Tier B may need them.
- Add a short banner at top of root `README.md` linking to `ANYANG-AI.md`.

### Mentor commit example

```bash
git checkout -b anyang-tier-a-overlay
# add docs/anyang-ai/* and ANYANG-AI.md
git commit -m "docs(anyang-ai): Tier A China quickstart overlay"
git push origin anyang-tier-a-overlay
# merge to main on Gitee (web PR or local merge)
```

---

## 5. Student fork flow (Builder lane only)

**Foundation (预备轨) members do not fork until [graduation](../anyang-ai-foundation/README.md#graduation-to-builder-预备--实操).** This section is for **Builder (实操轨)** only.

**Students never import from GitHub.** In weekly session or WeChat pin:

1. Register / log in to **Gitee**.
2. Open mentor template: `https://gitee.com/<MENTOR_GITEE_USER>/anyang-ai-template`
3. Click **Fork** / **复刻** → create **your** repo under your account.
4. Copy **your** fork URL; post in WeChat `anyang-ai` (proof).
5. Clone locally:

```bash
git clone https://gitee.com/<YOUR_GITEE_USER>/<YOUR_FORK_NAME>.git
cd <YOUR_FORK_NAME>
```

6. Read `ANYANG-AI.md` → `docs/anyang-ai/README.zh-CN.md`.
7. Complete first win (e.g. add `docs/my-goal.md`, commit, push).
8. Post **完成** or **卡在：…** in WeChat within 48h.

**Initiation bar:** [anyang-ai-cn-software-stack.md § Phase-1 checklist](../anyang-ai-cn-software-stack.md#phase-1-initiation-checklist-replaces-cici-ob1-day-one-bar)

---

## 6. Updating the template later

| Situation | Action |
|---|---|
| Cici upstream moved; mentor wants new baseline | Re-import or `git fetch` from GitHub on mentor machine; merge; re-apply Anyang overlay |
| Student already forked | Students **pull** from their fork’s `origin` — mentor announces breaking changes in WeChat |
| Tier B student wants GitHub parity | Separate track: fork [Xavier-x01/Cici](https://github.com/Xavier-x01/Cici) on GitHub; tag `track=tier_b` in progress sheet |

**Discipline:** Record template version in WeChat pin when mentor updates (`template@vYYYY-MM-DD`).

---

## 7. Failure modes

| Symptom | Likely cause | Mitigation |
|---|---|---|
| Import stalls | GitHub unreachable from mentor network | Retry off-peak; use git mirror §3 |
| Student cannot fork | Template private or wrong link | Fix visibility; repost pin |
| Student clone OK, push fails | Auth (HTTPS token / SSH) | Mentor demo `git config` + Gitee personal access token in room |
| Student lost in Cici README | Supabase/Claude steps still prominent | Strengthen `ANYANG-AI.md` banner; phase-1 meeting script |

Log resolved blockers under `singularity/work-anyang/evidence/anyang-gitee-preflight-YYYY-MM-DD.md`.

---

## 8. Checklist — mentor done when

- [ ] `anyang-ai-template` exists on Gitee (public or cohort-private by policy)
- [ ] Import provenance recorded (SHA + date)
- [ ] Tier A overlay committed (`ANYANG-AI.md` + `docs/anyang-ai/`)
- [ ] Mentor test fork + push succeeded
- [ ] Template URL in WeChat pin (when group exists)
- [ ] Preflight items in [China stack](../anyang-ai-cn-software-stack.md#mentor-preflight-before-wave-one) checked on student network

---

## Return path

- [anyang-ai-core/README.md](README.md)
- [anyang-community-mission-operator.md](../anyang-community-mission-operator.md)

## Revision

| Date | Note |
|------|------|
| 2026-06-08 | Initial import guide: Gitee UI + git mirror; Tier A overlay; student fork flow. |
