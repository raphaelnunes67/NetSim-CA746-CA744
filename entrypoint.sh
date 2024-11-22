#!/bin/bash

cd src || { echo "Directory 'src' does not exist. Exiting."; exit 1; }

CIRCUIT=${1:-"ca746"}
EV_LEVEL=${2:-0}
PV_LEVEL=${3:-20}
DB_PATH=${4:-"../databases"}


DB_PATH=$(realpath "$DB_PATH")

mkdir -p "$DB_PATH"

COMMAND="PYTHONPATH=\"$PWD/..\" ../venv/bin/python3 main.py -c $CIRCUIT -ev $EV_LEVEL -pv $PV_LEVEL -db $DB_PATH"

HISTORY_FILE="../history_commands.txt"
echo "$(date) - Command: $COMMAND" >> "$HISTORY_FILE"

LOG_FILE="../simulation_logs/simulation_${CIRCUIT}_ev${EV_LEVEL}_pv${PV_LEVEL}.log"
PID_FILE="../simulation_logs/simulation_${CIRCUIT}_ev${EV_LEVEL}_pv${PV_LEVEL}.pid"

nohup bash -c "
for i in {1..1000}
do
    echo \"-----------Running simulation \$i for circuit $CIRCUIT with EV $EV_LEVEL% and PV $PV_LEVEL%-----------------\"
    eval $COMMAND
done
" > "$LOG_FILE" 2>&1 &

echo $! > "$PID_FILE"

echo "Simulation process started in the background."
echo "Logs: $LOG_FILE"
echo "PID saved in $PID_FILE"
echo "Command history recorded in $HISTORY_FILE."