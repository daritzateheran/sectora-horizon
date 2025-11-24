import logging
import os
import time
from typing import Optional
from config import DATA_PATH

class Logger:
    def __init__(
        self,
        name: str = "superintendencia",
        level: int = logging.DEBUG,
        log_to_file: bool = False,
        log_file_path: Optional[str] = None
    ):
        self.logger = logging.getLogger(name)

        if not self.logger.handlers:
            self.logger.setLevel(level)

            # Console handler
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

            # Optional file handler
            if log_to_file:
                path = log_file_path or f"{DATA_PATH}/logs/{name}.log"
                os.makedirs(os.path.dirname(path), exist_ok=True)
                file_handler = logging.FileHandler(path)
                file_formatter = logging.Formatter(
                    '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
                )
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def exception(self, message: str):
        self.logger.exception(message)

class Timer:
    def __init__(self, name: str, logger: Optional[Logger] = None):
        self.name = name
        self.logger = logger or Logger(name)

    def __enter__(self):
        self.start = time.time()
        self.logger.debug(f"[{self.name}] - Starting...")

    def __exit__(self, exc_type, exc_value, traceback):
        elapsed = time.time() - self.start
        self.logger.debug(f"[{self.name}] - Completed in {elapsed:.2f} seconds")

_logger_instance: Optional[Logger] = None

def get_logger() -> Logger:
    global _logger_instance

    if _logger_instance is None:
        _logger_instance = Logger(
            name="superintendencia",
            log_to_file=True,
        )

    return _logger_instance
