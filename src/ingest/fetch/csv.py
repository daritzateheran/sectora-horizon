import csv
from ingest.fetch.raw import RawPort

class CsvAdapter(RawPort):

    def fetchRaw(self, resource: str, params=None) -> list[dict]:
        with open(resource, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [dict(r) for r in reader]
