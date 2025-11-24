from dataclasses import dataclass
from enum import Enum
from typing import Optional

class SourceType(Enum):
    CSV = "csv"
    SOCRATA = "socrata"
    EXCEL = "excel"

@dataclass
class Dataset:
    name: str
    source: SourceType
    path: str | None = None
    resource_id: str | None = None