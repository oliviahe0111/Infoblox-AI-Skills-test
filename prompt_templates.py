#!/usr/bin/env python3
"""
Universal LLM prompt templates for fallback field extraction.
No actual LLM calls — these are logged to prompts.md for human review.
"""

OWNER_PROMPT_TEMPLATE = """\
Temperature: 0.2

You are a data normalization assistant. Extract owner information from the raw input.

## Input Row (JSON)
{row_json}

## Notes
{notes}

## Task
Parse the owner-related fields and return structured JSON.

- Extract the human owner name (not team, not email).
- Extract the email address if present.
- Extract the team name if present (often in brackets or parentheses).
- If a field cannot be determined, use "unknown" for strings or null for email.

## Output Schema (JSON only, no extra text)
{{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email string or null>",
  "owner_team": "<team string or 'unknown'>"
}}

## Examples
Input: "Jane Doe <jane.doe@acme.com> [NetOps]"
Output: {{"owner": "Jane Doe", "owner_email": "jane.doe@acme.com", "owner_team": "NetOps"}}

Input: "security-team@acme.com"
Output: {{"owner": "unknown", "owner_email": "security-team@acme.com", "owner_team": "unknown"}}

Input: "IT Infrastructure Team"
Output: {{"owner": "unknown", "owner_email": null, "owner_team": "IT Infrastructure Team"}}

Respond with valid JSON only.
"""

DEVICE_TYPE_PROMPT_TEMPLATE = """\
Temperature: 0.2

You are a network device classification assistant. Classify the device type from the raw input.

## Input Row (JSON)
{row_json}

## Notes
{notes}

## Task
Determine the canonical device type and confidence level.

Canonical device types:
  router, switch, server, printer, access_point, firewall,
  workstation, laptop, phone, camera, storage, load_balancer, unknown

Confidence levels:
  - high: exact keyword match or well-known model
  - medium: substring match or vendor inference
  - low: uncertain or guessing

## Output Schema (JSON only, no extra text)
{{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}}

## Examples
Input: {{"device_type": "Cisco Catalyst 3850"}}
Output: {{"device_type": "switch", "device_type_confidence": "high"}}

Input: {{"device_type": "Bob's old machine"}}
Output: {{"device_type": "workstation", "device_type_confidence": "low"}}

Input: {{"device_type": "xyzabc123"}}
Output: {{"device_type": "unknown", "device_type_confidence": "low"}}

Respond with valid JSON only.
"""

SITE_PROMPT_TEMPLATE = """\
Temperature: 0.2

You are a site/location normalization assistant. Normalize the site name to a canonical format.

## Input Row (JSON)
{row_json}

## Notes
{notes}

## Task
Normalize the site field to a standard uppercase, hyphenated format.

Common normalizations:
  - "Headquarters", "Head Quarters", "Main Office" → "HQ"
  - "Building", "Bldg", "Blg" → "BLDG"
  - "Data Center", "Datacenter" → "DC"
  - City names → airport codes (e.g., "San Francisco" → "SFO")

Rules:
  - Uppercase the result.
  - Replace spaces and underscores with hyphens.
  - Combine components: "HQ Bldg 1" → "HQ-BLDG-1"
  - If unrecognizable, return input uppercased with hyphens.

## Output Schema (JSON only, no extra text)
{{
  "site": "<trimmed original or ''>",
  "site_normalized": "<canonical uppercase or 'UNKNOWN'>"
}}

## Examples
Input: {{"site": "san francisco data center"}}
Output: {{"site": "san francisco data center", "site_normalized": "SFO-DC"}}

Input: {{"site": "Headqaurters Bldg 2"}}
Output: {{"site": "Headqaurters Bldg 2", "site_normalized": "HQ-BLDG-2"}}

Input: {{"site": ""}}
Output: {{"site": "", "site_normalized": "UNKNOWN"}}

Respond with valid JSON only.
"""
