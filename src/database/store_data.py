import csv
import os.path
import re

import pandas as pd
from pathlib import Path
from datetime import datetime
from src.database.models import Session, Simulation, VoltageData, PowerData, DrpDrc, Loss, TotalComp, EusdLoads
from logging import Logger


class StoreData:
    def __init__(self, logger: Logger):
        self.session = Session()
        self.logger = logger
        self.control_modes = ('no_control', 'voltwatt_on', 'voltvar_on')
        self.pv_ev_percentages = ('pv_ev_0', 'pv_ev_20', 'pv_ev_40', 'pv_ev_60', 'pv_ev_80', 'pv_ev_100')

    @staticmethod
    def read_simulation_detail(results_path) -> dict:
        file_path = Path(results_path + '/simulation_details.xlsx').resolve()

        df = pd.read_excel(file_path, sheet_name='for_each_residence')
        columns = [
            'random_target_loads',
            'random_ev_kwh',
            'random_phases',
            'random_ev_chargers_power',
            'random_max_power_pv'
        ]
        data = {col: df[col].tolist() for col in columns}

        df = pd.read_excel(file_path, sheet_name='simulation_time')

        data.update(
            {
                'started_at': df['started_at'].iloc[0],
                'finished_at': df['finished_at'].iloc[0],
             }
        )

        df = pd.read_excel(file_path, sheet_name='pv_shape_possibilities')

        data.update(
            {
                'random_pv_shape_possibilities': df['shape'].tolist()
            }
        )

        return data

    def insert_losses_values(self, simulation_id, results_path):
        all_losses = []
        file_path = Path(results_path) / 'energy_meters.xlsx'
        df = pd.read_excel(file_path, sheet_name='LOSSES')

        for control_mode in self.control_modes:
            df_filtered = df[df['control_mode'] == control_mode]
            n_day = 1

            for _, row in df_filtered.iterrows():
                new_losses = Loss(
                    simulation_id=simulation_id,
                    control_mode=control_mode,
                    percentage=int(row['percentage']),
                    n_day=n_day,
                    loss=float(row['losses (kWh)'])
                )
                all_losses.append(new_losses)
                n_day += 1
                if n_day == 8:
                    n_day = 1

        self.session.bulk_save_objects(all_losses)
        self.session.commit()

    def insert_total_comp(self, simulation_id, results_path):
        all_total_comp = []
        for control_mode in self.control_modes:
            df = pd.read_excel(Path(results_path + '/comp_total.xlsx'), sheet_name=control_mode)
            new_total_comp = TotalComp(
                simulation_id=simulation_id,
                control_mode=control_mode,
                total_comp_20=float(df['20%'][0]),
                total_comp_40=float(df['40%'][0]),
                total_comp_60=float(df['60%'][0]),
                total_comp_80=float(df['80%'][0]),
                total_comp_100=float(df['100%'][0])
            )
            if df['0%'][0] != '-':
                new_total_comp.total_comp_0 = float(df['0%'])
            all_total_comp.append(new_total_comp)
        self.session.bulk_save_objects(all_total_comp)
        self.session.commit()

    def insert_drp_drc_from_file(self, simulation_id, control_mode, file_path, percentage, n_res, n_day):
        df = pd.read_excel(Path(file_path))
        drp = float(df['DRP(%)'][0])
        drc = float(df['DRC(%)'][0])
        comp = float(df['COMP(R$)'][0])

        new_drp_drc = DrpDrc(
            simulation_id=simulation_id,
            control_mode=control_mode,
            percentage=percentage,
            n_res=n_res,
            n_day=n_day,
            drp=drp,
            drc=drc,
            comp=comp
        )
        self.session.add(new_drp_drc)
        self.session.commit()

    def insert_voltages_data_from_file(self, simulation_id, control_mode, file_path, percentage, n_res, n_day):
        all_voltage_data = []
        with open(Path(file_path), 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for index, row in enumerate(csv_reader):
                if index == 0:
                    continue

                new_voltage_data = VoltageData(
                    simulation_id=simulation_id,
                    control_mode=control_mode,
                    percentage=percentage,
                    n_res=n_res,
                    n_day=n_day,
                    hour=int(row[0]),
                    t_sec=float(row[1]),
                    v1=float(row[2]),
                    v_angle_1=float(row[3]),
                    v2=float(row[4]),
                    v_angle_2=float(row[5]),
                    v3=float(row[6]),
                    v_angle_3=float(row[7]),
                    v4=float(row[8]),
                    v_angle_4=float(row[9]),
                    i1=float(row[10]),
                    i_angle_1=float(row[11]),
                    i2=float(row[12]),
                    i_angle_2=float(row[13]),
                    i3=float(row[14]),
                    i_angle_3=float(row[15]),
                    i4=float(row[16]),
                    i_angle_4=float(row[17])
                )
                all_voltage_data.append(new_voltage_data)
        self.session.bulk_save_objects(all_voltage_data)
        self.session.commit()

    def insert_powers_data_from_file(self, simulation_id, control_mode, file_path, percentage, n_res, n_day):
        all_power_data = []
        with open(Path(file_path), 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for index, row in enumerate(csv_reader):
                if index == 0:
                    continue

                new_power_data = PowerData(
                    simulation_id=simulation_id,
                    control_mode=control_mode,
                    percentage=percentage,
                    n_res=n_res,
                    n_day=n_day,
                    hour=int(row[0]),
                    t_sec=float(row[1]),
                    p1=float(row[2]),
                    q1=float(row[3]),
                    p2=float(row[4]),
                    q2=float(row[5]),
                    p3=float(row[6]),
                    q3=float(row[7]),
                    p4=float(row[8]),
                    q4=float(row[9])
                )
                all_power_data.append(new_power_data)
        self.session.bulk_save_objects(all_power_data)
        self.session.commit()

    def insert_data_from_results_folder(self, circuit_name: str, results_path: str):
        if not os.path.exists(results_path):
            self.logger.debug('results path does not exist')
            return

        data = self.read_simulation_detail(results_path)

        if not data:
            self.logger.debug('simulation start data not found')
            return

        new_simulation = Simulation(
            circuit_name=circuit_name,
            started_at=datetime.fromisoformat(data['started_at']),
            finished_at=datetime.fromisoformat(data['finished_at']),
            random_target_loads=str(data['random_target_loads']),
            random_ev_kwh=str(data['random_ev_kwh']),
            random_pv_shape_possibilities=str(data['random_pv_shape_possibilities']),
            random_phases=str(data['random_phases']),
            random_ev_chargers_power=str(data['random_ev_chargers_power']),
            random_max_power_pv=str(data['random_max_power_pv'])
        )

        self.session.add(new_simulation)
        self.session.commit()

        self.insert_losses_values(new_simulation.id, results_path)
        self.insert_total_comp(new_simulation.id, results_path)

        for control_mode in self.control_modes:
            for pv_ev_percentage in self.pv_ev_percentages:
                inside_results = f'./{results_path}/{control_mode}/{pv_ev_percentage}'
                if pv_ev_percentage == 'pv_ev_0' and control_mode != 'no_control':
                    continue

                for file in os.listdir(Path(inside_results)):
                    file_path = inside_results + '/' + file

                    n_res = re.search(r'residence(\d+)_', file).group(1)
                    percentage = re.search(r'percentage_(\d+)_', file).group(1)
                    n_day = re.search(r'day_(\d+)_', file).group(1)

                    if file.find('drp_drc') != -1:
                        self.insert_drp_drc_from_file(
                            new_simulation.id, control_mode, file_path, percentage, n_res, n_day
                        )
                    elif file.find('voltage') != -1:
                        self.insert_voltages_data_from_file(
                            new_simulation.id, control_mode, file_path, percentage,
                            n_res, n_day
                        )
                    else:
                        self.insert_powers_data_from_file(
                            new_simulation.id, control_mode, file_path, percentage, n_res,
                            n_day
                        )

    def insert_ckt_eusd_loads(self, circuit_name: str, results_path: str):
        eusd_loads = []
        circuit_data = self.session.query(EusdLoads).filter(EusdLoads.circuit_name == circuit_name).first()
        if circuit_data is None:
            with open(Path(results_path + '/eusd_loads.csv'), 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for index, row in enumerate(csv_reader):
                    new_eusd_load = EusdLoads(
                        circuit_name=circuit_name,
                        n_res=index + 1,
                        eusd=float(row[0]),
                    )
                    eusd_loads.append(new_eusd_load)
            self.session.bulk_save_objects(eusd_loads)
            self.session.commit()

    def erase_data(self):
        pass
