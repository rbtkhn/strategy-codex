# Codex chat push auth boundary

**Status:** WORK-layer operator note. Not Record authority.

**Lesson:** A one-command agent workflow only stays trustworthy when local repo state, host identity, and remote authority remain visibly separate.

**Safety-story link:** This is the git version of [visible state, not chat-only reassurance](safety-story-ux.md): a commit hash, an SSH authentication result, and a remote push receipt answer different questions. Keep them separate so the operator is not asked to trust a smooth sentence where a receipt should be.

## Problem

`git commit` and `git push` look like one shipping action, but they cross different boundaries.

- `git commit` is local repo state. Codex can usually do it once the staged diff is intentional.
- `git push` crosses host identity and remote authorization. It depends on SSH config, keys, `known_hosts`, sandbox elevation, and GitHub permission.

Treat a push failure as host identity plumbing first, not as evidence that the repo commit is bad.

## Default rule

Codex may commit from chat when the operator asks and the staged diff is scoped.

Codex may push from chat when all of these are true:

- The operator explicitly asked to push.
- The branch/ahead count has been disclosed if pushing will publish earlier local commits too.
- SSH identity is explicit in `~/.ssh/config` or another durable auth path.
- Sandbox elevation is approved when home-directory SSH material is needed.

If those are not true, prefer: Codex commits, then the operator pushes from PowerShell.

## Durable SSH shape

For this workstation, `origin` uses SSH:

```text
git@github.com:rbtkhn/strategy-codex.git
```

The durable fix is explicit key selection in `C:\Users\rober\.ssh\config`:

```sshconfig
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_codex_predictive_history
  IdentitiesOnly yes
```

After that, this preflight should work from both PowerShell and chat-side elevated shell:

```powershell
ssh -T git@github.com
git -C C:\dev\strategy-codex push origin main
```

Expected success receipt for a no-op push:

```text
Everything up-to-date
```

## Receipts

- **Failure:** Non-elevated chat-side push could not use SSH home material (`known_hosts: Permission denied`) and unaided SSH did not offer an accepted key (`Permission denied (publickey)`).
- **Fix:** Add explicit key selection for `github.com` in `C:\Users\rober\.ssh\config`, then run chat-side push with approved elevation.
- **Proof:** On 2026-05-14, elevated `ssh -T git@github.com` authenticated as `rbtkhn` (GitHub exits nonzero because it does not provide a shell), and elevated `git -C C:\dev\strategy-codex push origin main` returned `Everything up-to-date`.

## Failure interpretation

| Failure | Meaning | Next move |
|---------|---------|-----------|
| `known_hosts: Permission denied` | Sandbox cannot read SSH trust material. | Retry with approved elevation. |
| `Permission denied (publickey)` | SSH did not offer an accepted key. | Check `~/.ssh/config` and GitHub SSH keys. |
| HTTPS `403` | Credential identity lacks repo push permission. | Use SSH or refresh GitHub credentials. |
| Branch is many commits ahead | Push would publish more than the current commit. | Disclose ahead count and get explicit approval. |

## Operator posture

Do not retry push loops blindly. Once the commit exists, preserve the distinction:

- Local completion: commit hash exists.
- Remote completion: `origin/<branch>` includes that hash.

The clean closeout names which one is true.
