import os
from pathlib import Path

# Environment
ENV = os.getenv("HARVEST_ENV", "uat").lower()

# API endpoints
API_ENDPOINTS = {
  "dev": "http://qc-cdos-css-1:8815/api/portal/dataset/harvest", 
  "uat": "https://internet.dfo-mpo.gc.ca/pssi-issp/api/portal/dataset/harvest",
  # PROD will be added later
  # "prod": ""
}

if ENV not in API_ENDPOINTS:
  raise ValueError(
    f"HARVEST_ENV must be one of {list(API_ENDPOINTS.keys())}"
  )

API_URL = API_ENDPOINTS[ENV]

# Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
