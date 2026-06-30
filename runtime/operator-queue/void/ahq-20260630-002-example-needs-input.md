---
id: ahq-20260630-002
title: Example needs-input — health-check integration timing
status: void
owner: codex
requester: operator
created_at: 2026-06-30T14:00:00Z
membrane_class: instrumental_work
allowed_actions:
  - edit_docs
  - edit_validator
  - run_validation
forbidden_actions:
  - mutate_record
  - mutate_source_archive
  - auto_promote_to_health_check
stop_conditions:
  - operator decision on integration timing recorded
context:
  - scripts/check_repo_health.py
  - docs/repo-convergence.md
  - docs/agent-handoff-queue.md
definition_of_done:
  - operator answers blocking question
  - decision recorded in queue item or doctrine
  - no silent enrollment in check_repo_health --quick
receipt_required: true
void_reason: >-
  Example retired after operator decision (2026-06-30): check_agent_handoff_queue.py
  remains standalone; no check_repo_health --quick enrollment until queue grammar stabilizes.
labels:
  - agent-handoff-queue
  - adoption
priority: medium
---

# Example needs-input — health-check integration timing (void)

Illustrative item demonstrating stop grammar. Operator decision recorded in `void_reason`: validator stays standalone in Phase 1 per [agent-handoff-queue.md](../../docs/agent-handoff-queue.md) non-goals.
