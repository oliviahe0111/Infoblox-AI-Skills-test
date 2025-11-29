#!/usr/bin/env python3
"""
Deterministic FQDN validation and normalization helpers.
Used by run.py; no standalone execution.
"""

import re

_LABEL_PATTERN = re.compile(r"^[a-z0-9][a-z0-9\-]{0,61}[a-z0-9]$|^[a-z0-9]$")


def validate_fqdn_field(row, hostname_result, anomalies, normalization_steps):
    """
    Validate and normalize the 'fqdn' field of a row.
    """
    raw = row.get("fqdn")

    # --- Missing ---
    if raw is None or str(raw).strip() == "":
        anomalies.append({"field": "fqdn", "type": "fqdn_missing"})
        return {"fqdn": "", "fqdn_consistent": "false", "reverse_ptr": ""}

    raw_str = str(raw)
    value = raw_str.strip()

    if value != raw_str:
        normalization_steps.append("fqdn: trimmed whitespace")

    lowered = value.lower()
    if lowered != value:
        normalization_steps.append("fqdn: lowercased")
    value = lowered

    if value.endswith("."):
        value = value.rstrip(".")
        normalization_steps.append("fqdn: removed trailing dot")

    # --- Validate labels ---
    labels = value.split(".")
    for label in labels:
        # Empty label (host..example.com)
        if label == "":
            anomalies.append({
                "field": "fqdn",
                "type": "fqdn_empty_label",
                "value": raw_str
            })
            return {"fqdn": raw_str, "fqdn_consistent": "false", "reverse_ptr": ""}

        # Length > 63
        if len(label) > 63:
            anomalies.append({
                "field": "fqdn",
                "type": "fqdn_label_too_long",
                "value": raw_str
            })
            return {"fqdn": raw_str, "fqdn_consistent": "false", "reverse_ptr": ""}

        # Invalid characters (not matching allowed pattern)
        if not _LABEL_PATTERN.match(label):
            anomalies.append({
                "field": "fqdn",
                "type": "fqdn_label_invalid_chars",
                "value": raw_str
            })
            return {"fqdn": raw_str, "fqdn_consistent": "false", "reverse_ptr": ""}

    normalization_steps.append(f"fqdn: normalized to {value}")

    # --- fqdn_consistent ---
    fqdn_consistent = "false"
    if hostname_result.get("hostname_valid"):
        first_label = labels[0]
        if first_label == hostname_result.get("hostname", ""):
            fqdn_consistent = "true"
        else:
            anomalies.append({
                "field": "fqdn",
                "type": "fqdn_hostname_mismatch",
                "value": f"fqdn={value}, hostname={hostname_result.get('hostname', '')}"
            })

    # --- reverse_ptr ---
    reverse_ptr = ""
    ip_valid = row.get("ip_valid", "")
    ip = row.get("ip", "")
    if str(ip_valid).lower() == "true" and ip:
        parts = ip.split(".")
        if len(parts) == 4:
            reverse_ptr = f"{parts[3]}.{parts[2]}.{parts[1]}.{parts[0]}.in-addr.arpa."

    return {"fqdn": value, "fqdn_consistent": fqdn_consistent, "reverse_ptr": reverse_ptr}
