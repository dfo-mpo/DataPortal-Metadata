import requests

def fetch_json(api_url):
  try:
    response = requests.get(api_url, timeout=30)
    response.raise_for_status()
    return response.json()
  except requests.exceptions.RequestException as e:
    raise RuntimeError(
      f"Failed to connect to API endpoint.\n"
      f"Reason: {str(e)}"
    )
