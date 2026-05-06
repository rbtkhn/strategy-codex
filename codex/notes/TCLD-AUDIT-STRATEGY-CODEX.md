# T-C-L-D audit for strategy-codex
<!-- word_count: 760 -->

WORK only; not Record.

**Purpose:** Apply the **Theater / Commodity / On-the-Line / Durable** audit to strategy-codex so the notebook compounds **judgment**, not just archive volume or operator reassurance.

## Core claim

The critique is directionally correct:

- Much strategy labor that feels sophisticated is actually **Theater** or **Commodity**.
- A large share of **On-the-Line** work is drifting toward Commodity as models get better at synthesis, retrieval, formatting, and standard framework output.
- The durable core is smaller than most strategists prefer to admit.

For this repo, the practical question is not whether the notebook stores impressive material. The question is whether it improves **non-obvious judgment under uncertainty**.

**Test:** If strategy-codex disappeared, would the operator lose mainly **formatting / coordination / research throughput**, or would they lose **better framing, better bets, better warnings, and better consequence-tracking**?

If the answer is mostly the first, the system is overweight on **T + C**.

## The repo split

Use the notebook layers deliberately:

- **`raw-input/`**
  - compresses **Commodity** capture and retention
  - preserves literal source text so the operator does not waste judgment time re-finding or re-pasting words
  - should not pretend to be judgment

- **`codex-page`**
  - compresses the best parts of **On-the-Line**
  - turns messy source material into reusable evidence surfaces with curated `### Verbatim`
  - should reduce rereading cost and improve citation quality
  - should not become decorative mini-essays that merely sound strategic

- **`strategy-page`** in thread files
  - is where the notebook should spend its scarce **Durable** energy
  - reframing, tension-holding, analogy choice, contested interpretation, prediction, and explicit bets belong here
  - if this layer becomes a polished recap of sources, the notebook is drifting backward into **L -> C**

- **`days.md`**
  - is the continuity and consequence layer
  - it should show what changed, what still seems true, what is unresolved, and what needs to be checked later
  - this is where judgment compounds across time instead of resetting each session

## What counts as durable here

Inside strategy-codex, **Durable** usually looks like:

- spotting that the stated question is wrong or too shallow
- naming the seam between surface events and the real strategic driver
- choosing between competing analogies rather than lazily stacking them
- distinguishing signal from operator anxiety
- making a call despite incomplete evidence and marking the uncertainty honestly
- noticing when an elegant thesis will break on contact with institutions, incentives, or execution
- revisiting old calls against outcomes and updating taste

The repo should help with these moves. It should not mainly produce more elegant containers for standard synthesis.

## Failure modes

The main failure mode is **theater multiplication**:

- more transcripts
- more pages
- more impressive structure
- more derived views
- more workflow vocabulary
- but no sharper decisions

Common warning signs:

- `codex-page` volume grows faster than reusable judgment
- `strategy-page` blocks mostly mirror source order or inbox order
- `days.md` records activity but not changed conviction
- old pages are accumulated but not revisited against reality
- the operator cannot point to specific calls that became better because the notebook existed

## Design rule

**Compress T and C aggressively so D has room to happen.**

That means:

- automate capture, backfill, indexing, and first-pass synthesis without guilt
- shorten or eliminate rituals that do not change decisions
- prefer evidence surfaces that reduce rereading over documents that simulate depth
- keep the center of gravity on judgment with consequences

The notebook is strongest when it acts as a **judgment compounding machine**:

1. capture the source material cheaply
2. extract the few passages worth keeping near the operator
3. write the contested interpretation explicitly
4. make or refine a bet
5. revisit the call later
6. let that outcome update future taste

Without steps 4-6, the repo is at risk of becoming a high-status research warehouse.

Derived revisit surfacing reduces the notebook's own thin-ice exposure because it makes old calls visible again at the moment they are most likely to matter. Instead of rewarding archive accumulation alone, the system starts rewarding consequence-tracking, falsification visibility, and cross-stream tension handling. That moves the notebook away from passive strategic theater and closer to a live judgment instrument.

## Operational implications

- **`raw-input/` success:** lower friction, higher fidelity, less duplicated search labor
- **`codex-page` success:** better evidence retrieval and cleaner quote discipline
- **`strategy-page` success:** clearer contested claims, stronger reframes, sharper predictions
- **`days.md` success:** visible continuity of judgment, not just a diary of ingestion

When choosing work, prefer changes that increase **durable judgment yield per unit of attention**, not just notebook completeness.

## Operator checks

Use these checks periodically:

- Did a recent `strategy-page` change a real framing, or just summarize inputs well?
- What judgment call from the last month was genuinely non-obvious?
- Which page or day block produced a better warning, avoidance move, or conviction line?
- Where is the notebook still serving anxiety-management rather than decision quality?
- Which repeated tasks should be pushed down into scripts, agents, or templates next?

## Short verdict

The critique is not a verdict against strategy-codex. It is a warning about what this repo could become if left ungoverned.

Used badly, the notebook amplifies **Theater**.

Used well, it compresses **Commodity**, disciplines **On-the-Line** work, and protects more time and attention for the small but decisive **Durable** core.

**Canonical implementation surface:** the notebook's lightweight judgment loop lives in [strategy-codex-template-page.md](../strategy-codex-template-page.md), [NOTEBOOK-CONTRACT.md](../NOTEBOOK-CONTRACT.md), and [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../STRATEGY-NOTEBOOK-ARCHITECTURE.md).
