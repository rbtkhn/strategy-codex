# museum identity knowledge (archive) -> museum identity knowledge (archive) + self-identity migration (grace-mar)

Purpose: propagate the template split safely in the instance without risky direct rewrites of existing Record truth.

---

## Migration policy

- Do **not** bulk-move existing `self.md` IX entries by hand.
- Keep current Record stable.
- Introduce `self-identity.md` gradually through gated candidates and companion approval.

---

## Recommended rollout

1. **Contract first** (done): update protocol/path docs so split is recognized.
2. **Scaffold**: add `self-identity.md` only when companion approves activation for that instance.
3. **Gated reclassification**:
   - New identity-commitment signals stage to `self-identity.md` targets.
   - Knowledge facts continue to stage to museum knowledge section A / museum identity knowledge (archive).
4. **Optional backfill**:
   - Only move legacy lines if companion explicitly approves candidate-by-candidate migration.

---

## Classification rule of thumb

- Put in `museum identity knowledge (archive)`:
  - factual understanding, learned topics, observations
- Put in `self-identity`:
  - durable "who I am / who I am becoming"
  - non-negotiables and boundaries
  - role commitments and long-horizon identity direction

If uncertain, stage as a candidate and let review resolve destination.

---

## Safety

- No direct edits to `self.md` or evidence files outside the gated merge process.
- Preserve provenance/evidence linkage on any migrated or newly added identity entries.

