from typing import TypeVar, Protocol, Optional, Generic, List
from ingest.fetch.metadata import BaseMetadata

class RawPort(Protocol):
    def fetch_raw(self, identifier: str) -> List[dict]:
        ...

    def fetch_metadata(self, identifier: str) -> Optional[BaseMetadata]:
        ...