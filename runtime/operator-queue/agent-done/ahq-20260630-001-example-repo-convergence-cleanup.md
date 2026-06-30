---
id: ahq-20260630-001
title: Example repo convergence cleanup
status: agent_done
owner: codex
requester: operator
created_at: 2026-06-30T12:00:00Z
membrane_class: instrumental_work
allowed_actions:
  - edit_tests
  - run_validation
forbidden_actions:
  - mutate_record
  - mutate_source_archive
  - resolve_events
  - publish_essay
context:
  - scripts/run_repo_convergence.py
  - tests/test_run_repo_convergence.py
  - docs/repo-convergence.md
definition_of_done:
  - tests pass
  - no lingering runtime artifact diffs
  - check mode remains non-mutating
stop_conditions:
  - ambiguity about authority boundary
  - validation failure requiring operator decision
receipt_required: true
receipt:
  status: agent_done
  completed_at: 2026-06-30T13:15:00Z
  actor: codex
  changed_files:
    - tests/test_run_repo_convergence.py
  commands_run:
    - python3 -m pytest tests/test_run_repo_convergence.py -q
    - python3 scripts/run_repo_convergence.py --check --json
  evidence:
    - tests passed
    - report/log files restored after mutating tests
  stopped_because: completed
  remaining_questions: []
labels:
  - repo-convergence
  - test-hygiene
priority: medium
---

# Example repo convergence cleanup

This example demonstrates the expected queue item shape for agent work that ends with a receipt.

The work loop paired repo convergence `--check` with pytest on the convergence test module. Receipts document commands and changed files; they do not promote authority automatically.
