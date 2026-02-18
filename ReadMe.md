# Data Portal Metadata Harvester

This repository contains a Python-based harvesting tool that retrieves metadata records from an API and generates HNAP-compliant XML files for downstream harvesting and ingestion.

---

## Requirements

- Python 3.9+
- Network access to the target API
- Private DFO Network access **required for DEV environment only**

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

## API Environments

The harvester supports multiple API environments, controlled via the `HARVEST_ENV` environment variable.

If no environment variable is provided, the harvester runs against the **PROD API** by default.

### Available Environments

| Environment | Description | Network Requirement |
|-------------|------------|---------------------|
| `prod` | Production API (Default) | Public |
| `prod_fr` | Production API (French) | Public |
| `uat`  | User Acceptance / Testing API | Public |
| `dev`  | Development API | Private DFO Network required |

---

## Running the Harvester

Before running the harvester, ensure the virtual environment is activated and the desired API environment is selected.

### Activate a virtual environment

```
# Linux / macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

---

### Default (PROD)

Runs against the Production API.

```
python main.py
```

---

### PROD (French)

To run against the PROD (French) API:

```
HARVEST_ENV=prod_fr python main.py
```

---

### UAT

To run against the UAT API:

```
HARVEST_ENV=uat python main.py
```

No Private DFO Network is required.

---

### DEV

To run against the Development API:

```
HARVEST_ENV=dev python main.py
```

**Requires active private DFO network connection.**

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

## Notes

- No API credentials are required for any environment
