import os

SOCRATA_BASE_URL = os.getenv("SOCRATA_BASE_URL", "https://www.datos.gov.co")
DATA_PATH = os.getenv("DATA_PATH", "/workspaces/data-ecosystem/data/")