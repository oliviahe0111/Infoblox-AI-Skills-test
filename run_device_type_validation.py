#!/usr/bin/env python3
"""
Deterministic device_type validation with LLM fallback placeholder.
Used by run.py; no standalone execution.
"""

import re
import json

from prompt_templates import DEVICE_TYPE_PROMPT_TEMPLATE
from llm_utils import append_prompt_to_md, get_llm_placeholder

# Keyword mapping: pattern → (canonical_type, confidence)
# Order matters: more specific patterns first
_DEVICE_TYPE_KEYWORDS = [
    # Exact matches (high confidence)
    (r"^router$", "router", "high"),
    (r"^switch$", "switch", "high"),
    (r"^server$", "server", "high"),
    (r"^printer$", "printer", "high"),
    (r"^firewall$", "firewall", "high"),
    (r"^workstation$", "workstation", "high"),
    (r"^laptop$", "laptop", "high"),
    (r"^phone$", "phone", "high"),
    (r"^camera$", "camera", "high"),
    (r"^access[_\s]?point$", "access_point", "high"),
    (r"^ap$", "access_point", "high"),
    (r"^storage$", "storage", "high"),
    (r"^load[_\s]?balancer$", "load_balancer", "high"),

    # Abbreviations (high confidence)
    (r"^rtr$", "router", "high"),
    (r"^rt$", "router", "high"),
    (r"^sw$", "switch", "high"),
    (r"^srv$", "server", "high"),
    (r"^prn$", "printer", "high"),
    (r"^fw$", "firewall", "high"),
    (r"^wap$", "access_point", "high"),
    (r"^pc$", "workstation", "high"),
    (r"^desktop$", "workstation", "high"),
    (r"^notebook$", "laptop", "high"),

    # Substring/model matches (medium confidence)
    (r"l[23]\s*switch", "switch", "medium"),
    (r"catalyst", "switch", "medium"),
    (r"nexus", "switch", "medium"),
    (r"virtual\s*machine", "server", "medium"),
    (r"^vm$", "server", "medium"),
    (r"esxi", "server", "medium"),
    (r"hypervisor", "server", "medium"),
    (r"mfp", "printer", "medium"),
    (r"laserjet", "printer", "medium"),
    (r"wifi", "access_point", "medium"),
    (r"aruba", "access_point", "medium"),
    (r"meraki", "access_point", "medium"),
    (r"palo\s*alto", "firewall", "medium"),
    (r"fortigate", "firewall", "medium"),
    (r"asa", "firewall", "medium"),
    (r"macbook", "laptop", "medium"),
    (r"thinkpad", "laptop", "medium"),
    (r"voip", "phone", "medium"),
    (r"ip\s*phone", "phone", "medium"),
    (r"polycom", "phone", "medium"),
    (r"handset", "phone", "medium"),
    (r"ipcam", "camera", "medium"),
    (r"cctv", "camera", "medium"),
    (r"axis", "camera", "medium"),
    (r"netapp", "storage", "medium"),
    (r"san\b", "storage", "medium"),
    (r"nas\b", "storage", "medium"),
    (r"f5", "load_balancer", "medium"),
    (r"bigip", "load_balancer", "medium"),

    # Generic substring matches (medium confidence)
    (r"router", "router", "medium"),
    (r"switch", "switch", "medium"),
    (r"server", "server", "medium"),
    (r"printer", "printer", "medium"),
    (r"firewall", "firewall", "medium"),
    (r"workstation", "workstation", "medium"),
    (r"laptop", "laptop", "medium"),
    (r"phone", "phone", "medium"),
    (r"camera", "camera", "medium"),
    (r"access\s*point", "access_point", "medium"),
]


def deterministic_device_type_parse(device_raw, notes, steps):
    """
    Parse device_type field deterministically.
    Returns (canonical_device_type, confidence).
    """
    if device_raw is None or str(device_raw).strip() == "":
        return ("", "low")

    value = str(device_raw).strip().lower()
    steps.append("device_type: lowercased")

    # Try each pattern
    for pattern, canonical, confidence in _DEVICE_TYPE_KEYWORDS:
        if re.search(pattern, value, re.IGNORECASE):
            steps.append(f"device_type: matched pattern '{pattern}' → {canonical}")
            return (canonical, confidence)

    # No match
    return (value, "low")


def validate_device_type_field(row, anomalies, normalization_steps):
    """
    Validate and normalize device_type field.
    Returns dict with device_type, device_type_confidence.
    """
    device_raw = row.get("device_type", "")
    notes = row.get("notes", "")
    row_id = row.get("source_row_id", "unknown")

    steps = []
    device_type, confidence = deterministic_device_type_parse(device_raw, notes, steps)

    if confidence in ("high", "medium"):
        normalization_steps.extend(steps)
        return {
            "device_type": device_type,
            "device_type_confidence": confidence,
        }

    # LLM fallback for low confidence
    row_json = json.dumps({k: v for k, v in row.items() if k in ("device_type", "hostname", "owner", "site", "source_row_id")}, indent=2)
    prompt = DEVICE_TYPE_PROMPT_TEMPLATE.format(row_json=row_json, notes=notes)
    rationale = (
        f"Unable to classify device_raw='{device_raw}' "
        "using keyword/model rules."
    )
    expected_schema = {
        "device_type": "<canonical type or 'unknown'>",
        "device_type_confidence": "<low|medium|high>"
    }

    append_prompt_to_md("Device Type", row_id, prompt, rationale, expected_schema)

    normalization_steps.extend(steps)
    normalization_steps.append("device_type: llm_generated_placeholder")

    placeholder = get_llm_placeholder("device_type")
    return {
        "device_type": placeholder["device_type"],
        "device_type_confidence": placeholder["device_type_confidence"],
    }
