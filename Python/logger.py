from datetime import datetime
from pathlib import Path
import logging

class Logger:
    def __init__(self, log_path: str):
        self.log_file_name = self.generate_log_file_name()
        self.log_format = "[%(asctime)s][%(levelname)s] %(message)s"
        self.date_format = "%Y-%m-%d %H:%M:%S"

        path = self.generate_log_file_path(log_path)
        path = path.joinpath(self.log_file_name)
        self.log_file_path = str(path)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter(self.log_format, self.date_format)

        file_handler = logging.FileHandler(self.log_file_path, mode='w')
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)
        
    def generate_log_file_name(self):
        now = datetime.now()
        time_stamp = now.strftime("%Y_%m_%d__%H_%M_%S")
        return f"{time_stamp}_log.txt"
    
    def generate_log_file_path(self, log_path: str):
        path = Path(log_path)
        if not path.exists():
            raise FileNotFoundError(f"The path '{log_path}' does not exist.")

        if not path.is_dir():
            raise NotADirectoryError(f"The path '{log_path}' is not a directory")
        
        return path
    
    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)