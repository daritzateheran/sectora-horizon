import yaml
import config as cfg
from ingest.dataset import Dataset, SourceType
from ingest.errors import DatasetNotFoundError

class DatasetCatalog:
    def __init__(self, yaml_path: str = f"{cfg.DATA_PATH}/datasets.yaml"):
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self.raw = data["datasets"]

    def get(self, name: str) -> Dataset:
        if name not in self.raw: raise DatasetNotFoundError(name)
        ds = self.raw[name]        
        return Dataset(
            name=name,
            source=SourceType(ds["source"]),
            path=ds.get("path"),
            resource_id=ds.get("resource_id"),
        )

    def list(self) -> list[Dataset]:
        return [self.get(n) for n in self.raw.keys()]