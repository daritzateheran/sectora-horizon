import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class config:
    user: str
    password: str
    db: str
    port: int
    host: str
    sslmode: Optional[str] = None
    connect_timeout: int = 5 
    minconn: int = 1
    maxconn: int = 5

def load_config():
    usr=os.getenv('POSTGRES_USER')
    pwd=os.getenv('POSTGRES_PASSWORD')
    db=os.getenv('POSTGRES_DB')
    port=os.getenv('POSTGRES_PORT')
    host=os.getenv('POSTGRES_HOST')
    sslmode=os.getenv('POSTGRES_SSLMODE') or "require"
    return config(user=usr,
                password=pwd,
                db=db,
                port=port,
                host=host,
                sslmode=sslmode
    )

