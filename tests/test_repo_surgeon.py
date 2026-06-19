"""Tests for scripts/repo_surgeon.py."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from operator_report_utils import Finding, overall_status  # noqa: E402
from repo_surgeon import (  # noqa: E402
    build_findings,
    build_json_payload,
    build_markdown,
    findings_from_links,
    findings_from_local_path_leaks,
    main,
)
from validate_structured_files import collect_markdown_paths  # noqa: E402


def test_authority_header_present(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "ok.md").write_text("ok\n", encoding="utf-8")
    findings, check_outputs = build_findings(
        tmp_path,
        run_checks=False,
        scope="docs",
        verify_portable=False,
        max_link_errors=None,
    )
    md = build_markdown(
        findings,
        [],
        check_outputs,
        generated_at="2099-01-01 00:00 UTC",
        scope="docs",
        commands_run=[],
        md_link_cap=50,
    )
    assert "Mode: runtime / derived" in md
    assert "Authority: advisory only" in md
    assert "Canonical source: none" in md


def test_finds_broken_link_in_fixture(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a.md").write_text("[missing](./b.md)\n", encoding="utf-8")
    findings = findings_from_links(tmp_path, "docs")
    assert any(f.category == "broken_link" for f in findings)


def test_ignores_external_http_links(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "peer.md").write_text("ok\n", encoding="utf-8")
    (docs / "page.md").write_text(
        "[remote](https://example.com/foo) [local](./peer.md)\n",
        encoding="utf-8",
    )
    findings = findings_from_links(tmp_path, "docs")
    assert findings == []


def test_flags_local_path_leak(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "leak.md").write_text("See /C:/dev/strategy-codex/foo.md\n", encoding="utf-8")
    findings = findings_from_local_path_leaks(tmp_path, "docs")
    assert any(f.category == "local_path" for f in findings)


def test_overall_status_blocking_wins() -> None:
    assert overall_status([Finding("blocking", "root_layout", "x")]) == "red"
    assert overall_status([Finding("warning", "broken_link", "y")]) == "yellow"
    assert overall_status([]) == "green"


def test_fail_on_blocking_exit_code(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a.md").write_text("[ssot](../../AGENTS.md)\n", encoding="utf-8")

    monkeypatch.setattr("repo_surgeon.REPO_ROOT", tmp_path, raising=False)
    monkeypatch.setattr(
        "repo_surgeon.build_findings",
        lambda *a, **k: (
            [Finding("blocking", "broken_link", "missing AGENTS.md")],
            {},
        ),
    )
    out = tmp_path / "out.md"
    json_out = tmp_path / "out.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "repo_surgeon.py",
            "--out",
            str(out),
            "--json-out",
            str(json_out),
            "--no-existing-checks",
            "--fail-on-blocking",
        ],
    )
    assert main() == 1


def test_does_not_mutate_repo_files(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    source = docs / "stable.md"
    source.write_text("unchanged\n", encoding="utf-8")
    before = source.read_text(encoding="utf-8")
    out = tmp_path / "report.md"
    json_out = tmp_path / "report.json"
    findings, check_outputs = build_findings(
        tmp_path,
        run_checks=False,
        scope="docs",
        verify_portable=False,
        max_link_errors=None,
    )
    md = build_markdown(
        findings,
        [],
        check_outputs,
        generated_at="2099-01-01 00:00 UTC",
        scope="docs",
        commands_run=[],
        md_link_cap=50,
    )
    out.write_text(md, encoding="utf-8")
    json_out.write_text("{}", encoding="utf-8")
    assert source.read_text(encoding="utf-8") == before


def test_json_payload_shape() -> None:
    findings = [Finding("warning", "local_path", "leak", file="docs/x.md", line=1)]
    payload = build_json_payload(
        findings,
        ["fix leak"],
        generated_at="2099-01-01 00:00 UTC",
        commands_run=["python scripts/repo_surgeon.py"],
    )
    assert payload["authority"] == "runtime_derived"
    assert payload["status"] in {"green", "yellow", "red"}
    assert "blocking_count" in payload
    assert "findings" in payload
    assert "commands" in payload
    json.dumps(payload)


def test_scoped_docs_only(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "d.md").write_text("docs\n", encoding="utf-8")
    sc = tmp_path / "statecraft"
    sc.mkdir()
    (sc / "s.md").write_text("statecraft\n", encoding="utf-8")
    doc_paths = collect_markdown_paths(tmp_path, "docs")
    rels = {p.name for p in doc_paths}
    assert "d.md" in rels
    assert "s.md" not in rels


def test_missing_optional_checks_graceful(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "ok.md").write_text("fine\n", encoding="utf-8")
    findings, _ = build_findings(
        tmp_path,
        run_checks=False,
        scope="docs",
        verify_portable=False,
        max_link_errors=None,
    )
    assert isinstance(findings, list)
