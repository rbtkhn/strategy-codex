"""Strategy notebook extension: receipts, graph scaffolds (non-authoritative)."""

from .judgment_loops import (
    build_judgment_loop_report,
    format_due_open_loops_markdown,
)
from .receipts import (
    NotebookReceipt,
    PageOperation,
    append_receipt,
    default_receipt_log_path,
)

__all__ = [
    "build_judgment_loop_report",
    "format_due_open_loops_markdown",
    "NotebookReceipt",
    "PageOperation",
    "append_receipt",
    "default_receipt_log_path",
]
