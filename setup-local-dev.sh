#!/usr/bin/env bash
# setup-local-dev.sh
# Creates a local Python venv and installs all backend dependencies
# so the IDE (Pyright/Pylance/Pyre2) can resolve imports without Docker.
# Run once from the project root: bash setup-local-dev.sh

set -e

VENV_DIR="backend/.venv"
REQ_FILE="backend/requirements.txt"

echo "==> Creating virtual environment at $VENV_DIR ..."
python3 -m venv "$VENV_DIR"

echo "==> Upgrading pip ..."
"$VENV_DIR/bin/pip" install --upgrade pip

echo "==> Installing backend dependencies from $REQ_FILE ..."
"$VENV_DIR/bin/pip" install -r "$REQ_FILE"

echo ""
echo "✅  Done! Now select the interpreter in VS Code:"
echo "    1. Press Ctrl+Shift+P → Python: Select Interpreter"
echo "    2. Choose: backend/.venv/bin/python"
echo ""
echo "    (Or VS Code may auto-detect it via pyrightconfig.json)"
