# Codex Rehome Submodule Playbook

This note covers local clone repair for the `codex/academy/ph-civ` submodule after hoisting academy out of `codex/years/2026/`.

Tracked state after the migration:

- `.gitmodules` section: `[submodule "codex/academy/ph-civ"]`
- `.gitmodules` path: `codex/academy/ph-civ`
- submodule URL: `https://github.com/rbtkhn/ph-civ.git`

## Standard repair

```powershell
git submodule sync -- codex/academy/ph-civ
git submodule update --init -- codex/academy/ph-civ
```

If `git submodule status` fails on Windows because Git's Unix helper tools are missing from PATH, use direct checks instead:

```powershell
git ls-files -s codex/academy/ph-civ .gitmodules
git -c safe.directory=C:/dev/strategy-codex/codex/academy/ph-civ -C codex/academy/ph-civ rev-parse HEAD
git -c safe.directory=C:/dev/strategy-codex/codex/academy/ph-civ -C codex/academy/ph-civ remote -v
```

## `.git-local` split-gitdir repair

Some local clones store submodule gitdirs under `.git-local/modules/...`. If the old path still exists after the move, relocate it and update the worktree pointer:

```powershell
New-Item -ItemType Directory -Force .git-local/modules/codex/academy | Out-Null
Move-Item .git-local/modules/codex/years/2026/academy/ph-civ .git-local/modules/codex/academy/ph-civ
Set-Content codex/academy/ph-civ/.git "gitdir: ../../../.git-local/modules/codex/academy/ph-civ"
git config --file .git-local/modules/codex/academy/ph-civ/config core.worktree ../../../../../codex/academy/ph-civ
git submodule sync -- codex/academy/ph-civ
```

Do not commit `.git-local`; it is local clone metadata only.
