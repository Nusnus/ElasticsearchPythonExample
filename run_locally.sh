#!/bin/bash

VENV=".venv"
if [ ! -d "$VENV" ]; then
    echo "Installing virtual environment in $VENV"
    python3 -m venv .venv
fi

source $VENV/bin/activate

echo "Installing pip requirements files in the virtual environment"
echo

pip install --upgrade pip

pip install -r requirements.txt

echo
echo "Finished installing pip requirements files in the virtualenv" 
echo

python main.py

deactivate