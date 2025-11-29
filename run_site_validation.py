#!/usr/bin/env python3
"""
Deterministic site validation with LLM fallback placeholder.
Used by run.py; no standalone execution.
"""

import re
import json

from prompt_templates import SITE_PROMPT_TEMPLATE
from llm_utils import append_prompt_to_md, get_llm_placeholder

# Abbreviation mappings (applied in order)
_ABBREVIATIONS = [
    (r"\bheadquarters\b", "HQ"),
    (r"\bhead\s*quarters\b", "HQ"),
    (r"\bmain\s*office\b", "HQ"),
    (r"\bhq\b", "HQ"),
    (r"\bbuilding\b", "BLDG"),
    (r"\bbldg\b", "BLDG"),
    (r"\bblg\b", "BLDG"),
    (r"\bdata\s*center\b", "DC"),
    (r"\bdatacenter\b", "DC"),
    (r"\bdc\b", "DC"),
    (r"\blab\b", "LAB"),
    (r"\blaboratory\b", "LAB"),
    (r"\boffice\b", "OFFICE"),
    (r"\bremote\b", "REMOTE"),
    (r"\bwarehouse\b", "WAREHOUSE"),
    (r"\bwh\b", "WAREHOUSE"),
]

# City code mappings
_CITY_CODES = [
    (r"\bsan\s*francisco\b", "SFO"),
    (r"\bsf\b", "SFO"),
    (r"\bnew\s*york\b", "NYC"),
    (r"\bny\b", "NYC"),
    (r"\blos\s*angeles\b", "LAX"),
    (r"\bla\b", "LAX"),
    (r"\bchicago\b", "CHI"),
    (r"\bseattle\b", "SEA"),
    (r"\bboston\b", "BOS"),
    (r"\bdenver\b", "DEN"),
    (r"\baustin\b", "AUS"),
    (r"\batlanta\b", "ATL"),
    (r"\blondon\b", "LON"),
    (r"\btokyo\b", "TYO"),
]

# Pattern for structured site codes (confident)
_STRUCTURED_PATTERN = re.compile(
    r"^[A-Z]{2,4}(-[A-Z0-9]+)*$"  # e.g., HQ, HQ-BLDG-1, DC-1, SFO-DC
)


def deterministic_site_parse(site_raw, notes, steps):
    """
    Parse site field deterministically.
    Returns (site_original, site_normalized, confident).
    """
    if site_raw is None:
        return ("", "", False)

    value = str(site_raw).strip()
    steps.append("site: trimmed")

    # Blank or N/A
    if value == "" or value.upper() in ("N/A", "NA", "NONE", "UNKNOWN", "-"):
        return (value, "", False)

    site_original = value

    # Uppercase
    value = value.upper()
    steps.append("site: uppercased")

    # Normalize delimiters: spaces, underscores, dots → single hyphen
    value = re.sub(r"[\s_\.]+", "-", value)
    value = re.sub(r"-+", "-", value)  # collapse multiple hyphens
    value = value.strip("-")
    steps.append("site: delimiters_normalized")

    # Apply city code mappings first
    for pattern, code in _CITY_CODES:
        value = re.sub(pattern, code, value, flags=re.IGNORECASE)

    # Apply abbreviation mappings
    for pattern, abbrev in _ABBREVIATIONS:
        value = re.sub(pattern, abbrev, value, flags=re.IGNORECASE)

    # Clean up again after substitutions
    value = re.sub(r"-+", "-", value)
    value = value.strip("-")

    # Check if it looks structured
    confident = bool(_STRUCTURED_PATTERN.match(value))

    # Also mark as confident if it's a simple alphanumeric code (2-10 chars)
    if not confident and re.fullmatch(r"[A-Z0-9]{2,10}", value):
        confident = True

    return (site_original, value, confident)


def validate_site_field(row, anomalies, normalization_steps):
    """
    Validate and normalize site field.
    Returns dict with site, site_normalized.
    """
    site_raw = row.get("site", "")
    notes = row.get("notes", "")
    row_id = row.get("source_row_id", "unknown")

    steps = []
    site_original, site_normalized, confident = deterministic_site_parse(site_raw, notes, steps)

    if confident:
        normalization_steps.extend(steps)
        steps.append(f"site: normalized to {site_normalized}")
        return {
            "site": site_original,
            "site_normalized": site_normalized,
        }

    # LLM fallback
    row_json = json.dumps({k: v for k, v in row.items() if k in ("site", "hostname", "owner", "device_type", "source_row_id")}, indent=2)
    prompt = SITE_PROMPT_TEMPLATE.format(row_json=row_json, notes=notes)
    rationale = (
        f"Site '{site_raw}' did not match known location patterns "
        "and abbreviation rules could not normalize it."
    )
    expected_schema = {
        "site": "<trimmed original or ''>",
        "site_normalized": "<canonical uppercase or 'UNKNOWN'>"
    }

    append_prompt_to_md("Site", row_id, prompt, rationale, expected_schema)

    normalization_steps.extend(steps)
    normalization_steps.append("site: llm_generated_placeholder")

    placeholder = get_llm_placeholder("site")
    return {
        "site": site_original,
        "site_normalized": placeholder["site_normalized"],
    }
