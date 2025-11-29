#!/usr/bin/env python3
"""
Deterministic hostname validation and normalization helpers.
Used by run.py; no standalone execution.
"""

import re

# RFC 1123 relaxed: starts/ends with alnum, middle can have hyphens, max 63 chars
_HOSTNAME_PATTERN = re.compile(r"^[a-z0-9]([a-z0-9\-]{0,61}[a-z0-9])?$")


def validate_hostname_field(row, anomalies, normalization_steps):
    """
    Validate and normalize the 'hostname' field of a row.

    Parameters
    ----------
    row : dict
        The current CSV row (expects key 'hostname').
    anomalies : list
        Shared list to which anomaly dicts are appended.
    normalization_steps : list
        Shared list to which normalization action strings are appended.

    Returns
    -------
    dict
        {"hostname": <normalized_or_raw>, "hostname_valid": True/False}
    """
    raw = row.get("hostname")

    # --- Missing ---
    if raw is None or str(raw).strip() == "":
        anomalies.append({"field": "hostname", "type": "hostname_missing"})
        return {"hostname": "", "hostname_valid": False}

    raw_str = str(raw)
    value = raw_str.strip()

    # Note trimming
    if value != raw_str:
        normalization_steps.append("hostname: trimmed whitespace")

    # Lowercase
    lowered = value.lower()
    if lowered != value:
        normalization_steps.append("hostname: lowercased")
    value = lowered

    # Remove trailing dot (often seen in FQDN notation)
    if value.endswith("."):
        value = value.rstrip(".")
        normalization_steps.append("hostname: removed trailing dot")

    # If contains dots, extract first label as hostname
    if "." in value:
        value = value.split(".")[0]
        normalization_steps.append("hostname: extracted first label from FQDN")

    # --- Validation checks ---

    # Check for leading hyphen
    if value.startswith("-"):
        anomalies.append({"field": "hostname", "type": "hostname_leading_hyphen", "value": raw_str})
        return {"hostname": raw_str, "hostname_valid": False}

    # Check length
    if len(value) > 63:
        anomalies.append({"field": "hostname", "type": "hostname_too_long", "value": raw_str})
        return {"hostname": raw_str, "hostname_valid": False}

    # Check for invalid characters (anything outside a-z0-9-)
    if not re.fullmatch(r"[a-z0-9\-]*", value):
        anomalies.append({"field": "hostname", "type": "hostname_invalid_chars", "value": raw_str})
        return {"hostname": raw_str, "hostname_valid": False}

    # Full pattern match (RFC 1123 relaxed)
    if not _HOSTNAME_PATTERN.match(value):
        # Catches edge cases like ending with hyphen or empty after normalization
        anomalies.append({"field": "hostname", "type": "hostname_invalid_chars", "value": raw_str})
        return {"hostname": raw_str, "hostname_valid": False}

    normalization_steps.append(f"hostname: normalized to {value}")
    return {"hostname": value, "hostname_valid": True}
