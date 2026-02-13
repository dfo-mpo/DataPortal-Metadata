"""
XML Builder Module
==================

This module generates ISO-compliant XML metadata records
from structured source records using a base ISO-compliant XML template

Overview
--------
1. Load base XML template (language + spatial variant)
2. Iterate through mapping configuration
3. Extract values from source record
4. Normalize controlled values if required
5. Inject values via XPath
6. Clean illegal placeholders
7. Enforce required ISO fields
8. Return final XML tree

Important
---------
This module assumes:
  - The base template is ISO-valid
  - Mapping configuration is correct
  - Controlled vocabularies are pre-defined
"""

from lxml import etree
from datetime import datetime
from .normalization import normalize_controlled_value
from .codelist_registry import resolve_codelist_value
import os
from copy import deepcopy

# Register ISO namespaces
namespaces = {
  "gmd": "http://www.isotc211.org/2005/gmd",
  "gco": "http://www.isotc211.org/2005/gco",
  "gfc": "http://www.isotc211.org/2005/gfc",
  "srv": "http://www.isotc211.org/2005/srv",
  "gmx": "http://www.isotc211.org/2005/gmx",
  "gts": "http://www.isotc211.org/2005/gts",
  "gsr": "http://www.isotc211.org/2005/gsr",
  "gss": "http://www.isotc211.org/2005/gss",
  "gmi": "http://www.isotc211.org/2005/gmi",
  "napm": "http://www.geconnections.org/nap/napMetadataTools/napXsd/napm",
  "gml": "http://www.opengis.net/gml/3.2",
  "xlink": "http://www.w3.org/1999/xlink",
  "xsi": "http://www.w3.org/2001/XMLSchema-instance"
}

def load_base_xml(path):
  """
  Load and parse the base ISO XML template.
  """
  if not os.path.exists(path):
    raise FileNotFoundError(f"Base XML template not founc: {path}")
  
  parser = etree.XMLParser(remove_blank_text=True)
  return etree.parse(path, parser)

def resolve_tag(tag):
  """
  Convert namespace-prefixed tag to fully-qualified QName.

  Example:
    -  "gmd:fileIdentifier" -> "{http://www.isotc211.org/2005/gmd}fileIdentifier"

  Used for safe XML element lookup and manipulation.
  """
  if ":" not in tag:
    return tag
  
  prefix, tag = tag.split(":")
  return f"{{{namespaces[prefix]}}}{tag}"

def get_value(record, source, default=None):
  """
  Extract nested value from a record using dot-separated path.

  Supports:
    - Dictionary traversal
    - List indexing (e.g., "files.0.id")

  Example: 
    - "edhProfile.characterSet": str
    - "files.0.id": str. get("files") is a list, "0" is the index
    - "topicCategory": []

  Returns
  -------
  Resolved value or default if path not found.
  """
  if not source:
    return default
  
  value = record
  parts = source.split(".")

  for part in parts:
    if isinstance(value, list):
      try:
        idx = int(part)
        value = value[idx]
      except (ValueError, IndexError):
        return default
    else:
      try:
        value = value[part]
      except (KeyError, TypeError):
        return default

  return value

def normalize_date(value):
  """
  Normalize ISO datetime string to date-only format.

  Example:
    "2025-11-19T20:55:54+00:00" -> "2025-11-19"

  Returns original value if parsing fails.
  """
  if not value:
    return ""
  try:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
  except Exception:
    return value

def normalize_code(value):
  """
  Normalize spatial reference codes.

  Examples:
    "EPSG-4326" -> "EPSG:4326"
    "SR-ORG-123" -> "SR-ORG:123"

  Returns original value if no transformation required.
  """
  if not value:
    return ""
  try:
    if value.startswith("EPSG"):
      return value.replace("EPSG-", "EPSG:")
    elif value.startswith("SR-ORG"):
      return value.replace("SR-ORG-", "SR-ORG:")
    else:
      return value
  except Exception:
    return value

def set_text(lang, tree, xpath, value, secondary_value=None):
  """
  Inject scalar value into XML using XPath.

  Features:
    - Automatic date normalization
    - Spatial code normalization
    - ISO codeList resolution
    - Removal of gco:nilReason
    - Optional bilingual PT_FreeText handling

  Parameters
  ----------
  lang : str
    Base language ("en" or "fr")
  tree : etree._ElementTree
  xpath : str
  value : str
  secondary_value : str (optional)

  If codeList resolution fails:
    -> Template value is preserved.
  """
  if value in (None, "", []):
    return
  
  # Normalize date to YYYY-MM-DD format
  if "/gco:Date" in xpath:
    value = normalize_date(value)

  if "/gmd:code" in xpath:
    value = normalize_code(value)

  nodes = tree.xpath(xpath, namespaces=namespaces)
  for node in nodes:
    codeList_url = node.get("codeList")

    if codeList_url:
      resolved_code = resolve_codelist_value(codeList_url, str(value))

      if not resolved_code:
        # Skip modification completely - keep template default value
        print(f"[WARN] Codelist value not found for {value}, keeping template fallback.")
        # node.attrib.pop("codeList")
        # node.attrib.pop("codeListValue")
        # node.text = str(value)
        continue

      # Safe to update
      node.text = str(value)
      node.set("codeListValue", resolved_code)

    else:
      node.text = str(value)
    
    # Remove nilReason if present
    parent = node.getparent()
    parent.attrib.pop(resolve_tag("gco:nilReason"), None)

    if secondary_value not in (None, "", []):
      secondary_locale = "#fra" if lang == "en" else "#eng"
      fr_nodes = parent.xpath(
        f".//gmd:LocalisedCharacterString",
        namespaces=namespaces
      )
      if fr_nodes:
        fr_nodes[0].set("locale", secondary_locale)
        fr_nodes[0].text = str(secondary_value)

def set_repeated_values(lang, tree, container_xpath, repeat_tag, value_xpath, values, secondary_values=None):
  """
  Inject repeated values into XML container.

  Process:
    - Locate container element
    - Use first existing child as template
    - Clone template for each value
    - Insert values in correct order
    - Handle optional bilingual values

  Parameters
  ----------
  container_xpath : str
  repeat_tag : str
  value_xpath : str
  values : list
  secondary_values : list (optional)
  """
  if not values:
    return

  containers = tree.xpath(container_xpath, namespaces=namespaces)
  if not containers:
    return
  container = containers[0]

  repeat_qname = resolve_tag(repeat_tag)
  
  # Find existing placeholder(s)
  existing = container.findall(repeat_qname)
  if not existing:
    return

  # Use first placeholder as template
  template = existing[0]
  insert_index = list(container).index(template)

  # Remove all placeholders
  for elem in existing:
    container.remove(elem)

  # Ensure secondary_values alignment
  if isinstance(secondary_values, list):
    fr_list = secondary_values
  elif secondary_values:
    fr_list = [secondary_values] * len(values)
  else:
    fr_list = [None] * len(values)

  for i, value in enumerate(values):
    # Clone template
    new_elem = deepcopy(template)

    # Insert at correct position
    container.insert(insert_index + i, new_elem)

    # Set EN value
    value_node = new_elem.find(".//" + resolve_tag(value_xpath), namespaces)
    if value_node is not None:
      # Remove nilReason if present
      value_node.getparent().attrib.pop(resolve_tag("gco:nilReason"), None)
      value_node.text = str(value)

    # Set FR value if present
    if fr_list and i < len(fr_list) and fr_list[i]:
      fr_node = new_elem.xpath(
        ".//gmd:LocalisedCharacterString",
        namespaces=namespaces
      )
      if fr_node:
        # Update locale
        secondary_locale = "#fra" if lang == "en" else "#eng"
        fr_node[0].set("locale", secondary_locale)
        fr_node[0].text = str(fr_list[i])

def clean_illegal_placeholders(tree):
  """
  Remove invalid or empty ISO blocks.

  Currently removes:
    - Empty CI_Date blocks
    - Empty topicCategory elements

  Ensures final XML passes ISO validation.
  """
  # Remove empty CI_Date blocks
  for date in tree.xpath(".//gco:Date", namespaces=namespaces):
    if not (date.text and date.text.strip()):
      ci_date = date.getparent().getparent()
      ci_date.getparent().remove(ci_date)

  # Remove empty topicCategory
  for tc in tree.xpath(".//gmd:topicCategory", namespaces=namespaces):
    code = tc.find(".//gmd:MD_TopicCategoryCode", namespaces)
    if code is None or not (code.text and code.text.strip()):
      tc.getparent().remove(tc)

def enforce_required_fields(tree, record_id):
  """
  Enforce mandatory ISO fields.

  Always sets:
    - fileIdentifier
    - dateStamp (current UTC timestamp)

  Ensures ISO compliance even if mapping omits them.
  """
  # fileIdentifier
  fid = tree.xpath(
    ".//gmd:fileIdentifier/gco:CharacterString",
    namespaces=namespaces
  )
  if fid:
    fid[0].text = str(record_id)

  # dateStamp
  ds = tree.xpath(
    ".//gmd:dateStamp/gco:DateTime",
    namespaces=namespaces
  )
  if ds:
    ds[0].text = datetime.now().isoformat() + "Z"

def build_xml(record, record_id, mapping, base_xml_path=None):
  """
  Main XML generation entry point.

  Parameters
  ----------
  record : dict
  record_id : str
  mapping : list
  base_xml_path : str (optional)

  Process
  -------
  1. Determine language and spatial type
  2. Load appropriate base template
  3. Iterate through mapping configuration
  4. Inject scalar or repeated values
  5. Clean invalid placeholders
  6. Enforce required ISO fields

  Returns
  -------
  etree._ElementTree
    Fully constructed ISO-compliant XML tree.
  """
  # Determine spatial
  is_spatial = bool(get_value(record, "spatialType"))

  # Determine base language
  if base_xml_path is None:
    lang = get_value(record, "edhProfile.language", default="en")
    lang = str(lang).strip().lower()
    lang = "fr" if lang.startswith("fr") else "en"
    base_xml_suffix = "_spatial" if is_spatial else ""
    base_xml_path = f"src/xml/base_{lang}{base_xml_suffix}.xml"
  else:
    lang = "fr" if "fr" in base_xml_path.lower() else "en"

  print(f"[INFO] Record {str(record_id)}")
  print(f"[INFO] {"Spatial" if is_spatial else "Non-spatial"} {lang.upper()} record. Load template from {base_xml_path}")

  tree = load_base_xml(base_xml_path)

  for field in mapping:
    is_repeat = field.get("repeat")

    if lang == "fr":
      if field.get("source_fr"):
        primary_source = field.get("source_fr")
        secondary_source = field.get("source")
      else:
        primary_source = field.get("source")
        secondary_source = None
    else:
      primary_source = field.get("source")
      secondary_source = field.get("source_fr")

    # Scalar type
    if not is_repeat:
      value = get_value(record, primary_source)
      value = normalize_controlled_value(
        field.get("controlled"), value
      )

      secondary_value = None
      if secondary_source:
        secondary_value = get_value(record, secondary_source)
        secondary_value = normalize_controlled_value(
          field.get("controlled"), secondary_value
        )

      set_text(
        lang,
        tree,
        field["xpath"],
        value,
        secondary_value
      )

    # Repeat type
    else:
      if "container_xpath" not in field:
        raise ValueError("Repeat requires container_xpath")
      
      raw_value = get_value(record, primary_source)
      values = normalize_controlled_value(
        field.get("controlled"), raw_value
      )

      secondary_values = None
      if secondary_source:
        raw_secondary_values = get_value(record, secondary_source)
        secondary_values = normalize_controlled_value(
          field.get("controlled"), raw_secondary_values
        )

      set_repeated_values(
        lang,
        tree,
        field["container_xpath"],
        field["repeat_tag"],
        field["value_xpath"],
        values,
        secondary_values
      )

  clean_illegal_placeholders(tree)
  enforce_required_fields(tree, record_id)

  return tree
