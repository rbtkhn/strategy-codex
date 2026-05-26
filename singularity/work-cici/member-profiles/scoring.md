# cici-ai support scoring

This is the quantitative floor used by the member-profile audit.

## Threshold floor

- **Support floor:** `70 / 100`
- **Pass rule:** a member must score at least `70` to stay on the next-month payment track
- **Penalty rule:** unresolved handle mapping or weak public evidence reduces the score, even if the repo exists

## Scoring model

The review script scores four dimensions:

| Dimension | Max points | What it measures |
|---|---:|---|
| Evidence strength | 30 | Whether the profile shows confirmed GitHub activity at the A/B/C level |
| Recency | 30 | How recently the latest verified GitHub activity happened |
| Work substance | 20 | Whether the current status shows active build work rather than passive presence |
| Clarity | 20 | Whether the member mapping is clean and the support reason is explicit |

## Point table

### Evidence strength

- `A` = 30
- `B` = 20
- `C` = 10

### Recency

- `0 to 7 days` = 30
- `8 to 14 days` = 25
- `15 to 30 days` = 20
- `31 to 45 days` = 10
- `46+ days` or unknown = 0

### Work substance

- `Active builder-coordinator` = 20
- `Active builder` = 20
- `Active but mapping needs cleanup` = 15
- `Active` = 15
- `Quiet` = 0
- Other / unclear = 10

### Clarity

- Clean mapping and explicit support reason = 20
- Minor mapping ambiguity or partial cleanup note = 10
- Unresolved handle / unclear reason = 0

## Interpretation

- `70-100`: on track for next-month support
- `50-69`: borderline, needs stronger public evidence or clearer mapping
- `<50`: hold

## Use rule

The scoring floor is a decision aid, not a substitute for human review.
It exists to make the monthly review repeatable, visible, and consistent.
