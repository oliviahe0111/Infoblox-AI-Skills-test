#!/usr/bin/env python3
"""
Deterministic MAC address validator and normalizer.
Canonical output format: AA:BB:CC:DD:EE:FF (uppercase, colon-delimited).
"""

import re

# ---------------------------------------------------------------------------
# Helper: detect delimiter style
# ---------------------------------------------------------------------------

def _detect_delimiter(mac_str):
    """
    Detect which delimiter is used in mac_str.
    Returns one of: ":", "-", ".", "" (none), or "mixed" if more than one type.
    """
    has_colon = ":" in mac_str
    has_dash = "-" in mac_str
    has_dot = "." in mac_str

    count = sum([has_colon, has_dash, has_dot])
    if count > 1:
        return "mixed"
    if has_colon:
        return ":"
    if has_dash:
        return "-"
    if has_dot:
        return "."
    return ""


# ---------------------------------------------------------------------------
# Main validation function
# ---------------------------------------------------------------------------

def validate_mac_field(row, anomalies, normalization_steps):
    """
    Validate and normalize the 'mac' field of a row.

    Parameters
    ----------
    row : dict
        The current CSV row (expects key 'mac').
    anomalies : list
        Shared list to which anomaly dicts are appended.
    normalization_steps : list
        Shared list to which normalization action strings are appended.

    Returns
    -------
    dict
        {"mac": <canonical_or_raw>, "mac_valid": True/False}
    """
    raw = row.get("mac")

    # --- Missing ---
    if raw is None or str(raw).strip() == "":
        anomalies.append({"field": "mac", "type": "mac_missing"})
        return {"mac": "", "mac_valid": False}

    raw_str = str(raw)
    trimmed = raw_str.strip()

    # Note trimming if whitespace was removed
    if trimmed != raw_str:
        normalization_steps.append("mac: trimmed whitespace")

    # --- Detect delimiter ---
    delim = _detect_delimiter(trimmed)
    if delim == "mixed":
        anomalies.append({"field": "mac", "type": "mac_mixed_delimiters", "value": raw_str})
        return {"mac": raw_str, "mac_valid": False}

    # --- Remove delimiters and uppercase ---
    stripped = trimmed.replace(":", "").replace("-", "").replace(".", "").upper()

    # --- Length check (must be exactly 12 hex chars) ---
    if len(stripped) != 12:
        anomalies.append({"field": "mac", "type": "mac_wrong_length", "value": raw_str})
        return {"mac": raw_str, "mac_valid": False}

    # --- Hex character check ---
    if not re.fullmatch(r"[0-9A-F]{12}", stripped):
        anomalies.append({"field": "mac", "type": "mac_invalid_chars", "value": raw_str})
        return {"mac": raw_str, "mac_valid": False}

    # --- Build canonical AA:BB:CC:DD:EE:FF ---
    canonical = ":".join(stripped[i:i+2] for i in range(0, 12, 2))

    normalization_steps.append(f"mac: normalized to {canonical}")

    return {"mac": canonical, "mac_valid": True}
