#!/usr/bin/env python3
"""
Unified data-cleaning pipeline for inventory_raw.csv.
Calls deterministic validators in order and writes inventory_clean.csv + anomalies.json.
"""

import csv
import json
import sys
from pathlib import Path

# Import IP validation helpers from existing module
from run_ipv4_validation import (
    ipv4_validate_and_normalize,
    default_subnet,
)
# Import MAC validation helper
from run_mac_validator import validate_mac_field
# Import hostname validation helper
from run_hostname_validation import validate_hostname_field
# Import FQDN validation helper
from run_fqdn_validation import validate_fqdn_field
# Import owner validation helper
from run_owner_validation import validate_owner_field
# Import device type validation helper
from run_device_type_validation import validate_device_type_field

HERE = Path(__file__).parent


def process(input_csv, out_csv, anomalies_json):
    all_anomalies = []

    with open(input_csv, newline="") as f, open(out_csv, "w", newline="") as g:
        reader = csv.DictReader(f)

        # Build output fieldnames: core validated columns first, then pass-through
        core_fields = [
            "ip", "ip_valid", "ip_version", "subnet_cidr",
            "mac", "mac_valid",
            "hostname", "hostname_valid",
            "fqdn", "fqdn_consistent", "reverse_ptr",
            "owner", "owner_email", "owner_team",
            "device_type", "device_type_confidence",
            "normalization_steps", "source_row_id",
        ]
        extra_fields = [c for c in reader.fieldnames if c not in core_fields]
        fieldnames = core_fields + extra_fields

        writer = csv.DictWriter(g, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            normalization_steps = []
            row_anomalies = []

            # ------------------------------------------------------------------
            # Step 1: IP validation (deterministic)
            # ------------------------------------------------------------------
            raw_ip = row.get("ip", "")
            valid_ip, canonical_ip, reason_ip = ipv4_validate_and_normalize(raw_ip)
            normalization_steps.append("ip_trim")

            if reason_ip == "ok":
                normalization_steps.append("ip_parse")
                normalization_steps.append("ip_normalize")
                ip_out = canonical_ip
                ip_valid = "true"
                ip_version = "4"
                subnet = default_subnet(ip_out)
            else:
                ip_out = str(raw_ip).strip()
                ip_valid = "false"
                ip_version = ""
                subnet = ""
                row_anomalies.append({"field": "ip", "type": reason_ip, "value": raw_ip})
                normalization_steps.append(f"ip_invalid_{reason_ip}")

            # ------------------------------------------------------------------
            # Step 2: MAC validation (deterministic)
            # ------------------------------------------------------------------
            mac_result = validate_mac_field(row, row_anomalies, normalization_steps)

            # ------------------------------------------------------------------
            # Step 3: Hostname validation (deterministic)
            # ------------------------------------------------------------------
            hostname_result = validate_hostname_field(row, row_anomalies, normalization_steps)

            # ------------------------------------------------------------------
            # Step 4: FQDN validation (deterministic)
            # ------------------------------------------------------------------
            # Pass ip_valid into row for fqdn validator to use
            row["ip_valid"] = ip_valid
            row["ip"] = ip_out
            fqdn_result = validate_fqdn_field(row, hostname_result, row_anomalies, normalization_steps)

            # ------------------------------------------------------------------
            # Step 5: Owner validation (deterministic + LLM fallback)
            # ------------------------------------------------------------------
            owner_result = validate_owner_field(row, row_anomalies, normalization_steps)

            # ------------------------------------------------------------------
            # Step 6: Device type validation (deterministic + LLM fallback)
            # ------------------------------------------------------------------
            device_type_result = validate_device_type_field(row, row_anomalies, normalization_steps)

            # ------------------------------------------------------------------
            # Build output row
            # ------------------------------------------------------------------
            clean_row = {
                "ip": ip_out,
                "ip_valid": ip_valid,
                "ip_version": ip_version,
                "subnet_cidr": subnet,
                "mac": mac_result["mac"],
                "mac_valid": str(mac_result["mac_valid"]).lower(),
                "hostname": hostname_result["hostname"],
                "hostname_valid": str(hostname_result["hostname_valid"]).lower(),
                "fqdn": fqdn_result["fqdn"],
                "fqdn_consistent": fqdn_result["fqdn_consistent"],
                "reverse_ptr": fqdn_result["reverse_ptr"],
                "owner": owner_result["owner"],
                "owner_email": owner_result["owner_email"],
                "owner_team": owner_result["owner_team"],
                "device_type": device_type_result["device_type"],
                "device_type_confidence": device_type_result["device_type_confidence"],
                "normalization_steps": "|".join(normalization_steps),
                "source_row_id": row.get("source_row_id", ""),
            }

            # Pass-through remaining fields unchanged
            for k in extra_fields:
                clean_row[k] = row.get(k, "")

            writer.writerow(clean_row)

            # Collect anomalies for this row
            if row_anomalies:
                all_anomalies.append({
                    "source_row_id": row.get("source_row_id"),
                    "issues": row_anomalies,
                    "recommended_actions": ["Review and correct flagged fields"],
                })

    with open(anomalies_json, "w") as h:
        json.dump(all_anomalies, h, indent=2)


def main():
    input_csv = HERE / "inventory_raw.csv"
    out_csv = HERE / "inventory_clean.csv"
    anomalies_json = HERE / "anomalies.json"

    if len(sys.argv) >= 2:
        input_csv = Path(sys.argv[1])

    process(str(input_csv), str(out_csv), str(anomalies_json))
    print(f"Wrote {out_csv} and {anomalies_json}")


if __name__ == "__main__":
    main()
