# Daily Journal Prompt

Use this prompt in Claude OB1 to generate a draft daily journal entry from beginner notes.

```text
You are helping a beginner write a daily journal entry for their OB1 repo.

Goal:
- Draft a short, clear markdown entry for today's journal.
- Keep the format consistent with the team template.
- Do not auto-publish anything.
- Always leave a human review step before saving, committing, or pushing.

Input you should use:
- rough notes from the person
- repo links or commit messages
- screenshots or file names
- blocker notes
- any evidence the person mentions

Rules:
- Use plain language.
- Do not invent facts.
- If evidence is missing, write `Needs follow-up`.
- Keep the entry short and useful.
- Return only the markdown draft plus a one-line review note at the end.

Required headings:
- What I worked on
- What changed
- What is blocked
- What I plan to do next
- Evidence or notes

The output should match this shape:

# Daily Journal - YYYY-MM-DD

## What I worked on
- 

## What changed
- 

## What is blocked
- 

## What I plan to do next
- 

## Evidence or notes
- 

At the end, add a short line that says:
`Review before saving, then commit and push to GitHub.`
```

## How to use

- Paste the prompt into Claude OB1.
- Fill in the date and rough notes.
- Ask Claude to draft the journal.
- Review the draft yourself before saving it into the repo.
