Repo-specific paths and commands for **audit-index** (from `.cursor/skills/audit-index/`).

| Topic | Path |
|--------|------|
| Audit CLI | [scripts/audit_statecraft_archive_index.py](../../../scripts/audit_statecraft_archive_index.py) |
| Channel index (md/json) | [statecraft/channels/channel-index.md](../../../statecraft/channels/channel-index.md) |
| Day-index builder | [scripts/build_statecraft_day_indices.py](../../../scripts/build_statecraft_day_indices.py) |
| Global navigation builder | [scripts/build_statecraft_archive_navigation.py](../../../scripts/build_statecraft_archive_navigation.py) |
| Day-index spec | [source-archive/statecraft/day-index-spec.md](../../../source-archive/statecraft/day-index-spec.md) |
| Archive root | [source-archive/statecraft/](../../../source-archive/statecraft/) |
| Source intake (post-land) | [statecraft-source-intake/SKILL.md](../statecraft-source-intake/SKILL.md) |
| LLM routing — day-index row | [LLM-ROUTING.md](../../../LLM-ROUTING.md) |
| Portable manifest | [skills/manifest.yaml](../../../skills/manifest.yaml) |

**Bounded read (Windows harness):** when path is known, `Read` `source-archive/statecraft/YYYY-MM-DD/day-index.md` with **limit ≤ 60** — do not grep the archive for index truth.

**Common commands (one Shell per turn; batch with `;` on Windows):**

```powershell
python scripts/audit_statecraft_archive_index.py --day 2026-06-28
python scripts/audit_statecraft_archive_index.py --day 2026-06-28 --table
python scripts/audit_statecraft_archive_index.py --global
python scripts/audit_statecraft_archive_index.py --channel-index --table
python scripts/audit_statecraft_archive_index.py --channel-index --fix
python scripts/audit_statecraft_archive_index.py --month 2026-06 --table-only --table-limit 50
python -m pytest tests/test_audit_statecraft_archive_index.py -q
python scripts/sync_portable_skills.py --skill audit-index --verify
```

**Fix law:** `--fix` rebuilds stale day-index (scoped days) and/or full global navigation. Apply only on operator **EXECUTE** or explicit fix confirm. After `--fix`, receipt reflects post-fix state (audit runs after rebuild).

**Do not:** monolithic read of all `source-*.md` for audit; use CLI table mode instead.
