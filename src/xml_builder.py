from lxml import etree

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

def resolve_tag(tag):
  """
  Convert 'gmd:tag' to '{uri}tag' using namespace mappings
  """
  if ":" not in tag:
      return tag

  prefix, tag = tag.split(":", 1)
  return f"{{{namespaces[prefix]}}}{tag}"

def get_value(record, source, default=""):
  """
  Extracts nested values from the dict record using the source path connected by dot
  Example: 
    - "edhProfile.characterSet": str
    - "files.0.id": str. get("files") is a list, "0" is the index
    - "topicCategory": []
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

def ensure_child(parent, tag, attrib=None):
  """
  Find an existing child with the same tag, or create it.
  """
  tag = resolve_tag(tag)
  
  for child in parent:
    if child.tag == tag:
      return child
    
  # Special attrib xsi:type 
  attrib = {
    resolve_tag(k): v for k, v in (attrib or {}).items()
  }

  return etree.SubElement(parent, tag, attrib)

def normalize_path_item(item):
  """
  Normalize path item into (tag, attrib)
  Support
  - ("tag") -> (tag, None)
  - ("tag",) -> (tag, None)
  - ("tag", {attrib}) -> (tag, attrib)
  """
  if isinstance(item, str):
    return item, None
  
  if isinstance(item, tuple):
    if len(item) == 1:
      return item[0], None
    elif len(item) == 2:
      return item[0], item[1]
    else:
      raise ValueError(f"Invalid tuple length in path item {item}")
  raise ValueError(f"Invalid path entry {item}")

def add_bilingual_text(parent, en_value, fr_value=None):
  """
  Builds bilingual text
  """
  en_elem = etree.SubElement(parent, resolve_tag("gco:CharacterString"))
  en_elem.text = str(en_value)

  if fr_value:
    pt = etree.SubElement(parent, resolve_tag("gmd:PT_FreeText"))
    tg = etree.SubElement(pt, resolve_tag("gmd:textGroup"))
    fr_elem = etree.SubElement(
      tg,
      resolve_tag("gmd:LocalisedCharacterString"),
      {"locale": "#fra"}
    )
    fr_elem.text = str(fr_value)

def attach_value(node, value, fr_value=None, is_bilingual=False):
  """
  Attach value (optional bilingual) to a leaf node.
  """
  if is_bilingual:
    add_bilingual_text(node, value, fr_value)
  else:
    node.text = str(value)

def apply_mapping(root, record, mapping):
  # Collect all repeat tags defined in the mapping
  all_repeat_tags = {
    conf.get("repeat")
    for conf in mapping.values()
    if isinstance(conf.get("repeat"), str)
  }
  
  for _, conf in mapping.items():
    repeat_tag = conf.get("repeat")
    is_repeat = isinstance(repeat_tag, str)

    # Resolve value
    if "text" in conf:
      value = conf.get("text")
    else:
      value = get_value(record, conf.get("source"))
    
    if value in (None, "", []):
      value = ""

    # Normalize path
    path = [normalize_path_item(item) for item in conf["path"]]

    # Resolve bilingual values once
    fr_values = None
    is_bilingual = "source_fr" in conf or "text_fr" in conf
    if is_bilingual:
      if "text_fr" in conf:
        fr_values = conf.get("text_fr")
      else:
        fr_values = get_value(record, conf.get("source_fr"))

    # CASE 1: Defines repetition
    # ==========================

    # Split path into container -> repeat subtree
    if is_repeat:
      # Normalize values
      values = value if isinstance(value, list) else [str(value)]
      
      try:
        repeat_idx = next(
          i for i, (tag, _) in enumerate(path) if tag == repeat_tag
        )
      except StopIteration:
        raise ValueError(
          f"Repeat tag '{repeat_tag}' not found in path: {path}"
        )
      container_path = path[:repeat_idx]
      repeat_path = path[repeat_idx:]

      # Build container once
      parent = root
      for tag, attrib in container_path:
        parent = ensure_child(parent, tag, attrib)

      # Repeat repeated subtree
      for idx, value in enumerate(values):
        current = parent

        for tag, attrib in repeat_path:
          current = etree.SubElement(
            current,
            resolve_tag(tag),
            {resolve_tag(k): v for k, v in (attrib or {}).items()}
          )

        fr_value = None
        if is_bilingual:
          if isinstance(fr_values, list) and idx < len(fr_values):
            fr_value = fr_values[idx]
          elif not isinstance(fr_values, list):
            fr_value = fr_values

        attach_value(current, value, fr_value, is_bilingual)

    # CASE 2: Decorates an existing repeating structure
    # =================================================
    else:
      repeat_positions = [
        i for i, (tag, _) in enumerate(path) if tag in all_repeat_tags
      ]

      if repeat_positions:
        repeat_idx = repeat_positions[0]
        container_path = path[:repeat_idx]
        post_repeat_path = path[repeat_idx + 1:]
        repeat_tag_name, _ = path[repeat_idx]

        # Walk to parent to repeated elements
        parent = root
        for tag, attrib in container_path:
          parent = ensure_child(parent, tag, attrib)

        repeated_nodes = parent.findall(resolve_tag(repeat_tag_name))

        for idx, repeated_node in enumerate(repeated_nodes):
          current = repeated_node
          for tag, attrib in post_repeat_path:
            current = ensure_child(current, tag, attrib)

          fr_value = None
          if is_bilingual:
            if isinstance(fr_values, list) and idx < len(fr_values):
              fr_value = fr_values[idx]
            elif not isinstance(fr_values, list):
              fr_value = fr_values

          attach_value(current, value, fr_value, is_bilingual)
      
      # CASE 3: Normal non-repeat field
      # ===============================
      else:
        parent = root
        for tag, attrib in path[:-1]:
          parent = ensure_child(parent, tag, attrib)

        leaf_tag, leaf_attrib = path[-1]
        leaf = ensure_child(parent, leaf_tag, leaf_attrib)

        fr_value = None
        if is_bilingual:
          fr_value = fr_values

        attach_value(leaf, value, fr_value, is_bilingual)

def build_xml(record, record_id, field_mapping):
  root = etree.Element(resolve_tag("gmd:MD_Metadata"), nsmap=namespaces)
  apply_mapping(root, record, field_mapping)
  return etree.ElementTree(root)
