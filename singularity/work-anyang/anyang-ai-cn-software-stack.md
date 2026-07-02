# anyang-ai — China software stack (operator WORK)

**Purpose:** Replace cici-ai's default toolchain recommendations — tuned for **Philippines / international** access — with a **China-first** stack for Anyang cohorts. The **learning goal** stays the same (governed personal workspace, git-shaped habits, visible artifacts); the **vendors** change.

**Upstream contrast:** [cici-ai onboarding prerequisites](../work-cici/evidence/cici-neural-sandbox-pt2-rtf-ingest-2026-04-21.md) (GitHub, Claude Pro/Max, Supabase, Telegram). **Do not** paste that list into Anyang member copy without this mapping.

**Owner:** Anyang mentor validates live access on student machines before wave-one launch.

---

## Design principle

| Keep (concept) | Change (vendor) |
|---|---|
| Social cohort room | **WeChat** — not Telegram |
| Durable code + docs spine | **Gitee primary** — not GitHub-as-default |
| AI-assisted setup and learning | **Domestic coding assistants** — not Claude/OpenAI-as-default |
| Optional cloud backend | **Deferred or domestic cloud** — not Supabase-as-default |
| Weekly proof | **In-person + WeChat screenshots** — same discipline, different chat |

**Initiation success** for phase 1 = member owns a **repo + local workspace + one governed markdown habit + public stuck/done posts** — not "replicated every Cici cloud dependency on day one."

---

## Learning lanes vs infrastructure tracks

| Axis | Names | Meaning |
|---|---|---|
| **Learning lane** | **Foundation (预备轨)** / **Builder (实操轨)** | Coding readiness — [anyang-ai-lanes.md](anyang-ai-lanes.md). Foundation **does not use Gitee in week one**. |
| **Infrastructure track** | **China default** / **Bridge (optional)** | Builder-only add-on: GitHub + Claude + Supabase parity when access already stable. |

**Builder lane** uses the stack below. **Foundation lane** uses WeChat + in-room + domestic AI only until [graduation](anyang-ai-foundation/README.md#graduation-to-builder-预备--实操).

---

## Recommended stack — China default (Builder lane)

Use for **Builder** members. Foundation members graduate into this stack.

### 1. Coordination

| Role | Recommendation | Notes |
|---|---|---|
| Group chat | **WeChat 微信群** `anyang-ai` | Pin mission + one-artifact rule; evidence = screenshots / quotes |
| Meetings | **Weekly in-person** (Anyang) | Artifact block every session |
| Docs / FAQ | **微信文档** or **腾讯文档** (optional) | Mirror links also in pinned message |

### 2. Code hosting (proof layer)

| Role | Recommendation | Notes |
|---|---|---|
| Primary git remote | **[Gitee](https://gitee.com)** | Stable inside China; fork/import from mentor template |
| Template source | Mentor-maintained **Gitee 模板仓库** | One-time import: [anyang-ai-gitee-template-import.md](anyang-ai-core/anyang-ai-gitee-template-import.md); students fork mentor template only |
| Local git | **Git** + **VS Code** (or mentor-standard IDE) | Use domestic install mirrors if download is slow |
| Proof signal | Gitee repo URL in WeChat | Same function as GitHub fork URL in cici-ai |

**Do not** require GitHub on day one. Track `github_capable` separately for members who already have reliable access.

### 3. AI coding assistant (execution layer)

| Role | Recommendation | Notes |
|---|---|---|
| Default | **DeepSeek** (网页 / API / IDE 插件 — mentor picks one standard) | Widely usable in China; strong coding |
| IDE alternatives | **通义灵码**, **CodeGeeX**, **豆包 MarsCode** | Pick **one** cohort standard to reduce support load |
| Mentor demo machine | May use Cursor / Claude / other | **Demos ≠ student requirement**; students post proof from Tier A tool |

**Do not** list **Claude Pro/Max**, **ChatGPT Plus**, or **Telegram** as student prerequisites.

### 4. Memory / backend (simplify phase 1)

| Role | Recommendation | Notes |
|---|---|---|
| Phase 1 default | **Git + markdown files in repo** | Companion-self / OB1 **ideas** without Supabase Edge on week one |
| Phase 2 (optional) | **腾讯云** or **阿里云** serverless | Only after Tier A initiation works; mentor documents one path |
| Avoid as default | **Supabase** | Foreign SaaS; flaky or slow for many China networks |

### 5. Secrets hygiene

- No API keys in WeChat chat or public Gitee commits.
- Use `.env` local only + `.gitignore`; mentor reviews in **room**, not via DMs alone.
- Same rule as cici-ai; different chat surface.

---

## Bridge track — optional infrastructure (Builder + mentor-gated)

**Not** a learning lane — optional **infra** upgrade when a **Builder** member already has stable GitHub/Claude access.

| Component | Bridge |
|---|---|
| Git remote | GitHub fork of Cici (or sync Gitee ↔ GitHub) |
| AI | Claude Code / Cursor / ChatGPT per member subscription |
| Backend | Supabase free tier per Cici README |
| Chat | WeChat still primary for cohort; no Telegram required |

**Rule:** Bridge is **advanced infra**, not cohort default. Progress dashboard: `learning_lane` + `infra_track=china_default|bridge`.

---

## cici-ai → anyang-ai mapping table

| cici-ai default | anyang-ai default | Why |
|---|---|---|
| Telegram | WeChat | Telegram blocked / unusable as primary in China |
| GitHub fork | Gitee fork of mentor template | GitHub access uneven; Gitee is domestic-stable |
| Claude Pro/Max + Claude Code | DeepSeek + one domestic IDE plugin | Western model subscriptions not reliable as mass prerequisite |
| Supabase | Repo-local markdown first; domestic cloud later | Reduces foreign dependency on initiation day |
| Async remote mesh | Weekly physical + WeChat | Already an Anyang advantage — lean into it |

---

## Phase-1 initiation checklist — Builder lane (replaces cici OB1 day-one bar)

**Foundation lane** uses a separate bar: [anyang-ai-foundation/README.md](anyang-ai-foundation/README.md#foundation-initiation-bar).

**Builder** member counts as **initiation done** when all are true:

1. Joined WeChat `anyang-ai` and posted intro (name + goal in one sentence).
2. **Gitee** account created; forked mentor template; repo URL posted in group.
3. Cloned repo locally; opened in IDE; **no secrets committed**.
4. Completed **one** mentor-defined first win (e.g. edit `README.md` or add `docs/my-goal.md`, commit, push — visible on Gitee).
5. Posted **done** or **stuck on X** in WeChat within 48h of first meeting.

Supabase, Claude, and GitHub are **not** required for this bar.

---

## Mentor preflight (before wave one)

Mentor confirms on **student lab machines**:

- [ ] Gitee signup and push work on classroom network
- [ ] Chosen domestic AI tool loads and accepts a trivial coding prompt
- [ ] Git install path documented (Windows/Mac)
- [ ] Template repo imported to Gitee and fork flow tested once
- [ ] WeChat pin + 置顶 tested

Document blockers in `singularity/work-anyang/evidence/` when discovered.

---

## What we are not claiming

- This doc is **operator routing**, not legal advice on VPNs, cross-border data, or vendor terms.
- Domestic tools change quickly — mentor owns **one-page student quickstart** with screenshots.
- Tier A teaches **governed workspace habits**; full OB1/Cici parity may be a **later** milestone.

---

## Return path

- [anyang-community-mission-operator.md](anyang-community-mission-operator.md)
- [anyang-ai-core/README.md](anyang-ai-core/README.md)
- [anyang-ai-gitee-template-import.md](anyang-ai-core/anyang-ai-gitee-template-import.md)
- [cici-ai golden path (international)](../work-cici/telegram-cici-ai-pinned-and-welcome-copy.md)

## Revision

| Date | Note |
|------|------|
| 2026-06-08 | Initial China-first stack: WeChat, Gitee, domestic AI, deferred Supabase; Tier B bridge; initiation checklist. |
| 2026-06-08 | Gitee import guide + Tier A overlay file set in `anyang-ai-core/`. |
| 2026-06-08 | Foundation vs Builder learning lanes; Bridge track renamed (was Tier B infra). |
