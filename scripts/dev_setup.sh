#!/usr/bin/env bash
set -euo pipefail

REQ="services/policy-gateway/requirements-dev.txt"

echo "Installing dev dependencies (prefers 'uv' if available, falls back to pip)"
if command -v uv >/dev/null 2>&1; then
  echo "Using uv to install requirements from $REQ"
  # try a couple of common uv CLI forms
  if uv install -r "$REQ" 2>/dev/null; then
    echo "Installed with: uv install -r $REQ"
  elif uv add -r "$REQ" 2>/dev/null; then
    echo "Installed with: uv add -r $REQ"
  else
    echo "uv present but failed to install requirements; falling back to pip" >&2
    python3 -m pip install --upgrade pip
    python3 -m pip install -r "$REQ"
  fi
else
  echo "uv not found; using pip"
  python3 -m pip install --upgrade pip
  python3 -m pip install -r "$REQ"
fi

export PYTHONPATH="$PWD/services/policy-gateway/src:$PYTHONPATH"

echo
echo "Running linter (ruff) if available..."
if command -v ruff >/dev/null 2>&1; then
  ruff check services/policy-gateway || true
else
  echo "ruff not installed; skipping lint step"
fi

echo
echo "Running pytest for policy-gateway tests..."
python3 -m pytest services/policy-gateway/tests -q

echo
echo "Done. If tests passed, the environment is ready."
