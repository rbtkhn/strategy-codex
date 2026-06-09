# Session continuity â€” explicit contract, not implicit memory

**Purpose:** Treat **continuity as a written contract** â€” specific files, optional scripts, and CI â€” **not** as â€œthe agent should remember last time.â€ LLM sessions and harnesses **do not** carry repo state unless you **load** it.

---

## What we do *not* promise

| Anti-pattern | Why it fails |
|--------------|--------------|
| â€œThe agent remembersâ€ | New chats have **no** thread memory of SESSION-LOG, gate, or EVIDENCE unless those artifacts are **read or injected**. |
| â€œWe talked about itâ€ | Conversation in another tool is **not** canonical Record continuity. |
| Vibes-based handoff | Operator assumes the next session â€œknowsâ€ context without **explicit steps**. |

**UX rule:** Do not imply seamless recall. **Continuity is an operator + harness obligation** expressed as **steps** (or automation that runs those steps).

---

## The contract (three layers)

Layers stack; none replaces the companion gate or merge authority.

### Layer 1 â€” Canonical files (human or agent must *read*)

For user id `[id]` (default **`strategy-codex`**; **`grace-mar`** only on explicit fork revive), **before** substantive work in a shared workspace:

| Path | Role |
|------|------|
| `session-log.md` | What happened last; session narrative |
| `recursion-gate.md` | Staged candidates; approval queue |
| `self-archive.md` | Recent ACT- / gated-approved activity entries (skim the last 1â€“2 relevant blocks); fall back to `self-evidence.md` only for legacy or pre-migration layouts |

**Contract:** Continuity means **these paths were consulted** (by a human or by a tool that ingests them), not that a model â€œfelt caught up.â€

Full checklist and OpenClaw patterns: [openclaw-integration.md Â§ Session continuity](../../openclaw-integration.md#2-session-continuity-startup-checklist).

### Layer 2 â€” Scripts (machine-checkable behavior)

| Script | What it does |
|--------|----------------|
| `python scripts/continuity_read_log.py -u strategy-codex` | Verifies continuity files **exist**, logs a JSONL line to `continuity-log.jsonl` (audit trail). Does **not** merge into the Record. Use `--dry-run` to print payload only. |
| `python scripts/harness_warmup.py -u strategy-codex` | Emits a **pasteable** digest for **new Cursor/agent threads** â€” Record frozen by default (interpretive-machine health, not gate nudges). Still requires **pasting**; not automatic recall. |
| `python scripts/session_brief.py -u strategy-codex` | Short operator brief (alternative to manual file skim). Fork revive: `-u grace-mar`. |
| `python scripts/openclaw_heartbeat.py -u strategy-codex` | Periodic pulse for long OpenClaw runs. |

**Contract:** â€œWe ran continuityâ€ can mean **either** a human read the files **or** a documented script ran **and** its output was used â€” not â€œthe model was warm.â€

### Layer 3 â€” CI proves the contract stays executable

| Check | What it guarantees |
|-------|---------------------|
| `pytest tests/test_continuity_read_log.py` | `continuity_read_log.py` exits 0 on `--dry-run` for `grace-mar`, and the continuity surfaces (`session-log.md`, `recursion-gate.md`, canonical evidence path) exist under ``. |

**Contract:** The **proof-of-read script and paths** do not silently rot. It does **not** prove an operator read anything â€” only that the **automation contract** remains valid in the repo.

---

## One-line summary for partners

**Continuity is encoded:** read these files (or run these scripts); CI ensures the continuity script and paths still work â€” **not** â€œthe AI remembers.â€

---

## Relation to visible safety state

Continuity answers **â€œdid we load context?â€** The **safety story** answers **â€œwhatâ€™s pending vs committed, with receipts?â€** â€” see [safety-story-ux.md](safety-story-ux.md).

---

## Relation to runtime memory (OpenClaw / plugins)

If a **runtime** memory plugin is used, treat it as **adjunct** â€” bounded, non-canonical â€” per [openclaw-integration.md](../../openclaw-integration.md). It **does not** replace Layer 1 or Layer 2 for **Record-adjacent** truth.

---

## Guardrail

`continuity_read_log.py` checks **file presence** and optional logging; it does **not** verify a human or model **understood** contents. The **companion gate** remains the authority for what enters SELF/EVIDENCE.
