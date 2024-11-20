#!/bin/bash

cd src

PID_FILE="../script_pid.txt"

PYTHONPATH="$PWD/../" nohup ../venv/bin/python3 main.py &

echo $! > "$PID_FILE"

echo "Script started in background. PID: $!"
echo "O PID saved in: $PID_FILE"