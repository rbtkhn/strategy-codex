**strategy-codex instance notes**

- Preferred operator invocation: `memory`
- Legacy alias note: older references to `state-memory` as a skill mean this skill
- Keep `state-memory` as the canonical statecraft object family:
  - `civilization/objects/state-memory.md`
  - `statecraft/templates/state-memory.md`
  - migration and inventory object-class keys
- Do not blur this skill with repo meanings such as `memory`, runtime memory, or speaker-memory.

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill memory
python scripts/sync_portable_skills.py --verify --skill memory
python scripts/validate_skills.py
```
