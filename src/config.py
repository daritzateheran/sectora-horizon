import os

SOCRATA_BASE_URL = os.getenv("SOCRATA_BASE_URL", "https://www.datos.gov.co")
SOCRATA_TOKEN = os.getenv("SOCRATA_TOKEN")
DEFAULT_PAGE_SIZE = int(os.getenv("DEFAULT_PAGE_SIZE", "5000"))
DATA_PATH = os.getenv("DATA_PATH", "/workspaces/data-ecosystem/data/")