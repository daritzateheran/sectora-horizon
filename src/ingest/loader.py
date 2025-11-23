from typing import Optional
from ingest.errors import UnsupportedSourceError
from ingest.dataset import Dataset, SourceType
from ingest.fetch.raw import RawPort
from ingest.fetch.metadata import BaseMetadata

class RawDatasetLoader:

    def __init__(self, csv_adapter: RawPort, sct_adapter: RawPort, excel_adapter: RawPort):
        self.csv = csv_adapter
        self.sct = sct_adapter
        self.excel = excel_adapter

    def load(self, ds: Dataset) -> list[dict]:
        """
        Carga todos los registros del dataset según su tipo de origen.
        """
        if ds.source == SourceType.CSV:
            return self.csv.fetchRaw(ds.path)
        if ds.source == SourceType.EXCEL:
            return self.excel.fetchRaw(ds.path)
        if ds.source == SourceType.SOCRATA:
            #  paginación interna
            return self.sct.fetchRaw(ds.resource_id)
        raise UnsupportedSourceError(ds.source)


    def metadata(self, ds: Dataset) -> Optional[BaseMetadata]:
        """
        Devuelve metadata del origen si está disponible.
        """
        if ds.source == SourceType.CSV:
            return self.csv.fetchMetadata(ds.path)
        if ds.source == SourceType.EXCEL:
            return self.excel.fetchMetadata(ds.path)
        if ds.source == SourceType.SOCRATA:
            return self.sct.fetchMetadata(ds.resource_id)
        raise UnsupportedSourceError(ds.source)
