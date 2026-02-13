"""
CodeList Registry Loader
========================

This module dynamically parses the ISO NAP Metadata Register XML file
and builds a runtime lookup registry for ISO codeList resolution.

Purpose
-------

ISO metadata elements often require both:
  1. Display text (e.g., "onGoing; enContinue")
  2. Corresponding codeList identifier (e.g., "RI_602")

This script loads the official napMetadataRegister.xml file and builds:

  IC_xxx → { display_name → RI_xxx }

At runtime, this registry allows the builder to:
  - Extract IC identifier from a codeList URL
  - Map display text to the correct RI identifier
  - Populate codeListValue attributes correctly

Design
------

The registry is constructed once at import time and stored in:

  CODELIST_REGISTRY

Dependencies
------------

napMetadataRegister.xml stored under: src/codelists/

Public API
----------

resolve_codelist_value(codeList_url, display_text)

Returns:
  The matching RI identifier or None if not found.
"""

from lxml import etree
import os

CODELIST_FILE = os.path.join(
  os.path.dirname(__file__),
  "codelists",
  "napMetadataRegister.xml"
)

NS = {
    "grg": "http://www.isotc211.org/2005/grg",
    "gco": "http://www.isotc211.org/2005/gco",
    "xlink": "http://www.w3.org/1999/xlink"
}

def _load_codelists():
  """
  Parse napMetadataRegister.xml and build a registry dictionary.

  Process:
  1. Extract all RE_RegisterItem entries to build an RI lookup:
    RI_id -> display_name

  2. Extract all RE_ItemClass entries (IC_xxx).
  For each IC:
    - Find describedItem references
    - Resolve xlink:href -> RI_id
    - Map display_name -> RI_id

  Returns:
    dict:
      {
        "IC_106": {
          "onGoing": "RI_602",
          ...
        },
        ...
      }

  This function is executed once at import time.
  """

  tree = etree.parse(CODELIST_FILE)
  root = tree.getroot()

  registry = {}

  # Temporary lookup for RI identifiers -> display names
  ri_lookup = {}

  # Extract all individual register items (RI_xxx definitions)
  register_items = root.xpath(
    ".//grg:RE_RegisterItem",
    namespaces=NS
  )

  for item in register_items:
    ri_id = item.get("id")

    name_node = item.xpath(
      ".//grg:name/gco:CharacterString",
      namespaces=NS
    )

    if ri_id and name_node:
      name = name_node[0].text.strip()
      ri_lookup[ri_id] = name

  # Now build IC mapping
  item_classes = root.xpath(
    ".//grg:RE_ItemClass",
    namespaces=NS
  )

  for ic in item_classes:
    ic_id = ic.get("id")
    value_map = {}

    described = ic.xpath(
      ".//grg:describedItem",
      namespaces=NS
    )

    for d in described:
      href = d.get("{http://www.w3.org/1999/xlink}href")
      if not href:
        continue

      ri_id = href.replace("#", "")

      name = ri_lookup.get(ri_id)
      if name:
        value_map[name] = ri_id

    registry[ic_id] = value_map

  return registry

CODELIST_REGISTRY = _load_codelists()
# print(CODELIST_REGISTRY.get("IC_90"))
# print(CODELIST_REGISTRY.get("IC_106"))
# print(CODELIST_REGISTRY.get("IC_102"))
# print(CODELIST_REGISTRY.get("IC_96"))
# print(CODELIST_REGISTRY.get("IC_109"))

def resolve_codelist_value(codeList_url, display_text):
  """
  Resolve ISO codeList display text to its RI identifier.

  Parameters
  ----------
  codeList_url : str
    Full codeList URL including IC reference.
    Example:
      "...#IC_106"

  display_text : str
    Display string inserted in XML.
    Example:
      "onGoing; enContinue"

  Returns
  -------
  str or None
    The corresponding RI identifier (e.g., "RI_602"),
    or None if resolution fails.

  Notes
  -----
  - Only the first portion before ';' is used for matching.
  - Returns None if:
    - codeList_url malformed
    - IC not found
    - display_text not mapped
  """
  if not display_text or not codeList_url:
    return None

  # Extract IC_XXX
  if "#" not in codeList_url:
    return None

  ic_id = codeList_url.split("#")[-1]

  # Extract first part before ;
  name = display_text.split(";")[0].strip()

  value_map = CODELIST_REGISTRY.get(ic_id)
  if not value_map:
    return None

  return value_map.get(name)
