from typing import Protocol, Any, Mapping

class RawPort(Protocol):
    def fetchRaw(
        self,
        resource: str,
        params: Mapping[str, Any] | None = None
    ) -> list[dict]:
        ...