# cici-ai Member Profiles

This folder holds standardized member profiles for the cici-ai team.

Use the template for every member so the team can compare roles, obligations, and value in the same format.

## Standard form

- Identity and role
- Repo and evidence signals
- Team value
- Current obligations
- Support threshold
- Open loops and risks
- Next actions

## Files

- [template.md](template.md) - reusable form for any member
- [xavier.md](xavier.md) - Xavier's filled profile
- [nana-rpix.md](nana-rpix.md) - Hannah / Han nah profile
- [jhon-ell16.md](jhon-ell16.md) - Jhon Ell / Ell profile
- [adelle-sims.md](adelle-sims.md) - Kervy / Kekerv profile
- [salajosefinojr-sys.md](salajosefinojr-sys.md) - Jayr / Dismantle profile

## Use rule

Keep the profile factual, short, and evidence-based.
Update it when the member's GitHub activity or team role changes.

## Review automation

Use `python scripts/cici_support_review.py` to regenerate the support review table and the Telegram-ready payment-track message from these profiles.

The script is read-only. It does not change the profiles or make payment decisions by itself.

## Canonical snapshot

- [`support-review.md`](support-review.md) is the shared audit snapshot.
- Run `python scripts/cici_support_review.py --write` to refresh it from the profile files.
- Run `python scripts/cici_support_review.py --format telegram` to generate the matching Telegram summary.
- See [`scoring.md`](scoring.md) for the point-based threshold floor.
