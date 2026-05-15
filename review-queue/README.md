# grace-mar change-review queue

Minimal scaffold for **material change-review** (escalation from [identity-fork-protocol.md](../../docs/identity-fork-protocol.md) Â§4.3). Routine candidates still use **`recursion-gate.md`**.

See [_template/review-queue/README.md](../_template/review-queue/README.md) for semantics, canonical filenames, and validation.

```bash
# Empty or partially filled scaffold (no strict minimums for proposals/decisions/diffs):
python3 scripts/validate-change-review.py review-queue --allow-empty

# Proposals + diffs present, decisions/ still empty (pre-companion decision):
python3 scripts/validate-change-review.py review-queue --allow-missing-decisions
```

