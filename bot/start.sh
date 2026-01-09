#!/bin/sh
set -e
if [ $DEBUG -eq 0 ]; then
    echo Starting in normal mode
    python3 ./main.py
fi
if [ $DEBUG -eq 1 ]; then
    echo Starting in debug mode
    echo Debugpy will listen on $DEBUGPY_PORT
    python -m debugpy --listen 0.0.0.0:$DEBUGPY_PORT --wait-for-client ./main.py
fi

exec "$@"