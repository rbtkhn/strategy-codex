# Default path — strategy pass

**Purpose:** The minimum viable **`strategy` / `strategy pass`** on `/codex`. Three moves, then stop. Everything else (civ-mem, promotion, verify, history notebook, commentator threads, voice/lens) is **optional** and triggered only when the operator asks or the day demands it.

**Activation (no skill):** The **`skill-strategy` Cursor skill is dissolved** — see [SKILL-STRATEGY-DEPRECATED.md](SKILL-STRATEGY-DEPRECATED.md). Agents follow [.cursor/rules/strategy-codex-pass.mdc](../../../.cursor/rules/strategy-codex-pass.mdc) and this file.

**Naming:** `strategy-codex` is the active operator surface and `/codex` is the canonical corpus. **`strategy-notebook`** is deprecated — [STRATEGY-NOTEBOOK-DEPRECATED.md](STRATEGY-NOTEBOOK-DEPRECATED.md).

**When:** Normal day. Operator says **`strategy`** or **`strategy pass`**. **`strategy page read`** — read-only frontier (no `days.md` / **`strategy-page`** writes); see [architecture § *End-of-day strategy session* — *Read-only variant*](../../../codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md#end-of-day-strategy-session-terminology).

**Boundary:** **`strategy` = codex ledger only.** Live judgment, intake, and voice passes → **[statecraft](../../../statecraft/README.md)**, **`coffee` C**, or **conductor** — not the default codex menu.

**Full sequence (SSOT):** [STRATEGY-NOTEBOOK-ARCHITECTURE.md — Default operating path](../../../codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md#default-operating-path-ssot).

---

## When to say what (operator one-pager)

| Say this | Contract |
|----------|----------|
| **`strategy`** / **`strategy pass`** | This file — STATUS → inbox → menu |
| **`compass`** (legacy) | Same as strategy lane without opening **`coffee`** Step 1 ([menu-reference](../work-coffee/menu-reference.md)) |
| **`coffee` C** | **Statecraft** router — live judgment, lanes, intake ([statecraft/README.md](../../../statecraft/README.md)) |
| **`conductor` / master name** | Named mid-day emphasis; close on daily/note/watch |
| **`strategy page` / compose** | EOD session — architecture § End-of-day strategy session |
| **`strategy + verify`** | [wire-verify](../../../skills/wire-verify/SKILL.md) / [fact-check](../../../.cursor/skills/fact-check/SKILL.md) |
| **`strategy write`** | Substance from codex frontier + [skill-write](../../../.cursor/skills/skill-write/SKILL.md) |
| **Voice / multi-lens** | After **statecraft handoff**, on **compose**, or when operator names a speaker — [VOICES-SUPERSEDE-MINDS.md](VOICES-SUPERSEDE-MINDS.md) |

---

## The three moves

### 1. Read the frontier

If the operator said **`strategy page read`**, stay in **read-only** mode: summarize where the notebook stands, then stop or offer a short pivot menu — **do not** compose into `days.md` or **`strategy-page`**.

Open **two files**, scan **one**:

- [`codex/STATUS.md`](../../../codex/STATUS.md) — where are we?
- [`codex/daily-strategy-inbox.md`](../../../codex/daily-strategy-inbox.md) — what accumulated?
- Tail of active `codex/chapters/YYYY-MM/days.md` — what did the last entry leave in **Open**?

If a daily brief exists for today (`daily-brief-YYYY-MM-DD.md`), skim its lead.

Access warning: thin capture is not the same as a thin field.

**Time:** <1 minute.

### 2. Write the inbox (Capture)

Append paste-ready lines to [`codex/daily-strategy-inbox.md`](../../../codex/daily-strategy-inbox.md). Shape: one-liner or two-tier gist (`cold: … // hook: …`). Tag the plane when load-bearing ([FIVE-THREAD-WATCH-TAGS.md](FIVE-THREAD-WATCH-TAGS.md) §1d–§1h).

Do **not** touch `days.md` unless the operator says **`strategy page`**, **`strategy page compose`**, or **EOD notebook compose**.

Verbatim **`strategy input`** → **`source-intake`** → [`source-archive/statecraft/`](../../../source-archive/statecraft/README.md) first per [strategy-input-raw-ingest.mdc](../../../.cursor/rules/strategy-input-raw-ingest.mdc) and [RAW-INPUT-DEPRECATED.md](RAW-INPUT-DEPRECATED.md). Do **not** write new captures to deprecated [`codex/raw-input/`](../../../codex/raw-input/README.md).

**Time:** Variable (5–30 min depending on ingest volume).

### 3. Offer the menu

End the pass with **3–5 options** (standard WORK menu). Typical forks:

| Letter | Option |
|--------|--------|
| **A** | **`strategy page`** / **`strategy page compose`** — inbox + **source archive** → **`strategy-page`** + `days.md`; voice/lens **may** appear in Reflection on compose days only |
| **B** | **Verify** — `strategy + verify` on a claim (`wire-verify` / `fact-check`) |
| **C** | **Pivot statecraft** — hand off to [statecraft](../../../statecraft/README.md), **`coffee` C**, or named statecraft skill — **not** voice menu on codex pass |
| **D** | **Promote** — stabilized arc → [STRATEGY.md](STRATEGY.md) |
| **E** | **Park** — another lane or stop |

If the operator picks **A**, follow [architecture § End-of-day strategy session](../../../codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md#end-of-day-strategy-session-terminology).

---

## What is NOT part of the default path

| Feature | When to add |
|---------|-------------|
| **Voice / multi-lens** | **Statecraft handoff**, **`strategy page compose`**, or operator names a speaker — [VOICES-SUPERSEDE-MINDS.md](VOICES-SUPERSEDE-MINDS.md) |
| **Civ-mem lookup** | Operator asks — [memory](../../../skills/memory/SKILL.md) |
| **History notebook wire** | [hn-bookshelf-lookup](../../../.cursor/skills/hn-bookshelf-lookup/SKILL.md) |
| **Commentator correlation** | [strategy-notebook-expert-cross-weave](../../../skills/strategy-notebook-expert-cross-weave/SKILL.md) |
| **ROME-PASS** | Holy See load-bearing day |
| **Watch threads §1d–§1h** | [FIVE-THREAD-WATCH-TAGS.md](FIVE-THREAD-WATCH-TAGS.md) |
| **Promotion to STRATEGY.md** | Arc stabilized |

---

## See also

| Doc | Role |
|-----|------|
| [README.md](README.md) | Lane entry + routing table |
| [NOTEBOOK-PREFERENCES.md](../../../codex/NOTEBOOK-PREFERENCES.md) | Prose register, EOD rhythm |
| [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../../codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md) | Full architecture |
| [SKILL-STRATEGY-DEPRECATED.md](SKILL-STRATEGY-DEPRECATED.md) | Migration from dissolved skill |
