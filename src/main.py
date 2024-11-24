from utils.tools import Log
from common.constants import *
from simulation import CktSimulation
from pathlib import Path
import sys
import os
import click

def normalize_path(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))

def run_ca746(pl_ev: int, pl_pv: int, db_path: str, save_voltages_data: int):
    log = Log()
    simulation_logger = log.set_logger_file_and_stdout(f'SIMULATION_PL_EV_{pl_ev}_PL_PV_{pl_pv}')
    normalized_db_path = os.path.join(normalize_path(db_path), f"database_ca746_ev_{pl_ev}_pv_{pl_pv}.db")
    CktSimulation(
        circuit_name='ca746', loads_quantity=26, target_loads=TARGET_LOADS_CA746, target_file=str(Path('dss/ca746.dss').resolve()),
        database_path=normalized_db_path, save_voltages_data=save_voltages_data, _logger=simulation_logger
    ).execute_case_with_pl(
        pl_ev=pl_ev,
        pl_pv=pl_pv
    )

def run_ca744(pl_ev: int, pl_pv: int, db_path: str, save_voltages_data: int):
    log = Log()
    simulation_logger = log.set_logger_file_and_stdout(f'SIMULATION_PL_EV_{pl_ev}_PL_PV_{pl_pv}')
    normalized_db_path = os.path.join(normalize_path(db_path), f"database_ca744_ev_{pl_ev}_pv_{pl_pv}.db")
    CktSimulation(
        circuit_name='ca744', loads_quantity=47, target_loads=TARGET_LOADS_CA744, target_file=str(Path('dss/ca744.dss').resolve()),
        database_path=normalized_db_path, save_voltages_data=save_voltages_data, _logger=simulation_logger
    ).execute_case_with_pl(
        pl_ev=pl_ev,
        pl_pv=pl_pv
    )

@click.command()
@click.option('-c', '--circuit', type=click.Choice(['ca746', 'ca744']), required=True,
              help="Circuit name to simulate: 'ca746' or 'ca744'.")
@click.option('-ev', '--electric_vehicles', type=int, required=True,
              help="Electric vehicle penetration level (percentage).")
@click.option('-pv', '--photovoltaics', type=int, required=True,
              help="Photovoltaic penetration level (percentage).")
@click.option('-db', '--database_path', type=str, required=True,
              help="Base path for the database. This can be in Linux or Windows format.")
@click.option('-sv', '--save_voltages_data', type=int, required=True,
              help="Save voltages data in database")

def main(circuit, electric_vehicles, photovoltaics, database_path, save_voltages_data):
    normalized_path = normalize_path(database_path)
    if circuit == 'ca746':
        run_ca746(pl_ev=electric_vehicles, pl_pv=photovoltaics, db_path=normalized_path, save_voltages_data=save_voltages_data)
    elif circuit == 'ca744':
        run_ca744(pl_ev=electric_vehicles, pl_pv=photovoltaics, db_path=normalized_path, save_voltages_data=save_voltages_data)

if __name__ == '__main__':
    sys.path.append(os.getcwd())
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../')))
    main()
