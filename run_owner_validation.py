#!/usr/bin/env python3
"""
Deterministic owner validation with LLM fallback placeholder.
Used by run.py; no standalone execution.
"""

import re
import json

from prompt_templates import OWNER_PROMPT_TEMPLATE
from llm_utils import append_prompt_to_md, get_llm_placeholder

_EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
_TEAM_BRACKET_PATTERN = re.compile(r"\[([^\]]+)\]")
_TEAM_PAREN_PATTERN = re.compile(r"\(([^)]+)\)")
_TEAM_PREFIX_PATTERN = re.compile(r"(?:team\s*:\s*)(.+)", re.IGNORECASE)


def deterministic_owner_parse(owner_raw, notes, steps):
    """
    Parse owner field deterministically.
    Returns (owner, owner_email, owner_team, confident).
    """
    if owner_raw is None or str(owner_raw).strip() == "":
        return ("", "", "", False)

    value = str(owner_raw).strip()
    steps.append("owner: trimmed")

    owner = ""
    owner_email = ""
    owner_team = ""

    # Extract email
    email_match = _EMAIL_PATTERN.search(value)
    if email_match:
        owner_email = email_match.group(0)
        steps.append(f"owner_email: extracted {owner_email}")
        value = value.replace(owner_email, "").strip()

    # Extract team from brackets [Team]
    team_match = _TEAM_BRACKET_PATTERN.search(value)
    if team_match:
        owner_team = team_match.group(1).strip()
        steps.append(f"owner_team: extracted from brackets [{owner_team}]")
        value = _TEAM_BRACKET_PATTERN.sub("", value).strip()

    # Extract team from parentheses (Team)
    if not owner_team:
        team_match = _TEAM_PAREN_PATTERN.search(value)
        if team_match:
            owner_team = team_match.group(1).strip()
            steps.append(f"owner_team: extracted from parentheses ({owner_team})")
            value = _TEAM_PAREN_PATTERN.sub("", value).strip()

    # Extract team from prefix "Team: X"
    if not owner_team:
        team_match = _TEAM_PREFIX_PATTERN.search(value)
        if team_match:
            owner_team = team_match.group(1).strip()
            steps.append(f"owner_team: extracted from prefix Team: {owner_team}")
            value = _TEAM_PREFIX_PATTERN.sub("", value).strip()

    # Remaining value is the owner name
    # Clean up delimiters
    value = re.sub(r"[<>]", "", value).strip()
    value = re.sub(r"\s+", " ", value).strip()

    if value:
        # Title case the name
        owner = value.title()
        steps.append(f"owner: extracted name {owner}")
    elif owner_email:
        # Derive name from email local part
        local_part = owner_email.split("@")[0]
        # Replace dots/underscores with spaces, title case
        derived = re.sub(r"[._]", " ", local_part).title()
        owner = derived
        steps.append(f"owner: derived from email as {owner}")

    # Confidence check
    confident = False
    if owner_email:
        confident = True
    elif owner and re.fullmatch(r"[A-Za-z\s\-']+", owner):
        confident = True

    return (owner, owner_email, owner_team, confident)


def validate_owner_field(row, anomalies, normalization_steps):
    """
    Validate and normalize owner field.
    Returns dict with owner, owner_email, owner_team.
    """
    owner_raw = row.get("owner", "")
    notes = row.get("notes", "")
    row_id = row.get("source_row_id", "unknown")

    steps = []
    owner, owner_email, owner_team, confident = deterministic_owner_parse(owner_raw, notes, steps)

    if confident:
        normalization_steps.extend(steps)
        return {
            "owner": owner,
            "owner_email": owner_email,
            "owner_team": owner_team,
        }

    # LLM fallback
    row_json = json.dumps({k: v for k, v in row.items() if k in ("owner", "hostname", "device_type", "site", "source_row_id")}, indent=2)
    prompt = OWNER_PROMPT_TEMPLATE.format(row_json=row_json, notes=notes)
    rationale = (
        f"Deterministic rules failed because owner_raw='{owner_raw}' "
        "did not include a clear name, email, or team tag."
    )
    expected_schema = {
        "owner": "<string or 'unknown'>",
        "owner_email": "<email or null>",
        "owner_team": "<team or 'unknown'>"
    }

    append_prompt_to_md("Owner", row_id, prompt, rationale, expected_schema)

    normalization_steps.extend(steps)
    normalization_steps.append("owner: llm_generated_placeholder")

    placeholder = get_llm_placeholder("owner")
    return {
        "owner": placeholder["owner"],
        "owner_email": placeholder["owner_email"],
        "owner_team": placeholder["owner_team"],
    }
