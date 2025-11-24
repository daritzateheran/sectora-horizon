import csv, json
from io import StringIO
from typing import Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import config as cfg
from ingest.fetch.raw import RawPort
from ingest.errors import RawLoadError, MetadataUnavailableError
from ingest.fetch.metadata import SocrataColumn, SocrataMetadata

class SocrataAdapter(RawPort):

    BASE = cfg.SOCRATA_BASE_URL.rstrip("/")

    def _download(self, url: str, headers: dict) -> bytes:
        try:
            with urlopen(Request(url, headers=headers), timeout=20) as resp:
                return resp.read()
        except Exception as e:
            raise RawLoadError(f"Socrata fetch failed: {e}")

    def fetch_paged(self, resource_id: str, batch_size: int = 50_000):
        """
        Itera sobre todas las páginas del recurso usando $limit/$offset.
        No forma parte del contrato RawPort, pero se mantiene para uso interno.
        """
        offset = 0
        while True:
            params = {"$limit": batch_size, "$offset": offset}
            batch = self._fetch_single_batch(resource_id, params)
            if not batch:
                break
            for row in batch:
                yield row
            offset += batch_size

    def _fetch_single_batch(self, resource_id: str, params=None) -> list[dict]:
        params = params or {}
        query = urlencode(params)
        headers = {}

        if cfg.SOCRATA_TOKEN:
            headers["X-App-Token"] = cfg.SOCRATA_TOKEN
        csv_url = f"{self.BASE}/resource/{resource_id}.csv"
        if query:
            csv_url += f"?{query}"

        try:
            raw_bytes = self._download(csv_url, headers)
            text = raw_bytes.decode("utf-8")
            return list(csv.DictReader(StringIO(text)))
        except Exception:
            pass
        json_url = f"{self.BASE}/resource/{resource_id}.json"
        if query:
            json_url += f"?{query}"

        raw_bytes = self._download(json_url, headers)
        data = json.loads(raw_bytes)
        return data if isinstance(data, list) else []

    def fetch_raw(self, resource_id: str) -> list[dict]:
        """
        Llama a fetch_paged internamente y devuelve todo el dataset en memoria.
        """
        return list(self.fetch_paged(resource_id))

    def fetch_metadata(self, resource_id: str) -> Optional[SocrataMetadata]:
        headers = {}
        if cfg.SOCRATA_TOKEN:
            headers["X-App-Token"] = cfg.SOCRATA_TOKEN
        url = f"{self.BASE}/api/views/{resource_id}"
        try:
            raw = json.loads(self._download(url, headers))
            cols = [
                SocrataColumn(
                    name=c.get("name"),
                    fieldName=c.get("fieldName"),
                    dataTypeName=c.get("dataTypeName"),
                )
                for c in raw.get("columns", [])
            ]
            return SocrataMetadata(
                name=raw.get("name"),
                description=raw.get("description"),
                columns=cols,
            )
        except Exception as e:
            raise MetadataUnavailableError(f"Metadata unavailable: {e}")
