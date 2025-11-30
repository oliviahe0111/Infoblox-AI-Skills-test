# Approach: Network Inventory Data Cleaning Pipeline

## Overview

This project implements a **deterministic-first, LLM-fallback** data cleaning pipeline for normalizing raw network inventory records. The pipeline processes `inventory_raw.csv` and produces three outputs:

1. **`inventory_clean.csv`** — Normalized inventory with validated fields
2. **`anomalies.json`** — Structured list of validation errors per row
3. **`TEMPLATES/prompts.md`** — Logged LLM prompts for ambiguous cases (no real LLM calls)

The design prioritizes **reproducibility** and **transparency**: deterministic regex-based rules handle the majority of cases, while an LLM fallback mechanism is scaffolded for truly ambiguous inputs—without invoking any actual language model.

---

## Pipeline Architecture

```
┌─────────────────────┐
│  inventory_raw.csv  │
└──────────┬──────────┘
           ▼
┌──────────────────────────────────────────────────────────┐
│                      run.py                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│  │ IP / MAC   │→ │ Hostname   │→ │ FQDN       │          │
│  │ Validation │  │ Validation │  │ Validation │          │
│  └────────────┘  └────────────┘  └────────────┘          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│  │ Owner      │→ │ Device     │→ │ Site       │          │
│  │ Validation │  │ Type Valid │  │ Validation │          │
│  └────────────┘  └────────────┘  └────────────┘          │
└──────────────────────────────────────────────────────────┘
           │                              │
           ▼                              ▼
┌─────────────────────┐       ┌─────────────────────┐
│ inventory_clean.csv │       │   anomalies.json    │
└─────────────────────┘       └─────────────────────┘
           │
           ▼
┌─────────────────────┐
│ TEMPLATES/prompts.md│  (logged prompts for LLM fallback)
└─────────────────────┘
```

---

## Field Validation Strategies

### 1. IP Address (`run_ipv4_validation.py`)
- **Deterministic**: Parse with `ipaddress` stdlib, validate octets, normalize to dotted-decimal.
- **Output**: `ip`, `ip_valid`, `ip_version`, `subnet_cidr`
- **Anomalies**: `ip_missing`, `ip_invalid_format`, `ip_private_range`, etc.

### 2. MAC Address (`run_mac_validator.py`)
- **Deterministic**: Regex extraction of 6 hex octets; normalize to `AA:BB:CC:DD:EE:FF`.
- **Handles**: colons, hyphens, dots, mixed delimiters, missing separators.
- **Anomalies**: `mac_missing`, `mac_wrong_length`, `mac_invalid_chars`, `mac_mixed_delimiters`

### 3. Hostname (`run_hostname_validation.py`)
- **Deterministic**: RFC 1123-relaxed validation (alphanumeric + hyphens, max 63 chars).
- **Output**: `hostname`, `hostname_valid`
- **Anomalies**: `hostname_invalid_chars`, `hostname_too_long`, `hostname_leading_hyphen`

### 4. FQDN (`run_fqdn_validation.py`)
- **Deterministic**: Split by dots, validate each label, check hostname consistency.
- **Output**: `fqdn`, `fqdn_consistent`, `reverse_ptr`
- **Anomalies**: `fqdn_label_too_long`, `fqdn_label_invalid_chars`, `fqdn_hostname_mismatch`

### 5. Owner (`run_owner_validation.py`)
- **Deterministic rules** (in order):
  1. Extract email via regex → confident
  2. Extract team from `[brackets]`, `(parentheses)`, or `Team: X` prefix → confident
  3. Multi-word alphabetic string matching human-name pattern → confident
  4. Single-token matching Infoblox whitelist (`platform`, `security`, `network`, etc.) → `owner="unknown"`, `owner_team=<Token>`
- **LLM fallback**: Triggered when none of the above apply.
- **Output**: `owner`, `owner_email`, `owner_team`

### 6. Device Type (`run_device_type_validation.py`)
- **Deterministic**: Keyword/regex table with confidence tiers:
  - **High**: Exact canonical matches (`router`, `switch`, `server`, etc.)
  - **Medium**: Model names, vendor prefixes (`Cisco Catalyst`, `Palo Alto`, `Meraki`)
  - **Low**: No match → LLM fallback
- **Output**: `device_type`, `device_type_confidence`

### 7. Site (`run_site_validation.py`)
- **Deterministic**: Abbreviation mappings (`Headquarters`→`HQ`, `Building`→`BLDG`) and city codes (`San Francisco`→`SFO`).
- **Normalization**: Uppercase, hyphen-delimited (`HQ-BLDG-1`).
- **Confident if**: Matches structured pattern `^[A-Z]{2,4}(-[A-Z0-9]+)*$` or simple alphanumeric code.
- **LLM fallback**: If pattern unrecognized.
- **Output**: `site`, `site_normalized`

---

## LLM Fallback Mechanism

When deterministic rules fail to confidently parse a field, the pipeline:

1. **Generates a prompt** using a template from `prompt_templates.py`
2. **Logs the prompt** to `TEMPLATES/prompts.md` with:
   - Row identifier
   - Full prompt text
   - Rationale for fallback
   - Expected JSON output schema
3. **Returns a placeholder value** (e.g., `llm_generated_unknown`)

### Prompt Design Principles
- **Temperature: 0.2** — Minimizes creativity, maximizes determinism
- **JSON-only output** — No prose, strict schema enforcement
- **Defensive instructions** — "Do NOT hallucinate names", "If unsure, return unknown"
- **Examples provided** — Demonstrates expected input/output mappings

### Placeholder Values
| Field | Placeholder |
|-------|-------------|
| `owner` | `llm_generated_unknown` |
| `owner_email` | `llm_generated_null` |
| `owner_team` | `llm_generated_unknown` |
| `device_type` | `llm_generated_unknown` |
| `device_type_confidence` | `low` |
| `site_normalized` | `LLM_GENERATED_UNKNOWN` |

---

## Reproducibility Guarantees

1. **No external API calls**: All LLM interactions are simulated with logged prompts and placeholder outputs.
2. **Deterministic ordering**: Validators run in fixed sequence; same input → same output.
3. **Normalization audit trail**: Each row's `normalization_steps` column records every transformation applied.
4. **Versioned prompt templates**: Templates are stored in `prompt_templates.py` with fixed temperature settings.

---

## Running the Pipeline

```bash
# Default: reads inventory_raw.csv from current directory
python3 run.py

# Custom input
python3 run.py /path/to/custom_inventory.csv
```

### Output Files
- `inventory_clean.csv` — Fully normalized inventory
- `anomalies.json` — Validation errors with row IDs and issue types
- `TEMPLATES/prompts.md` — All generated LLM prompts (append-only log)

---

## Interpreting Outputs

### `inventory_clean.csv`
| Column | Description |
|--------|-------------|
| `ip`, `ip_valid`, `ip_version`, `subnet_cidr` | Validated IP with inferred CIDR |
| `mac`, `mac_valid` | Canonical MAC address |
| `hostname`, `hostname_valid` | RFC-compliant hostname |
| `fqdn`, `fqdn_consistent`, `reverse_ptr` | FQDN with consistency check and PTR record |
| `owner`, `owner_email`, `owner_team` | Parsed owner information |
| `device_type`, `device_type_confidence` | Classified device with confidence level |
| `site`, `site_normalized` | Original and normalized site code |
| `normalization_steps` | Pipe-delimited audit trail |
| `source_row_id` | Original row reference |

### `anomalies.json`
```json
[
  {
    "source_row_id": "5",
    "issues": [
      {"field": "ip", "type": "ip_invalid_format", "value": "999.999.999.999"},
      {"field": "mac", "type": "mac_wrong_length", "value": "AA:BB:CC"}
    ],
    "recommended_actions": ["Review and correct flagged fields"]
  }
]
```

### `TEMPLATES/prompts.md`
Each entry contains the full prompt, rationale, and expected schema—ready for human review or future LLM integration.

---

## Summary

This pipeline demonstrates a **hybrid validation architecture** that maximizes deterministic coverage while providing a clear path to LLM-assisted extraction for edge cases. The design ensures auditability, reproducibility, and alignment with enterprise data governance requirements.
