#!/usr/bin/env python3
"""Compatibility shim — use validate_statecraft_synthesis.py."""
from validate_statecraft_synthesis import *  # noqa: F403,F401
from validate_statecraft_synthesis import main

if __name__ == "__main__":
    raise SystemExit(main())
