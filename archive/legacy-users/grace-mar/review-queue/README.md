# grace-mar change-review queue

Minimal scaffold for **material change-review** (escalation from [identity-fork-protocol.md](../../docs/identity-fork-protocol.md) §4.3). Routine candidates still use **`platform/users/grace-mar/recursion-gate.md`**.

See [platform/users/platform/template/archive/queues/review-queue/README.md](../platform/template/archive/queues/review-queue/README.md) for semantics, canonical filenames, and validation.

```bash
# Empty or partially filled scaffold (no strict minimums for proposals/decisions/diffs):
python3 scripts/validate-change-review.py platform/users/grace-mar/review-queue --allow-empty

# Proposals + diffs present, decisions/ still empty (pre-companion decision):
python3 scripts/validate-change-review.py platform/users/grace-mar/review-queue --allow-missing-decisions
```
