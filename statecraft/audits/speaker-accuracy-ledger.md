# Speaker Accuracy Ledger

WORK only; not Record.

This ledger tracks bounded claims and their later review status.

Question:

**When this speaker makes a bounded claim, how well does it survive later review?**

V1 is deliberately narrow. It does not try to score every utterance.

## Status Vocabulary

- `hit`
- `partial`
- `miss`
- `mistimed`
- `mechanism-right-outcome-wrong`
- `outcome-right-mechanism-wrong`
- `unresolved`
- `not-yet-scoreable`

## Claim Type Vocabulary

- `forecast`
- `timing call`
- `mechanism claim`
- `capability claim`
- `settlement claim`
- `institutional / political read`

## Testability Weight

- `high-testability`
- `medium-testability`
- `low-testability`

## Ledger

| speaker | claim id | claim date | source file | claim type | testability | claim summary | predicted or asserted outcome | review date | status | notes |
|---|---|---:|---|---|---|---|---|---:|---|---|
| `mercouris` | `MERC-A001` | 2026-01-11 | [2026-01-11 Mercouris](/C:/dev/strategy-codex/source-archive/statecraft/2026-01-11/youtube-alex-mercouris-russia-prepares-biggest-ukraine-strike-duma-wants-reserve-armies-committ-2026-01-11.md) | timing call | high-testability | He says he had predicted a major event before the end of 2025. | Event would occur before the end of 2025. | 2026-05-27 | `mistimed` | He explicitly says the timetable was wrong while defending the broader underlying read. |
| `mercouris` | `MERC-A002` | 2026-01-24 | [2026-01-24 Mercouris](/C:/dev/strategy-codex/source-archive/statecraft/2026-01-24/youtube-alex-mercouris-russia-hits-kiev-biggest-strike-as-us-military-joins-us-russia-ukraine-t-2026-01-24.md) | institutional / political read | high-testability | He had identified the wrong head of the Ukrainian delegation. | Delegation headed by Budanov rather than Umerov. | 2026-05-27 | `miss` | Fast factual correction on record; useful as a credibility signal even though the original claim was wrong. |
| `mercouris` | `MERC-A003` | 2026-03-21 | [2026-03-21 Mercouris](/C:/dev/strategy-codex/source-archive/statecraft/2026-03-21/youtube-alex-mercouris-iran-strikes-diego-garcia-putin-tells-iran-russia-loyal-ally-reports-ira-2026-03-21.md) | capability claim | high-testability | He overestimated the size of the U.S. assault force implied by carrier deployment. | Assault force might number about 3,000 troops. | 2026-05-27 | `miss` | He explicitly attributes the error to a misreading of the deployment signal. |
| `ritter` | `RITT-A001` | 2026-03-11 | [2026-03-11 Ritter](/C:/dev/strategy-codex/source-archive/statecraft/2026-03-11/transcript-dialogue-works-scott-ritter-the-u-s-has-lost-and-is-trapped-in-the-iran-war-with-no-way-2026-03-11.md) | capability claim | high-testability | Prior targeting judgment treated a site as command and control rather than a civilian shelter. | The target was a legitimate military command site. | 2026-05-27 | `miss` | Important because Ritter openly records the mistake and its moral burden. |
| `ritter` | `RITT-A002` | 2026-05-14 | [2026-05-14 Ritter](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-14/youtube-daniel-davis-deep-dive-scott-ritter-russia-retaliation-on-europe-no-longer-in-doubt-2026-05-14.md) | institutional / political read | medium-testability | He says he initially read the opening of the Russia-Ukraine war as a full military invasion. | Russia was going in for the kill rather than a special military operation. | 2026-05-27 | `miss` | Retrospective correction; the later broader war outcome does not erase the initial read being wrong. |
| `ritter` | `RITT-A003` | 2026-05-20 | [2026-05-20 Ritter](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-20/youtube-ritter-dialogue-works-trump-s-iran-attack-is-a-trap-that-leads-to-huge-humiliation-2026-05-20.md) | institutional / political read | high-testability | He had said Xi Jinping would meet Putin at the airport. | Airport greeting would be led by Xi rather than the foreign minister. | 2026-05-27 | `miss` | Small factual miss; useful for tracking willingness to correct minor details. |
| `mearsheimer` | `MEAR-A001` | 2025-08-01 | [2025-08-01 Mearsheimer](/C:/dev/strategy-codex/source-archive/statecraft/2025-08-01/transcript-diesen-mearsheimer-liberal-delusions-and-how-nato-led-ukraine-down-the-primrose-path-2025-08-01.md) | institutional / political read | medium-testability | In the 1990s it looked like liberal hegemony might work better than he expected. | Early post-Cold War evidence suggested his warning might be wrong. | 2026-05-27 | `partial` | He treats this as a temporary contrary signal, not a full disproof of the deeper model. |
| `mearsheimer` | `MEAR-A002` | 2025-08-01 | [2025-08-01 Mearsheimer](/C:/dev/strategy-codex/source-archive/statecraft/2025-08-01/transcript-diesen-mearsheimer-liberal-delusions-and-how-nato-led-ukraine-down-the-primrose-path-2025-08-01.md) | settlement claim | high-testability | The West could not force NATO expansion into Ukraine down Russia's throat. | Russia would not accept Ukrainian NATO entry and the project would crash into war. | 2026-05-27 | `hit` | This is a strong scoreable strategic claim with later confirmation inside the corpus. |
| `mearsheimer` | `MEAR-A003` | 2025-05-29 | [2025-05-29 Mearsheimer x Mercouris x Diesen](/C:/dev/strategy-codex/source-archive/statecraft/2025-05-29/transcript-diesen-mearsheimer-mercouris-russia-won-the-war-2025-05-29.md) | institutional / political read | low-testability | Greater Europe will remain intensely hostile with ever-present flashpoints. | Hostile and unstable postwar Europe rather than quick normalization. | 2026-05-27 | `unresolved` | Strong strategic read, but the review window is still too early to close it cleanly. |
| `freeman` | `FREE-A001` | 2025-08-15 | [2025-08-15 Freeman x Parsi](/C:/dev/strategy-codex/source-archive/statecraft/2025-08-15/transcript-dialogue-works-amb-chas-freeman-and-trita-parsi-the-next-israel-iran-war-is-coming-2025-08-15.md) | settlement claim | medium-testability | Ceasefire-plus-property-swaps talk will not solve the underlying issue. | A shallow ceasefire frame will fail without broader reassurance and settlement architecture. | 2026-05-27 | `unresolved` | Strong mechanism claim; still not cleanly closed by the current review window. |
| `freeman` | `FREE-A002` | 2025-08-15 | [2025-08-15 Freeman x Parsi](/C:/dev/strategy-codex/source-archive/statecraft/2025-08-15/transcript-dialogue-works-amb-chas-freeman-and-trita-parsi-the-next-israel-iran-war-is-coming-2025-08-15.md) | forecast | low-testability | He hopes he is wrong, but predicts more mass slaughter if the no-rules posture continues. | Further large-scale civilian killing if current logic continues. | 2026-05-27 | `unresolved` | Morally weighty but still too broad and open-ended for a stronger score. |
| `freeman` | `FREE-A003` | 2026-04-21 | [2026-04-21 Freeman theme anchor](/C:/dev/strategy-codex/codex/speakers/freeman/themes/bombing-is-not-political-success.md) | mechanism claim | medium-testability | Bombing does not itself produce durable political leverage or settlement. | Coercive destruction without architecture will not yield stable political success. | 2026-05-27 | `partial` | Mechanism is strongly evidenced, but the claim is broad enough that final closure depends on multiple cases, not one event. |
| `macgregor` | `MACG-A001` | 2026-02-10 | [2026-02-10 Macgregor](/C:/dev/strategy-codex/source-archive/statecraft/2026-02-10/transcript-napolitano-macgregor-us-iran-war-could-spiral-out-of-control-2026-02-10.md) | institutional / political read | medium-testability | Prior assumption that negotiations would prevent attack had been wrong. | Ongoing negotiations would deter direct attack. | 2026-05-27 | `miss` | Retrospective correction of a failed assumption. |
| `macgregor` | `MACG-A002` | 2026-03-10 | [2026-03-10 Macgregor](/C:/dev/strategy-codex/source-archive/statecraft/2026-03-10/transcript-davis-macgregor-no-the-iran-war-is-not-over-2026-03-10.md) | capability claim | medium-testability | Offensive posture will not work in the new precision-guided war paradigm. | U.S. or allied offensive schemes will fail against current defensive realities. | 2026-05-27 | `unresolved` | Force-model strong; still too early for clean closure across the whole claim. |
| `macgregor` | `MACG-A003` | 2026-04-21 | [2026-04-21 Macgregor](/C:/dev/strategy-codex/source-archive/statecraft/2026-04-21/transcript-macgregor-diesen-total-war-iran-2026-04-21.md) | institutional / political read | low-testability | Europe will face energy crisis and political upheaval as the war logic continues. | Current European governments will not be able to master the resulting crisis. | 2026-05-27 | `unresolved` | High-consequence but still too open to close in v1. |
| `wilkerson` | `WILK-A001` | 2025-06-22 | [2025-06-22 Wilkerson x Freeman x Parsi](/C:/dev/strategy-codex/source-archive/statecraft/2025-06-22/transcript-dialogue-works-col-larry-wilkerson-amb-chas-freeman-and-trita-parsi-the-us-could-face-a-war-it-can-t-win-2025-06-22.md) | capability claim | medium-testability | The U.S. could face a war it cannot win if it enters deeply in Iran. | Escalation would exceed sustainable military and fiscal carrying capacity. | 2026-05-27 | `unresolved` | Strong warning claim, but the ledger needs more downstream closure before scoring harder. |
| `wilkerson` | `WILK-A002` | 2025-06-22 | [2025-06-22 Wilkerson x Freeman x Parsi](/C:/dev/strategy-codex/source-archive/statecraft/2025-06-22/transcript-dialogue-works-col-larry-wilkerson-amb-chas-freeman-and-trita-parsi-the-us-could-face-a-war-it-can-t-win-2025-06-22.md) | institutional / political read | low-testability | This kind of war would be part of the unraveling of the empire. | Large-scale Southwest Asia escalation would accelerate imperial decline. | 2026-05-27 | `unresolved` | Core Wilkerson thesis, but too macro and longitudinal for rapid closure. |
| `wilkerson` | `WILK-A003` | 2025-06-22 | [2025-06-22 Wilkerson x Freeman x Parsi](/C:/dev/strategy-codex/source-archive/statecraft/2025-06-22/transcript-dialogue-works-col-larry-wilkerson-amb-chas-freeman-and-trita-parsi-the-us-could-face-a-war-it-can-t-win-2025-06-22.md) | capability claim | medium-testability | Mounting Iran directly with ground forces would be strategically absurd and likely disastrous. | Ground-war pathway would resemble a major strategic blunder rather than a clean solution. | 2026-05-27 | `partial` | Mechanism and military logic are strong, but no direct execution has occurred to produce a clean hit/miss closure. |

## Boundary

- This ledger is not a speaker-wide percentage table.
- A speaker can have strong credibility and several unresolved accuracy rows at the same time.
- Broad civilizational or imperial claims will often remain `unresolved` longer than factual or timing claims.
