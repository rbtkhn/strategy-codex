from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

def test_strategy_page_scaffold_prefers_standalone_stream_path(tmp_path: Path) -> None:
    strategy_page = load_module(REPO_ROOT / "scripts" / "strategy_page.py", "strategy_page_script")

    path = strategy_page.page_path_for_stream(
        tmp_path / "codex",
        "pape",
        "2026-05-09",
        "escalation-trap",
        explicit_id=True,
    )

    assert path == tmp_path / "codex" / "2026" / "pape" / "pape-page-2026-05-09-escalation-trap.md"

def test_strategy_page_scaffold_uses_public_signal_judgment_prediction() -> None:
    strategy_page = load_module(REPO_ROOT / "scripts" / "strategy_page.py", "strategy_page_script_public")

    text = strategy_page.build_strategy_page_document(
        stream_id="pape",
        page_date="2026-05-09",
        page_id="escalation-trap",
        watch="hormuz",
        streams=["pape"],
        inbox_lines=[],
    )

    assert "### Signal" in text
    assert "### Judgment" in text
    assert "### Prediction" in text
    assert "- **Prediction:**" in text
    banned_body_terms = ("civ-mem", "WORK", "Record", "raw-input", "source_mode", "strategy-codex")
    body = text.split("### Sources", 1)[0]
    for term in banned_body_terms:
        assert term not in body

def test_observability_counts_new_strategy_chapter_headings(tmp_path: Path) -> None:
    observability = load_module(
        REPO_ROOT / "scripts" / "build_strategy_observability.py",
        "build_strategy_observability_module",
    )
    days = tmp_path / "days.md"
    days.write_text(
        """## 2026-05-09

### Signal

x

### Judgment

y

### Prediction

z

### References

- ref
""",
        encoding="utf-8",
    )

    assert observability._section_density(days)["avg_sections"] == 4.0

def test_signal_snippets_prefer_signal_with_chronicle_fallback() -> None:
    snippets = load_module(
        REPO_ROOT / "scripts" / "list_strategy_pages_by_month.py",
        "list_strategy_pages_module",
    )

    signal = snippets.chronicle_snippets_from_page_content(
        "### Signal\n\nFirst signal paragraph.\n\n> Quoted sentence.\n\n### Judgment\n\nx"
    )
    chronicle = snippets.chronicle_snippets_from_page_content(
        "### Chronicle\n\nLegacy paragraph.\n\n### Reflection\n\nx"
    )

    assert signal["signal_found"] is True
    assert signal["first_paragraph"] == "First signal paragraph."
    assert signal["blockquotes"] == ["Quoted sentence."]
    assert chronicle["signal_found"] is True
    assert chronicle["first_paragraph"] == "Legacy paragraph."
