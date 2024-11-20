from utils.tools import Log
from common.constants import *
from simulation import CktSimulation
from multiprocessing import Process
import sys
import os


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

if __name__ == '__main__':
    # Solving paths
    sys.path.append(os.getcwd())
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../')))

    # CktSimulation(
    #     circuit_name='ca746', loads_quantity=26, target_loads=TARGET_LOADS_CA746, target_file='dss/ca746.dss',
    #     database_path='/mnt/d/database_ca746.db', _logger=simulation_logger
    # ).execute_case_with_pl(
    #     loops_quantity=1000,
    #     pl_ev=20,
    #     pl_pv=0
    # )


    # CktSimulation(
    #     circuit_name='ca744', loads_quantity=47, target_loads=TARGET_LOADS_CA744, target_file='dss/ca744.dss',
    #     _logger=simulation_logger,  database_path='D:\database_ca744.db'
    # ).execute_case_with_pl(
    #     loops_quantity=10,
    #     pl_ev=20,
    #     pl_pv=20
    # )


    # Execute with Multiprocess

    processes = [
        Process(target=run_ca746, args=(20, 0, 1000)),
        Process(target=run_ca746, args=(40, 0, 1000)),
        Process(target=run_ca746, args=(60, 0, 1000)),
        Process(target=run_ca746, args=(80, 0, 1000)),
        Process(target=run_ca746, args=(100, 0, 1000)),

        Process(target=run_ca746, args=(0, 20, 1000)),
        Process(target=run_ca746, args=(0, 40, 1000)),
        Process(target=run_ca746, args=(0, 60, 1000)),
        Process(target=run_ca746, args=(0, 80, 1000)),
        Process(target=run_ca746, args=(0, 100, 1000)),
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()
