from dataclasses import dataclass
from typing import Optional, List

class BaseMetadata:
    pass

@dataclass
class SocrataColumn:
    name: str
    fieldName: str
    dataTypeName: str

@dataclass
class SocrataMetadata(BaseMetadata):
    name: str
    description: Optional[str]
    columns: List[SocrataColumn]
