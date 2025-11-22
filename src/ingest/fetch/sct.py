import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from typing import Any, Mapping

from ingest.fetch.raw import RawPort
import config as cfg


class SocrataAdapter(RawPort):

    def fetchRaw(
        self,
        resource: str,
        params: Mapping[str, Any] | None = None
    ) -> list[dict]:

        base = f"{cfg.SOCRATA_BASE_URL}/{resource.lstrip('/')}"
        query = urlencode(params or {})
        full_url = f"{base}?{query}" if query else base

        headers = {}
        if cfg.SOCRATA_TOKEN:
            headers["X-App-Token"] = cfg.SOCRATA_TOKEN

        req = Request(full_url, headers=headers)

        try:
            with urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
        except Exception as e:
            raise RuntimeError(f"Error fetching from Socrata: {e}")

        return data if isinstance(data, list) else []
