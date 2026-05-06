# Voice Benchmark Suite

Explicit benchmark harness for emulation quality. The system prompt carries many constraints: stay in character, respect the knowledge boundary, speak as a six-year-old, keep language simple, and never pretend. This suite measures **voice stability** and **boundary compliance** across model and prompt updates.

## Dimensions

| Dimension | What it measures |
|-----------|------------------|
| **Tone** | Stays in character; no AI disclosure or formal assistant voice when probed. |
| **Age realism** | Speaks as a six-year-old: simple words, short sentences (e.g. avg â‰¤20 words), no sophisticated vocabulary. |
| **Abstention** | On out-of-scope questions, says "I don't know" / "haven't learned that yet" / offers "do you want me to look it up?" instead of guessing. |
| **Bilingual** | Handles English and Chinese appropriately from the Record; stays in character when prompted in Chinese. |
| **Recall fidelity** | Answers from documented knowledge only; in-scope questions get substantive replies grounded in the Record. |
| **Overreach detection** | Does not claim knowledge or experiences not in the Record; does not over-offer "look it up?" after answering from Record. |

## Relation to other checks

- **Counterfactual Pack** (`run_counterfactual_harness.py`) â€” Adversarial knowledge-boundary and in-scope probes; shared abstain/answer/no-over-offer logic. Voice benchmark adds tone, age, and bilingual dimensions and a single place to run all emulation-quality dimensions.
- **Linguistic authenticity** (`test_voice_linguistic_authenticity.py`) â€” In-character prompts, forbidden phrases, readability, fingerprint markers. Voice benchmark reuses the same forbidden-phrase and vocabulary checks in a structured probe set.
- **Uniqueness** (`measure_uniqueness.py`) â€” Compares Grace-Mar vs generic baseline (abstention score, divergence, readability gap). Voice benchmark does not compare to baseline; it scores the Voice alone against expected behavior per dimension.

## How to run

```bash
# All probes (default)
python scripts/run_voice_benchmark.py

# One category
python scripts/run_voice_benchmark.py --category tone

# Single probe
python scripts/run_voice_benchmark.py --probe VB-TONE-001

# JSON output for CI or trending across runs
python scripts/run_voice_benchmark.py -o artifacts/voice_benchmark_results.json
```

Requires `OPENAI_API_KEY`; uses `OPENAI_MODEL` (default: gpt-4o).

## Probe set

Probes live in `scripts/voice_benchmark/probes.json`. Each probe has:

- `id` â€” e.g. VB-TONE-001
- `category` â€” tone, age_realism, abstention, bilingual, recall_fidelity, overreach
- `expected_behavior` â€” in_character, age_appropriate, abstain, answer, answer_no_lookup_offer, bilingual_ok
- `input` â€” user message sent to the Voice
- `notes` â€” short rationale

Add or edit probes there to extend coverage or tighten criteria.

## Success criteria

- **Pass:** All probes in the run pass their expected_behavior check.
- **Fail:** Any probe fails; exit code 1. Use `-o results.json` to inspect replies and reasons and to track regressions over time.

Run the suite after prompt or model changes to guard voice stability and boundary compliance; use with the counterfactual pack and linguistic authenticity tests for full coverage.

