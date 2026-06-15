from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from prose_slop_lint import lint_file, lint_text  # noqa: E402


def rule_ids(findings) -> set[str]:
    return {f.rule_id for f in findings}


# Golden strings from docs/essay-voice.md template slop section
BAD_LEDE = """# Test Essay

Leo names what no algorithm may inherit — moral judgment and pastoral witness. Barnes names who pays when finance and energy reorganize around an overstated product. Jiang names the end-state hidden inside the branding. This essay compares those three refusals.
"""

GOOD_REVISION = """# Test Essay

Artificial intelligence is scaling faster than anyone responsible for it. Pope Leo XIV treats that gap as a crisis of office: machines may assist judgment, but they cannot inherit the weight of moral witness Rome has carried for centuries. Robert Barnes reads the same moment as political economy — circular finance, Gulf energy, campaign money — and asks who still pays when the product is oversold. Jiang Xueqin hears occult branding and bailout theater, and asks what kind of person the system is training while elites pretend the mechanism is still "just tech." Three registers converge on one constraint: competence is not answerability.
"""

SET_PIECE_BLOCKQUOTE = """# Test Essay

Leo refuses delegation in plain prose here.

> Nor do they have a moral conscience, since they do not judge good and evil — grasp the ultimate meaning — or bear responsibility for consequences.

One closing sentence without em-dash symmetry in body paragraphs.
"""


def test_must_flag_bad_lede() -> None:
    findings = lint_text(BAD_LEDE)
    ids = rule_ids(findings)
    assert "SLOP-01" in ids
    assert "SLOP-04" in ids


def test_must_pass_good_revision() -> None:
    findings = lint_text(GOOD_REVISION)
    slop = {f.rule_id for f in findings if f.rule_id.startswith("SLOP-")}
    assert slop == set()


def test_must_flag_tri_mind() -> None:
    text = "# X\n\nThis is a tri-mind roundtable about AI.\n"
    findings = lint_text(text)
    assert "SLOP-08" in rule_ids(findings)


def test_must_pass_set_piece_blockquote() -> None:
    findings = lint_text(SET_PIECE_BLOCKQUOTE)
    assert "SLOP-02" not in rule_ids(findings)


def test_must_flag_legacy_meta_strict() -> None:
    path = REPO_ROOT / "essays/leo-barnes-jiang-on-ai.md"
    findings = lint_file(path, strict=True)
    assert "SLOP-04" in rule_ids(findings)


def test_must_pass_legacy_open_default_skip() -> None:
    path = REPO_ROOT / "essays/leo-barnes-jiang-on-ai.md"
    findings = lint_file(path, strict=False, diff_mode=False)
    assert findings == []


def test_legacy_opening_no_slop_01_when_strict() -> None:
    path = REPO_ROOT / "essays/leo-barnes-jiang-on-ai.md"
    findings = lint_file(path, strict=True)
    assert "SLOP-01" not in rule_ids(findings)


def test_rhetorical_question_closer_full_scan() -> None:
    text = "# Essay\n\nBody paragraph with a claim.\n\n## Falsifiers\n\nMaybe this fails?\n"
    findings = lint_text(text, opening_only=False, full=True)
    assert "SLOP-07" in rule_ids(findings)
