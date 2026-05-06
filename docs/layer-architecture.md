# Layer Architecture

**Companion-Self template -- Four-layer instruction model**

---

## Problem

A single monolithic instruction file (AGENTS.md) mixing core doctrine, instance-specific paths, operational procedures, and lane-specific rules becomes a bloat vector as the system grows. Every new lane, mode, or instance adds lines to a file that every session must parse.

## Principle

> Keep the center lean enough that its logic stays legible.

The instruction architecture splits into four layers. Later layers may narrow but never contradict earlier ones.

---

## The four layers

| Layer | Canonical location | Scope | Reload frequency |
|-------|-------------------|-------|-----------------|
| **1. Core Doctrine** | `AGENTS.md` | State separation, authority classes, promotion law, knowledge boundary, gated pipeline, terminology, permission boundaries | Always loaded |
| **2. Instance Doctrine** | `instance-doctrine.md` | Operating modes, repo structure, file update protocol, success metrics, prompt architecture | Always loaded for the active instance |
| **3. Lane Overlays** | `docs/skill-work/work-*/` | Per-lane focus, ledger, history, framing, background context | Loaded when the lane is active |
| **4. Mode Overlays** | `.cursor/skills/*/SKILL.md` | Cadence rituals (coffee, dream, bridge, harvest, thanks), review passes, specialized workflows | Loaded when the mode is triggered |

---

## Load order

```
Core Doctrine (always)
  â””â”€â”€ Instance Doctrine (always for active instance)
        â”œâ”€â”€ Lane Overlay (when lane is active)
        â””â”€â”€ Mode Overlay (when mode is triggered)
```

**Narrowing rule:** Each layer may add constraints or specifics. No layer may loosen or contradict a higher layer. If a lane overlay says "allow X" but core doctrine says "never X," core doctrine wins.

---

## What belongs where

| Content type | Layer | Example |
|-------------|-------|---------|
| Knowledge boundary rule | Core | "Never merge facts the companion didn't provide" |
| Gated pipeline law | Core | "The agent may stage. It may not merge." |
| Merge script paths | Instance | `python scripts/process_approved_candidates.py --apply` |
| Repository tree | Instance | `self.md`, `bot/prompt.py` |
| Success metric commands | Instance | `python scripts/run_voice_benchmark.py` |
| Lane-specific strategy | Lane | `docs/skill-work/work-politics/STRATEGY.md` |
| Lane history log | Lane | `docs/skill-work/work-dev/work-dev-history.md` |
| Cadence ritual steps | Mode | `.cursor/skills/coffee/SKILL.md` |
| Bridge packet format | Mode | `.cursor/skills/bridge/SKILL.md` |

---

## For template instances

companion-self provides:
- `AGENTS.md` â€” core doctrine (template version, near-identical across instances)
- `_template/instance-doctrine.md` â€” scaffold with placeholder sections
- `demo/instance-doctrine.md` â€” demo content
- Lane overlay structure in `docs/skill-work/work-template/`
- Mode overlay structure in `.cursor/skills/`

When `companion_factory.py` creates a new instance, it copies the template scaffold. The instance operator fills in instance-specific paths, scripts, and metrics.

---

## Cross-references

- [AGENTS.md](../AGENTS.md) â€” Core Doctrine (Layer 1)
- [architectural-principles.md](architectural-principles.md) â€” Named design principles including this layer model
- [docs/skill-work/work-template/MAPPING.md](skill-work/work-template/MAPPING.md) â€” Lane overlay mapping

