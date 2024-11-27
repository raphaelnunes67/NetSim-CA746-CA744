if (!(Test-Path -Path "src")) {
    Write-Host "Directory 'src' does not exist. Exiting."
    exit 1
}
Set-Location -Path "src"

$CIRCUIT = $args[0] -or "ca746"
$EV_LEVEL = $args[1] -or 0
$PV_LEVEL = $args[2] -or 20
$DB_PATH = $args[3] -or "../databases"
$NUM_LOOPS = $args[4] -or 1000
$SAVE_VOLTAGES_DATA = $args[5] -or 1

$DB_PATH = Resolve-Path -Path $DB_PATH

if (!(Test-Path -Path $DB_PATH)) {
    New-Item -ItemType Directory -Path $DB_PATH | Out-Null
}

$COMMAND = "PYTHONPATH=`"$PWD/..`" ../venv/bin/python3 main.py -c $CIRCUIT -ev $EV_LEVEL -pv $PV_LEVEL -db $DB_PATH -sv $SAVE_VOLTAGES_DATA"

$HISTORY_FILE = "../history_commands.txt"
Add-Content -Path $HISTORY_FILE -Value "$(Get-Date) - Command: $COMMAND"

$LOG_FILE = "../simulation_${CIRCUIT}_ev${EV_LEVEL}_pv${PV_LEVEL}.log"

Start-Job -ScriptBlock {
    param($COMMAND, $LOG_FILE, $NUM_LOOPS, $CIRCUIT, $EV_LEVEL, $PV_LEVEL)
    for ($i = 1; $i -le $NUM_LOOPS; $i++) {
        Add-Content -Path $LOG_FILE -Value "-----------Running simulation $i for circuit $CIRCUIT with EV $EV_LEVEL% and PV $PV_LEVEL%-----------------"
        Invoke-Expression $COMMAND | Out-File -Append -FilePath $LOG_FILE
    }
} -ArgumentList $COMMAND, $LOG_FILE, $NUM_LOOPS, $CIRCUIT, $EV_LEVEL, $PV_LEVEL

Write-Host "Simulation process started in the background."
Write-Host "Logs: $LOG_FILE"
Write-Host "Command history recorded in $HISTORY_FILE."
