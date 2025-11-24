from logging.logger import Logger, get_logger
from enum import Enum

class PipelineTag(Enum):
    INGESTION = "INGESTION"
    EXTRACTION = "EXTRACTION"
    TRANSFORM = "TRANSFORM"
    DOMAIN = "DOMAIN"
    DB = "DB"
    TRAINING = "TRAINING"
    GENERAL = "GENERAL"

class PipelineLoggingService:
    """
    Servicio de logging especializado para el pipeline Superintendencia.
    """

    def __init__(self, logger: Logger = None):
        self.logger = logger or get_logger()

    def log(self, tag: PipelineTag, message: str):
        self.logger.info(f"[{tag.value}] {message}")

    def debug(self, tag: PipelineTag, message: str):
        self.logger.debug(f"[{tag.value}] {message}")

    def warning(self, tag: PipelineTag, message: str):
        self.logger.warning(f"[{tag.value}] {message}")

    def error(self, tag: PipelineTag, message: str):
        self.logger.error(f"[{tag.value}] {message}")

    def exception(self, tag: PipelineTag, message: str):
        self.logger.exception(f"[{tag.value}] {message}")