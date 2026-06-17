# Public mirrors

Repo-root staging for **official public book mirrors**. In strategy-codex, edit the corpus **only** under these paths; ship to GitHub only through the named publish command.

| Mirror | Remote | Workspace path | Inbound (pull) | Outbound (publish) |
|--------|--------|----------------|----------------|---------------------|
| Predictive History (`ph-civ`) | [`rbtkhn/ph-civ`](https://github.com/rbtkhn/ph-civ) | [ph-civ/](ph-civ/) | `python scripts/sync_public_ph_civ_mirror.py` | `python scripts/publish_public_ph_civ.py -m "…" --push` |

Sync check: `python scripts/check_academy_mirror_sync.py`

## Discipline

1. **Edit** Predictive History corpus only in `public/ph-civ/` — not under legacy `codex/predictive-history/`, frozen residue trees, or scattered workshop paths.
2. **Commit** workspace changes in strategy-codex when the staging slice is ready.
3. **Publish** to the public repo only via `publish_public_ph_civ.py --push` (robocopy → ph-civ clone → commit → push). There is no automatic upstream push from a normal strategy-codex commit.
4. **Pull** upstream with `sync_public_ph_civ_mirror.py` when reconciling against remote `main`.

## Upstream ship (mandatory)

Transcript or corpus changes that should land in [`rbtkhn/ph-civ`](https://github.com/rbtkhn/ph-civ) require:

```powershell
python scripts/publish_public_ph_civ.py -m "your message" --push
```

Default publish clone: `C:\dev\ph-civ` (override with `--clone-dir` or `PH_CIV_PUBLISH_CLONE`).

Dry-run: `python scripts/publish_public_ph_civ.py --dry-run`

**Do not** push to `ph-civ` manually from scattered paths; **do not** assume a strategy-codex commit updates the public repo.
