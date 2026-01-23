import requests

def fetch_json(api_url):
  response = requests.get(api_url)
  response.raise_for_status()
  return response.json()
