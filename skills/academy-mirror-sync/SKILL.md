---
name: academy-mirror-sync
preferred_activation: academy-mirror-sync
description: "Verify academy mirror folders against their public remotes and the parent strategy-codex gitlink. Use when the user asks whether a mirrored repo folder such as public/ph-civ is in sync with its GitHub repo, origin/main, or parent submodule pointer."
portable: true
version: 0.1.0
tags:
  - operator
  - work-strategy
  - git
  - academy
---

# Academy Mirror Sync

Use this skill to verify that an academy mirror folder, its remote repository, and the parent `strategy-codex` pointer all agree.

## Default target

- Mirror folder: `public/ph-civ`
- Remote branch: `origin/main`
- Parent pointer: the gitlink recorded by `strategy-codex`

## Workflow

1. Run the deterministic check:

   ```powershell
   python scripts/check_academy_mirror_sync.py
   ```

2. If fetch is blocked by sandbox or credentials, rerun with the appropriate approval. If fetch remains unavailable, run:

   ```powershell
   python scripts/check_academy_mirror_sync.py --no-fetch
   ```

   Then state clearly that the comparison used the existing local `origin/main` ref.

3. Interpret the checks independently:
   - `status: synced`: fetch succeeded and all mirror checks agree.
   - `status: remote_unverified`: all local refs agree, but fetch failed; treat remote freshness as unverified.
   - `status: out_of_sync`: at least one mirror check failed.
   - `nested_clean`: the mirror folder itself has no dirty files.
   - `nested_matches_remote`: mirror HEAD equals fetched `origin/main`.
   - `parent_gitlink_matches_nested`: strategy-codex records the same commit as the mirror folder HEAD.
   - `parent_has_no_mirror_diff`: the parent worktree has no unstaged/staged diff for the mirror folder.

4. Report unrelated parent dirt separately. A dirty parent repo does not mean the academy mirror is out of sync unless the mirror path or gitlink is dirty.

## JSON mode

Use JSON when a later script or audit will consume the result:

```powershell
python scripts/check_academy_mirror_sync.py --json
```

## Guardrails

- Do not use `git submodule status`; it can fail on Windows if Git helper Unix tools are missing.
- Do not broad-stage parent changes during a sync check.
- Do not repair drift unless the user asks. This skill verifies and explains; update/push is a separate action.
