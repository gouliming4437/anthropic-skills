#!/bin/bash
# Wrapper to run calendar_utils.py in the miniconda 'pytest' environment

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Initialize conda for the current shell
eval "$(conda shell.bash hook)"

# Activate the pytest environment and run the Python script
conda activate pytest
python "$SCRIPT_DIR/calendar_utils.py" "$@"
