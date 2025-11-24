# data-ecosystem-superintendencia

This repository contains the analytical work for challenge:

- Superintendencia de Sociedades

The project follows a modular structure. Shared logic lives in a common core; challenge-specific logic lives in dedicated modules.

## Repository Structure
```bash
data-ecosystem/
├── src/
│   ├── core/               # Shared logic for both challenges
│   └── superintendencia/   # Challenge-specific code
├── scripts/                # ETLs, preprocessing, EDA runners, pipelines
├── data/
│   ├── raw/                # Unmodified datasets
│   └── processed/          # Cleaned / engineered datasets
├── sandbox/                # Personal workspaces
│       ├── eda/
│       ├── dari/
│       └── ...
│       # general notebooks can go directly under sandbox/
│       # example: sandbox/eda_xdataset.ipynb
└── .devcontainer/
```

## Environment Variables

```.devcontainer/.env```

This file will hold any credentials, paths, or configuration required for local execution inside the devcontainer.

```bash
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_PORT=
POSTGRES_HOST=

SOCRATA_BASE_URL=https://www.datos.gov.co
DATA_PATH=/path/to/data/
```

## Development Guidelines

- Domain logic → src/
- Scripts (ETL, EDA, preprocessing, pipelines) → scripts/
- Notebooks → ```sandbox/<user>/``` or in ```sandbox/<process>```
- Data → data/raw/ and data/processed/
- No credentials outside .devcontainer/.env

## Using the Devcontainer

1. Install the Dev Containers extension in VS Code.
2. Open the command palette (Ctrl + Shift + P) and select: ```Dev Containers: Reopen in Container```

This will start the environment defined in .devcontainer/.
