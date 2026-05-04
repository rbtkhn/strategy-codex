---
name: bridge
preferred_activation: bridge
requires: [handoff-check]
description: "Session-scale handoff ritual for the current workspace. Primary trigger: bridge. Before Step 1, synthesize the previous four cadence events into Recent rhythm prose. Assess the current repo first, recommend whether it needs commit/push, seal the agreed scope, and generate a structured transfer prompt for a fresh session or thread. In strategy-codex, bridge is codex-only by default and must stay current-workspace unless the operator explicitly broadens scope."
---

# Bridge

**Preferred activation (operator):** say the exact phrase **`bridge`**. **Aliases:** **`session handoff`**, **`close session`**, **`transfer`**.

`bridge` is the session-scale handoff. In this workspace it is **current-repo-first**: assess the active repo, recommend whether it needs commit/push, seal the agreed scope, and synthesize state into a single structured markdown block for the next fresh session or thread.

**Workspace rule for strategy-codex:** treat this workspace as **exclusively strategy-codex work**. Do **not** inspect, summarize, recommend, or mention sibling repos unless the operator explicitly broadens scope.

Its purpose is **high-fidelity context transfer** across boundaries where continuity becomes non-guaranteed: a fresh session, a new thread, cross-agent handoff, or a compaction boundary. A good bridge means the next session starts oriented instead of reconstructing what happened from residue.

`coffee` may resume from the latest authoritative checkpoint, but `bridge` remains the explicit seal-and-transfer ritual. `coffee` recovers orientation from on-disk checkpoint state; `bridge` commits, pushes when needed, and produces the carry-forward packet.

## When to use

| Scenario | Path | Why |
|----------|------|-----|
| **End of day + closing session** | `dream` then `bridge` | Dream settles continuity; bridge seals the repo and generates the transfer prompt |
| **End of day, keeping session** | `dream` alone | Maintenance pass; same thread continues tomorrow |
| **Mid-day, closing session** | `bridge` alone | Seal repo, carry context forward; no maintenance needed |
| **Quick check before stepping away** | **`coffee`** + signing-off intent | Lightweight status; no commit/push, no transfer prompt |

**Default:** If in doubt, `bridge`. It surfaces the current repo recommendation, then commits and pushes per scope, and produces a transfer prompt. If it's also end of day, run `dream` first.

This is event-driven: the operator says `bridge` when they're ready. There is no scheduled cadence.

---

## Step 0 — Recent rhythm

1. Open **`docs/skill-work/work-cadence/work-cadence-events.md`**.
2. Take the **last 4** event lines already in the file. If fewer than four exist, use what exists; if none, say **Recent rhythm:** _(no prior events)_.
3. Synthesize them using the cadence voice principle:
   - acknowledge what we settled or clarified
   - project the best next direction
   - use **"we"** framing
   - no timestamps, commit hashes, or process jargon in the prose
4. Put **Recent rhythm:** at the top of the first bridge reply.

If the file is missing or empty below the anchor, note that and continue.

---

## Step 1 — Read on-disk state

When the operator says `bridge`, read the following files if they exist:

1. **`docs/skill-work/work-cadence/work-cadence-events.md`** — recent cadence rhythm
2. **`docs/skill-work/work-coffee/work-coffee-history.md`** — recent coffee lane activity
3. **`docs/skill-work/work-dream/work-dream-history.md`** — recent dream lane activity
4. **`docs/skill-work/work-strategy/`** surfaces that clearly anchored the session, if relevant
5. **`docs/skill-work/work-dev/work-dev-history.md`** — recent dev activity, if relevant
6. **`docs/skill-work/work-politics/work-politics-history.md`** — recent politics activity, if relevant
7. **Workspace-local bridge/handoff artifacts** if the repo has them

Also run:

8. **`git status -sb`** — current repo worktree state
9. **`git log --oneline -10`** — recent commits
10. **`git diff --stat`** — current scope/shape of local changes

**Do not** reach into sibling repos or foreign workspace state unless the operator explicitly expands scope.

---

## Step 2 — Push/sync assessment

When the operator says **`bridge`**, assume **the current repo only** unless they explicitly name more scope.

Gather:

- `git status -sb` (dirty? branch? ahead/behind?)
- whether `origin` exists and whether `HEAD` is ahead of `@{u}`

### Worktree risk preflight

Classify the current repo from `git status -sb` and `git diff --stat`:

| Class | Meaning |
|-------|---------|
| **safe** | Clean worktree or trivial residue |
| **inspect** | Light/moderate residue; manageable but review before sealing |
| **conflict-prone** | Unmerged paths, conflicts, or very large/wide change set |

Emit one line, e.g. `Worktree risk (strategy-codex): inspect — review diff before sealing.`

If the repo is **conflict-prone**, pause and ask before committing.

Then output a short **Push/sync recommendation** block:

| Repo | Dirty? | Unpushed commits? | Recommendation |
|------|--------|-------------------|----------------|
| current repo | … | … | push after seal / already clean — nothing to push / pull first |

**Default recommendation:** seal the current repo if it is dirty or ahead. If it is clean and not ahead, say so clearly.

**Ask the operator** only when:

- the repo is behind origin
- there are conflicts
- there is no upstream
- the session obviously touched another repo and the operator may want to include it

If the operator explicitly widens scope, list each extra repo with path + role and assess them separately. Otherwise stay current-repo-only.

---

## Step 3 — Commit and push

Seal the session by committing and pushing **the agreed current-repo scope**.

### Bucket 1: Runtime residue

If the repo has clearly runtime/generated residue that is safe to isolate, commit it separately.

Commit message:

`chore: bridge session residue [YYYY-MM-DD]`

### Bucket 2: Substantive work

Any remaining dirty files are real work:

1. Run `git diff --stat`
2. Draft a concise summary commit message
3. Commit and report what was included

Then push:

```bash
git push
```

If push fails because the remote moved, pull-rebase first, then push. If there are conflicts, stop and report — do not force-push.

After push, run `git status -sb` to confirm clean state for the sealed scope.

If the repo uses cadence event logging for bridge, append that event after a successful push. Keep it repo-local.

---

## Step 4 — Generate the transfer prompt

Now synthesize the readings from Step 1 into a single markdown block using the canonical contract in `docs/skill-work/work-cadence/bridge-packet-contract.md`.

Required shape:

```markdown
# Session Bridge — [YYYY-MM-DD]

## Session Arc

## Session Output

## Carry-forward from last dream

## Active territories

## Repo status

## Since last bridge

## Open loops

## Agent surface

## Model transition note

coffee
```

**Notes for strategy-codex bridge packets**

- Replace any legacy instance-specific sections with repo-local ones.
- If there is no local dream/handoff artifact, say so plainly.
- If there is no gate-equivalent surface relevant to the session, omit it rather than inventing one.
- `## Repo status` should describe the current repo first.
- `## Since last bridge` can compare against the last visible bridge packet or prior sealed state when available; if not, say no prior bridge delta available.
- The final line must be exactly **`coffee`**, alone on its line.

Output the entire block so the operator can copy it.

---

## Step 5 — Done

Bridge is complete when:

- the agreed repo scope is sealed or explicitly skipped
- the transfer prompt is generated
- the current repo status after seal is reported honestly

---

## Guardrails

- **Current repo first.** In this workspace, bridge is `strategy-codex`-scoped by default.
- **No implicit cross-repo references.** Do not mention sibling repos or their files unless the operator explicitly broadens scope.
- **No gate action.** Report queue/state only if the current repo has an equivalent and it mattered to the session; do not approve or merge anything.
- **Signal over volume.** Keep the packet concise and actually useful.
- **Narrative arc matters.** `Session Arc` should explain what happened, not just list files.
- **Stop on conflict.** If push/rebase conflicts appear, stop and report.

## Related files

- `docs/skill-work/work-cadence/README.md`
- `docs/skill-work/work-cadence/bridge-packet-contract.md`
- `.cursor/skills/coffee/SKILL.md`
- `.cursor/skills/dream/SKILL.md`
