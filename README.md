# SECTORA HORIZON
A Future-Focused Analytics System for Industries and Businesses.

<p align="center">
<img src="src/utils/assets/logo.png" width="300" alt="Logo">

This repository contains the analytical work for challenge:

- Superintendencia de Sociedades

The project follows a modular structure. Shared logic lives in a common core; challenge-specific logic lives in dedicated modules.

## Repository Structure
```bash
data-ecosystem/
├── src/                    # Core logic for challenge
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
