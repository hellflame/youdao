#!/bin/bash

source venv/bin/activate
pip install -U build twine

rm -rf dist

python -m build --sdist --wheel

twine upload dist/*
