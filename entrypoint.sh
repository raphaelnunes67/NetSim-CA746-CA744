#!/bin/bash

cd src || { echo "Directory 'src' does not exist. Exiting."; exit 1; }

CIRCUIT=${1:-"ca746"}
EV_LEVEL=${2:-0}
PV_LEVEL=${3:-20}
DB_PATH=${4:-"../databases"}
NUM_LOOPS=${5:-1000}
SAVE_VOLTAGES_DATA=${6:-1}

DB_PATH=$(realpath "$DB_PATH")

mkdir -p "$DB_PATH"

COMMAND="PYTHONPATH=\"$PWD/..\" ../venv/bin/python3 main.py -c $CIRCUIT -ev $EV_LEVEL -pv $PV_LEVEL -db $DB_PATH -sv $SAVE_VOLTAGES_DATA"

HISTORY_FILE="../history_commands.txt"
echo "$(date) - Command: $COMMAND" >> "$HISTORY_FILE"

LOG_FILE="../simulation_${CIRCUIT}_ev${EV_LEVEL}_pv${PV_LEVEL}.log"

nohup bash -c "
for i in \$(seq 1 $NUM_LOOPS)
do
    echo \"-----------Running simulation \$i for circuit $CIRCUIT with EV $EV_LEVEL% and PV $PV_LEVEL%-----------------\" >> \"$LOG_FILE\"
    eval $COMMAND >> \"$LOG_FILE\" 2>&1
done
" > "$LOG_FILE" 2>&1 &

echo "Simulation process started in the background."
echo "Logs: $LOG_FILE"
echo "Command history recorded in $HISTORY_FILE."
