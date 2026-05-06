# Tree-Shaping Audit — 2026-05-06

## Purpose

Pause the YAML-compat and root-layout cleanup long enough to describe the current worktree in **commit-sized families**. The goal is to keep future cleanup slices clean instead of reabsorbing mixed churn.

## Current shape

Top dirty buckets from `git status --short` on 2026-05-06:

- `docs`: about 407 paths
- `users`: about 160 paths
- `codex`: about 136 paths
- `scripts`: about 129 paths
- `tests`: about 54 paths
- `.cursor`: about 25 paths
- `artifacts`: about 20 paths
- `research`: about 13 paths
- `src`: about 12 paths

The important read is that the tree is **not** one big blob. It is several overlapping migrations:

1. root-vs-users relocation
2. strategy/codex doctrine rewrite
3. runtime and operator script hardening
4. YAML dependency hardening
5. lane/raw-input/content growth

## Clean families already established

These families now have coherent commit history and should stay conceptually separate from later work:

- root-layout continuity and observability repairs
- runtime/operator `profile_dir(...)` normalization
- seed/gate/continuity helper normalization
- proposal/evidence tooling normalization
- optional dependency gracefulness for `orjson` and `PyYAML`
- shared `yaml_compat` rollout across:
  - bookshelf / gate
  - history notebook builders
  - runtime / MCP readers
  - portable skill helpers

This matters because the next passes should preserve those family boundaries instead of reopening them casually.

## Mixed-churn holdouts

Four files looked like likely next YAML candidates but are **not safe** for a clean compatibility-only commit right now:

- `scripts/strategy_watch.py`
- `scripts/strategy_expert_corpus.py`
- `scripts/mcp_risk_scan.py`
- `scripts/mcp_manifest_admission.py`

Why they are holdouts:

- they already contain unrelated local changes
- their diffs are not narrow dependency-only rewrites
- they mix runtime/path/prose/encoding churn with the YAML seam

Observed diff shape:

- `strategy_expert_corpus.py`: large structural and terminology churn
- `strategy_watch.py`: YAML seam plus broader local logic/content changes
- `mcp_risk_scan.py`: YAML seam mixed with existing path/policy edits
- `mcp_manifest_admission.py`: YAML seam mixed with existing malformed path-string replacements and encoding noise

Rule for these files:

- do not use them as “easy next commits”
- either disentangle them intentionally into a dedicated cleanup pass
- or leave them alone until their broader family is being worked

## Remaining YAML surface

A repo-wide search still shows a large remaining YAML caller population under `scripts/`.

High-level state:

- the **highest-leverage live CLI families** already touched are much healthier
- the remaining surface is now skewed toward:
  - content/build scripts
  - work-jiang corpus tooling
  - migration helpers
  - older one-off utilities

This means the next YAML work should be chosen by **family ownership**, not by random first-hit search results.

## Recommended next cleanup families

### 1. Validation and export utilities

Good candidate family because these scripts are usually narrow, CLI-shaped, and operator-facing.

Examples worth evaluating together:

- `scripts/build_strategy_observability.py`
- `scripts/ci_validation_inventory.py`
- `scripts/validate.py`
- nearby `validate_*` helpers not already touched

Why this family is attractive:

- low conceptual overlap with strategy doctrine churn
- clear operator payoff
- easier to verify with `--help` and clean error behavior

### 2. Work-Jiang corpus builders and validators

This is likely the largest remaining coherent YAML family.

Why it should be its own pass:

- many scripts share the same corpus assumptions
- they can probably share one internal pattern
- mixing them with general runtime cleanup would muddy both stories

Important caution:

- this family is valuable, but it is **not** a small wedge
- if touched, it should be framed explicitly as `work-jiang YAML tooling hardening`

### 3. Legacy one-off generators and migration helpers

These should be treated as lower-priority cleanup unless they are actively blocking work.

Why:

- many are not hot-path tools
- some may be better left alone until a real maintenance reason appears
- chasing them too early risks turning disciplined cleanup back into repo-wide churn

## Recommended operating rule after this audit

Use this triage rule before each cleanup slice:

1. Is the target set a coherent family with one story?
2. Can the family be verified with one compact test approach?
3. Is the family already mixed with unrelated local churn?

If the answer to 3 is yes, do **not** force it into a “small cleanup commit.”

## Residue triage rule

Not every dirty path is the same kind of residue.

Classify each remaining path into one of three buckets before you decide what to do with it:

- `keep and finish`: intentional in-flight work that still belongs to the active branch
- `park/archive`: legacy mirrors, temp worktrees, review queues, handoff artifacts, and other non-active residue
- `ignore as generated`: rebuildable outputs and snapshots that should not be treated as feature work

Practical rule:

- if it is intentional and testable, keep it in the active branch slice
- if it is useful but not active, park it
- if it is rebuildable, leave it out of the active slice and handle it as generated

This triage is what makes the tree-shaping plan safe: it protects useful work from being mistaken for clutter while still preventing parked residue from re-entering feature commits.

## Bottom line

The repo is in better shape than the raw dirty-tree size suggests:

- the live root-layout migration is largely stabilized
- the hottest YAML-dependent CLIs now fail gracefully
- the main danger has shifted from broken defaults to **mixed-churn recontamination**

So the next compounding move is no longer “patch whatever still imports YAML.”
It is:

- pick one clean family
- keep the story narrow
- leave mixed-churn holdouts isolated until they deserve their own pass
