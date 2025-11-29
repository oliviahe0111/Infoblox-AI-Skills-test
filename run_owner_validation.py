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

# Infoblox-provided valid single-token team names (whitelist)
KNOWN_SINGLE_TOKEN_TEAMS = {
    "platform",
    "security",
    "network",
    "infrastructure",
    "systems",
    "devops",
    "it",
    "support",
}


def deterministic_owner_parse(owner_raw, notes, steps):
    """
    Parse owner field deterministically.
    Returns (owner, owner_email, owner_team, confident).

    Confidence logic:
    1. Email found → confident
    2. Explicit team tag (brackets, parens, or "Team: X") → confident
    3. Multi-word string that looks like a human name → confident
    4. Single token matching Infoblox whitelist → owner="unknown", team=<token>, confident
    5. Otherwise → LLM fallback
    """
    if owner_raw is None or str(owner_raw).strip() == "":
        return ("", "", "", False)

    value = str(owner_raw).strip()
    steps.append("owner: trimmed")

    owner = ""
    owner_email = ""
    owner_team = ""
    team_tag_extracted = False

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
        team_tag_extracted = True
        steps.append(f"owner_team: extracted from brackets [{owner_team}]")
        value = _TEAM_BRACKET_PATTERN.sub("", value).strip()

    # Extract team from parentheses (Team)
    if not owner_team:
        team_match = _TEAM_PAREN_PATTERN.search(value)
        if team_match:
            owner_team = team_match.group(1).strip()
            team_tag_extracted = True
            steps.append(f"owner_team: extracted from parentheses ({owner_team})")
            value = _TEAM_PAREN_PATTERN.sub("", value).strip()

    # Extract team from prefix "Team: X"
    if not owner_team:
        team_match = _TEAM_PREFIX_PATTERN.search(value)
        if team_match:
            owner_team = team_match.group(1).strip()
            team_tag_extracted = True
            steps.append(f"owner_team: extracted from prefix Team: {owner_team}")
            value = _TEAM_PREFIX_PATTERN.sub("", value).strip()

    # Clean up delimiters from remaining value
    value = re.sub(r"[<>]", "", value).strip()
    value = re.sub(r"\s+", " ", value).strip()

    # Confidence check
    confident = False

    # Case 1: Email found → confident
    if owner_email:
        confident = True
        steps.append("owner: confident because email found")
        # Derive owner name from remaining value or email
        if value:
            owner = value.title()
            steps.append(f"owner: extracted name {owner}")
        else:
            local_part = owner_email.split("@")[0]
            derived = re.sub(r"[._]", " ", local_part).title()
            owner = derived
            steps.append(f"owner: derived from email as {owner}")
        return (owner, owner_email, owner_team, confident)

    # Case 2: Explicit team tag extracted → confident
    if team_tag_extracted:
        confident = True
        steps.append("owner: confident because explicit team tag extracted")
        if value:
            owner = value.title()
            steps.append(f"owner: extracted name {owner}")
        return (owner, owner_email, owner_team, confident)

    # Case 3: Multi-word string that looks like a human name → confident
    # Must have at least 2 tokens and match typical name pattern (letters only, each capitalized)
    tokens = value.split()
    if len(tokens) >= 2:
        # Check if it looks like a human name (each token is alphabetic)
        looks_like_name = all(re.match(r"^[A-Za-z]+$", t) for t in tokens)
        if looks_like_name:
            owner = value.title()
            confident = True
            steps.append(f"owner: confident multi-word name '{owner}'")
            return (owner, owner_email, owner_team, confident)

    # Case 4: Single token matching Infoblox whitelist → treat as team, not person
    if len(tokens) == 1 and tokens[0].lower() in KNOWN_SINGLE_TOKEN_TEAMS:
        owner = "unknown"
        owner_team = tokens[0].title()  # Capitalize first letter
        confident = True
        steps.append(f"owner: single-token whitelist match, team='{owner_team}'")
        return (owner, owner_email, owner_team, confident)

    # Case 5: Otherwise → ambiguous → LLM fallback
    confident = False
    if value:
        steps.append(f"owner: ambiguous '{value}', fallback to LLM")
    else:
        steps.append("owner: empty after parsing, fallback to LLM")

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
