# Grace-Mar — archived fork doctrine

**Archive only — not active product identity.** Active work belongs to **strategy-codex** ([`../product-identity.md`](../product-identity.md)).

**Operational boundary (short):** [`../grace-mar-instance-boundary.md`](../grace-mar-instance-boundary.md) · **CLI compatibility:** [`grace-mar-compatibility.md`](grace-mar-compatibility.md)

---

## What Grace-Mar was

**Grace-Mar** was a **cognitive fork** — a versioned personal Record (`self.md`, evidence, gate queue) plus deprecated **Voice** bots (Telegram / WeChat) that emulated the Record in chat. It lived in the **companion-self** template lineage.

**strategy-codex** superseded it as the active system: a **governed interpretive machine** (`statecraft` + `singularity`). Growing the fork is **not** a system objective (`platform/config/strategy_codex.yaml`: `record_frozen: true`).

---

## Core terms (fork revive context)

| Term | Meaning |
|------|---------|
| **Record** | Documented self at `archive/grace-mar-instance/` — identity, evidence, gate |
| **Voice** | Deprecated chat emulation over the Record — not operator default |
| **Companion** | The human authority; merge requires companion approval |
| **Fork / fork revive** | Explicit lane to stage and merge Record growth via `recursion-gate.md` |
| **RECURSION-GATE** | Staging queue — `archive/grace-mar-instance/recursion-gate.md` |
| **Triadic cognition (legacy)** | Mind + Record + Voice — historical only |

---

## Physical paths

| Path | Role |
|------|------|
| [`archive/grace-mar-instance/`](../../archive/grace-mar-instance/) | Embedded Record bundle (`self.md`, `recursion-gate.md`, `self-archive.md`, bot/) |
| [`archive/grace-mar-corpus/`](../../archive/grace-mar-corpus/) | Quarantined historical doctrine |
| [`archive/grace-mar-instance/bot/`](../../archive/grace-mar-instance/bot/) | Deprecated Telegram / WeChat runtime |

Record markdown **does not** live at repository root. Scripts resolve via [`scripts/repo_io.py`](../../scripts/repo_io.py) → `profile_dir()` / `GRACE_MAR_INSTANCE_DIR`.

**Active adjacent (not Record):** [`self-library.md`](../../archive/grace-mar-instance/self-library.md) (reference routing), [`self-memory.md`](../../archive/grace-mar-instance/self-memory.md) (WORK continuity).

---

## What is frozen

| Surface | Status |
|---------|--------|
| `self.md`, `self-archive.md`, `recursion-gate.md`, `session-log.md`, `self-skills.md` | **Frozen** — archaeology; no default growth |
| Voice bots, miniapp as Record growth path | **Deprecated** |
| Default gate review / “grow the Record” menus | **Disallowed** |

---

## When to revive the fork lane

Invoke **only** when you intentionally reopen Grace-Mar archive work:

| Token | Effect |
|-------|--------|
| `grace-mar archive` | Read-only archaeology + export paths |
| `fork revive` | Gate staging/merge rules apply; companion approval required |
| Coffee **`A gate`** | Steward gate track (not default Confirm) |
| `harness_warmup.py --territory companion` | Show companion/gate pending in warmup |

**Default operator capture:** [`../replacement-capture-habits.md`](../replacement-capture-habits.md) — WORK lanes, not ambient RECURSION-GATE staging.

---

## What active strategy-codex work does instead

```text
source-archive → synthesis → lane judgment object
```

- Archive: [`source-archive/statecraft/`](../../source-archive/statecraft/README.md)
- Synthesis: [`statecraft/synthesis/day/`](../../statecraft/synthesis/METHOD.md)
- Channels: [`statecraft/`](../../statecraft/README.md), [`singularity/`](../../singularity/README.md)

See [`../start-here.md`](../start-here.md).

---

## Merge law (fork revive only)

1. **Stage** candidates in `recursion-gate.md` — agent may stage, **may not merge**
2. **Companion approves** — echo `CANDIDATE-XXXX` + one-line summary
3. **Merge** only via `python scripts/process_approved_candidates.py --apply`

**Never** edit `self.md`, `self-archive.md`, or `archive/grace-mar-instance/bot/prompt.py` directly on approval.

**Immutability:** Evidence is append-only; SKILLS may upgrade, never downgrade.

---

## Maintenance checks

**Phrase-level fork-default language:**

```bash
python3 scripts/audit_fork_language.py
python3 scripts/audit_fork_language.py --strict
```

Rules: [`platform/config/fork-language-audit.v1.json`](../../platform/config/fork-language-audit.v1.json)

**Section-level Grace-Mar sprawl in primary docs:**

```bash
python3 scripts/check_archive_boundary.py
python3 scripts/check_archive_boundary.py --strict
```

---

## Related

- [`../legacy-operator-concepts.md`](../legacy-operator-concepts.md)
- [`../deprecated-surfaces.md`](../deprecated-surfaces.md)
- [`../runtime-vs-record.md`](../runtime-vs-record.md)
- [`../../archive/grace-mar-corpus/README.md`](../../archive/grace-mar-corpus/README.md)
