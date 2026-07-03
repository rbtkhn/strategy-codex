# Abundance Pack for Cici AI

This is the Cici-facing wrapper for the portable `abundance-native-ventures` skill.

## Use it when

- You want venture ideas grounded in the Cici AI work.
- You want a one-afternoon sprint package that stays approval-first.
- You want a recursion-gate-ready proposal or skill-card draft.
- You want a daily or weekly operator brief that stays evidence-based.

## Lane routing

- **Telegram**: use for intake prompts, short announcements, and lightweight public-facing framing.
- **Core**: use for repo, prompt, and governed-state changes that would need approval in the Cici repo.
- **Progress**: use for proof packets, evidence pointers, and success/failure notes.

## Inputs

Read only the minimum needed from:

- `self.md`
- `self-library.md`
- `self-skills.md`
- `self-archive.md` / evidence surfaces
- `singularity/work-cici/README.md`
- `singularity/work-cici/cici-ai-lanes.md`

## Outputs

Keep the artifact small and copyable:

- idea list
- one-afternoon sprint plan
- gate-ready proposal skeleton
- skill card draft
- operator brief

## Boundary

This wrapper does not edit `self.md` directly and does not create a new `cici-ai` lane. It only helps route abundance-native work through the existing cici-ai lanes.
