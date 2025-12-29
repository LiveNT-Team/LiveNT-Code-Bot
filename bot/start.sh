#!/bin/bash
set -e
echo Starting...
python3 ./main.py
echo Finished
exec "$@"