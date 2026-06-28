"""Ensure legacy transaction paths are stubs or inventoried."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STUB = "Deprecated compatibility stub"
TX_ROOT = REPO_ROOT / "statecraft"


def _collect_transaction_files() -> list[Path]:
    files: list[Path] = []
    for path in TX_ROOT.rglob("*"):
        if "/transactions/" not in path.as_posix():
            continue
        if path.is_file() and path.suffix == ".md":
            files.append(path)
    return sorted(files)


def test_legacy_transaction_md_files_are_stubs_or_tombstones() -> None:
    allowed_non_stub = {
        "statecraft/america/transactions/README.md",
        "statecraft/persia/transactions/README.md",
        "statecraft/russia/transactions/README.md",
        "statecraft/china/transactions/README.md",
    }
    for path in _collect_transaction_files():
        rel = path.relative_to(REPO_ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        if rel in allowed_non_stub:
            assert "deprecated" in text.lower() or "Deprecated" in text
            continue
        assert STUB in text, f"{rel} missing compatibility stub marker"
