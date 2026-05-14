"""Unit tests for identity_library_boundary_rules (IX-A vs library boundary)."""

from pathlib import Path

from identity_library_boundary_rules import (
    collect_ix_a_topic_violations_from_block,
    collect_ix_a_violations_from_self_md,
    gate_suggested_reference_surface,
)

from validate_identity_library_boundary import collect_identity_library_violations


def test_gate_path_leak_triggers_without_long_text():
    text = "See docs/civilization-memory/essays/foo.md for the full argument."
    surf, reasons = gate_suggested_reference_surface(text, long_ref_threshold=500)
    assert surf == "CIV-MEM / SELF-LIBRARY"
    assert any("path" in r.lower() for r in reasons)


def test_gate_corpus_keyword_requires_length():
    short = "She mentioned CIV-MEM once."
    assert gate_suggested_reference_surface(short)[0] is None
    long = "She mentioned CIV-MEM once. " + "word " * 50
    surf, _ = gate_suggested_reference_surface(long)
    assert surf == "CIV-MEM / SELF-LIBRARY"


def test_ix_a_topic_path_leak_in_block():
    block = """
  - id: LEARN-0999
    topic: "Read docs/civilization-memory/notes/x.md for details"
"""
    viol = collect_ix_a_topic_violations_from_block(block, rel_path="x/self.md")
    assert len(viol) == 1
    assert "CIV-MEM/library path" in viol[0]


def test_ix_a_merge_preview_full_self():
    body = """# Self

### IX-A. Knowledge
- list
  - id: LEARN-0999
    topic: "okay short topic"

### IX-B. Curiosity
"""
    assert collect_ix_a_violations_from_self_md(body, rel_path="u/self.md") == []


def test_ix_a_topic_too_long():
    long_topic = "x" * 400
    block = f'  - id: LEARN-1\n    topic: "{long_topic}"\n'
    viol = collect_ix_a_topic_violations_from_block(block)
    assert len(viol) == 1
    assert "length" in viol[0]


def test_identity_library_boundary_prefers_self_knowledge_file():
    user_dir = Path(".codex-test-temp") / "identity-library-boundary" / "demo"
    user_dir.mkdir(parents=True, exist_ok=True)
    (user_dir / "self.md").write_text("# SELF\n", encoding="utf-8")
    (user_dir / "self-knowledge.md").write_text(
        """# SELF-KNOWLEDGE

### IX-A. KNOWLEDGE

```yaml
- id: LEARN-0001
  topic: "Read docs/civilization-memory/notes/x.md for details"
```
""",
        encoding="utf-8",
    )
    viol = collect_identity_library_violations(user_dir.resolve(), repo_root=Path.cwd())
    assert viol
    assert "self-knowledge.md" in viol[0]
