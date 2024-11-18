from utils.tools import Log
from common.constants import *
from simulation import CktSimulation

if __name__ == '__main__':
    log = Log()
    simulation_logger = log.set_logger_file_and_stdout('SIMULATION')
    # CktSimulation(
    #     circuit_name='ca746', loads_quantity=26, target_loads=TARGET_LOADS_CA746, target_file='dss/ca746.dss',
    #     _logger=simulation_logger
    # ).execute_case_with_pl(
    #     simulation_quantity=1,
    #     pl_ev=0,
    #     pl_pv=100
    # )

    CktSimulation(
        circuit_name='ca744', loads_quantity=47, target_loads=TARGET_LOADS_CA744, target_file='dss/ca744.dss',
        _logger=simulation_logger
    ).execute_case_with_pl(
        loops_quantity=100,
        pl_ev=20,
        pl_pv=0
    )

