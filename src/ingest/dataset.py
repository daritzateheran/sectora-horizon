from dataclasses import dataclass
from enum import Enum
from typing import Optional

class SourceType(Enum):
    CSV = "csv"
    SOCRATA = "socrata"
    TAB = "tab"

@dataclass
class Dataset:
    name: str
    source: SourceType
    path_or_url: str
    page_size: Optional[int] = None