import json
import re

import pandas as pd
import requests

from datetime import datetime

def _format_player_name(player_name):
    """Convert a player's name to Tennis Abstract's filename format."""
    if not isinstance(player_name, str) or not player_name.strip():
        raise ValueError("Player name must be a non-empty string.")

    if " " not in player_name.strip():
        return player_name.strip()[0].upper() + player_name.strip()[1:]

    return "".join(word.capitalize() for word in player_name.split())


def _download_career_js(player_name):
    """Download a player's career match JavaScript file."""
    formatted_name = _format_player_name(player_name)
    url = f"https://www.tennisabstract.com/jsmatches/{formatted_name}Career.js"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as error:
        raise ValueError(
            f"Could not retrieve career data for '{player_name}'. "
            "Check the player name or your internet connection."
        ) from error

    return response.text


def _parse_career_js(js_text):
    """Extract career match records from Tennis Abstract JavaScript."""
    match = re.search(r"var\s+morematchmx\s*=\s*(\[[\s\S]*?\]);", js_text)

    if not match:
        raise ValueError("Could not find career match data in JavaScript.")

    try:
        records = json.loads(match.group(1))
    except json.JSONDecodeError as error:
        raise ValueError("Career match data contains invalid JSON.") from error

    if not isinstance(records, list) or not records:
        raise ValueError("Career match data is empty or invalid.")

    return pd.DataFrame(records)


def _calculate_age(birth_date, match_date):
    """Calculate age in years at the time of a match."""
    birth = datetime.strptime(birth_date, "%Y%m%d")
    match = datetime.strptime(match_date, "%Y%m%d")

    return (match - birth).days / 365.25

