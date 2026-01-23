import uuid
from .api_client import fetch_json
from .xml_builder import build_xml
from .mapping import FIELD_MAPPING
from .config import API_URL, OUTPUT_DIR

def extract_record_id(record):
  return record.get("files", [{}])[0].get("id", str(uuid.uuid4()))

def generate_xml():
  raw = fetch_json(API_URL)
  records = raw.get("data", [])

  print(f"Found {len(records)} records.")

  for record in records:
    record_id = extract_record_id(record)
    xml_tree = build_xml(record, record_id, FIELD_MAPPING)

    filename = f"{OUTPUT_DIR}/{record_id}.xml"
    xml_tree.write(filename, pretty_print=True)
    print(f"Saved {filename}")
