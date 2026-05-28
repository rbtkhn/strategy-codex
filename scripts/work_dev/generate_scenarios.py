#!/usr/bin/env python3
"""
Expand baseline scenarios × runtimes × dimensions into a scenario matrix.

Use `--format markdown --check path/to/matrix.md` to verify a checked-in file matches
the generator without writing (BUILD-AI-GAP-005 drift guard).

Backwards compatible with the existing simple baseline format:
- scenario_id
- failure_family
- required_checks
- severity

New supported fields per baseline YAML:
- description: str
- expected_failure_mode: str
- runtimes: [openclaw, cursor, ...]              # optional per-scenario override
- dimensions:
    receipt_state: [valid, missing, stale]
    topology: [local, remote]
- fixed:
    source: browser_extension
- exclude:
    - {runtime: cursor, topology: remote}
- variations:
    - id: stale_remote
      values: {receipt_state: stale, topology: remote}
      severity: high
      expected_failure_mode: stale continuity receipt on remote runtime
      required_checks: [continuity_required]
- tags: [continuity, boundary]
"""

from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from yaml_compat import has_yaml, safe_load_path

BASE = REPO_ROOT / "docs" / "skill-work" / "work-dev" / "scenarios" / "baseline_scenarios"
_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:\s+(.*))?$")


@dataclass(frozen=True)
class ScenarioRow:
    scenario_id: str
    runtime: str
    variation: str
    expected_failure_mode: str
    required_checks: list[str]
    severity: str
    tags: list[str]
    values: dict[str, Any]

    def sort_key(self) -> tuple[str, str, str]:
        return (self.scenario_id, self.runtime, self.variation)


def _coerce_scalar(value: str) -> Any:
    text = value.strip()
    if not text:
        return ""
    if text[0] == text[-1] and text[0] in {"'", '"'}:
        return text[1:-1]
    lowered = text.casefold()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none"}:
        return None
    if re.fullmatch(r"-?\d+", text):
        try:
            return int(text)
        except ValueError:
            return text
    return text


def _nonempty_lines(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        lines.append((indent, raw.strip()))
    return lines


def _parse_list(lines: list[tuple[int, str]], idx: int, indent: int) -> tuple[list[Any], int]:
    items: list[Any] = []
    while idx < len(lines):
        line_indent, stripped = lines[idx]
        if line_indent < indent:
            break
        if line_indent != indent or not stripped.startswith("- "):
            break
        item_text = stripped[2:].strip()
        idx += 1
        if not item_text:
            if idx < len(lines) and lines[idx][0] > indent:
                nested_indent = lines[idx][0]
                if lines[idx][1].startswith("- "):
                    value, idx = _parse_list(lines, idx, nested_indent)
                else:
                    value, idx = _parse_map(lines, idx, nested_indent)
                items.append(value)
            else:
                items.append("")
            continue

        match = _KEY_RE.match(item_text)
        if match:
            key, value_text = match.groups()
            item: dict[str, Any] = {}
            if value_text is None or not value_text.strip():
                if idx < len(lines) and lines[idx][0] > indent:
                    nested_indent = lines[idx][0]
                    if lines[idx][1].startswith("- "):
                        value, idx = _parse_list(lines, idx, nested_indent)
                    else:
                        value, idx = _parse_map(lines, idx, nested_indent)
                else:
                    value = ""
            else:
                value = _coerce_scalar(value_text)
            item[key] = value
            while idx < len(lines) and lines[idx][0] > indent:
                nested_indent = lines[idx][0]
                more, idx = _parse_map(lines, idx, nested_indent)
                item.update(more)
            items.append(item)
            continue

        items.append(_coerce_scalar(item_text))
    return items, idx


def _parse_map(lines: list[tuple[int, str]], idx: int, indent: int) -> tuple[dict[str, Any], int]:
    data: dict[str, Any] = {}
    while idx < len(lines):
        line_indent, stripped = lines[idx]
        if line_indent < indent:
            break
        if line_indent != indent:
            break
        match = _KEY_RE.match(stripped)
        if not match:
            raise ValueError(f"unsupported YAML line in scenario baseline: {stripped!r}")
        key, value_text = match.groups()
        idx += 1
        if value_text is not None and value_text.strip():
            data[key] = _coerce_scalar(value_text)
            continue
        if idx < len(lines) and lines[idx][0] > indent:
            nested_indent = lines[idx][0]
            if lines[idx][1].startswith("- "):
                value, idx = _parse_list(lines, idx, nested_indent)
            else:
                value, idx = _parse_map(lines, idx, nested_indent)
            data[key] = value
        else:
            data[key] = ""
    return data, idx


def _load_baseline_yaml_fallback(path: Path) -> dict[str, Any]:
    lines = _nonempty_lines(path.read_text(encoding="utf-8"))
    if not lines:
        return {}
    data, idx = _parse_map(lines, 0, lines[0][0])
    if idx != len(lines):
        raise ValueError(f"{path}: unparsed YAML tail at line {idx + 1}")
    return data


def _load_yaml(path: Path) -> dict[str, Any]:
    if has_yaml():
        raw = safe_load_path(path, feature="scenario matrix generation") or {}
    else:
        raw = _load_baseline_yaml_fallback(path)
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: scenario file must decode to a mapping")
    return raw


def _normalize_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _runtime_list(raw: dict[str, Any], default_runtimes: list[str]) -> list[str]:
    runtimes = _normalize_list(raw.get("runtimes"))
    if not runtimes:
        return default_runtimes
    out = [str(x).strip() for x in runtimes if str(x).strip()]
    return out or default_runtimes


def _dimensions(raw: dict[str, Any]) -> dict[str, list[Any]]:
    dims = raw.get("dimensions") or {}
    if not isinstance(dims, dict):
        raise ValueError("dimensions must be a mapping")
    out: dict[str, list[Any]] = {}
    for k, v in dims.items():
        vals = _normalize_list(v)
        if not vals:
            raise ValueError(f"dimension {k!r} must have at least one value")
        out[str(k)] = vals
    return out


def _fixed_values(raw: dict[str, Any]) -> dict[str, Any]:
    fixed = raw.get("fixed") or {}
    if not isinstance(fixed, dict):
        raise ValueError("fixed must be a mapping")
    return {str(k): v for k, v in fixed.items()}


def _exclude_rules(raw: dict[str, Any]) -> list[dict[str, Any]]:
    ex = raw.get("exclude") or []
    if not isinstance(ex, list):
        raise ValueError("exclude must be a list of mappings")
    out: list[dict[str, Any]] = []
    for item in ex:
        if not isinstance(item, dict):
            raise ValueError("exclude entries must be mappings")
        out.append({str(k): v for k, v in item.items()})
    return out


def _matches_rule(values: dict[str, Any], rule: dict[str, Any]) -> bool:
    for k, v in rule.items():
        if values.get(k) != v:
            return False
    return True


def _cartesian_rows(
    *,
    scenario_id: str,
    runtime: str,
    dims: dict[str, list[Any]],
    fixed: dict[str, Any],
) -> list[dict[str, Any]]:
    if not dims:
        values = dict(fixed)
        values["runtime"] = runtime
        return [values]

    keys = sorted(dims.keys())
    rows: list[dict[str, Any]] = []
    for combo in itertools.product(*(dims[k] for k in keys)):
        values = dict(fixed)
        values.update(dict(zip(keys, combo)))
        values["runtime"] = runtime
        rows.append(values)
    return rows


def _variation_id(values: dict[str, Any]) -> str:
    keys = [k for k in sorted(values.keys()) if k != "runtime"]
    if not keys:
        return "default"
    return "__".join(f"{k}={values[k]}" for k in keys)


def _base_failure_mode(raw: dict[str, Any]) -> str:
    return str(
        raw.get("expected_failure_mode")
        or raw.get("failure_family")
        or "scenario-triggered failure"
    ).strip()


def _base_required_checks(raw: dict[str, Any]) -> list[str]:
    return [str(x).strip() for x in _normalize_list(raw.get("required_checks")) if str(x).strip()]


def _base_tags(raw: dict[str, Any]) -> list[str]:
    return [str(x).strip() for x in _normalize_list(raw.get("tags")) if str(x).strip()]


def _expanded_variations(raw: dict[str, Any]) -> list[dict[str, Any]]:
    vars_ = raw.get("variations") or []
    if not vars_:
        return []
    if not isinstance(vars_, list):
        raise ValueError("variations must be a list")
    out: list[dict[str, Any]] = []
    for item in vars_:
        if not isinstance(item, dict):
            raise ValueError("variation entries must be mappings")
        values = item.get("values") or {}
        if not isinstance(values, dict):
            raise ValueError("variation.values must be a mapping")
        out.append(item)
    return out


def _build_rows_for_file(raw: dict[str, Any], default_runtimes: list[str]) -> list[ScenarioRow]:
    scenario_id = str(raw.get("scenario_id") or "").strip()
    if not scenario_id:
        raise ValueError("scenario_id is required")

    severity = str(raw.get("severity") or "medium").strip()
    base_mode = _base_failure_mode(raw)
    base_checks = _base_required_checks(raw)
    base_tags = _base_tags(raw)

    runtimes = _runtime_list(raw, default_runtimes)
    dims = _dimensions(raw)
    fixed = _fixed_values(raw)
    excludes = _exclude_rules(raw)
    explicit_variations = _expanded_variations(raw)

    rows: list[ScenarioRow] = []

    if explicit_variations:
        for rt in runtimes:
            for item in explicit_variations:
                values = dict(fixed)
                values.update(item.get("values") or {})
                values["runtime"] = rt
                if any(_matches_rule(values, rule) for rule in excludes):
                    continue
                row = ScenarioRow(
                    scenario_id=scenario_id,
                    runtime=rt,
                    variation=str(item.get("id") or _variation_id(values)),
                    expected_failure_mode=str(item.get("expected_failure_mode") or base_mode),
                    required_checks=[
                        str(x).strip()
                        for x in _normalize_list(item.get("required_checks") or base_checks)
                        if str(x).strip()
                    ],
                    severity=str(item.get("severity") or severity),
                    tags=sorted(
                        set(
                            base_tags
                            + [str(x).strip() for x in _normalize_list(item.get("tags")) if str(x).strip()]
                        )
                    ),
                    values={k: v for k, v in values.items() if k != "runtime"},
                )
                rows.append(row)
        return sorted(rows, key=lambda r: r.sort_key())

    for rt in runtimes:
        for values in _cartesian_rows(scenario_id=scenario_id, runtime=rt, dims=dims, fixed=fixed):
            if any(_matches_rule(values, rule) for rule in excludes):
                continue
            rows.append(
                ScenarioRow(
                    scenario_id=scenario_id,
                    runtime=rt,
                    variation=_variation_id(values),
                    expected_failure_mode=base_mode,
                    required_checks=base_checks,
                    severity=severity,
                    tags=base_tags,
                    values={k: v for k, v in values.items() if k != "runtime"},
                )
            )

    return sorted(rows, key=lambda r: r.sort_key())


def build_matrix(
    *,
    scenario_filter: str = "",
    runtimes: list[str],
    base_dir: Path = BASE,
) -> list[ScenarioRow]:
    rows: list[ScenarioRow] = []
    for path in sorted(base_dir.glob("*.yaml")):
        raw = _load_yaml(path)
        sid = str(raw.get("scenario_id") or path.stem)
        if scenario_filter and not sid.startswith(scenario_filter):
            continue
        rows.extend(_build_rows_for_file(raw, runtimes))
    return sorted(rows, key=lambda r: r.sort_key())


def render_markdown(rows: list[ScenarioRow]) -> str:
    lines = [
        "# Scenario Matrix\n\n",
        f"- Rows: **{len(rows)}**\n\n",
    ]
    last_sid = None
    for row in rows:
        if row.scenario_id != last_sid:
            lines.append(f"## {row.scenario_id}\n\n")
            last_sid = row.scenario_id
        vals = ", ".join(f"{k}={v}" for k, v in sorted(row.values.items())) or "default"
        checks = ", ".join(row.required_checks) or "_none_"
        tags = ", ".join(row.tags) or "_none_"
        lines.append(
            f"- **{row.runtime}** / `{row.variation}`"
            f" — {row.expected_failure_mode}"
            f" | severity={row.severity}"
            f" | values: {vals}"
            f" | checks: {checks}"
            f" | tags: {tags}\n"
        )
    return "".join(lines)


def _normalize_matrix_markdown(text: str) -> str:
    """Strip optional generated-file HTML comment; normalize newlines for drift checks."""
    lines = text.splitlines()
    if lines and lines[0].strip().startswith("<!--"):
        lines = lines[1:]
    body = "\n".join(lines).strip() + "\n"
    return "\n".join(line.rstrip() for line in body.splitlines()) + "\n"


def matrix_markdown_matches(rows: list[ScenarioRow], path: Path) -> tuple[bool, str]:
    """Return (ok, diff_or_empty). Expected file may start with <!-- Generated ... --> line."""
    expected = _normalize_matrix_markdown(path.read_text(encoding="utf-8"))
    got = _normalize_matrix_markdown(render_markdown(rows))
    if got == expected:
        return True, ""
    return False, (
        f"matrix drift: {path} does not match regenerated output "
        f"(regenerate per docs/skill-work/work-dev/scenarios/baseline_scenarios/README.md)\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate factorial scenario matrix rows.")
    ap.add_argument("--scenario", default="", help="Filter by scenario_id prefix")
    ap.add_argument(
        "--runtimes",
        default="openclaw,cursor,claude-code",
        help="Comma-separated runtime labels",
    )
    ap.add_argument("--format", default="json", choices=["json", "markdown"])
    ap.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Write output to FILE with UTF-8 encoding instead of stdout.",
    )
    ap.add_argument(
        "--check",
        type=Path,
        default=None,
        metavar="FILE",
        help="With --format markdown, verify FILE matches output (exit 1 on drift); for CI / pre-commit",
    )
    args = ap.parse_args()

    runtimes = [x.strip() for x in args.runtimes.split(",") if x.strip()]
    rows = build_matrix(scenario_filter=args.scenario.strip(), runtimes=runtimes)

    if args.check is not None:
        if args.format != "markdown":
            print("--check requires --format markdown", file=sys.stderr)
            return 2
        ok, msg = matrix_markdown_matches(rows, args.check)
        if not ok:
            print(msg, file=sys.stderr)
            return 1
        return 0

    if args.format == "markdown":
        rendered = render_markdown(rows)
    else:
        payload = {
            "version": 2,
            "rows": [asdict(r) for r in rows],
        }
        rendered = json.dumps(payload, indent=2) + "\n"

    if args.output is not None:
        out = args.output
        if not out.is_absolute():
            out = REPO_ROOT / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
