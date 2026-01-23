# Data Portal Metadata Harvester

This repository contains a Python-based harvesting tool that retrieves metadata records from an API and generates HNAP–compliant XML files for downstream harvesting and ingestion.

The project is designed to be executed as a scheduled job and does not require user interaction once configured.

---

## Requirements

- Python 3.9+
- Network access to the target API
- VPN access **required for DEV environment only**

---

## Installation

1. Clone the repository
2. Create and activate a virtual environment:

```
python -m venv .venv
```

```
# Linux / macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```
pip install -r requirements.txt
```

---

## Repository Structure

```
./
├─ src/
│ ├─ api_client.py        # Handles API requests=
│ ├─ config.py            # Environment configuration, API selection, and paths
│ ├─ harvester.py         # Orchestrates harvesting and XML generation
│ ├─ mapping.py           # Field mapping configuration
│ └─ xml_builder.py       # XML construction and mapping application logic
│
├─ notebooks/
│ └─ xml_harvester_dev.ipynb    # Development and debugging notebook
│
├─ output/                # Generated XML files
│
├─ main.py                # Entry point for execution
├─ requirements.txt
└─ README.md
```

---

## API Environments

The harvester supports multiple API environments, controlled via an environment variable.

### Current environments

| Environment | Description | Network Requirement |
|------------|-------------|---------------------|
| `dev` | Development API | **VPN required** |
| `uat` | User Acceptance / Testing API | Public |
| `prod` | Production API | **Not yet available** |

> **Note:** The PROD API is not yet available and will be added once provided by the upstream team.

---

## Running the Harvester

### DEV (Default)

If no environment variable is provided, the harvester runs against the **DEV API** by default.

```
python main.py
```

**Requires active VPN connection.**

---

### UAT (Public)

To run against the UAT API:

```
HARVEST_ENV=uat python main.py
```

No VPN is required.

---

### PROD (TBA)

Once the PROD API becomes available, it will be enabled via:

```
HARVEST_ENV=prod python main.py
```

---

## Output

Generated XML files are written to the following directory:

```
./output/
```

- One XML file is generated per record
- Filenames are derived from the record identifier
- Existing files with the same name will be overwritten

---

## Development Notebook

A development notebook is provided under:

```
./notebooks/
```

The notebook is intended for:
- Development
- Debugging
- Mapping validation

The notebook is **not** intended for scheduled or production execution.  
All scheduled runs should execute `main.py`.

---

## Notes

- No API credentials are required for any environment
