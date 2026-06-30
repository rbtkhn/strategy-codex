# Operator Queue

Local **Agent Handoff Queue** items for work that passes between humans, agents, validators, and gates.

**Doctrine:** [docs/agent-handoff-queue.md](../../docs/agent-handoff-queue.md)

**Validator:**

```bash
python3 scripts/check_agent_handoff_queue.py
python3 scripts/check_agent_handoff_queue.py --strict
```

## Status directories

| Directory | Status |
|-----------|--------|
| `agent-todo/` | `agent_todo` |
| `agent-working/` | `agent_working` |
| `needs-input/` | `needs_input` |
| `gate-required/` | `gate_required` |
| `agent-done/` | `agent_done` |
| `void/` | `void` |

## Rules

- Queue items are Markdown files with YAML frontmatter.
- Filename: `ahq-YYYYMMDD-NNN-short-slug.md`; frontmatter `id` must match the prefix.
- Directory status and frontmatter `status` must agree.
- `agent_done` items require a `receipt` block.
- `needs_input` items require a `blocking_question` block.
- `gate_required` items require a `gate` block.
- `void` items require `void_reason`.
- Queue receipts do **not** promote authority automatically.
