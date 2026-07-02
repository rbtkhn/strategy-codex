"""Moonshots intelligence compiler — transcript to structured epistemic output."""

from __future__ import annotations

COMPILER_VERSION = "1.0.0"
MIN_EVIDENCE_WORDS = 30
MIN_BULLETS_STRICT = 10
MIN_MECHANISM_WORDS = 5
PROMPT_ID = "dual_layer_v1"
CAUSAL_CUES = (
    "because",
    "therefore",
    "thus",
    "drives",
    "leads",
    "causes",
    "when",
    "if",
    "so that",
    "results in",
    "enables",
    "forces",
    "depends",
)
