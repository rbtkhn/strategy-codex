#!/usr/bin/env python3
"""Run the local presentation service for ph-civ and civ-emp deck generation."""
from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
from repo_io import SRC_DIR
sys.path.insert(0, str(SRC_DIR))

from grace_mar.presentations.service import create_app

def main() -> None:
    port = int(os.getenv("PRESENTATION_SERVICE_PORT", "5060"))
    host = os.getenv("PRESENTATION_SERVICE_HOST", "127.0.0.1").strip() or "127.0.0.1"
    store_root = Path(os.getenv("PRESENTATION_SERVICE_STORE", "runtime/artifacts/presentations"))
    app = create_app(store_root=store_root)
    app.run(host=host, port=port)

if __name__ == "__main__":
    main()
