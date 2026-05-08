# cici-ai Daily Journal

**Status:** WORK / beginner-facing journal system  
**Scope:** OB1 daily progress capture for cici-ai team members  
**Boundary:** This is a reusable operating pattern and guidance package. It does not imply ownership of any member's OB1 repo.

## Purpose

Give every team member the same lightweight daily journal routine so progress stays visible in GitHub without turning into a long report.

The system is designed for beginners:

- one standard file path
- one simple markdown template
- one semi-automated drafting prompt
- one human review step before commit

## Canonical journal path

Use this path inside each member's own OB1 repo:

`docs/personal/daily-journal/YYYY-MM-DD.md`

If the repo does not yet have `docs/personal/`, create it once and keep the same structure for everyone.

## What goes in the journal

- what you worked on
- what changed
- what is blocked
- what you plan to do next
- evidence links or notes

## What the workflow should feel like

1. Collect rough notes during the day.
2. Ask Claude to draft the journal from those notes.
3. Review the draft yourself.
4. Save the markdown file.
5. Commit and push to GitHub so the team can see it.

## Companion files

- [daily-journal-template.md](daily-journal-template.md)
- [daily-journal-prompt.md](daily-journal-prompt.md)
- [daily-journal-helper.md](daily-journal-helper.md)
- [scripts/cici_daily_journal_helper.py](../../../../scripts/cici_daily_journal_helper.py)

## Recommended use

For cici-ai team coordination, treat GitHub as the durable proof layer and the daily journal as the easiest place to record steady progress.

This package lives in `work-cici` as a shared reference. Each team member applies it in their own repo.

The journal should stay short, consistent, and easy to fill out every day.
