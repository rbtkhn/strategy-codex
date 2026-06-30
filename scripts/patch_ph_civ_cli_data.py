#!/usr/bin/env python3
"""Patch ph-civ cli.py and data.py after ph-mus strip."""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA_PY = REPO / "public" / "ph-civ" / "src" / "civ_ph" / "data.py"
CLI_PY = REPO / "public" / "ph-civ" / "src" / "civ_ph" / "cli.py"
PYPROJECT = REPO / "public" / "ph-civ" / "pyproject.toml"

def patch_data_py() -> None:
    text = DATA_PY.read_text(encoding="utf-8")
    text = text.replace('        "museum": data["museum"],\n', "")
    text = re.sub(
        r"\ndef load_museum_index\(\) -> list\[dict\]:.*?^\s+\[\"exhibits\"\]\)\n",
        "\n",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    DATA_PY.write_text(text, encoding="utf-8")

def patch_pyproject() -> None:
    text = PYPROJECT.read_text(encoding="utf-8")
    text = text.replace('ph-mus = "civ_ph.cli:mus_main"\n', "")
    PYPROJECT.write_text(text, encoding="utf-8")

def patch_cli_py() -> None:
    text = CLI_PY.read_text(encoding="utf-8")
    text = text.replace("    load_museum_index,\n", "")
    text = text.replace('    "### Museum Hooks",\n', "")
    text = text.replace('    "ph-mus",\n', "")

    text = text.replace(
        """        "museum": {
            "status": route["museum_status"],
            "exhibit_path": route.get("museum_exhibit_path"),
        },
""",
        "",
    )
    text = text.replace(
        '                "museum_exhibit_path": route.get("museum_exhibit_path"),\n',
        "",
    )
    text = text.replace(
        "    print(f\"museum: {payload['museum']['status']}\\t{payload['museum']['exhibit_path']}\")\n",
        "",
    )

    text = re.sub(
        r"\ndef cmd_museum_list\(args\) -> int:.*?\n    return 2\n",
        "\n",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(
        r"\ndef build_museum_parser\(\) -> argparse\.ArgumentParser:.*?\n    return parser\n\n",
        "\n",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(
        r"\ndef mus_main\(argv: list\[str\] \| None = None\) -> int:.*?\n    return args\.func\(args\)\n",
        "\n",
        text,
        flags=re.DOTALL,
    )

    text = text.replace('            "`ph-mus` is not a third volume",\n', '            "two-volume public artifact",\n')
    text = text.replace('            "ph-mus` is not a third volume",\n', '            "two-volume public artifact",\n')

    text = text.replace(
        """    if llm_surfaces.get("museum", {}).get("surface") != "ph-mus":
        errors.append("llm-experience museum must use ph-mus")
    if llm_surfaces.get("museum", {}).get("not_a_volume") is not True:
        errors.append("llm-experience must mark ph-mus as not a volume")
""",
        "",
    )
    text = text.replace('        "ph-mus is not a third volume",\n', "")

    text = text.replace(
        """    museum_ids = [exhibit.get("source_id") for exhibit in load_museum_index()]
    if set(museum_ids) != set(seed_route_ids):
        errors.append("museum index must contain the same route IDs as the seed")
""",
        "",
    )
    text = text.replace(
        """        if source_id in set(seed_route_ids) or source_id in set(museum_ids):
            errors.append(f"{source_id} must not be promoted into routes or museum exhibits before review")
""",
        """        if source_id in set(seed_route_ids):
            errors.append(f"{source_id} must not be promoted into routes before review")
""",
    )

    text = text.replace(
        """    if architecture.get("museum", {}).get("surface") != "ph-mus":
        errors.append("museum layer must route through ph-mus")
    if architecture.get("museum", {}).get("role") != "chapter_exhibit_layer":
        errors.append("museum layer must use chapter_exhibit_layer role")
""",
        "",
    )

    text = text.replace('                "museum": architecture["museum"],\n', "")
    text = text.replace('    print("ph-mus: chapter_exhibit_layer for both volumes")\n', "")
    text = text.replace('        "museum": architecture["museum"],\n', "")
    text = text.replace(
        "    print(f\"ph-mus\\t{payload['museum']['role']}\\t{payload['museum']['description']}\")\n",
        "",
    )

    CLI_PY.write_text(text, encoding="utf-8")

def main() -> int:
    patch_data_py()
    patch_pyproject()
    patch_cli_py()
    print("patched data.py, pyproject.toml, cli.py")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
