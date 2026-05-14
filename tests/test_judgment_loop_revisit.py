"""Tests for derived judgment-loop revisit surfacing."""

from __future__ import annotations

from datetime import date
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from cadence_conductor_resolution import build_conductor_revisit_block  # noqa: E402
from strategy_notebook.judgment_loops import build_judgment_loop_report  # noqa: E402


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_build_judgment_loop_report_surfaces_due_loop_and_register_status(tmp_path: Path) -> None:
    nb = tmp_path / "codex"
    _write(
        nb / "2026" / "pape" / "pape-page-2026-04-10-test.md",
        """# Pape codex-page - 2026-04-10

WORK only; not Record.

### Reflection

Commodity pain will harden into a blockade calendar rather than easing into diplomacy.

### Predictive Outlook

- **Call:** The blockade thesis will stay live through late April.
- **Falsifier:** Shipping normalizes before the end of April.
- **Revisit:** 2026-04-20 or earlier if tanker flow normalizes.
""",
    )
    _write(
        nb / "2026" / "chapters" / "2026-04" / "days.md",
        "## 2026-04-28\n\n### Reflection\n\ncontinuity moved\n",
    )
    _write(
        nb / "notes" / "JUDGMENT-LOOP-REGISTER.md",
        """# Judgment loop register

## 2026-04-11 - tanker flow watch

- **Reference:** [pape loop](../2026/pape/pape-page-2026-04-10-test.md)
- **Call:** The blockade thesis will stay live through late April.
- **Falsifier:** Shipping normalizes before the end of April.
- **Revisit:** 2026-04-20
- **Status:** `open`
- **Outcome note:** Waiting for flow data.
""",
    )
    report = build_judgment_loop_report(nb, today=date(2026, 5, 4), user_id="grace-mar")
    loops = report["loops"]
    assert loops
    loop = loops[0]
    assert loop.stream == "pape"
    assert loop.derived_state == "due"
    assert loop.register_status == "open"
    assert "Update register status" in loop.suggested_next_action or "tag outcome" in loop.suggested_next_action


def test_build_judgment_loop_report_accepts_prediction_field(tmp_path: Path) -> None:
    nb = tmp_path / "codex"
    _write(
        nb / "2026" / "pape" / "pape-page-2026-04-10-test.md",
        """# Pape strategy-page - 2026-04-10

### Signal

- A shipping disruption moved from background risk to active strategic signal.

### Judgment

- The market signal matters because it can discipline the diplomatic calendar.

### Prediction

- **Prediction:** The pressure thesis will remain live through late April.
- **Falsifier:** Shipping normalizes before the end of April.
- **Revisit:** 2026-04-20
""",
    )
    _write(nb / "2026" / "chapters" / "2026-04" / "days.md", "## 2026-04-28\n")

    report = build_judgment_loop_report(nb, today=date(2026, 5, 4), user_id="grace-mar")

    loops = report["loops"]
    assert loops
    assert loops[0].call == "The pressure thesis will remain live through late April."
    assert loops[0].falsifier == "Shipping normalizes before the end of April."


def test_build_judgment_loop_report_detects_polyphonic_tension(tmp_path: Path) -> None:
    nb = tmp_path / "codex"
    _write(
        nb / "2026" / "pape" / "pape-page-2026-04-10-hormuz.md",
        """# Pape codex-page - 2026-04-10

### Reflection

Escalation pressure is intensifying around Hormuz.

### Predictive Outlook

- **Call:** Hormuz pressure is likely to escalate again before talks stabilize.
- **Falsifier:** A durable shipping corridor reopens without new military signaling.
- **Revisit:** 2026-04-20
""",
    )
    _write(
        nb / "2026" / "diesen" / "diesen-page-2026-04-10-hormuz.md",
        """# Diesen codex-page - 2026-04-10

### Reflection

Institutional pressure is moving toward a negotiated stabilization path.

### Predictive Outlook

- **Call:** Hormuz pressure is likely to stabilize through diplomacy before a renewed clash.
- **Falsifier:** Shipping seizures resume and talks collapse.
- **Revisit:** 2026-04-20
""",
    )
    _write(nb / "2026" / "chapters" / "2026-04" / "days.md", "## 2026-04-20\n")
    report = build_judgment_loop_report(nb, today=date(2026, 5, 4), user_id="grace-mar")
    tensions = report["tensions"]
    assert tensions
    tension = tensions[0]
    assert tension.topic == "Hormuz / blockade mechanics vs bargaining logic"
    assert {loop.stream for loop in tension.loops} == {"pape", "diesen"}
    assert "Compare side-by-side" in tension.suggested_next_action


def test_build_judgment_loop_report_ignores_scaffold_word_overlap_without_anchor(tmp_path: Path) -> None:
    nb = tmp_path / "codex"
    _write(
        nb / "2026" / "pape" / "pape-page-2026-04-10-weave.md",
        """# Pape codex-page - 2026-04-10

### Reflection

The page keeps returning to weave language and abstract framing.

### Predictive Outlook

- **Call:** The weave will stabilize before the abstract frame breaks.
- **Falsifier:** The abstract frame collapses first.
- **Revisit:** 2026-04-20
""",
    )
    _write(
        nb / "2026" / "diesen" / "diesen-page-2026-04-10-weave.md",
        """# Diesen codex-page - 2026-04-10

### Reflection

The same weave language now points toward a break in the frame.

### Predictive Outlook

- **Call:** The weave will break before the abstract frame stabilizes.
- **Falsifier:** The abstract frame holds steady.
- **Revisit:** 2026-04-20
""",
    )
    _write(nb / "2026" / "chapters" / "2026-04" / "days.md", "## 2026-04-20\n")

    report = build_judgment_loop_report(nb, today=date(2026, 5, 4), user_id="grace-mar")

    assert report["tensions"] == []


def test_build_judgment_loop_report_collapses_duplicate_topics_into_family(tmp_path: Path) -> None:
    nb = tmp_path / "codex"
    _write(
        nb / "2026" / "pape" / "pape-page-2026-04-10-hormuz.md",
        """# Pape codex-page - 2026-04-10

### Reflection

Blockade pressure is intensifying around Hormuz and energy chokepoints.

### Predictive Outlook

- **Call:** Hormuz blockade pressure is likely to escalate before talks stabilize.
- **Falsifier:** A durable shipping corridor reopens without new military signaling.
- **Revisit:** 2026-04-20
""",
    )
    _write(
        nb / "2026" / "diesen" / "diesen-page-2026-04-10-hormuz.md",
        """# Diesen codex-page - 2026-04-10

### Reflection

Commodity pressure is moving toward a negotiated stabilization path.

### Predictive Outlook

- **Call:** Commodity and Hormuz pressure are likely to stabilize through diplomacy before a renewed clash.
- **Falsifier:** Shipping seizures resume and talks collapse.
- **Revisit:** 2026-04-20
""",
    )
    _write(
        nb / "2026" / "ritter" / "ritter-page-2026-04-12-hormuz.md",
        """# Ritter codex-page - 2026-04-12

### Reflection

Currency and energy stress still point toward an escalation track.

### Predictive Outlook

- **Call:** Currency and energy strain around Hormuz are likely to widen before diplomacy can hold.
- **Falsifier:** Talks lock in a stable corridor and market relief persists.
- **Revisit:** 2026-04-22
""",
    )
    _write(nb / "2026" / "chapters" / "2026-04" / "days.md", "## 2026-04-22\n")

    report = build_judgment_loop_report(nb, today=date(2026, 5, 4), user_id="grace-mar")

    tensions = report["tensions"]
    assert len(tensions) == 1
    tension = tensions[0]
    assert tension.topic == "Hormuz / blockade mechanics vs bargaining logic"
    assert {loop.stream for loop in tension.loops} == {"pape", "diesen", "ritter"}
    assert tension.suppressed_duplicates >= 1


def test_build_conductor_revisit_block_formats_tension(tmp_path: Path) -> None:
    nb = tmp_path / "codex"
    _write(
        nb / "2026" / "pape" / "pape-page-2026-04-10-hormuz.md",
        """# Pape codex-page - 2026-04-10

### Reflection

Escalation pressure is intensifying around Hormuz.

### Predictive Outlook

- **Call:** Hormuz pressure is likely to escalate again before talks stabilize.
- **Falsifier:** A durable shipping corridor reopens without new military signaling.
- **Revisit:** 2026-04-20
""",
    )
    _write(
        nb / "2026" / "diesen" / "diesen-page-2026-04-10-hormuz.md",
        """# Diesen codex-page - 2026-04-10

### Reflection

Institutional pressure is moving toward a negotiated stabilization path.

### Predictive Outlook

- **Call:** Hormuz pressure is likely to stabilize through diplomacy before a renewed clash.
- **Falsifier:** Shipping seizures resume and talks collapse.
- **Revisit:** 2026-04-20
""",
    )
    _write(nb / "2026" / "chapters" / "2026-04" / "days.md", "## 2026-04-20\n")
    text = build_conductor_revisit_block("grace-mar", notebook_root=nb)
    assert "Open loops due for revisit" in text
    assert "### Tension" in text
    assert "`pape`" in text and "`diesen`" in text
