# Infoblox — AI + DDI Take‑Home (Option 3: Data Cleaning via LLM)

## Summary of My Solution

This project implements a deterministic-first, LLM-fallback data-cleaning pipeline for normalizing
the synthetic `inventory_raw.csv` dataset into the IPAM-ready schema defined below.

For highly structured fields (IP, MAC, hostname, FQDN), the pipeline uses strict regex,
RFC-inspired validators, and normalization functions. For ambiguous fields (owner, device_type,
site), deterministic heuristics run first, and only when they cannot confidently classify a value,
the system prepares an LLM prompt using pre-defined templates. Since this assignment does not make
real API calls, all LLM interactions are logged to `prompts.md` and replaced with consistent
placeholder outputs.

The pipeline emphasizes:
- **Reproducibility** — deterministic transforms, versioned prompt templates  
- **Transparency** — every normalization step logged per row  
- **Auditability** — anomalies captured in `anomalies.json`  
- **LLM readiness** — prompts designed for low-temperature, schema-restricted outputs  

The resulting `inventory_clean.csv` contains fully normalized values, with no critical field left
blank, and with clear fallbacks where additional semantic interpretation would normally require an
LLM.


## Challenge
Clean, normalize, and enrich `inventory_raw.csv` into a structured dataset fit for IPAM/DNS/DHCP workflows. Use deterministic rules first; use LLMs only where rules are weak. Log every prompt and explain your iterations briefly.

## Deliverables
1. `inventory_clean.csv`
2. `anomalies.json`
3. `prompts.md`
4. `approach.md`
5. `cons.md`
6. `run.py` or `run.sh`
7. (Optional) `ddi_ideas.md`

## Target Schema
```
ip, ip_valid, ip_version, subnet_cidr,
hostname, hostname_valid, fqdn, fqdn_consistent, reverse_ptr,
mac, mac_valid,
owner, owner_email, owner_team,
device_type, device_type_confidence,
site, site_normalized,
source_row_id, normalization_steps
```

## Provided
- `inventory_raw.csv` (synthetic)
- `run_ipv4_validation.py.txt` (example IPv4 normalization)
- `TEMPLATES/` (documents to fill)
- `run.py.txt` (orchestrator you can extend)
