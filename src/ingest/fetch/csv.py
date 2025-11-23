import csv
from ingest.errors import MetadataUnavailableError
from ingest.fetch.raw import RawPort
from ingest.fetch.metadata import BaseMetadata

class CsvAdapter(RawPort):

    def fetchRaw(self, path: str) -> list[dict]:
        with open(path, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def fetchMetadata(self, path: str) -> BaseMetadata | None:
        raise MetadataUnavailableError(f"Csv format does not support metadata")
