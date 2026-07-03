# Skill surface naming contract - 2026-05-12

**Purpose:** Resolve the active naming contract for the repo's Record-bound skill surfaces and state the migration consequence, if any.

**Status:** Active steward decision for `strategy-codex`.

## Decision

This repo uses a **split contract**:

- **`self-skill-*`** is the **conceptual / doctrinal label family**
- **`skill-*.md`** is the **active concrete root filename family** for split skill files in this repo
- **`self-skills.md`** remains the canonical capability index

So, for `strategy-codex` today:

- **self-skill-think** = conceptual label
- [skill-think.md](../../../skill-think.md) = concrete root file

- **self-skill-write** = conceptual label
- [skill-write.md](../../../skill-write.md) = concrete root file

- **self-skill-steward** = conceptual label
- [skill-steward.md](../../../skill-steward.md) = concrete root file

## Rule

When writing doctrine, audits, taxonomy, or architecture prose:

- prefer **self-skill-think**
- prefer **self-skill-write**
- prefer **self-skill-steward**

When referring to actual current repo paths, scripts, tests, or file IO:

- use `skill-think.md`
- use `skill-write.md`
- use `skill-steward.md`

Do **not** create parallel root files named `self-skill-think.md`, `self-skill-write.md`, or `self-skill-steward.md` in this repo unless a deliberate migration decision is made first.

## Why this contract

This resolves two valid pressures without flattening them:

1. **Conceptual clarity**
   The `self-skill-*` labels keep the triad legible and prevent a purely modular reading of the companion self.

2. **Operational continuity**
   The current script and test stack still depends materially on `skill-think.md`, `skill-write.md`, and `skill-steward.md` as concrete filenames.

So the repo should not pretend it is already in a pure `self-skill-*.md` filename world.

## Migration consequence

There is **no immediate filename migration** implied by this decision.

Any future rename from `skill-*.md` to `self-skill-*.md` would require:

1. a script and test migration plan
2. path updates across exports, loaders, validators, and generated views
3. a deliberate compatibility story for old references
4. a follow-up steward decision that explicitly promotes the rename

Until then, the correct move is:

- **doctrine normalization**
- **not filename churn**

## Steward consequence

Future cleanup passes should treat:

- `self-skill-*` language as **conceptual precision**
- `skill-*.md` root filenames as **active repo mechanics**

The membrane failure to avoid is not “two names exist.”
It is “the repo silently implies that the conceptual name and the concrete filename are already the same thing.”

## Related

- [authority-ambiguity-vs-file-abundance.md](authority-ambiguity-vs-file-abundance.md)
- [duplicate-canonical-surfaces-audit-2026-05-12.md](dev-notebook/work-dev/duplicate-canonical-surfaces-audit-2026-05-12.md)
- [contract-wording-vs-filename-test-2026-05-12.md](contract-wording-vs-filename-test-2026-05-12.md)
- [canonical-paths.md](../../canonical-paths.md)
