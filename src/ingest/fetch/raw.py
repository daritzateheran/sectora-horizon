from typing import TypeVar, Protocol, Optional, Generic, List
from ingest.fetch.metadata import BaseMetadata

class RawPort(Protocol):
    def fetchRaw(self, identifier: str) -> List[dict]:
        ...

    def fetchMetadata(self, identifier: str) -> Optional[BaseMetadata]:
        ...