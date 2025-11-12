#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR/.."
REQ="$REPO_ROOT/services/policy-gateway/requirements-dev.txt"

echo "Preparing virtual environment and installing dev dependencies (prefers 'uv' when possible)"

# Create virtualenv if it doesn't exist. Prefer `uv venv .venv` when `uv` is available
# because it manages environments consistently; otherwise fall back to python venv.
if [ ! -d "$REPO_ROOT/.venv" ]; then
  if command -v uv >/dev/null 2>&1; then
    echo "Creating virtualenv with uv: uv venv $REPO_ROOT/.venv"
    if uv venv "$REPO_ROOT/.venv" 2>/dev/null; then
      echo "Created .venv with uv"
    else
      echo "uv failed to create venv, falling back to python3 -m venv" >&2
      python3 -m venv "$REPO_ROOT/.venv"
    fi
  else
    echo "uv not present; creating venv with python3 -m venv"
    python3 -m venv "$REPO_ROOT/.venv"
  fi
fi

# Activate the venv for the remainder of the script
echo "Activating virtualenv: $REPO_ROOT/.venv"
source "$REPO_ROOT/.venv/bin/activate"

# Ensure pip is recent inside venv
python3 -m pip install --upgrade pip

# Install requirements preferring uv if available inside the venv
  if command -v uv >/dev/null 2>&1; then
  echo "Using uv to install requirements from $REQ inside venv"
  # Use uv to run pip inside the venv. Do not suppress errors so failures are visible.
  if uv pip install -r "$REQ"; then
    echo "Installed with: uv pip install -r $REQ"
  else
    echo "uv present but failed to install requirements; falling back to pip" >&2
    python3 -m pip install -r "$REQ"
  fi
else
  echo "uv not found inside venv; using pip to install requirements"
  python3 -m pip install -r "$REQ"
fi

export PYTHONPATH="$REPO_ROOT/services/policy-gateway/src:${PYTHONPATH:-}"

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
