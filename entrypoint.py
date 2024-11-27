import os
import sys
import subprocess
from datetime import datetime

def main():
    src_dir = "src"
    if not os.path.isdir(src_dir):
        print("Directory 'src' does not exist. Exiting.")
        sys.exit(1)
    os.chdir(src_dir)

    circuit = sys.argv[1] if len(sys.argv) > 1 else "ca746"
    ev_level = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    pv_level = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    db_path = sys.argv[4] if len(sys.argv) > 4 else "../databases"
    num_loops = int(sys.argv[5]) if len(sys.argv) > 5 else 1000
    save_voltages_data = int(sys.argv[6]) if len(sys.argv) > 6 else 1

    db_path = os.path.abspath(db_path)
    os.makedirs(db_path, exist_ok=True)

    command = (
        f'PYTHONPATH="{os.getcwd()}/.." ../venv/bin/python3 main.py '
        f'-c {circuit} -ev {ev_level} -pv {pv_level} -db "{db_path}" -sv {save_voltages_data}'
    )

    history_file = os.path.abspath("../history_commands.txt")
    with open(history_file, "a") as history:
        history.write(f"{datetime.now()} - Command: {command}\n")

    log_file = os.path.abspath(f"../simulation_{circuit}_ev{ev_level}_pv{pv_level}.log")

    with open(log_file, "a") as log:
        nohup_command = [
            "bash",
            "-c",
            f"""
            for i in $(seq 1 {num_loops})
            do
                echo "-----------Running simulation $i for circuit {circuit} with EV {ev_level}% and PV {pv_level}%-----------------" >> "{log_file}"
                eval {command} >> "{log_file}" 2>&1
            done
            """
        ]
        subprocess.Popen(nohup_command, stdout=log, stderr=log)

    print("Simulation process started in the background.")
    print(f"Logs: {log_file}")
    print(f"Command history recorded in {history_file}.")

if __name__ == "__main__":
    main()
