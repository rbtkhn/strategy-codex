# Handoff: Mercouris Raw-Input Check Stream

Runtime work layer only. This packet is not Record truth and does not stage or merge companion evidence. It exists to seed a new agent session devoted to the `check-streams` Mercouris raw-input backfill.

## Session Seed

Use the `check-streams` workflow. Continue the Alexander Mercouris raw-input check-stream run from the already completed February 2026 tranche. Default to checking backward one day at a time unless the operator names a different target date.

Primary task: verify or materialize canonical `codex/years/2026/raw-input/YYYY-MM-DD/` captures for Mercouris main uploads using operator-pasted transcript bodies when YouTube subtitle/materialization is blocked.

## Repo Anchors

- Workspace: `C:\dev\strategy-codex`
- Canonical workflow: `.cursor/skills/check-streams/SKILL.md`
- Legacy alias: `.cursor/skills/cognition-streams/SKILL.md`
- Canonical raw-input tree: `codex/years/2026/raw-input/YYYY-MM-DD/`
- Useful cached index: `.codex-tmp/youtube-alex-mercouris-index/CHANNEL-VIDEO-INDEX.md`

## Boundaries

- Do not edit Record surfaces: `self.md`, `self-archive.md`, `recursion-gate.md`, `session-log.md`, or `bot/prompt.py`.
- Raw-input capture is the task. Do not update speaker folders, lattice rows, memory, or Record material unless the operator explicitly asks.
- The worktree contains unrelated dirty files. Do not stage, commit, revert, or clean them.
- Use `apply_patch` for manual edits.
- Never claim a capture is done if the raw-input file is metadata-only, header-only, placeholder-only, or lacks a non-stub transcript body.

## Current State

Latest relevant pushed commit:

- `6ed7b8b3 Backfill Mercouris February transcripts`
- Pushed to `origin/main` on 2026-05-18.

The run materialized or reconciled Mercouris captures for 2026-02-21 through 2026-02-27. Online YouTube audit repeatedly timed out or returned a bot-wall style failure: `Sign in to confirm you're not a bot`. Treat that as expected. The reliable fallback has been local raw-input inspection plus the cached channel index.

There are unrelated unstaged changes elsewhere in the tree, including raw-input dates outside the completed Mercouris tranche. Inspect before touching any file, especially `2026-02-28` and `2026-03-01`, which already appear dirty.

## Completed Tranche

These dates were included in the pushed commit:

- 2026-02-21: `wnPHmF8rpq8` - `Putin Orders Medinsky Tough Line; Zelensky Meltdown Wants 3 Year War; Kiev Shocked; Orekhov Cauldron`
- 2026-02-22: `lroblskfwuQ` - `Zelensky Coup Fears; Kiev Crisis Restarts; Moscow Blames UK For Alexeyev Hit; Strikes Kiev; Blackout`
- 2026-02-23: `Y3rew0LRHU0` - `Iran Debacle; US Military/Intel Chiefs Doubt Success; Russia/NATO Naval War Looms; Votkinsk Flamingo`
- 2026-02-24: `9gLKfOdFOc4` - `Medvedev Wants Kiev; Moscow: UK France Plot Giving Kiev Nuke; Slaviansk; Trump Caine Row On Iran War`
- 2026-02-25: `0tqxM1yKn6s` - `Putin Says Kiev Plans Black Sea Pipeline Attack Gives West Nuclear Warning; Trump Speech Iran Strike`
- 2026-02-26: `yolLJMmeQrk` - `Kiev Fortifying Odessa As Zaporozhzhia Counter Attack Fails; Desperate Zelensky Wants Putin Meeting`
- 2026-02-27: `HQyttm7M-oE` - `US Iran Talks Fail; Embassies Evacuated Attack Imminent; Konstaninovka Defence Collapses; UK Crisis`

The 2026-02-27 item was reconciled across a Duran transcript-bearing file and a Mercouris metadata pointer:

- `codex/years/2026/raw-input/2026-02-27/duran-mercouris-us-iran-geneva-embassies-konstantinovka-uk-2026-02-27.md`
- `codex/years/2026/raw-input/2026-02-27/youtube-alex-mercouris-us-iran-talks-fail-embassies-evacuated-attack-imminent-konstaninovka-def-2026-02-27.md`

## Default Next Target

Unless the operator says otherwise, continue backward:

- `check-stream mercouris feb 20 2026`

If the operator asks to go forward instead, inspect `2026-02-28` and `2026-03-01` carefully because they already have unrelated dirty state in the working tree.

## Per-Date Procedure

1. Run the date-scoped audit, expecting possible timeout:

```powershell
python scripts/cognition_streams_audit.py --start YYYY-MM-DD --end YYYY-MM-DD --recent-start YYYY-MM-DD --channel alex-mercouris
```

2. If online discovery fails, use local fallback:

```powershell
Get-ChildItem -Path codex/years/2026/raw-input/YYYY-MM-DD -Force -ErrorAction SilentlyContinue | Select-Object Name,Length
rg -n "alex-mercouris|Mercouris|Alexander Mercouris|source_url|title:" codex/years/2026/raw-input/YYYY-MM-DD
rg -n "YYYY-MM-DD" .codex-tmp/youtube-alex-mercouris-index artifacts/cognition-streams -g "*.md" -g "*.json" -g "*.jsonl"
```

3. Open the candidate raw-input file and classify it:

- transcript-bearing: verify non-stub body and report done
- metadata-only: report exact title/source URL and ask for or wait for operator transcript paste
- absent: use cached index to identify title/video id, then create a canonical metadata scaffold only if the operator supplies or approves enough metadata

4. When the operator pastes a transcript, edit the existing metadata capture only:

- Update `source_note` to include `operator-supplied transcript body appended on 2026-05-18` (or the current date in a future session).
- Append a `## Transcript (operator paste)` section.
- Paste the transcript body exactly enough for provenance-safe raw-input; do not summarize it into the capture.

5. Verify the capture:

```powershell
rg -n "source_note|## Transcript \(operator paste\)|Good day|Have a very good day" <raw-input-file>
git diff --stat -- <raw-input-file>
Get-Content <raw-input-file> -TotalCount 22
```

6. Close with a concise receipt:

- raw-input path
- source URL / video id
- transcript marker line
- opening line and closing line found
- diff stat
- whether it is committed or not

## Commit Discipline

If the operator asks to commit and push:

1. Stage only the relevant Mercouris raw-input files for the tranche.
2. Verify the staged slice:

```powershell
git diff --cached --stat
git diff --cached --name-only
```

3. Use a narrow message, for example:

```powershell
git commit -m "Backfill Mercouris February transcripts"
```

4. Push:

```powershell
git push origin main
```

Push may need escalation because the credential helper can fail silently in the sandbox. Do not include unrelated dirty files in the commit.

## Useful Operator-Facing Line

Use this if starting a new session:

> I am continuing the Mercouris raw-input check-stream run. The pushed baseline is `6ed7b8b3`, covering 2026-02-21 through 2026-02-27. I will start with 2026-02-20 unless you name another date, and I will treat YouTube bot-wall failures as expected, falling back to local raw-input plus the cached channel index.
