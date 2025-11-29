#!/usr/bin/env python3
"""
Assignment-safe LLM utilities.
No actual LLM calls — logs prompts to prompts.md and returns placeholder values.
"""

import json
from pathlib import Path

PROMPTS_MD_PATH = Path(__file__).parent / "TEMPLATES" / "prompts.md"


def append_prompt_to_md(field_name, row_id, prompt, rationale, expected_schema):
    """
    Append a structured prompt log entry to prompts.md.
    """
    schema_json = json.dumps(expected_schema, indent=2)

    entry = f"""
### {field_name} Validation — Row {row_id}

**Prompt:**
```
{prompt}
```

**Rationale:**
{rationale}

**Expected Output Schema:**
```json
{schema_json}
```
---
"""
    with open(PROMPTS_MD_PATH, "a") as f:
        f.write(entry)


def get_llm_placeholder(field):
    """
    Return placeholder values for LLM fallback fields.
    Raises ValueError if field is unknown.
    """
    if field == "owner":
        return {
            "owner": "llm_generated_unknown",
            "owner_email": "llm_generated_null",
            "owner_team": "llm_generated_unknown",
        }
    elif field == "device_type":
        return {
            "device_type": "llm_generated_unknown",
            "device_type_confidence": "low",
        }
    elif field == "site":
        return {
            "site_normalized": "LLM_GENERATED_UNKNOWN",
        }
    else:
        raise ValueError(f"Unknown field for LLM placeholder: {field}")
