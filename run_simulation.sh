#!/bin/bash

cd src

COMMAND="PYTHONPATH=\"$PWD/..\" ../venv/bin/python3 main.py -c ca746 -ev 0 -pv 20 -l 1"

# Run the command 1000 times
for i in {1..1000}
do
    echo "-----------Running simulation $i-----------------"
    eval $COMMAND
done