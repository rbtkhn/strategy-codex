Grace-mar paths and commands for this repository (from `.cursor/skills/packet-before-synthesis/`).

| Topic | Path |
|--------|------|
| Packet recipe | [docs/skill-work/work-strategy/source-hygiene-packets.md](../../docs/skill-work/work-strategy/source-hygiene-packets.md) |
| Packet doctrine | [docs/skill-work/work-strategy/packet-before-synthesis-doctrine.md](../../docs/skill-work/work-strategy/packet-before-synthesis-doctrine.md) |
| Packet chooser | [docs/skill-work/work-strategy/packet-crosswalk.md](../../docs/skill-work/work-strategy/packet-crosswalk.md) |
| Rome-Persia stress test | [codex/rome-persia-legitimacy-signal-check.md](../../codex/rome-persia-legitimacy-signal-check.md) |
| Portable skill manifest | [skills-portable/manifest.yaml](../../../skills-portable/manifest.yaml) |
| Sync script | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |
| Skill validator | [scripts/validate_skills.py](../../../scripts/validate_skills.py) |

**Repo notes**

- This skill is for **strategy-notebook judgment hygiene**, not Record or gate work.
- The owning WORK docs are the live doctrine:
  - [source-hygiene-packets.md](../../docs/skill-work/work-strategy/source-hygiene-packets.md)
  - [packet-before-synthesis-doctrine.md](../../docs/skill-work/work-strategy/packet-before-synthesis-doctrine.md)
  - [packet-crosswalk.md](../../docs/skill-work/work-strategy/packet-crosswalk.md)
- Use the Rome-Persia file as the stress-test example when checking whether the rule generalizes beyond hard-security seams.

**Common local command pattern**

```powershell
python scripts/sync_portable_skills.py --skill packet-before-synthesis
python scripts/sync_portable_skills.py --verify --skill packet-before-synthesis
python scripts/validate_skills.py
```
