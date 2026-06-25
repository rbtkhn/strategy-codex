# Predictive History operator workspace

Canonical public home: **[`rbtkhn/predictive-history`](https://github.com/rbtkhn/predictive-history)** (formerly `ph-civ`).

## Clone and env

```powershell
git clone https://github.com/rbtkhn/predictive-history.git C:\dev\predictive-history
$env:PREDICTIVE_HISTORY_ROOT = "C:\dev\predictive-history"
```

Legacy env shims (one release): `PH_CIV_ROOT`, `PREDICTIVE_HISTORY_ROOT` — prefer `PREDICTIVE_HISTORY_ROOT`.

## Daily loop

1. **Open** `C:\dev\predictive-history` (or set `PREDICTIVE_HISTORY_ROOT`) for corpus EXECUTE.
2. **Edit** essays, book chapters, cards, registries, docs in that repo.
3. **Validate:** `ph-civ validate` (CLI name unchanged).
4. **Ship:** `git commit` + `git push origin main` in the canonical repo.
5. **Refresh strategy-codex snapshot** (read-only mirror for cite/review):

```powershell
cd C:\dev\strategy-codex
python scripts/sync_predictive_history_mirror.py
git add public/predictive-history
git commit -m "[predictive-history-sync] inbound mirror refresh"
```

## strategy-codex roles

| Surface | Role |
|---------|------|
| `public/predictive-history/` | Inbound snapshot — **do not edit** corpus here |
| `codex/predictive-history/` | Frozen workshop residue — read for intake only |
| `statecraft/` | Synthesis, critique, cite public `essay-NN` / `civ-NN` IDs |

Boundary law: [predictive-history-external-boundary.md](predictive-history-external-boundary.md).

## Deprecated

- **`publish_public_ph_civ.py`** — outbound staging publish removed; edit canonical repo directly.
- **`sync_predictive_history_mirror.py`** — shim; use **`sync_predictive_history_mirror.py`**.

## Cursor setup

- **PH corpus sessions:** workspace root `C:\dev\predictive-history`
- **Strategy + statecraft:** `C:\dev\strategy-codex` — treat `public/predictive-history/` as read-only

Agent rule: [`.cursor/rules/predictive-history-direct-edit.mdc`](../.cursor/rules/predictive-history-direct-edit.mdc).
