# Grace-Mar instance boundary

The embedded **Grace-Mar** cognitive fork in this repo is **operator-archived**. Growing a personal cognitive fork is **not** an objective of `strategy-codex`.

**SSOT config:** [`config/strategy_codex.yaml`](../config/strategy_codex.yaml) (`record_frozen: true`)

**Product identity:** [`product-identity.md`](product-identity.md) · [`start-here.md`](start-here.md)

**Archive pointer:** [`archive/grace-mar-frozen.md`](../archive/grace-mar-frozen.md) · **Grace-Mar corpus (archaeology):** [`archive/grace-mar-corpus/README.md`](../archive/grace-mar-corpus/README.md) · **Legacy concepts:** [`legacy-operator-concepts.md`](legacy-operator-concepts.md)

---

## What strategy-codex is now

A **governed interpretive machine**:

- verbatim sources → [`source-archive/statecraft/`](../source-archive/statecraft/README.md)
- bounded synthesis → [`statecraft/daily/`](../statecraft/daily/METHOD.md)
- judgment objects → [`statecraft/`](../statecraft/README.md) lane transactions
- operator channels → [`statecraft`](../statecraft/README.md) and [`singularity`](../singularity/README.md)

Durable work normally ends at **governed adjacent** surfaces. See [`work-membrane-v2.md`](work-membrane-v2.md).

---

## Freeze status

| Surface | Status |
|---------|--------|
| `self.md`, `self-archive.md`, `recursion-gate.md`, `session-log.md`, `self-skills.md` | **Frozen** — operator backup; no default growth |
| `bot/`, Telegram/WeChat, `apps/miniapp_server.py` | **Deprecated** — legacy only |
| `self-library.md`, CIV-MEM routing | **Active reference** — statecraft retrieval; not IX-A identity growth |
| `self-memory.md` | **Active WORK continuity** — not Record; dream may normalize |

---

## Allowed (default strategy-codex work)

- Statecraft and singularity operator lanes
- Archive intake, daily synthesis, transactions, validators
- Coffee / conductor / dream / bridge / harvest cadence
- Read or cite frozen Record for archaeology
- Export frozen Record (`scripts/export_fork.py`) — read-only consumption
- **Cici / BrewMind governed state** — separate membrane; not Grace-Mar fork revival

---

## Disallowed as default (unless explicit revive)

- Staging IX-A/B/C candidates to `recursion-gate.md`
- Offering gate review, elicit-knowledge, or "grow the Record" menus
- Auto-pipeline on **"we finished [book]"** or companion identity signals
- Bot/Voice maintenance or new Telegram/WeChat deployments
- Treating warmup capture-gap or pipeline-velocity as primary nudges

---

## Explicit fork revive

Invoke only when you intentionally reopen Grace-Mar archive work:

| Token | Effect |
|-------|--------|
| `grace-mar archive` | Read-only archaeology + export paths |
| `fork revive` | Gate staging/merge rules apply; companion approval required |
| Coffee **`A gate`** | Steward gate track (not default Confirm) |
| `harness_warmup.py --territory companion` | Show companion/gate pending in warmup |

Merge law unchanged: **`scripts/process_approved_candidates.py --apply`** only after approval.

---

## Terminology guard

| Term | Meaning here |
|------|----------------|
| **recursion-gate** | Frozen Grace-Mar Approval Inbox (`recursion-gate.md`) |
| **statecraft gate object** | Active judgment artifact (e.g. recognition-gate transaction) — **not** frozen |
| **governed state** (Cici/BrewMind) | Business-fact membrane in work-cici — **not** this fork |

---

## Maintenance — fork-language audit

Read-only scan for operator docs that still imply fork growth or Voice as default:

```bash
python3 scripts/audit_fork_language.py
python3 scripts/audit_fork_language.py --strict   # fail on warns too (CI optional)
```

Rules: [`config/fork-language-audit.v1.json`](../config/fork-language-audit.v1.json). Tune `skip_paths_exact` for intentional historical corpora.

---

## Portable skills sync

After doctrine changes land here, run portable skill sync if you use Codex host copies:

`python3 scripts/sync_portable_skills.py` (see [`skills-portable/README.md`](../skills-portable/README.md)).

---

## Related boundaries

- Predictive History: [`predictive-history-external-boundary.md`](predictive-history-external-boundary.md)
- Deprecated surfaces index: [`deprecated-surfaces.md`](deprecated-surfaces.md)
- Runtime vs Record: [`runtime-vs-record.md`](runtime-vs-record.md)
