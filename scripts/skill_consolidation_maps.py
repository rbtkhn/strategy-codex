"""Shared category/status maps for skill consolidation (Commit 1–2)."""

from __future__ import annotations

CATEGORY_VALUES = frozenset({
    "truth-pipeline",
    "operator-coherence",
    "judgment-enhancement",
    "domain-pack",
    "product-narrative",
    "legacy-redirect",
})

STATUS_VALUES = frozenset({
    "active",
    "merged",
    "redirect",
    "draft",
    "archived",
    "deprecated",
})

_TRUTH = [
    "statecraft-source-intake", "source-clean", "transcript-cleanup",
    "transcript-proper-noun-normalization", "youtube-raw-input-transcript",
    "check-sources", "news-verify", "state-note", "state-synthesis",
    "packet-before-synthesis", "validator-first", "fact-check",
]
_OPERATOR = [
    "memory", "recursive-learn", "repo-hygiene-pass", "portable-skills-sync",
    "extract-skill-from-session", "repo-feedback-prompt", "dream", "bridge", "harvest",
]
_JUDGMENT = [
    "primary-overhearing-analysis", "statecraft-intelligence-essay",
    "tufte-data-viz", "singularity-monthly-synthesis", "singularity-note-promotion",
]
_DOMAIN = [
    "civ-state", "civ-state-note", "civ-state-essay",
    "politics-massie", "jurisdiction-campaign-history",
    "work-jiang-ingest-fallback", "state-america", "state-china", "state-persia", "state-russia",
    "state-deploy", "civ-state-volume-architect",
    "skill-cici", "skill-jiang", "skill-write", "weekly-brief-run", "work-jiang-feature-checklist",
    "anyang-ai", "brewmind-governed-steward", "hn-bookshelf-lookup", "statecraft-bridge",
    "statecraft-lane-intake-router", "speaker-shelf-hygiene", "speaker-structural-continuity",
    "speaker-relations-membrane", "skill-elicitation",
    "strategy-notebook-lane-split", "lane-survey", "pros-and-cons",
]
_PRODUCT = [
    "product-strategy", "first-wave-service-sales",
    "arc-to-chapter-seeds", "voice-profile-panel", "skill-narrative", "academy-mirror-sync",
    "ph-civ-comment-proof-objects", "ph-civ-orientation-harden", "ph-civ-to-civ-state-promoter",
    "predictive-history-chapter-spine", "civilization-part-writer", "empire-part-writer",
    "statecraft-guidebook-writer",
]
_REDIRECT = [
    "wire-verify", "check-streams", "cognition-streams",
    "strategy-notebook-expert-cross-weave", "strategy-notebook-guest-canon-note",
    "tri-mind", "conductor", "elicit-knowledge", "gate-review-pass", "thanks",
    "ideation-engine", "mtp", "abundance-native-ventures",
    "last30days", "monthly-deepening",
    "civ-state-primary-text-acquisition", "civ-state-volume-harden",
]

CATEGORY_MAP: dict[str, str] = {}
STATUS_MAP: dict[str, str] = {}
REPLACEMENT_MAP: dict[str, str] = {}
REVIEW_DATE_MAP: dict[str, str] = {}

for n in _TRUTH:
    CATEGORY_MAP[n] = "truth-pipeline"
    STATUS_MAP[n] = "active"
for n in _OPERATOR:
    CATEGORY_MAP[n] = "operator-coherence"
    STATUS_MAP[n] = "active"
for n in _JUDGMENT:
    CATEGORY_MAP[n] = "judgment-enhancement"
    STATUS_MAP[n] = "active"
for n in _DOMAIN:
    CATEGORY_MAP[n] = "domain-pack"
    STATUS_MAP[n] = "active"
for n in _PRODUCT:
    CATEGORY_MAP[n] = "product-narrative"
    STATUS_MAP[n] = "active"
for n in _REDIRECT:
    CATEGORY_MAP[n] = "legacy-redirect"
    STATUS_MAP[n] = "redirect"

REPLACEMENT_MAP.update({
    "wire-verify": "news-verify",
    "check-streams": "check-sources",
    "cognition-streams": "check-sources",
    "strategy-notebook-expert-cross-weave": "strategy-notebook-expert-cross-weave",
    "strategy-notebook-guest-canon-note": "strategy-notebook-guest-canon-note",
    "tri-mind": "periodic-statecraft-review",
    "conductor": "coffee",
    "elicit-knowledge": "fork-revive",
    "gate-review-pass": "fork-revive",
    "thanks": "archive",
    "civ-state-volume-architect": "civ-state",
    "ideation-engine": "product-strategy",
    "mtp": "product-strategy",
    "abundance-native-ventures": "product-strategy",
    "last30days": "periodic-statecraft-review",
    "monthly-deepening": "periodic-statecraft-review",
    "civ-state-primary-text-acquisition": "civ-state-primary-text",
    "civ-state-volume-harden": "civ-state-volume-hardening",
})

STATUS_MAP.update({
    "statecraft-framework": "archived",
    "statecraft-multi-lens": "archived",
    "statecraft-helix-synthesis": "archived",
    "last30days": "deprecated",
    "monthly-deepening": "deprecated",
    "civ-state-primary-text-acquisition": "deprecated",
    "civ-state-volume-harden": "deprecated",
    "america-art": "archived",
    "america-lit": "archived",
    "china-art": "archived",
    "china-lit": "archived",
    "iran-art": "archived",
    "iran-lit": "archived",
    "russia-art": "archived",
    "russia-god": "archived",
    "russia-lit": "archived",
})

CATEGORY_MAP.update({
    "last30days": "legacy-redirect",
    "monthly-deepening": "legacy-redirect",
    "civ-state-primary-text-acquisition": "legacy-redirect",
    "civ-state-volume-harden": "legacy-redirect",
})

REVIEW_DATE_MAP.update({
    "wire-verify": "2026-12-31",
    "check-streams": "2026-12-31",
    "cognition-streams": "2026-12-31",
    "strategy-notebook-expert-cross-weave": "2026-12-31",
    "strategy-notebook-guest-canon-note": "2026-12-31",
    "tri-mind": "2026-12-31",
    "conductor": "2026-12-31",
    "elicit-knowledge": "2026-12-31",
    "gate-review-pass": "2026-12-31",
    "thanks": "2026-12-31",
    "ideation-engine": "2026-12-31",
    "mtp": "2026-12-31",
    "abundance-native-ventures": "2026-12-31",
    "last30days": "2026-12-31",
    "monthly-deepening": "2026-12-31",
    "civ-state-primary-text-acquisition": "2026-12-31",
    "civ-state-volume-harden": "2026-12-31",
    "statecraft-framework": "2026-12-31",
    "statecraft-multi-lens": "2026-12-31",
    "statecraft-helix-synthesis": "2026-12-31",
    "america-art": "2026-12-31",
    "america-lit": "2026-12-31",
    "china-art": "2026-12-31",
    "china-lit": "2026-12-31",
    "iran-art": "2026-12-31",
    "iran-lit": "2026-12-31",
    "russia-art": "2026-12-31",
    "russia-god": "2026-12-31",
    "russia-lit": "2026-12-31",
})
