import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Union
import pandas as pd


class Log:
    """
    A class used to manage the logging functionality of the application.

    Attributes:
        dir_path (str): The default path where log files are stored.
        logger (logging.Logger): The logger instance.
        logs_path (Path): The path where log files will be stored.

    Methods:
        set_logger_stdout(name: str) -> logging.Logger: Set up a logger to output logs to stdout.
        set_logger_file(logger_name: str) -> logging.Logger: Set up a logger to output logs to a file.
    """

    dir_path = os.path.dirname(__file__) + "/../logs"

    def __init__(self, logs_path=dir_path):
        self.logger = None
        self.logs_path = logs_path

    def set_logger_stdout(self, name):
        """
        Set up a logger to output logs to stdout.

        Args:
            name (str): The name of the logger instance.

        Returns:
            logging.Logger: The logger instance.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        return self.logger

    def set_logger_file(self, logger_name):
        """
        Set up a logger to output logs to a file.

        Args:
            logger_name (str): The name of the logger instance.

        Returns:
            logging.Logger: The logger instance.
        """
        self.logs_path = Path(self.logs_path)
        if not os.path.exists(self.logs_path):
            os.makedirs(self.logs_path, exist_ok=True)

        self.logger = logging.getLogger(logger_name)
        path = Path(self.logs_path, logger_name + '.log')
        file_handler = logging.handlers.RotatingFileHandler(filename=str(path),
                                                            mode='a',
                                                            maxBytes=10000000,
                                                            backupCount=0)
        formatter = logging.Formatter('[ %(asctime)s ] %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.DEBUG)

        return self.logger

    def set_logger_file_and_stdout(self, logger_name):
        """
        Set up a logger to output logs both to stdout and a file.

        Args:
            logger_name (str): The name of the logger instance.

        Returns:
            logging.Logger: The logger instance.
        """
        self.set_logger_stdout(logger_name)
        self.set_logger_file(logger_name)

        return self.logger


class HandleFiles:

    def __init__(self):
        self.target_folder_path = None
        self.new_results_folder_path = None
        self.file_path = os.path.dirname(__file__)
        self.results_path = self.file_path + '/../results/'
        if not os.path.exists(Path(self.results_path)):
            os.mkdir(Path(self.results_path))

    def get_target_file_path(self, folder, file) -> Union[str, bool]:

        if os.path.exists(Path(self.file_path + '/../dss/' + folder + '/' + file)):
            self.target_folder_path = self.file_path + '/../dss/' + folder
            return str(Path(self.target_folder_path + '/' + file))
        return False

    def get_target_folder_path(self) -> str:

        return str(Path(self.target_folder_path))

    def set_folder_in_results(self, new_folder: str) -> None:
        self.new_results_folder_path = self.results_path + new_folder

        if os.path.exists(Path(self.new_results_folder_path)):
            return

        os.mkdir(Path(self.results_path + new_folder))

    def get_folder_path_in_results(self) -> str:
        return str(Path(self.new_results_folder_path))

    def remove_results_folder_content(self) -> None:

        files = os.listdir(self.new_results_folder_path)

        for file in files:
            file_path = os.path.join(self.new_results_folder_path, file)
            os.remove(file_path)

    def remove_file(self, file_name: str) -> bool:
        try:
            os.remove(Path(self.new_results_folder_path + '/' + file_name))
            return True
        except FileNotFoundError:
            return False

    def remove_folder(self) -> bool:
        try:
            os.rmdir(Path(self.new_results_folder_path))
            return True
        except FileNotFoundError:
            return False


class HandleEvData:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def process_file(self):
        df = pd.read_csv(self.input_file, header=None)
        df = df * -1
        df.to_csv(self.output_file, header=False, index=False)
        return f"Arquivo modificado salvo em: {self.output_file}"


if __name__ == '__main__':
    input_file_path = r'C:\Users\rapha\Documentos\Acadêmico\UFAM\PPGEE\Dissertação\OpenDSS\Github\PyDSS\src\data\electrical_vehicles\ev_shapes.csv'
    output_file_path = r'C:\Users\rapha\Documentos\Acadêmico\UFAM\PPGEE\Dissertação\OpenDSS\Github\PyDSS\src\data\electrical_vehicles\ev_shapes_charge.csv'

    handler = HandleEvData(input_file_path, output_file_path)
    print(handler.process_file())
