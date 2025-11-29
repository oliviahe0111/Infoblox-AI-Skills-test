#!/usr/bin/env python3
"""
Deterministic IPv4 validation and normalization helpers.
Used by run.py; no standalone execution.
"""


def ipv4_validate_and_normalize(ip_str):
    if ip_str is None:
        return (False, None, "missing")
    # remove surrounding whitespace
    s = str(ip_str).strip() 
    # quick reject obvious IPv6 / non-dot forms
    if ":" in s:
        return (False, None, "ipv6_or_non_ipv4")
    # split into 4 octects
    parts = s.split(".")
    if len(parts) != 4:
        return (False, None, "wrong_part_count")
    canonical_parts = []
    # ensure each part is numeric and in range
    for p in parts:
        if p == "":
            return (False, None, "empty_octet")
        # negative or non-digit
        # ignore leading plus sign for digit check, and ensure octect doesn't start with '-'
        if not (p.lstrip("+").isdigit() and not p.startswith("-")):
            return (False, None, "non_numeric_or_negative")
        try:
            # ensures it is strictly base 10 ASCII digits
            v = int(p, 10)
        except ValueError:
            return (False, None, "non_decimal_format")
        if v < 0 or v > 255:
            return (False, None, "octet_out_of_range")
        canonical_parts.append(str(v))
    canonical = ".".join(canonical_parts)
    return (True, canonical, "ok")

def classify_ipv4_type(ip):
    # Simple classification for context; not required for validity
    o = list(map(int, ip.split(".")))
    if o[0] == 10:
        return "private_rfc1918"
    if o[0] == 172 and 16 <= o[1] <= 31:
        return "private_rfc1918"
    if o[0] == 192 and o[1] == 168:
        return "private_rfc1918"
    if o[0] == 169 and o[1] == 254:
        return "link_local_apipa"
    if o[0] == 127:
        return "loopback"
    return "public_or_other"
    
def default_subnet(ip):
    # Heuristic: /24 for RFC1918, else None (you can adapt this)
    iptype = classify_ipv4_type(ip)
    if iptype == "private_rfc1918":
        parts = list(map(int, ip.split(".")))
        return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
    return ""
