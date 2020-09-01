#!/bin/sh

set -e
set -u

SHEPHERD_DIR='/opt/shepherd-bot'
SHEPHERD_SCRIPT='shepherd-bot.py'
PYTHON_VENV='shepherd_venv'

printf '[LAUNCHER] Changing working directory to "%s".\n' "$SHEPHERD_DIR"
cd "$SHEPHERD_DIR"

printf '[LAUNCHER] Activating virtual environment "%s".\n' "$PYTHON_VENV"
. "$SHEPHERD_DIR/$PYTHON_VENV/bin/activate"

printf '[LAUNCHER] Launching script "%s".\n' "$SHEPHERD_SCRIPT"
set +e
python3 "$SHEPHERD_DIR/$SHEPHERD_SCRIPT"

printf '[LAUNCHER] Script quit with exit code %s.\n' "$?"
