# prompts.md (Template)

Document each LLM interaction: prompt, constraint, expected output format, and 1–2 lines of rationale.


### Owner Validation — Row 2

**Prompt:**
```
Temperature: 0.2

You are a data normalization assistant. Deterministic rules could not confidently
identify the owner, so this prompt is ONLY for ambiguous cases.

IMPORTANT:
- Do NOT assume a person name unless extremely obvious.
- Do NOT hallucinate names.
- If unsure, output owner="unknown".
- If the string looks like an environment, location, or description,
  treat it as non-human.
- Use the team field ONLY if explicitly mentioned (brackets, parentheses, or "Team:" style).
- If nothing can be determined, return:
    owner="unknown"
    owner_email=null
    owner_team="unknown"

## Input Row (JSON)
{
  "source_row_id": "2",
  "hostname": "host-02",
  "owner": "ops",
  "device_type": "",
  "site": "HQ Bldg 1"
}

## Notes
edge gw?

## Output Schema (JSON only, no extra text)
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email string or null>",
  "owner_team": "<team string or 'unknown'>"
}

## Examples
Input: "Main Server Room"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "ops"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "old storage rack"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Respond with valid JSON only.

```

**Rationale:**
Deterministic rules failed because owner_raw='ops' did not include a clear name, email, or team tag.

**Expected Output Schema:**
```json
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email or null>",
  "owner_team": "<team or 'unknown'>"
}
```
---

### Device Type Validation — Row 2

**Prompt:**
```
Temperature: 0.2

You are a network device classification assistant. Classify the device type from the raw input.

## Input Row (JSON)
{
  "source_row_id": "2",
  "hostname": "host-02",
  "owner": "ops",
  "device_type": "",
  "site": "HQ Bldg 1"
}

## Notes
edge gw?

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
{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}

## Examples
Input: {"device_type": "Cisco Catalyst 3850"}
Output: {"device_type": "switch", "device_type_confidence": "high"}

Input: {"device_type": "Bob's old machine"}
Output: {"device_type": "workstation", "device_type_confidence": "low"}

Input: {"device_type": "xyzabc123"}
Output: {"device_type": "unknown", "device_type_confidence": "low"}

Respond with valid JSON only.

```

**Rationale:**
Unable to classify device_raw='' using keyword/model rules.

**Expected Output Schema:**
```json
{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}
```
---

### Owner Validation — Row 4

**Prompt:**
```
Temperature: 0.2

You are a data normalization assistant. Deterministic rules could not confidently
identify the owner, so this prompt is ONLY for ambiguous cases.

IMPORTANT:
- Do NOT assume a person name unless extremely obvious.
- Do NOT hallucinate names.
- If unsure, output owner="unknown".
- If the string looks like an environment, location, or description,
  treat it as non-human.
- Use the team field ONLY if explicitly mentioned (brackets, parentheses, or "Team:" style).
- If nothing can be determined, return:
    owner="unknown"
    owner_email=null
    owner_team="unknown"

## Input Row (JSON)
{
  "source_row_id": "4",
  "hostname": "printer-01",
  "owner": "Facilities",
  "device_type": "printer",
  "site": "HQ"
}

## Notes


## Output Schema (JSON only, no extra text)
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email string or null>",
  "owner_team": "<team string or 'unknown'>"
}

## Examples
Input: "Main Server Room"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "ops"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "old storage rack"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Respond with valid JSON only.

```

**Rationale:**
Deterministic rules failed because owner_raw='Facilities' did not include a clear name, email, or team tag.

**Expected Output Schema:**
```json
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email or null>",
  "owner_team": "<team or 'unknown'>"
}
```
---

### Owner Validation — Row 5

**Prompt:**
```
Temperature: 0.2

You are a data normalization assistant. Deterministic rules could not confidently
identify the owner, so this prompt is ONLY for ambiguous cases.

IMPORTANT:
- Do NOT assume a person name unless extremely obvious.
- Do NOT hallucinate names.
- If unsure, output owner="unknown".
- If the string looks like an environment, location, or description,
  treat it as non-human.
- Use the team field ONLY if explicitly mentioned (brackets, parentheses, or "Team:" style).
- If nothing can be determined, return:
    owner="unknown"
    owner_email=null
    owner_team="unknown"

## Input Row (JSON)
{
  "source_row_id": "5",
  "hostname": "iot-cam01",
  "owner": "sec",
  "device_type": "iot",
  "site": "Lab-1"
}

## Notes
camera PoE on port 3

## Output Schema (JSON only, no extra text)
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email string or null>",
  "owner_team": "<team string or 'unknown'>"
}

## Examples
Input: "Main Server Room"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "ops"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "old storage rack"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Respond with valid JSON only.

```

**Rationale:**
Deterministic rules failed because owner_raw='sec' did not include a clear name, email, or team tag.

**Expected Output Schema:**
```json
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email or null>",
  "owner_team": "<team or 'unknown'>"
}
```
---

### Device Type Validation — Row 5

**Prompt:**
```
Temperature: 0.2

You are a network device classification assistant. Classify the device type from the raw input.

## Input Row (JSON)
{
  "source_row_id": "5",
  "hostname": "iot-cam01",
  "owner": "sec",
  "device_type": "iot",
  "site": "Lab-1"
}

## Notes
camera PoE on port 3

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
{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}

## Examples
Input: {"device_type": "Cisco Catalyst 3850"}
Output: {"device_type": "switch", "device_type_confidence": "high"}

Input: {"device_type": "Bob's old machine"}
Output: {"device_type": "workstation", "device_type_confidence": "low"}

Input: {"device_type": "xyzabc123"}
Output: {"device_type": "unknown", "device_type_confidence": "low"}

Respond with valid JSON only.

```

**Rationale:**
Unable to classify device_raw='iot' using keyword/model rules.

**Expected Output Schema:**
```json
{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}
```
---

### Owner Validation — Row 6

**Prompt:**
```
Temperature: 0.2

You are a data normalization assistant. Deterministic rules could not confidently
identify the owner, so this prompt is ONLY for ambiguous cases.

IMPORTANT:
- Do NOT assume a person name unless extremely obvious.
- Do NOT hallucinate names.
- If unsure, output owner="unknown".
- If the string looks like an environment, location, or description,
  treat it as non-human.
- Use the team field ONLY if explicitly mentioned (brackets, parentheses, or "Team:" style).
- If nothing can be determined, return:
    owner="unknown"
    owner_email=null
    owner_team="unknown"

## Input Row (JSON)
{
  "source_row_id": "6",
  "hostname": "local-test",
  "owner": "",
  "device_type": "",
  "site": "N/A"
}

## Notes


## Output Schema (JSON only, no extra text)
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email string or null>",
  "owner_team": "<team string or 'unknown'>"
}

## Examples
Input: "Main Server Room"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "ops"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "old storage rack"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Respond with valid JSON only.

```

**Rationale:**
Deterministic rules failed because owner_raw='' did not include a clear name, email, or team tag.

**Expected Output Schema:**
```json
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email or null>",
  "owner_team": "<team or 'unknown'>"
}
```
---

### Device Type Validation — Row 6

**Prompt:**
```
Temperature: 0.2

You are a network device classification assistant. Classify the device type from the raw input.

## Input Row (JSON)
{
  "source_row_id": "6",
  "hostname": "local-test",
  "owner": "",
  "device_type": "",
  "site": "N/A"
}

## Notes


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
{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}

## Examples
Input: {"device_type": "Cisco Catalyst 3850"}
Output: {"device_type": "switch", "device_type_confidence": "high"}

Input: {"device_type": "Bob's old machine"}
Output: {"device_type": "workstation", "device_type_confidence": "low"}

Input: {"device_type": "xyzabc123"}
Output: {"device_type": "unknown", "device_type_confidence": "low"}

Respond with valid JSON only.

```

**Rationale:**
Unable to classify device_raw='' using keyword/model rules.

**Expected Output Schema:**
```json
{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}
```
---

### Site Validation — Row 6

**Prompt:**
```
Temperature: 0.2

You are a site/location normalization assistant. Normalize the site name to a canonical format.

## Input Row (JSON)
{
  "source_row_id": "6",
  "hostname": "local-test",
  "owner": "",
  "device_type": "",
  "site": "N/A"
}

## Notes


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
{
  "site": "<trimmed original or ''>",
  "site_normalized": "<canonical uppercase or 'UNKNOWN'>"
}

## Examples
Input: {"site": "san francisco data center"}
Output: {"site": "san francisco data center", "site_normalized": "SFO-DC"}

Input: {"site": "Headqaurters Bldg 2"}
Output: {"site": "Headqaurters Bldg 2", "site_normalized": "HQ-BLDG-2"}

Input: {"site": ""}
Output: {"site": "", "site_normalized": "UNKNOWN"}

Respond with valid JSON only.

```

**Rationale:**
Site 'N/A' did not match known location patterns and abbreviation rules could not normalize it.

**Expected Output Schema:**
```json
{
  "site": "<trimmed original or ''>",
  "site_normalized": "<canonical uppercase or 'UNKNOWN'>"
}
```
---

### Owner Validation — Row 7

**Prompt:**
```
Temperature: 0.2

You are a data normalization assistant. Deterministic rules could not confidently
identify the owner, so this prompt is ONLY for ambiguous cases.

IMPORTANT:
- Do NOT assume a person name unless extremely obvious.
- Do NOT hallucinate names.
- If unsure, output owner="unknown".
- If the string looks like an environment, location, or description,
  treat it as non-human.
- Use the team field ONLY if explicitly mentioned (brackets, parentheses, or "Team:" style).
- If nothing can be determined, return:
    owner="unknown"
    owner_email=null
    owner_team="unknown"

## Input Row (JSON)
{
  "source_row_id": "7",
  "hostname": "host-apipa",
  "owner": "",
  "device_type": "",
  "site": ""
}

## Notes


## Output Schema (JSON only, no extra text)
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email string or null>",
  "owner_team": "<team string or 'unknown'>"
}

## Examples
Input: "Main Server Room"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "ops"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "old storage rack"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Respond with valid JSON only.

```

**Rationale:**
Deterministic rules failed because owner_raw='' did not include a clear name, email, or team tag.

**Expected Output Schema:**
```json
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email or null>",
  "owner_team": "<team or 'unknown'>"
}
```
---

### Device Type Validation — Row 7

**Prompt:**
```
Temperature: 0.2

You are a network device classification assistant. Classify the device type from the raw input.

## Input Row (JSON)
{
  "source_row_id": "7",
  "hostname": "host-apipa",
  "owner": "",
  "device_type": "",
  "site": ""
}

## Notes


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
{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}

## Examples
Input: {"device_type": "Cisco Catalyst 3850"}
Output: {"device_type": "switch", "device_type_confidence": "high"}

Input: {"device_type": "Bob's old machine"}
Output: {"device_type": "workstation", "device_type_confidence": "low"}

Input: {"device_type": "xyzabc123"}
Output: {"device_type": "unknown", "device_type_confidence": "low"}

Respond with valid JSON only.

```

**Rationale:**
Unable to classify device_raw='' using keyword/model rules.

**Expected Output Schema:**
```json
{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}
```
---

### Site Validation — Row 7

**Prompt:**
```
Temperature: 0.2

You are a site/location normalization assistant. Normalize the site name to a canonical format.

## Input Row (JSON)
{
  "source_row_id": "7",
  "hostname": "host-apipa",
  "owner": "",
  "device_type": "",
  "site": ""
}

## Notes


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
{
  "site": "<trimmed original or ''>",
  "site_normalized": "<canonical uppercase or 'UNKNOWN'>"
}

## Examples
Input: {"site": "san francisco data center"}
Output: {"site": "san francisco data center", "site_normalized": "SFO-DC"}

Input: {"site": "Headqaurters Bldg 2"}
Output: {"site": "Headqaurters Bldg 2", "site_normalized": "HQ-BLDG-2"}

Input: {"site": ""}
Output: {"site": "", "site_normalized": "UNKNOWN"}

Respond with valid JSON only.

```

**Rationale:**
Site '' did not match known location patterns and abbreviation rules could not normalize it.

**Expected Output Schema:**
```json
{
  "site": "<trimmed original or ''>",
  "site_normalized": "<canonical uppercase or 'UNKNOWN'>"
}
```
---

### Owner Validation — Row 9

**Prompt:**
```
Temperature: 0.2

You are a data normalization assistant. Deterministic rules could not confidently
identify the owner, so this prompt is ONLY for ambiguous cases.

IMPORTANT:
- Do NOT assume a person name unless extremely obvious.
- Do NOT hallucinate names.
- If unsure, output owner="unknown".
- If the string looks like an environment, location, or description,
  treat it as non-human.
- Use the team field ONLY if explicitly mentioned (brackets, parentheses, or "Team:" style).
- If nothing can be determined, return:
    owner="unknown"
    owner_email=null
    owner_team="unknown"

## Input Row (JSON)
{
  "source_row_id": "9",
  "hostname": "badhost",
  "owner": "",
  "device_type": "",
  "site": ""
}

## Notes


## Output Schema (JSON only, no extra text)
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email string or null>",
  "owner_team": "<team string or 'unknown'>"
}

## Examples
Input: "Main Server Room"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "ops"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "old storage rack"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Respond with valid JSON only.

```

**Rationale:**
Deterministic rules failed because owner_raw='' did not include a clear name, email, or team tag.

**Expected Output Schema:**
```json
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email or null>",
  "owner_team": "<team or 'unknown'>"
}
```
---

### Device Type Validation — Row 9

**Prompt:**
```
Temperature: 0.2

You are a network device classification assistant. Classify the device type from the raw input.

## Input Row (JSON)
{
  "source_row_id": "9",
  "hostname": "badhost",
  "owner": "",
  "device_type": "",
  "site": ""
}

## Notes


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
{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}

## Examples
Input: {"device_type": "Cisco Catalyst 3850"}
Output: {"device_type": "switch", "device_type_confidence": "high"}

Input: {"device_type": "Bob's old machine"}
Output: {"device_type": "workstation", "device_type_confidence": "low"}

Input: {"device_type": "xyzabc123"}
Output: {"device_type": "unknown", "device_type_confidence": "low"}

Respond with valid JSON only.

```

**Rationale:**
Unable to classify device_raw='' using keyword/model rules.

**Expected Output Schema:**
```json
{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}
```
---

### Site Validation — Row 9

**Prompt:**
```
Temperature: 0.2

You are a site/location normalization assistant. Normalize the site name to a canonical format.

## Input Row (JSON)
{
  "source_row_id": "9",
  "hostname": "badhost",
  "owner": "",
  "device_type": "",
  "site": ""
}

## Notes


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
{
  "site": "<trimmed original or ''>",
  "site_normalized": "<canonical uppercase or 'UNKNOWN'>"
}

## Examples
Input: {"site": "san francisco data center"}
Output: {"site": "san francisco data center", "site_normalized": "SFO-DC"}

Input: {"site": "Headqaurters Bldg 2"}
Output: {"site": "Headqaurters Bldg 2", "site_normalized": "HQ-BLDG-2"}

Input: {"site": ""}
Output: {"site": "", "site_normalized": "UNKNOWN"}

Respond with valid JSON only.

```

**Rationale:**
Site '' did not match known location patterns and abbreviation rules could not normalize it.

**Expected Output Schema:**
```json
{
  "site": "<trimmed original or ''>",
  "site_normalized": "<canonical uppercase or 'UNKNOWN'>"
}
```
---

### Owner Validation — Row 10

**Prompt:**
```
Temperature: 0.2

You are a data normalization assistant. Deterministic rules could not confidently
identify the owner, so this prompt is ONLY for ambiguous cases.

IMPORTANT:
- Do NOT assume a person name unless extremely obvious.
- Do NOT hallucinate names.
- If unsure, output owner="unknown".
- If the string looks like an environment, location, or description,
  treat it as non-human.
- Use the team field ONLY if explicitly mentioned (brackets, parentheses, or "Team:" style).
- If nothing can be determined, return:
    owner="unknown"
    owner_email=null
    owner_team="unknown"

## Input Row (JSON)
{
  "source_row_id": "10",
  "hostname": "neg",
  "owner": "",
  "device_type": "",
  "site": ""
}

## Notes


## Output Schema (JSON only, no extra text)
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email string or null>",
  "owner_team": "<team string or 'unknown'>"
}

## Examples
Input: "Main Server Room"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "ops"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "old storage rack"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Respond with valid JSON only.

```

**Rationale:**
Deterministic rules failed because owner_raw='' did not include a clear name, email, or team tag.

**Expected Output Schema:**
```json
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email or null>",
  "owner_team": "<team or 'unknown'>"
}
```
---

### Device Type Validation — Row 10

**Prompt:**
```
Temperature: 0.2

You are a network device classification assistant. Classify the device type from the raw input.

## Input Row (JSON)
{
  "source_row_id": "10",
  "hostname": "neg",
  "owner": "",
  "device_type": "",
  "site": ""
}

## Notes


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
{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}

## Examples
Input: {"device_type": "Cisco Catalyst 3850"}
Output: {"device_type": "switch", "device_type_confidence": "high"}

Input: {"device_type": "Bob's old machine"}
Output: {"device_type": "workstation", "device_type_confidence": "low"}

Input: {"device_type": "xyzabc123"}
Output: {"device_type": "unknown", "device_type_confidence": "low"}

Respond with valid JSON only.

```

**Rationale:**
Unable to classify device_raw='' using keyword/model rules.

**Expected Output Schema:**
```json
{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}
```
---

### Site Validation — Row 10

**Prompt:**
```
Temperature: 0.2

You are a site/location normalization assistant. Normalize the site name to a canonical format.

## Input Row (JSON)
{
  "source_row_id": "10",
  "hostname": "neg",
  "owner": "",
  "device_type": "",
  "site": ""
}

## Notes


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
{
  "site": "<trimmed original or ''>",
  "site_normalized": "<canonical uppercase or 'UNKNOWN'>"
}

## Examples
Input: {"site": "san francisco data center"}
Output: {"site": "san francisco data center", "site_normalized": "SFO-DC"}

Input: {"site": "Headqaurters Bldg 2"}
Output: {"site": "Headqaurters Bldg 2", "site_normalized": "HQ-BLDG-2"}

Input: {"site": ""}
Output: {"site": "", "site_normalized": "UNKNOWN"}

Respond with valid JSON only.

```

**Rationale:**
Site '' did not match known location patterns and abbreviation rules could not normalize it.

**Expected Output Schema:**
```json
{
  "site": "<trimmed original or ''>",
  "site_normalized": "<canonical uppercase or 'UNKNOWN'>"
}
```
---

### Owner Validation — Row 11

**Prompt:**
```
Temperature: 0.2

You are a data normalization assistant. Deterministic rules could not confidently
identify the owner, so this prompt is ONLY for ambiguous cases.

IMPORTANT:
- Do NOT assume a person name unless extremely obvious.
- Do NOT hallucinate names.
- If unsure, output owner="unknown".
- If the string looks like an environment, location, or description,
  treat it as non-human.
- Use the team field ONLY if explicitly mentioned (brackets, parentheses, or "Team:" style).
- If nothing can be determined, return:
    owner="unknown"
    owner_email=null
    owner_team="unknown"

## Input Row (JSON)
{
  "source_row_id": "11",
  "hostname": "bcast",
  "owner": "",
  "device_type": "",
  "site": ""
}

## Notes
Potential broadcast

## Output Schema (JSON only, no extra text)
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email string or null>",
  "owner_team": "<team string or 'unknown'>"
}

## Examples
Input: "Main Server Room"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "ops"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "old storage rack"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Respond with valid JSON only.

```

**Rationale:**
Deterministic rules failed because owner_raw='' did not include a clear name, email, or team tag.

**Expected Output Schema:**
```json
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email or null>",
  "owner_team": "<team or 'unknown'>"
}
```
---

### Device Type Validation — Row 11

**Prompt:**
```
Temperature: 0.2

You are a network device classification assistant. Classify the device type from the raw input.

## Input Row (JSON)
{
  "source_row_id": "11",
  "hostname": "bcast",
  "owner": "",
  "device_type": "",
  "site": ""
}

## Notes
Potential broadcast

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
{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}

## Examples
Input: {"device_type": "Cisco Catalyst 3850"}
Output: {"device_type": "switch", "device_type_confidence": "high"}

Input: {"device_type": "Bob's old machine"}
Output: {"device_type": "workstation", "device_type_confidence": "low"}

Input: {"device_type": "xyzabc123"}
Output: {"device_type": "unknown", "device_type_confidence": "low"}

Respond with valid JSON only.

```

**Rationale:**
Unable to classify device_raw='' using keyword/model rules.

**Expected Output Schema:**
```json
{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}
```
---

### Site Validation — Row 11

**Prompt:**
```
Temperature: 0.2

You are a site/location normalization assistant. Normalize the site name to a canonical format.

## Input Row (JSON)
{
  "source_row_id": "11",
  "hostname": "bcast",
  "owner": "",
  "device_type": "",
  "site": ""
}

## Notes
Potential broadcast

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
{
  "site": "<trimmed original or ''>",
  "site_normalized": "<canonical uppercase or 'UNKNOWN'>"
}

## Examples
Input: {"site": "san francisco data center"}
Output: {"site": "san francisco data center", "site_normalized": "SFO-DC"}

Input: {"site": "Headqaurters Bldg 2"}
Output: {"site": "Headqaurters Bldg 2", "site_normalized": "HQ-BLDG-2"}

Input: {"site": ""}
Output: {"site": "", "site_normalized": "UNKNOWN"}

Respond with valid JSON only.

```

**Rationale:**
Site '' did not match known location patterns and abbreviation rules could not normalize it.

**Expected Output Schema:**
```json
{
  "site": "<trimmed original or ''>",
  "site_normalized": "<canonical uppercase or 'UNKNOWN'>"
}
```
---

### Owner Validation — Row 12

**Prompt:**
```
Temperature: 0.2

You are a data normalization assistant. Deterministic rules could not confidently
identify the owner, so this prompt is ONLY for ambiguous cases.

IMPORTANT:
- Do NOT assume a person name unless extremely obvious.
- Do NOT hallucinate names.
- If unsure, output owner="unknown".
- If the string looks like an environment, location, or description,
  treat it as non-human.
- Use the team field ONLY if explicitly mentioned (brackets, parentheses, or "Team:" style).
- If nothing can be determined, return:
    owner="unknown"
    owner_email=null
    owner_team="unknown"

## Input Row (JSON)
{
  "source_row_id": "12",
  "hostname": "netid",
  "owner": "",
  "device_type": "",
  "site": ""
}

## Notes
Potential network id

## Output Schema (JSON only, no extra text)
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email string or null>",
  "owner_team": "<team string or 'unknown'>"
}

## Examples
Input: "Main Server Room"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "ops"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "old storage rack"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Respond with valid JSON only.

```

**Rationale:**
Deterministic rules failed because owner_raw='' did not include a clear name, email, or team tag.

**Expected Output Schema:**
```json
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email or null>",
  "owner_team": "<team or 'unknown'>"
}
```
---

### Device Type Validation — Row 12

**Prompt:**
```
Temperature: 0.2

You are a network device classification assistant. Classify the device type from the raw input.

## Input Row (JSON)
{
  "source_row_id": "12",
  "hostname": "netid",
  "owner": "",
  "device_type": "",
  "site": ""
}

## Notes
Potential network id

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
{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}

## Examples
Input: {"device_type": "Cisco Catalyst 3850"}
Output: {"device_type": "switch", "device_type_confidence": "high"}

Input: {"device_type": "Bob's old machine"}
Output: {"device_type": "workstation", "device_type_confidence": "low"}

Input: {"device_type": "xyzabc123"}
Output: {"device_type": "unknown", "device_type_confidence": "low"}

Respond with valid JSON only.

```

**Rationale:**
Unable to classify device_raw='' using keyword/model rules.

**Expected Output Schema:**
```json
{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}
```
---

### Site Validation — Row 12

**Prompt:**
```
Temperature: 0.2

You are a site/location normalization assistant. Normalize the site name to a canonical format.

## Input Row (JSON)
{
  "source_row_id": "12",
  "hostname": "netid",
  "owner": "",
  "device_type": "",
  "site": ""
}

## Notes
Potential network id

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
{
  "site": "<trimmed original or ''>",
  "site_normalized": "<canonical uppercase or 'UNKNOWN'>"
}

## Examples
Input: {"site": "san francisco data center"}
Output: {"site": "san francisco data center", "site_normalized": "SFO-DC"}

Input: {"site": "Headqaurters Bldg 2"}
Output: {"site": "Headqaurters Bldg 2", "site_normalized": "HQ-BLDG-2"}

Input: {"site": ""}
Output: {"site": "", "site_normalized": "UNKNOWN"}

Respond with valid JSON only.

```

**Rationale:**
Site '' did not match known location patterns and abbreviation rules could not normalize it.

**Expected Output Schema:**
```json
{
  "site": "<trimmed original or ''>",
  "site_normalized": "<canonical uppercase or 'UNKNOWN'>"
}
```
---

### Owner Validation — Row 13

**Prompt:**
```
Temperature: 0.2

You are a data normalization assistant. Deterministic rules could not confidently
identify the owner, so this prompt is ONLY for ambiguous cases.

IMPORTANT:
- Do NOT assume a person name unless extremely obvious.
- Do NOT hallucinate names.
- If unsure, output owner="unknown".
- If the string looks like an environment, location, or description,
  treat it as non-human.
- Use the team field ONLY if explicitly mentioned (brackets, parentheses, or "Team:" style).
- If nothing can be determined, return:
    owner="unknown"
    owner_email=null
    owner_team="unknown"

## Input Row (JSON)
{
  "source_row_id": "13",
  "hostname": "dns-google",
  "owner": "",
  "device_type": "router",
  "site": "DC-1"
}

## Notes


## Output Schema (JSON only, no extra text)
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email string or null>",
  "owner_team": "<team string or 'unknown'>"
}

## Examples
Input: "Main Server Room"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "ops"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "old storage rack"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Respond with valid JSON only.

```

**Rationale:**
Deterministic rules failed because owner_raw='' did not include a clear name, email, or team tag.

**Expected Output Schema:**
```json
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email or null>",
  "owner_team": "<team or 'unknown'>"
}
```
---

### Owner Validation — Row 14

**Prompt:**
```
Temperature: 0.2

You are a data normalization assistant. Deterministic rules could not confidently
identify the owner, so this prompt is ONLY for ambiguous cases.

IMPORTANT:
- Do NOT assume a person name unless extremely obvious.
- Do NOT hallucinate names.
- If unsure, output owner="unknown".
- If the string looks like an environment, location, or description,
  treat it as non-human.
- Use the team field ONLY if explicitly mentioned (brackets, parentheses, or "Team:" style).
- If nothing can be determined, return:
    owner="unknown"
    owner_email=null
    owner_team="unknown"

## Input Row (JSON)
{
  "source_row_id": "14",
  "hostname": "host-10",
  "owner": "",
  "device_type": "server",
  "site": ""
}

## Notes


## Output Schema (JSON only, no extra text)
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email string or null>",
  "owner_team": "<team string or 'unknown'>"
}

## Examples
Input: "Main Server Room"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "ops"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "old storage rack"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Respond with valid JSON only.

```

**Rationale:**
Deterministic rules failed because owner_raw='' did not include a clear name, email, or team tag.

**Expected Output Schema:**
```json
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email or null>",
  "owner_team": "<team or 'unknown'>"
}
```
---

### Site Validation — Row 14

**Prompt:**
```
Temperature: 0.2

You are a site/location normalization assistant. Normalize the site name to a canonical format.

## Input Row (JSON)
{
  "source_row_id": "14",
  "hostname": "host-10",
  "owner": "",
  "device_type": "server",
  "site": ""
}

## Notes


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
{
  "site": "<trimmed original or ''>",
  "site_normalized": "<canonical uppercase or 'UNKNOWN'>"
}

## Examples
Input: {"site": "san francisco data center"}
Output: {"site": "san francisco data center", "site_normalized": "SFO-DC"}

Input: {"site": "Headqaurters Bldg 2"}
Output: {"site": "Headqaurters Bldg 2", "site_normalized": "HQ-BLDG-2"}

Input: {"site": ""}
Output: {"site": "", "site_normalized": "UNKNOWN"}

Respond with valid JSON only.

```

**Rationale:**
Site '' did not match known location patterns and abbreviation rules could not normalize it.

**Expected Output Schema:**
```json
{
  "site": "<trimmed original or ''>",
  "site_normalized": "<canonical uppercase or 'UNKNOWN'>"
}
```
---

### Owner Validation — Row 15

**Prompt:**
```
Temperature: 0.2

You are a data normalization assistant. Deterministic rules could not confidently
identify the owner, so this prompt is ONLY for ambiguous cases.

IMPORTANT:
- Do NOT assume a person name unless extremely obvious.
- Do NOT hallucinate names.
- If unsure, output owner="unknown".
- If the string looks like an environment, location, or description,
  treat it as non-human.
- Use the team field ONLY if explicitly mentioned (brackets, parentheses, or "Team:" style).
- If nothing can be determined, return:
    owner="unknown"
    owner_email=null
    owner_team="unknown"

## Input Row (JSON)
{
  "source_row_id": "15",
  "hostname": "missing-ip",
  "owner": "",
  "device_type": "",
  "site": ""
}

## Notes


## Output Schema (JSON only, no extra text)
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email string or null>",
  "owner_team": "<team string or 'unknown'>"
}

## Examples
Input: "Main Server Room"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "ops"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Input: "old storage rack"
Output: {"owner": "unknown", "owner_email": null, "owner_team": "unknown"}

Respond with valid JSON only.

```

**Rationale:**
Deterministic rules failed because owner_raw='' did not include a clear name, email, or team tag.

**Expected Output Schema:**
```json
{
  "owner": "<string or 'unknown'>",
  "owner_email": "<email or null>",
  "owner_team": "<team or 'unknown'>"
}
```
---

### Device Type Validation — Row 15

**Prompt:**
```
Temperature: 0.2

You are a network device classification assistant. Classify the device type from the raw input.

## Input Row (JSON)
{
  "source_row_id": "15",
  "hostname": "missing-ip",
  "owner": "",
  "device_type": "",
  "site": ""
}

## Notes


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
{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}

## Examples
Input: {"device_type": "Cisco Catalyst 3850"}
Output: {"device_type": "switch", "device_type_confidence": "high"}

Input: {"device_type": "Bob's old machine"}
Output: {"device_type": "workstation", "device_type_confidence": "low"}

Input: {"device_type": "xyzabc123"}
Output: {"device_type": "unknown", "device_type_confidence": "low"}

Respond with valid JSON only.

```

**Rationale:**
Unable to classify device_raw='' using keyword/model rules.

**Expected Output Schema:**
```json
{
  "device_type": "<canonical type or 'unknown'>",
  "device_type_confidence": "<low|medium|high>"
}
```
---

### Site Validation — Row 15

**Prompt:**
```
Temperature: 0.2

You are a site/location normalization assistant. Normalize the site name to a canonical format.

## Input Row (JSON)
{
  "source_row_id": "15",
  "hostname": "missing-ip",
  "owner": "",
  "device_type": "",
  "site": ""
}

## Notes


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
{
  "site": "<trimmed original or ''>",
  "site_normalized": "<canonical uppercase or 'UNKNOWN'>"
}

## Examples
Input: {"site": "san francisco data center"}
Output: {"site": "san francisco data center", "site_normalized": "SFO-DC"}

Input: {"site": "Headqaurters Bldg 2"}
Output: {"site": "Headqaurters Bldg 2", "site_normalized": "HQ-BLDG-2"}

Input: {"site": ""}
Output: {"site": "", "site_normalized": "UNKNOWN"}

Respond with valid JSON only.

```

**Rationale:**
Site '' did not match known location patterns and abbreviation rules could not normalize it.

**Expected Output Schema:**
```json
{
  "site": "<trimmed original or ''>",
  "site_normalized": "<canonical uppercase or 'UNKNOWN'>"
}
```
---
