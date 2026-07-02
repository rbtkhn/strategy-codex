from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-record-boundaries.py"

def load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_record_boundaries", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class InvalidUtf8Path:
    def read_text(self, encoding: str) -> str:
        assert encoding == "utf-8"
        raise UnicodeDecodeError("utf-8", b"\x97", 0, 1, "invalid start byte")

def test_read_markdown_utf8_reports_decode_error() -> None:
    validator = load_validator_module()

    text, error = validator.read_markdown_utf8(InvalidUtf8Path())

    assert text is None
    assert error is not None
    assert "not valid utf-8" in error
