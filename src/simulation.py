"""
This is a script to perform simulations and store data in database
Loop Simulation: Collection of simulations with 3 control possibilities, case with 7 days;
Simulation: 7 day of simple simulation (OpenDSS);
"""

from logging import Logger
from time import sleep

from opendssdirect import dss
from datetime import datetime
from common.constants import *
from common.drpdrc import DrpDrc
from typing import List, Type
import pandas as pd
from src.database.models import *
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from decimal import Decimal
import sys
import random
import json


class StoreData:
    def __init__(self, database_path: str, logger: Logger):
        engine = create_engine(f'sqlite:///{database_path}', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.logger = logger

    def create_loop_simulation(self, started_at: datetime, random_target_load_ev: str, random_target_load_pv: str,
                               random_ev_kwh: str, random_pv_shapes_possibilities, random_phases_ev: str,
                               random_phases_pv: str, random_ev_chargers_power: str, random_max_power_pv: str,
                               random_ev_shapes_by_day: str) -> int:
        new_loop_simulation = LoopSimulation(
            started_at=started_at,
            random_target_load_ev=random_target_load_ev,
            random_target_load_pv=random_target_load_pv,
            random_ev_kwh=random_ev_kwh,
            random_pv_shapes_possibilities=random_pv_shapes_possibilities,
            random_phases_ev=random_phases_ev,
            random_phases_pv=random_phases_pv,
            random_ev_chargers_power=random_ev_chargers_power,
            random_max_power_pv=random_max_power_pv,
            random_ev_shapes_by_day=random_ev_shapes_by_day
        )
        self.session.add(new_loop_simulation)
        self.session.commit()

        return new_loop_simulation.id

    def insert_loop_simulation_finished_at(self, loop_simulation_id: int, finished_at: datetime) -> None:
        loop_simulation = self.session.query(LoopSimulation).filter_by(id=loop_simulation_id).first()

        if loop_simulation:
            loop_simulation.finished_at = finished_at
            self.session.commit()
        else:
            raise ValueError(f"LoopSimulation with id {loop_simulation_id} not found")

    def save_simulation(self, loop_simulation_id: int, control_mode: str, started_at: datetime) -> int:
        new_simulation = Simulation(
            loop_simulation_id=loop_simulation_id,
            control_mode=control_mode,
            started_at=started_at
        )
        self.session.add(new_simulation)
        self.session.commit()

        return new_simulation.id

    def insert_simulation_finished_at(self, simulation_id: int, finished_at: datetime) -> None:
        simulation = self.session.query(Simulation).filter_by(id=simulation_id).first()

        if simulation:
            simulation.finished_at = finished_at
            self.session.commit()
        else:
            raise ValueError(f"Simulation with id {simulation_id} not found")

    def erase_last_simulation(self):
        last_simulation_id = (
            self.session.query(Simulation.id)
            .order_by(Simulation.id.desc())
            .limit(1)
            .scalar()
        )
        if last_simulation_id:
            self.session.query(Simulation).filter(Simulation.id == last_simulation_id).delete(synchronize_session=False)
            self.session.commit()

    def save_voltages_data(self, simulation_id: int, n_res: int, n_day: int, voltages_v1: list, voltages_v2: list,
                           voltages_v3: list) -> None:
        all_voltages_data = [
            VoltageData(
                simulation_id=simulation_id,
                n_res=n_res,
                n_day=n_day,
                v1=Decimal(f"{v1:.2f}"),
                v2=Decimal(f"{v2:.2f}"),
                v3=Decimal(f"{v3:.2f}")
            )
            for v1, v2, v3 in zip(voltages_v1, voltages_v2, voltages_v3)
        ]

        self.session.bulk_save_objects(all_voltages_data)
        self.session.commit()

    def save_energy_meters(self, simulation_id: int, n_res: int, n_day: int, bus: str, energy: float):
        new_energy_data = EnergyMeter(
            simulation_id=simulation_id,
            n_res=n_res,
            n_day=n_day,
            bus=bus,
            energy=round(energy, 3)
        )
        self.session.add(new_energy_data)
        self.session.commit()

    def save_compensation(self, simulation_id: int, compensation: float):
        new_compensation_data = Compensation(
            simulation_id=simulation_id,
            compensation=round(compensation, 2)
        )

        self.session.add(new_compensation_data)
        self.session.commit()

    def save_losses(self, simulation_id: int, n_day, loss: float):
        new_losses_data = Loss(
            simulation_id=simulation_id,
            n_day=n_day,
            loss=round(loss, 3)
        )
        self.session.add(new_losses_data)
        self.session.commit()

    def check_and_resolve_database_integrity(self):
        """
        Verifica se há um LoopSimulation incompleto (finished_at is None) e apaga todos
        os dados relacionados, incluindo os registros em simulations, voltages_data,
        energy_meters, compensations e losses.
        """
        # Buscar o último LoopSimulation
        last_loop_simulation = (
            self.session.query(LoopSimulation)
            .order_by(LoopSimulation.id.desc())
            .first()
        )

        if last_loop_simulation and last_loop_simulation.finished_at is None:
            self.logger.warning(
                f"Found an incomplete LoopSimulation with ID: {last_loop_simulation.id}. Cleaning up associated data."
            )
            try:

                for simulation in last_loop_simulation.simulations:

                    self.session.query(VoltageData).filter_by(simulation_id=simulation.id).delete()
                    self.session.query(EnergyMeter).filter_by(simulation_id=simulation.id).delete()
                    self.session.query(Compensation).filter_by(simulation_id=simulation.id).delete()
                    self.session.query(Loss).filter_by(simulation_id=simulation.id).delete()

                self.session.query(Simulation).filter_by(loop_simulation_id=last_loop_simulation.id).delete()

                self.session.delete(last_loop_simulation)

                self.session.commit()
                self.logger.info(
                    f"All data associated with LoopSimulation ID {last_loop_simulation.id} has been cleaned up.")
            except Exception as e:
                self.session.rollback()
                self.logger.error(f"An error occurred while cleaning up data: {e}")

        elif last_loop_simulation and last_loop_simulation.id == 1000:
            self.logger.info("Total simulation done.")
            sleep(5)
            sys.exit()
        else:
            self.logger.info("No incomplete LoopSimulation found. Database integrity is intact.")



    def _delete_in_batches(self, query, batch_size: int):
        """
        Helper function to delete records in batches without using query.limit().delete().
        :param query: SQLAlchemy Query object.
        :param batch_size: Number of records to delete per batch.
        """
        deleted_count = 0

        while True:
            records = query.limit(batch_size).all()

            if not records:
                break

            for record in records:
                self.session.delete(record)
                deleted_count += 1

            self.session.commit()

        self.logger.info(f"Deleted {deleted_count} records from {query.statement.froms[0].name}.")


class CktSimulation:
    def __init__(self, circuit_name: str, loads_quantity: int, target_loads: str, target_file: str, database_path: str,
                 save_voltages_data: int, _logger: Logger):
        self.logger = _logger
        self.circuit_name = circuit_name
        self.loads_quantity = loads_quantity
        self.target_loads = target_loads
        self.target_file = target_file
        self.dss_ckt = dss.NewContext()
        self.eusd_data_list = []
        self.started_at = datetime.now().isoformat()
        self.store_data = StoreData(str(Path(database_path).resolve()), _logger)

        self.save_voltages_data = bool(save_voltages_data)

    @staticmethod
    def generate_random_ev_kwh_list(enum: Type[Enum], n: int) -> List[float]:
        values = [e.value for e in enum]
        random_list = random.choices(values, k=n)
        return random_list

    @staticmethod
    def generate_random_pv_shape_for_week(enum: Type[Enum]) -> List[float]:
        values = [e.value for e in enum]
        random_list = random.choices(values, k=7)
        return random_list

    @staticmethod
    def generate_random_phases(n: int) -> list:
        random_phases = []
        for random_phase in range(n):
            random_phases.append(random.choice([(1, 2), (2, 3), (1, 3)]))

        return random_phases

    @staticmethod
    def generate_random_ev_charger_powers(n: int) -> list:
        random_powers = []

        for r in range(n):
            random_powers.append(random.choice(EV_CHARGER_POWER_POSSIBILITIES))

        return random_powers

    @staticmethod
    def generate_random_max_power_pv(n: int) -> list:
        random_powers = []

        for r in range(n):
            random_powers.append(random.randint(MaxPowerPVKW.MIN_KW.value, MaxPowerPVKW.MAX_KW.value))

        return random_powers

    def save_voltages_and_calculate_compensation_by_day(self, simulation_id, n_day) -> float:
        self.dss_ckt.Monitors.First()
        comp_total_day = 0
        load_index = 0
        while True:
            if self.dss_ckt.Monitors.Name().find('voltage') != -1:
                v1_values = self.dss_ckt.Monitors.Channel(ColumnsMapVoltages.V1.value)
                v2_values = self.dss_ckt.Monitors.Channel(ColumnsMapVoltages.V2.value)
                v3_values = self.dss_ckt.Monitors.Channel(ColumnsMapVoltages.V3.value)

                ckt_drp_drc = DrpDrc(_logger=self.logger, eusd=self.eusd_data_list[load_index])
                drp, drc, comp = ckt_drp_drc.calculate_from_voltages(v1_values, v2_values, v3_values)
                comp_total_day += comp

                if self.save_voltages_data:
                    self.store_data.save_voltages_data(
                        simulation_id=simulation_id,
                        n_res=load_index + 1,
                        n_day=n_day + 1,
                        voltages_v1=v1_values,
                        voltages_v2=v2_values,
                        voltages_v3=v3_values
                    )

                load_index += 1

            if not self.dss_ckt.Monitors.Next() > 0:
                break

        return round(comp_total_day, 2)

    def save_energy_meters(self, simulation_id: int, n_day: int) -> None:
        self.dss_ckt.Meters.First()
        n_res_pv = 1
        n_res_ev = 1
        while True:
            if self.dss_ckt.Meters.Name().find('residence') != -1:
                if self.dss_ckt.Meters.Name().find('pv') != -1:
                    self.store_data.save_energy_meters(
                        simulation_id=simulation_id,
                        n_day=n_day + 1,
                        n_res=n_res_pv,
                        energy=self.dss_ckt.Meters.RegisterValues()[0],
                        bus='PV'
                    )
                    n_res_pv += 1
                elif self.dss_ckt.Meters.Name().find('ev') != -1:
                    self.store_data.save_energy_meters(
                        simulation_id=simulation_id,
                        n_day=n_day + 1,
                        n_res=n_res_ev,
                        energy=self.dss_ckt.Meters.RegisterValues()[0],
                        bus='EV'
                    )

                    n_res_ev += 1

            elif self.dss_ckt.Meters.Name().find('transformer') != -1:
                self.store_data.save_losses(
                    simulation_id=simulation_id,
                    n_day=n_day + 1,
                    loss=self.dss_ckt.Meters.RegisterValues()[12],
                )

            if not self.dss_ckt.Meters.Next() > 0:
                break

    def calculate_eusd_data(self) -> list:
        if not self.eusd_data_list:
            dss_ckt = dss.NewContext()
            dss_ckt.Text.Command(f'Redirect {self.target_file}')
            dss_ckt.Text.Commands(self.target_loads)
            # all_target_loads = dss.Loads.AllNames()[target_load_index_start:target_load_index_end]
            all_target_loads = []
            for load in dss_ckt.Loads.AllNames():
                if load.find('residence') != -1:
                    all_target_loads.append(load)

            loads_infos = dict()

            dss_ckt.Loads.First()
            residential_loads_kw = []
            daily_shapes = []
            while True:
                load = dss_ckt.Loads.Name()
                if load in all_target_loads:
                    loads_infos[load] = dict()
                    loads_infos[load]['kw'] = dss_ckt.Loads.kW()
                    loads_infos[load]['load_shape'] = dss_ckt.Loads.Daily()

                    dss_ckt.LoadShape.First()
                    while True:
                        load_shape = dss_ckt.LoadShape.Name()
                        if load_shape == loads_infos[load]['load_shape']:
                            loads_infos[load]['PMult'] = dss_ckt.LoadShape.PMult()
                            break

                        if not dss_ckt.LoadShape.Next() > 0:
                            break
                    residential_loads_kw.append(dss_ckt.Loads.kW())
                    daily_shapes.append(dss_ckt.Loads.Daily())

                if not dss_ckt.Loads.Next() > 0:
                    break

            eusd = []

            for load in list(loads_infos.keys()):
                eusd_component = 0

                for element in loads_infos[load]['PMult']:
                    eusd_component = eusd_component + (element * loads_infos[load]['kw']) / 60

                eusd.append(eusd_component * 30 * 0.275)

            self.eusd_data_list = [value for value in eusd]
            self.logger.info(f'EUSD data calculated: {self.eusd_data_list}')
            return self.eusd_data_list

    def execute_case_base(self):
        pass

    def execute_case_with_pl(self, pl_ev: int = 20, pl_pv: int = 20):

        self.store_data.check_and_resolve_database_integrity()
        self.logger.info('---- Starting Simulation LOOP ----')
        self.calculate_eusd_data()
        self.logger.info(f'Penetration level EV: {pl_ev}%')
        self.logger.info(f'Penetration level PV: {pl_pv}%')

        # Verify if penetration level is OK
        if pl_ev not in PL_PERCENTAGES and pl_pv not in PL_PERCENTAGES:
            raise Exception('Penetration level is not valid')

        # Calculate the quantity of PV and EV based on penetration level
        ev_qty = round(self.loads_quantity * pl_ev / 100)
        pv_qty = round(self.loads_quantity * pl_pv / 100)

        try:
            # Generate random data
            random_target_load_ev = random.sample(range(1, self.loads_quantity + 1), self.loads_quantity)
            random_target_load_pv = random.sample(range(1, self.loads_quantity + 1), self.loads_quantity)
            random_ev_kwh = self.generate_random_ev_kwh_list(EvKwh, ev_qty)
            random_pv_shapes_possibilities = self.generate_random_pv_shape_for_week(PVShapesPossibilities)
            random_phases_ev = self.generate_random_phases(ev_qty)
            random_phases_pv = self.generate_random_phases(pv_qty)
            random_ev_chargers_power = self.generate_random_ev_charger_powers(ev_qty)
            random_max_power_pv = self.generate_random_max_power_pv(pv_qty)
            random_ev_shapes_by_day = dict()
            for index_ev in range(1, 8):
                random_ev_shapes_by_day[index_ev] = random.sample(list(range(1, 5001)), ev_qty)

            loop_simulation_started_at = datetime.now()
            # Store Loop Simulation data in database
            loop_simulation_id = self.store_data.create_loop_simulation(
                started_at=loop_simulation_started_at,
                random_target_load_ev=str(random_target_load_ev),
                random_target_load_pv=str(random_target_load_pv),
                random_ev_kwh=str(random_ev_kwh),
                random_pv_shapes_possibilities=json.dumps(random_pv_shapes_possibilities),
                random_phases_ev=str(random_phases_ev),
                random_phases_pv=str(random_phases_pv),
                random_ev_chargers_power=str(random_ev_chargers_power),
                random_max_power_pv=str(random_max_power_pv),
                random_ev_shapes_by_day=str(random_ev_shapes_by_day)

            )
            for control in ('no_control', 'voltvar', 'voltwatt'):  # Controls Loop
                comp_total = 0
                simulation_started_at = datetime.now()

                # Store Simulation data in database
                simulation_id = self.store_data.save_simulation(
                    loop_simulation_id=loop_simulation_id,
                    control_mode=control,
                    started_at=simulation_started_at
                )

                for n_day, pv_shape_possibility in enumerate(random_pv_shapes_possibilities):  # Days Loop
                    self.dss_ckt = dss.NewContext()

                    # self.dss_ckt._enable_exceptions(do_enable=False)
                    self.dss_ckt.Basic.ClearAll()
                    self.dss_ckt.Basic.DataPath('./')
                    self.dss_ckt.Text.Command(f'Redirect {self.target_file}')

                    # Verify if the target day is a Weekend day.
                    if n_day == 6:
                        self.target_loads = self.target_loads.replace('-WE', '-SA')
                    elif n_day == 7:
                        self.target_loads = self.target_loads.replace('-WE', '-SU')

                    self.dss_ckt.Text.Commands(self.target_loads)  # Insert Loads

                    csv_data = pd.read_csv('data/electrical_vehicles/ev_shapes_charge.csv', header=None)
                    # EVs Loop
                    for i in range(1, ev_qty + 1):
                        column_index = random_ev_shapes_by_day[n_day + 1][i - 1] - 1
                        column_values = csv_data[column_index].tolist()
                        mult_values = ' '.join(map(str, column_values))
                        self.dss_ckt.Text.Command(
                            f'New loadshape.shape_ev{i} '
                            f'npts=1440 '
                            f'minterval=1 '
                            f'mult=({mult_values})'
                        )

                        phase_a, phase_b = random_phases_ev[i - 1]

                        self.dss_ckt.Text.Command(
                            f'New Storage.ev_{i} '
                            f'bus1=EVRES{random_target_load_ev[i - 1]}.{phase_a}.{phase_b} '
                            'kV=0.220 '
                            f'kWhrated={random_ev_kwh[i - 1]} '
                            f'kW={random_ev_chargers_power[i - 1]} '
                            'pf=0.92 '
                            'conn=delta '
                            'kvarmax=0.44 '
                            'kvarmaxabs=0.44 '
                            'dispmode=follow '
                            f'daily=shape_ev{i} '
                            'model=1 '
                            'phases=2 '
                            'State=CHARGING '
                            '%stored=0'
                        )

                        if control == 'voltwatt':
                            self.dss_ckt.Text.Command(
                                f'New InvControl.voltwatt_ev{i} '
                                'mode=voltwatt '
                                'voltage_curvex_ref=rated '
                                'voltwattCH_curve=vw_curve_ev '
                                'refReactivePower=VARMAX '
                                'monVoltageCalc=MAX '
                                'RiseFallLimit=-1 '
                                'voltwattYaxis=PAVAILABLEPU '
                                'voltageChangeTolerance=0.01 '
                                'activePChangeTolerance=0.01 '
                                'deltaP_factor=0.1 '
                                'eventLog=yes '
                                'enabled=true '
                                f'DERlist=(Storage.ev_{i})'
                            )
                        elif control == 'voltvar':
                            self.dss_ckt.Text.Command(
                                f'New InvControl.voltvar_ev{i} '
                                'mode=voltvar '
                                'voltage_curvex_ref=rated '
                                'refReactivePower=VARMAX '
                                'vvc_curve1=vv_curve_ev '
                                'voltageChangeTolerance=0.01 '
                                'varChangeTolerance=0.01 '
                                'deltaQ_factor=-1 '
                                'eventLog=yes '
                                'enabled=true '
                                f'DERlist=(Storage.ev_{i})'
                            )

                    # PVs Loop
                    for i in range(1, pv_qty + 1):
                        phase_a, phase_b = random_phases_pv[i - 1]
                        self.dss_ckt.Text.Command(
                            f'New PvSystem.pv_{i} '
                            f'bus1=PVRES{random_target_load_pv[i - 1]}.{phase_a}.{phase_b} '
                            'phases=2 '
                            'conn=delta '
                            'kvarmax=0.44 '
                            'kvarmaxabs=0.44 '
                            'enabled=true '
                            'kV=0.220 '
                            f'kVA={random_max_power_pv[i - 1] + 4} '
                            f'Pmpp={random_max_power_pv[i - 1]} '
                            'pf=0.92 '
                            f'daily={pv_shape_possibility} '
                            '%cutIn=0.1 '
                            '%cutOut=0.1'
                        )

                        if control == 'voltwatt':
                            self.dss_ckt.Text.Command(
                                f'New InvControl.voltwatt_pv{i} '
                                'mode=voltwatt '
                                'voltage_curvex_ref=rated '
                                'voltwatt_curve=vw_curve_pv '
                                'refReactivePower=VARMAX '
                                'monVoltageCalc=MAX '
                                'RiseFallLimit=-1 '
                                'voltwattYaxis=PAVAILABLEPU '
                                'voltageChangeTolerance=0.01 '
                                'activePChangeTolerance=0.01 '
                                'deltaP_factor=0.1 '
                                'eventLog=yes '
                                'enabled=true '
                                f'DERlist=(PvSystem.pv_{i})'
                            )
                        elif control == 'voltvar':
                            self.dss_ckt.Text.Command(
                                f'New InvControl.voltvar_pv{i} '
                                'mode=voltvar '
                                'voltage_curvex_ref=rated '
                                'refReactivePower=VARMAX '
                                'vvc_curve1=vv_curve_pv '
                                'voltageChangeTolerance=0.01 '
                                'varChangeTolerance=0.01 '
                                'deltaQ_factor=0.1 '
                                'eventLog=yes '
                                'enabled=true '
                                f'DERlist=(PvSystem.pv_{i})'
                            )

                    # Monitors and Energy Meters Loop
                    for i in range(1, self.loads_quantity + 1):
                        self.dss_ckt.Text.Command(
                            f'New Monitor.residence{i}_PV_{pl_pv}_EV_{pl_ev}_{control}'
                            f'_voltage_day_{n_day + 1} '
                            f'element=Load.residence{i} terminal=1 mode=0'
                        )
                        self.dss_ckt.Text.Command(
                            f'New Monitor.residence{i}_PV_{pl_pv}_EV_{pl_ev}_{control}'
                            f'_power_day_{n_day + 1} '
                            f'element=Load.residence{i} terminal=1 mode=1 ppolar=no'
                        )
                        self.dss_ckt.Text.Command(
                            f'New EnergyMeter.residence{i}_PV_{pl_pv}_{control}_day_{n_day + 1} '
                            f'element=line.LINE_PV{i} terminal=1'
                        )

                        self.dss_ckt.Text.Command(
                            f'New EnergyMeter.residence{i}_EV_{pl_ev}_{control}_day_{n_day + 1} '
                            f'element=line.LINE_EV{i} terminal=1'
                        )

                    # Energy Meter Transformer
                    self.dss_ckt.Text.Command(
                        f'New Energymeter.transformer_percentage_PV_{pl_pv}_EV_{pl_ev}_{control}_day_{n_day + 1} '
                        f'element=Transformer.{self.circuit_name} terminal=1'
                    )

                    # Definitions and Solve
                    self.dss_ckt.Text.Command('Set voltagebases=[13.8 0.220]')
                    self.dss_ckt.Text.Command('Calcvoltagebases')
                    self.dss_ckt.Text.Command('Set mode=daily')
                    self.dss_ckt.Text.Command('Set stepsize=1m')
                    self.dss_ckt.Text.Command('Set number=1440')
                    self.dss_ckt.Text.Command('Set maxcontroliter=1000')
                    self.dss_ckt.Text.Command('Set maxiterations=1000')
                    self.dss_ckt.Text.Command('Set controlmode=time')
                    self.logger.info(f'Loop Simulation: {loop_simulation_id} - Solving case')
                    self.dss_ckt.Solution.Solve()
                    self.logger.info(f'Loop Simulation: {loop_simulation_id} - Solved!')
                    if not self.dss_ckt.Solution.Converged():
                        raise Exception('Solution not converged')

                    # self.dss_ckt.Solution.Cleanup()
                    self.logger.info(
                        f'Loop Simulation: {loop_simulation_id} - Calculating compensation and saving voltages')
                    comp_total_day = self.save_voltages_and_calculate_compensation_by_day(simulation_id, n_day)
                    self.logger.info(
                        f'Loop Simulation: {loop_simulation_id} - Calculate compensation and save voltages done!')
                    self.logger.info(f'Loop Simulation: {loop_simulation_id} - Saving energy meters data')
                    self.save_energy_meters(simulation_id, n_day)
                    self.logger.info(f'Loop Simulation: {loop_simulation_id} - Energy meters data saved!')

                    self.logger.info(
                        f'Loop Simulation: {loop_simulation_id} - Daily simulation done. Day: {n_day + 1}, control: {control}, compensation: R$ {comp_total_day}'
                    )

                    comp_total += comp_total_day

                self.logger.info(f'Loop Simulation: {loop_simulation_id} - Saving total compensation data')
                self.store_data.save_compensation(simulation_id, compensation=comp_total)
                self.logger.info(f'Loop Simulation: {loop_simulation_id} - Total compensation saved!')

                simulation_finished_at = datetime.now()

                delta_ = simulation_finished_at - simulation_started_at
                formatted_duration_ = f"{delta_.seconds // 3600}h {delta_.seconds % 3600 // 60} min {delta_.seconds % 60} s"
                self.logger.info(
                    f'Loop Simulation: {loop_simulation_id} - 7 days simulation finished! Elapsed time: {formatted_duration_}')

                self.store_data.insert_simulation_finished_at(
                    simulation_id=simulation_id,
                    finished_at=simulation_finished_at
                )
                self.logger.info(
                    f'Loop Simulation: {loop_simulation_id} - Compensation with {control}: R$ {round(comp_total, 2)}')

            self.logger.info(f'---- Loop simulation: {loop_simulation_id} finished -----')
            loop_simulation_finished_at = datetime.now()
            self.store_data.insert_loop_simulation_finished_at(
                loop_simulation_id=loop_simulation_id,
                finished_at=loop_simulation_finished_at
            )

            delta = loop_simulation_finished_at - loop_simulation_started_at
            formatted_duration = f"{delta.seconds // 3600}h {delta.seconds % 3600 // 60} min {delta.seconds % 60} s"
            self.logger.info(f'Elapsed time: {formatted_duration}')

        except Exception as e:
            self.logger.error(f'Error in simulation: {e}')
