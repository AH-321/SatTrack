#!/bin/bash

set -e

VENV_DIR=".venv"

echo "Beginning setup..."

if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Python is not installed." >&2
    exit 1
fi

"$PYTHON_CMD" -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

pip install --upgrade pip setuptools

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

echo "Setup complete."

exec "$SHELL"