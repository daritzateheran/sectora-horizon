import yaml
from ingest.dataset import Dataset
import config as cfg
from ingest.dataset import SourceType

class DatasetCatalog:
    def __init__(self, yaml_path: str = f"{cfg.DATA_PATH}/datasets.yaml"):
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self.raw = data["datasets"]

    def get(self, name: str) -> Dataset:
        ds = self.raw[name]
        page_size = ds.get("page_size", cfg.DEFAULT_PAGE_SIZE)
        return Dataset(
            name=name,
            source=SourceType(ds["source"]),
            path_or_url=ds["path_or_url"],
            page_size=page_size,
        )
    
    def list_datasets(self) -> list[Dataset]:
        """Devuelve todos los datasets del catálogo como objetos Dataset."""
        return [self.get(name) for name in self.raw.keys()]