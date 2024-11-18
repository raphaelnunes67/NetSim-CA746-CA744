import pandas as pd
from pathlib import Path
from typing import Tuple


class DrpDrc:
    """
    The DrpDrc class is designed for calculating DRP (Duration of Reduction of Power),
    DRC (Duration of Reduction of Capacity), and Compensation values based on voltage data.
    These calculations are essential for power quality analysis.

    Attributes are initialized based on various voltage thresholds and a default expected uninterrupted
    service duration (EUSD) value. The class also includes methods for calculating these values from a CSV file.
    """

    def __init__(self, _logger, voltage_nominal: float = 127.0, voltage_adequate_max: float = 133.0,
                 voltage_adequate_min: float = 117.0, voltage_precarious_bottom_min: float = 110.0,
                 voltage_precarious_bottom_max: float = 117.0, voltage_precarious_top_min: float = 133.0,
                 voltage_precarious_top_max: float = 135.0, voltage_critical_max: float = 135.0,
                 voltage_critical_min: float = 110.0, eusd: float = 1.0):
        """
        Initializes the DrpDrc object with various voltage thresholds and EUSD value.

        Args:
            voltage_nominal (float): The standard voltage level for the system, default is 127.0 volts.
            voltage_adequate_max (float): Maximum voltage threshold for 'adequate' range, default is 133.0 volts.
            voltage_adequate_min (float): Minimum voltage threshold for 'adequate' range, default is 117.0 volts.
            voltage_precarious_bottom_min (float): Minimum threshold for lower precarious range, default is 110.0 volts.
            voltage_precarious_bottom_max (float): Maximum threshold for lower precarious range, default is 117.0 volts.
            voltage_precarious_top_min (float): Minimum threshold for upper precarious range, default is 133.0 volts.
            voltage_precarious_top_max (float): Maximum threshold for upper precarious range, default is 135.0 volts.
            voltage_critical_max (float): Maximum voltage threshold for critical range, default is 135.0 volts.
            voltage_critical_min (float): Minimum voltage threshold for critical range, default is 110.0 volts.
            eusd (float): Expected Uninterrupted Service Duration, default is 1.0.
            _logger(Logger): Logger object for printing log messages.

        The per unit (pu) values of each voltage threshold are also calculated as part of the initialization.
        """
        self.logger = _logger
        self.voltage_nominal = voltage_nominal
        self.eusd = eusd

        self.voltage_adequate_max = voltage_adequate_max
        self.voltage_adequate_min = voltage_adequate_min

        self.voltage_precarious_bottom_min = voltage_precarious_bottom_min
        self.voltage_precarious_bottom_max = voltage_precarious_bottom_max
        self.voltage_precarious_top_min = voltage_precarious_top_min
        self.voltage_precarious_top_max = voltage_precarious_top_max

        self.voltage_critical_max = voltage_critical_max
        self.voltage_critical_min = voltage_critical_min

        self.voltage_adequate_max_pu = round(voltage_adequate_max / voltage_nominal, 3)
        self.voltage_adequate_min_pu = round(voltage_adequate_min / voltage_nominal, 3)

        self.voltage_precarious_bottom_min_pu = round(voltage_precarious_bottom_min / voltage_nominal, 3)
        self.voltage_precarious_bottom_max_pu = round(voltage_precarious_bottom_max / voltage_nominal, 3)
        self.voltage_precarious_top_min_pu = round(voltage_precarious_top_min / voltage_nominal, 3)
        self.voltage_precarious_top_max_pu = round(voltage_precarious_top_max / voltage_nominal, 3)

        self.voltage_critical_max_pu = round(voltage_critical_max / voltage_nominal, 3)
        self.voltage_critical_min_pu = round(voltage_critical_min / voltage_nominal, 3)

        self.drp_limit = 3 / 100
        self.drc_limit = 0.5 / 100
        self.total_measures = 1008

    def calculate_from_csv(self, file_path: str, columns_headers: list, n_days: int) -> Tuple[float, float, float]:
        """
        Calculates DRP, DRC and Compensation values. It receives as input a .csv file that must contain the voltage data
         and a list containing the names of the column headers with the voltage values.

        Args:
            file_path (str): .csv file location
            columns_headers (list): List with headers which indicate the columns of voltage values
            n_days (int): Number of days to calculate DRP and DRC

        Returns:
           Tuple[float, float, float]: A tuple with DRP, DRC and Compensation values
        """

        data = pd.read_csv(Path(file_path))

        nlp_list: list = []
        nlc_list: list = []

        for element in columns_headers:

            voltages = data[element]

            nlp = 0
            nlc = 0

            for day in range(n_days):
                for measure_time in range(0, 1440, 10):
                    target_voltage = voltages[measure_time]
                    if self.voltage_precarious_bottom_min <= target_voltage < self.voltage_precarious_bottom_max:
                        nlp = nlp + 1
                        # self.logger.debug(
                        #     f'precarious voltage '
                        #     f'({self.voltage_precarious_bottom_min}<= voltage <={self.voltage_precarious_bottom_max}): '
                        #     f'{target_voltage} on file: {file_path}')

                    elif self.voltage_precarious_top_min <= target_voltage <= self.voltage_precarious_top_max:
                        nlp = nlp + 1
                        # self.logger.debug(
                        #     f'precarious voltage '
                        #     f'({self.voltage_precarious_top_min}<= voltage <={self.voltage_precarious_top_max}): '
                        #     f'{target_voltage} on file: {file_path}')

                    elif target_voltage < self.voltage_critical_min:
                        # self.logger.debug(f'critical voltage (<{self.voltage_critical_min}) in file: {file_path}')
                        nlc = nlc + 1

                    elif target_voltage > self.voltage_critical_max:
                        nlc = nlc + 1
                        # self.logger.debug(f'critical voltage (>{self.voltage_critical_max}) in file: {file_path}')

            nlp_list.append(nlp)
            nlc_list.append(nlc)

        # print(f'NLP list: {nlp_list}')
        # print(f'NLC list: {nlc_list}')

        nlp = max(
            nlp_list)  # highest value between the phases of the number of readings located in the precarious range
        nlc = max(nlc_list)  # highest value between the phases of the number of readings located in the critical range

        drp = round((nlp / 1008) * 100, 3)
        drc = round((nlc / 1008) * 100, 3)

        if drp <= self.drp_limit:
            k1 = 0
        else:
            k1 = 3

        if drc <= self.drc_limit:
            k2 = 0
        elif (drc > self.drc_limit) and (self.voltage_nominal < 2.3 * 10 ** 3):
            k2 = 7
        elif (drc > self.drc_limit) and (2.3 * 10 ** 3 <= self.voltage_nominal < 69 * 10 ** 3):
            k2 = 5
        else:
            k2 = 3

        comp = round(((((drp - self.drp_limit) / 100) * k1) + (((drc - self.drc_limit) / 100) * k2)) * self.eusd, 2)

        return drp, drc, comp

    def calculate_from_voltages(self, v1_values: list, v2_values: list, v3_values: list) -> Tuple[float, float, float]:
        nlp_list: list = []
        nlc_list: list = []

        for voltage in (v1_values, v2_values, v3_values):
            nlp = 0
            nlc = 0
            for measure_time in range(0, 1440, 10):

                target_voltage = voltage[measure_time]
                if self.voltage_precarious_bottom_min <= target_voltage < self.voltage_precarious_bottom_max:
                    nlp = nlp + 1

                elif self.voltage_precarious_top_min <= target_voltage <= self.voltage_precarious_top_max:
                    nlp = nlp + 1

                elif target_voltage < self.voltage_critical_min:
                    nlc = nlc + 1

                elif target_voltage > self.voltage_critical_max:
                    nlc = nlc + 1

                nlp_list.append(nlp)
                nlc_list.append(nlc)

        nlp = max(
            nlp_list)  # highest value between the phases of the number of readings located in the precarious range
        nlc = max(nlc_list)  # highest value between the phases of the number of readings located in the critical range

        drp = round((nlp / 1008) * 100, 3)
        drc = round((nlc / 1008) * 100, 3)

        if drp <= self.drp_limit:
            k1 = 0
        else:
            k1 = 3

        if drc <= self.drc_limit:
            k2 = 0
        elif (drc > self.drc_limit) and (self.voltage_nominal < 2.3 * 10 ** 3):
            k2 = 7
        elif (drc > self.drc_limit) and (2.3 * 10 ** 3 <= self.voltage_nominal < 69 * 10 ** 3):
            k2 = 5
        else:
            k2 = 3

        comp = round(((((drp - self.drp_limit) / 100) * k1) + (((drc - self.drc_limit) / 100) * k2)) * self.eusd, 2)

        return drp, drc, comp


if __name__ == '__main__':
    drp_drc_calc = DrpDrc()

    drp, drc, comp = drp_drc_calc.calculate_from_csv(
        '../dss/CA746/REDE1_Mon_carga26_pv_ve_percentage_100_voltvar_off_voltage_1.csv', ['V1'])

    print(f'DRP: {drp}, DRC: {drc}, compensação(R$): {comp}')
