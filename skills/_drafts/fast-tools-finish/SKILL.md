---
name: fast-tools-finish
description: "Recovery after Cursor harness timeout on Windows: Read/Write first, one Shell per intent, no parallel Grep/Glob. Trigger: fast tools, read only, fast tools and finish <task>."
category: domain-pack
status: draft
---
# fast-tools-finish (draft pointer)

**Shipped elsewhere (2026-06-12):**

- [coffee/SKILL.md — Harness hang recovery](../../../../.cursor/skills/coffee/SKILL.md#harness-hang-recovery)
- [validator-first/SKILL.md — Civ-lens profile wedge](../../../.cursor/skills/validator-first/SKILL.md)
- [agent-tool-latency-discipline.mdc](../../../.cursor/rules/agent-tool-latency-discipline.mdc)

Promote to portable core + manifest only if the pattern repeats outside strategy-codex hosts.

## Operator phrases

- **`fast tools`** / **`read only`** — Read/Write + one Shell per turn; no Glob/Grep storms
- **`fast tools and finish <task>`** — Read/Write the target files, then one bounded Shell for `<task>`

## When to use

After tool output shows *Interrupted by the user after ~300000ms+* or repeated empty hangs — not after a normal git/network error with stdout.
