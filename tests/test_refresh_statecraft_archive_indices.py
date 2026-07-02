from __future__ import annotations

from pathlib import Path

import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_statecraft_day_indices as day_idx  # noqa: E402
import refresh_statecraft_archive_indices as refresh  # noqa: E402

def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")

def _sample_source(day_dir: Path, slug: str, *, thread: str = "hoh") -> None:
    _write(
        day_dir / slug,
        (
            "---\n"
            f'title: "{slug}"\n'
            "show: Judging Freedom\n"
            "host: Judge Andrew Napolitano\n"
            "guest: Matt Hoh\n"
            f"thread: {thread}\n"
            "---\n\n"
            "Body.\n"
        ),
    )

def test_refresh_writes_day_month_and_root_indices(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    day_one = root / "2026-05-26"
    day_two = root / "2026-05-27"
    _sample_source(day_one, "transcript-napolitano-hoh-why-the-pentagon-lies-2026-05-26.md")
    _sample_source(day_two, "transcript-napolitano-hoh-us-foreign-policy-2026-05-27.md")

    stale_count, _ = refresh.refresh_or_check(root, check=False)

    assert stale_count >= 4
    assert (day_one / "README.md").is_file()
    assert (day_two / "README.md").is_file()
    assert (root / "2026-05.md").is_file()
    assert (root / "2026.md").is_file()
    assert (root / "thread-index.md").is_file()
    assert (root / "stale-index-audit.md").is_file()

def test_check_passes_after_refresh(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    day_one = root / "2026-05-26"
    _sample_source(day_one, "transcript-napolitano-hoh-why-the-pentagon-lies-2026-05-26.md")

    refresh.refresh_or_check(root, check=False)
    stale_count, _ = refresh.refresh_or_check(root, check=True)

    assert stale_count == 0

def test_check_fails_when_day_index_stale(tmp_path: Path) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    day_one = root / "2026-05-26"
    _sample_source(day_one, "transcript-napolitano-hoh-why-the-pentagon-lies-2026-05-26.md")

    day_idx.write_day_index(day_one, check=False)
    _write(day_one / "README.md", "# stale\n")

    stale_count, changed = refresh.refresh_or_check(root, check=True)

    assert stale_count >= 1
    assert any(p.name == "README.md" for p in changed)

def test_main_check_exit_code(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "source-archive" / "statecraft"
    day_one = root / "2026-05-26"
    _sample_source(day_one, "transcript-napolitano-hoh-why-the-pentagon-lies-2026-05-26.md")
    _write(day_one / "README.md", "# stale\n")

    monkeypatch.setattr(
        sys,
        "argv",
        ["refresh_statecraft_archive_indices.py", "--root", str(root), "--check"],
    )
    assert refresh.main() == 1

    refresh.refresh_or_check(root, check=False)
    monkeypatch.setattr(
        sys,
        "argv",
        ["refresh_statecraft_archive_indices.py", "--root", str(root), "--check"],
    )
    assert refresh.main() == 0
