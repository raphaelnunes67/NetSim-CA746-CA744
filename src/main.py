from utils.tools import Log
from common.constants import *
from simulation import CktSimulation
import sys
import os
import click

def run_ca746(pl_ev: int, pl_pv: int, loops_quantity: int):
    log = Log()
    simulation_logger = log.set_logger_file_and_stdout(f'SIMULATION_PL_EV_{pl_ev}_PL_PV_{pl_pv}')
    CktSimulation(
        circuit_name='ca746', loads_quantity=26, target_loads=TARGET_LOADS_CA746, target_file='dss/ca746.dss',
        database_path=f'/mnt/d/database_ca746_ev_{pl_ev}_pv_{pl_pv}.db', _logger=simulation_logger
    ).execute_case_with_pl(
        loops_quantity=loops_quantity,
        pl_ev=pl_ev,
        pl_pv=pl_pv
    )

def run_ca744(pl_ev: int, pl_pv: int, loops_quantity: int):
    log = Log()
    simulation_logger = log.set_logger_file_and_stdout(f'SIMULATION_PL_EV_{pl_ev}_PL_PV_{pl_pv}')
    CktSimulation(
        circuit_name='ca744', loads_quantity=47, target_loads=TARGET_LOADS_CA744, target_file='dss/ca744.dss',
        database_path=f'/mnt/d/database_ca744_ev_{pl_ev}_pv_{pl_pv}.db', _logger=simulation_logger
    ).execute_case_with_pl(
        loops_quantity=loops_quantity,
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
@click.option('-l', '--loops', type=int, required=True,
              help="Number of simulation loops.")
def main(circuit, electric_vehicles, photovoltaics, loops):
    if circuit == 'ca746':
        run_ca746(pl_ev=electric_vehicles, pl_pv=photovoltaics, loops_quantity=loops)
    elif circuit == 'ca744':
        run_ca744(pl_ev=electric_vehicles, pl_pv=photovoltaics, loops_quantity=loops)

if __name__ == '__main__':
    sys.path.append(os.getcwd())
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../')))
    main()
