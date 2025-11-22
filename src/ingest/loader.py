from ingest.dataset import Dataset, SourceType
from ingest.fetch.raw import RawPort
import config as cfg


class RawDatasetLoader:

    def __init__(self, csv_adapter: RawPort, sct_adapter: RawPort, tab_adapter: RawPort):
        self.csv = csv_adapter
        self.sct = sct_adapter
        self.tab = tab_adapter

    def load(self, ds: Dataset, params=None):
        if ds.source == SourceType.CSV:
            return self.csv.fetchRaw(ds.path_or_url)

        if ds.source == SourceType.TAB:
            return self.tab.fetchRaw(ds.path_or_url)

        if ds.source == SourceType.SOCRATA:
            limit = ds.page_size or cfg.DEFAULT_PAGE_SIZE
            final = dict(params or {})
            final.setdefault("$limit", limit)
            final.setdefault("$offset", 0)
            return self.sct.fetchRaw(ds.path_or_url, final)

        raise ValueError(f"Unknown dataset source {ds.source}")

    def stream(self, ds: Dataset, params=None):
        if ds.source in (SourceType.CSV, SourceType.TAB):
            for row in self.load(ds):
                yield row
            return
        offset = 0
        limit = ds.page_size or cfg.DEFAULT_PAGE_SIZE
        base = params or {}

        while True:
            final = dict(base)
            final["$limit"] = limit
            final["$offset"] = offset
            chunk = self.sct.fetchRaw(ds.path_or_url, final)

            if not chunk:
                break

            for row in chunk:
                yield row

            offset += limit
