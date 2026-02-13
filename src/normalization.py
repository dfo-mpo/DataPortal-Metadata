"""
Controlled Vocabulary Normalization Module
==========================================

This module provides normalization logic for controlled vocabulary fields.

Purpose
-------
Source data may contain inconsistent casing, spacing, or formatting.
This module standardizes input values before they are inserted into XML.

It performs:
  - Case-insensitive matching
  - Whitespace trimming
  - Safe fallback to original value if not found

Design
------

1. CONTROLLED_VOCAB is imported from controlled_vocab.py
2. Keys are pre-normalized once at import time
3. normalize_controlled_value() is called by the XML builder
   when a mapping field is marked as "controlled"

Notes
-----

If a value is not found in the vocabulary:
  -> The original value is returned
  -> XML generation continues (no hard failure)
"""

from .controlled_vocab import CONTROLLED_VOCAB

def _normalize_vocab(vocab):
  """
  Preprocess the CONTROLLED_VOCAB dictionary.

  Converts all vocabulary keys to:
    - lowercase
    - stripped of surrounding whitespace

  This enables case-insensitive matching during normalization.

  Parameters
  ----------
  vocab : dict
    CONTROLLED_VOCAB structure.

  Returns
  -------
  dict
    A normalized vocabulary dictionary.
  """
  normalized = {}
  for field, mapping in vocab.items():
    normalized[field] = {
      str(k).strip().lower(): v
      for k, v in mapping.items()
    }
  return normalized

# Preprocess vocab once
NORMALIZED_VOCAB = _normalize_vocab(CONTROLLED_VOCAB)

def normalize_controlled_value(field, raw_value):
  """
  Normalize a controlled vocabulary value.

  Parameters
  ----------
  field : str
    The mapping field name (must exist in CONTROLLED_VOCAB).

  raw_value : str or list
    The original value from the source record.

  Returns
  -------
  str, list, or original value
    - Normalized controlled value if matched.
    - Original value if not found.
    - Preserves list structure when input is a list.

  Behavior
  --------
  - Matching is case-insensitive.
  - Whitespace is ignored.
  - Missing vocabulary field -> return original value.
  - Unmatched value -> fallback to original value.
  """

  if raw_value in (None, "", []):
    return [] if isinstance(raw_value, list) else ""
  
  vocab = NORMALIZED_VOCAB.get(field)

  if not vocab:
    return raw_value
  
  # Handle list values
  if isinstance(raw_value, list):
    normalized = []
    for item in raw_value:
      key = str(item).strip().lower()
      entry = vocab.get(key)

      if entry:
        normalized.append(entry)
      else:
        # fallback to original value if not found
        normalized.append(item)
    return normalized
    
  # Handle single / non-list values
  key = str(raw_value).strip().lower()
  # entry = string or dict
  entry = vocab.get(key)
  return entry if entry else raw_value
