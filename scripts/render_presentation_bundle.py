#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib import request

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))


def main() -> int:
    ap = argparse.ArgumentParser(description="Submit a prepared presentation bundle to the local presentation service.")
    ap.add_argument("--bundle", type=Path, required=True)
    ap.add_argument("--service-url", default="http://127.0.0.1:5060")
    ap.add_argument("--n-slides", type=int, default=None)
    ap.add_argument("--language", default="English")
    args = ap.parse_args()

    bundle_path = args.bundle if args.bundle.is_absolute() else (REPO_ROOT / args.bundle)
    payload = {
        "bundle": json.loads(bundle_path.read_text(encoding="utf-8")),
        "render_options": {
            "requested_outputs": ["pptx", "web"],
            "language": args.language,
        },
    }
    if args.n_slides:
        payload["render_options"]["n_slides"] = args.n_slides

    req = request.Request(
        f"{args.service_url.rstrip('/')}/v1/bundles/render",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=120) as resp:
        print(resp.read().decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
