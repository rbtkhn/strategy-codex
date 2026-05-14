"""Tests for primary-source bound bookshelf quiz receipts."""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
PY = sys.executable
CHECK = REPO / "scripts" / "check_gate_merge_readiness.py"
VALIDATE = REPO / "scripts" / "validate_bookshelf_quiz_anchors.py"
CATALOG = REPO / "docs" / "skill-work" / "work-strategy" / "history-notebook" / "research" / "bookshelf-catalog.yaml"
ANCHORS = REPO / "docs" / "skill-work" / "work-strategy" / "history-notebook" / "research" / "bookshelf-quiz-anchors.yaml"
TEST_TMP = REPO / ".codex-test-temp" / "bookshelf-quiz-binding"


SELF_FIXTURE = """# Self

## IX-A. KNOWLEDGE

#### Facts (LEARN-nnn)

```yaml
entries:
  - id: LEARN-0001
    date: 2026-01-01
    topic: "Existing"
    source: test
    provenance: human_approved

```

## IX-B. CURIOSITY

```yaml
entries:
```
"""


def _gate(candidate_yaml: str) -> str:
    return f"""# Gate

## Candidates

### CANDIDATE-9999 (test)

```yaml
{candidate_yaml.strip()}
```

## Processed
"""


def _run_check(candidate_yaml: str) -> subprocess.CompletedProcess[str]:
    TEST_TMP.mkdir(parents=True, exist_ok=True)
    self_path = TEST_TMP / "self.md"
    gate_path = TEST_TMP / "recursion-gate.md"
    self_path.write_text(SELF_FIXTURE, encoding="utf-8")
    gate_path.write_text(_gate(candidate_yaml), encoding="utf-8")
    return subprocess.run(
        [
            PY,
            str(CHECK),
            "--gate",
            str(gate_path),
            "--self",
            str(self_path),
            "--catalog",
            str(CATALOG),
            "--quiz-anchors",
            str(ANCHORS),
            "--strict",
        ],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )


VALID_CANDIDATE = """
status: pending
channel_key: operator:cursor:bookshelf-mcq-self-knowledge
proposal_class: SELF_KNOWLEDGE_ADD
source_binding_strength: strong
review_needed: false
shelf_refs: [HNSRC-0003]
quiz_receipt:
  source_kind: primary
  citation_label: "Thucydides, History of the Peloponnesian War"
  visible_prompt: "In Thucydides' account of the Melian Dialogue, what lesson is usually drawn?"
  stem_topic: "Melian Dialogue"
  selected_answer: "C - power asymmetry can override moral argument."
  correct_answer: "C - power asymmetry can override moral argument."
  validation_note: "Selected answer validates the claim."
  staged_claim: "Knows: the Melian Dialogue is a realist lesson about power asymmetry."
source_exchange:
  operator: |
    Primary source binding: Thucydides.
mind_category: knowledge
signal_type: operator_quiz_validated
summary: "IX-A: Melian Dialogue"
profile_target: IX-A. KNOWLEDGE
suggested_entry: "Knows: the Melian Dialogue is a realist lesson about power asymmetry."
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
"""


ADAMS_CANDIDATE = """
status: pending
channel_key: operator:cursor:bookshelf-mcq-self-knowledge
proposal_class: SELF_KNOWLEDGE_ADD
source: operator - bookshelf MCQ receipt
source_binding_strength: strong
review_needed: false
shelf_refs: [HNSRC-0269, HNSRC-0270]
quiz_receipt:
  source_kind: primary
  citation_label: "John Adams, Revolutionary Writings"
  visible_prompt: "Drawing on John Adams's revolutionary writings, which institutional design did he most strongly favor for a free republic?"
  stem_topic: "John Adams on mixed constitutional design"
  selected_answer: "C - a mixed constitution with bicameral legislature, executive, and independent judiciary."
  correct_answer: "C - a mixed constitution with bicameral legislature, executive, and independent judiciary."
  validation_note: "Companion selected the intended answer. Binding is strong to the Adams primary-source shelf anchor."
  staged_claim: "Knows: John Adams favored a mixed constitutional order with a bicameral legislature, executive, and independent judiciary."
source_exchange:
  operator: |
    Bookshelf quiz round on John Adams. Visible quiz prompt used academic prose and did not expose internal shelf ids.
    Source context: John Adams, Revolutionary Writings.
mind_category: knowledge
signal_type: operator_quiz_validated
summary: "IX-A: John Adams on mixed constitutional design"
profile_target: IX-A. KNOWLEDGE
suggested_entry: "Knows: John Adams favored a mixed constitutional order with a bicameral legislature, executive, and independent judiciary."
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
"""


def test_committed_quiz_anchors_validate() -> None:
    result = subprocess.run(
        [PY, str(VALIDATE), "--catalog", str(CATALOG), "--anchors", str(ANCHORS)],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr + result.stdout


def test_valid_primary_source_candidate_passes() -> None:
    result = _run_check(VALID_CANDIDATE)
    assert result.returncode == 0, result.stderr + result.stdout


def test_visible_prompt_must_not_leak_internal_hnsrc() -> None:
    bad = VALID_CANDIDATE.replace(
        "what lesson is usually drawn?",
        "what lesson is usually drawn from HNSRC-0003?",
    )
    result = _run_check(bad)
    assert result.returncode == 1
    assert "leaks internal source ids" in result.stdout


def test_unknown_shelf_ref_fails() -> None:
    bad = VALID_CANDIDATE.replace("HNSRC-0003", "HNSRC-9999")
    result = _run_check(bad)
    assert result.returncode == 1
    assert "unknown shelf_ref" in result.stdout


def test_weak_missing_shelf_refs_warns_but_passes() -> None:
    weak = VALID_CANDIDATE.replace("source_binding_strength: strong", "source_binding_strength: weak")
    weak = weak.replace("review_needed: false", "review_needed: true")
    weak = weak.replace("shelf_refs: [HNSRC-0003]", "shelf_refs: []")
    result = _run_check(weak)
    assert result.returncode == 0, result.stderr + result.stdout
    assert "missing shelf_refs" in result.stdout


def test_approval_receipt_prefers_full_quiz_receipt() -> None:
    import process_approved_candidates as pac

    receipt = pac._extract_approval_receipt(VALID_CANDIDATE)
    assert "quiz_receipt:" in receipt
    assert "selected_answer" in receipt
    assert "staged_claim" in receipt


def test_ix_a_merge_remains_prose_only() -> None:
    import process_approved_candidates as pac

    candidate = {
        "id": "CANDIDATE-9999",
        "block": VALID_CANDIDATE,
        "mind_category": "knowledge",
        "profile_target": "IX-A. KNOWLEDGE",
        "suggested_entry": "Knows: the Melian Dialogue is a realist lesson about power asymmetry.",
        "summary": "IX-A: Melian Dialogue",
        "prompt_section": "YOUR KNOWLEDGE",
        "prompt_addition": "none",
    }
    self_out, knowledge_out, _evidence_out, _prompt_out, _act_id, _entry_id = pac.merge_candidate_in_memory(
        candidate,
        SELF_FIXTURE,
        """# SELF-KNOWLEDGE

## IX-A. KNOWLEDGE

#### Facts (LEARN-nnn)

```yaml
entries:
```
""",
        """## V. ACTIVITY LOG

```yaml
entries:
```
""",
        "",
        "2026-05-02",
        3,
    )
    assert "shelf_refs:" not in self_out
    assert "quiz_receipt:" not in self_out
    assert "Knows: the Melian Dialogue" not in self_out
    assert "Knows: the Melian Dialogue" in knowledge_out


def test_john_adams_anchor_lookup_preflight_and_receipt_extraction() -> None:
    anchors_text = ANCHORS.read_text(encoding="utf-8")
    assert "id: bq-john-adams-revolutionary-writings" in anchors_text
    assert "source_kind: primary" in anchors_text
    assert "shelf_refs: [HNSRC-0269, HNSRC-0270]" in anchors_text

    result = _run_check(ADAMS_CANDIDATE)
    assert result.returncode == 0, result.stderr + result.stdout

    import process_approved_candidates as pac

    receipt = pac._extract_approval_receipt(ADAMS_CANDIDATE)
    assert "shelf_refs: [HNSRC-0269, HNSRC-0270]" in receipt
    assert "quiz_receipt:" in receipt
    assert 'citation_label: "John Adams, Revolutionary Writings"' in receipt
    assert "staged_claim:" in receipt


def test_bookshelf_receipt_checks_degrade_to_warning_without_pyyaml(monkeypatch) -> None:
    import check_gate_merge_readiness as cgr

    cgr = importlib.reload(cgr)
    monkeypatch.setattr(cgr, "has_yaml", lambda: False)
    blockers, warnings = cgr._receipt_binding_issues(
        "CANDIDATE-0060",
        {
            "shelf_refs": ["HNSRC-0269", "HNSRC-0270"],
            "quiz_receipt": {
                "source_kind": "primary",
                "citation_label": "John Adams, Revolutionary Writings",
                "stem_topic": "John Adams on mixed constitutional design",
                "selected_answer": "C",
                "correct_answer": "C",
                "validation_note": "validated",
                "staged_claim": "Knows: John Adams favored a mixed constitutional order.",
            },
        },
        catalog_ids={"HNSRC-0269", "HNSRC-0270"},
        anchor_refs={"HNSRC-0269", "HNSRC-0270"},
    )
    assert blockers == []
    assert any("PyYAML unavailable" in w for w in warnings)
