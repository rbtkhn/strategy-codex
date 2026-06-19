#!/usr/bin/env bash
# Generate profile and open it in the default browser (fast local loop).
set -e
cd "$(dirname "$0")/.."
python3 scripts/generate_profile.py
if command -v open >/dev/null 2>&1; then
  open platform/profile/index.html
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open platform/profile/index.html
else
  echo "Profile generated at platform/profile/index.html — open it in your browser."
fi
