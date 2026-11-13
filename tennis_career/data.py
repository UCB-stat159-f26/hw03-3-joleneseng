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


def _process_female_matches(raw_data, player_birth_date):
    """Clean female player matches and calculate age differences."""
    matches = raw_data[[0, 4, 11, 16]].copy()
    matches.columns = ["match_date", "result", "opponent", "opponent_birth"]

    matches["player_age"] = matches["match_date"].apply(
        lambda date: _calculate_age(player_birth_date, date)
    )
    matches["opponent_age"] = matches.apply(
        lambda row: _calculate_age(row["opponent_birth"], row["match_date"])
        if isinstance(row["opponent_birth"], str)
        and len(row["opponent_birth"]) == 8
        else float("nan"),
        axis=1,
    )
    matches["age_difference"] = matches["player_age"] - matches["opponent_age"]

    return matches.dropna(subset=["age_difference"])


def _process_male_matches(raw_data, player_birth_date):
    """Clean male player matches and calculate age differences."""
    matches = raw_data[[0, 4, 11, 16]].copy()
    matches.columns = ["match_date", "result", "opponent", "opponent_age"]

    matches["player_age"] = matches["match_date"].apply(
        lambda date: _calculate_age(player_birth_date, date)
    )
    matches["opponent_age"] = pd.to_numeric(
        matches["opponent_age"], errors="coerce"
    )
    matches["age_difference"] = matches["player_age"] - matches["opponent_age"]

    return matches.dropna(subset=["age_difference"])



def _get_player_birth_date(player_name, is_female):
    """Retrieve a player's birth date from Tennis Abstract."""
    formatted_name = _format_player_name(player_name)
    profile_type = "wplayer" if is_female else "player"
    url = f"https://www.tennisabstract.com/cgi-bin/{profile_type}.cgi?p={formatted_name}"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as error:
        raise ValueError(f"Could not retrieve profile for '{player_name}'.") from error

    match = re.search(r"var\s+dob\s*=\s*(\d{8})\s*;", response.text)
    if not match:
        raise ValueError(f"Birth date not found for '{player_name}'.")

    return match.group(1)


def _is_female_data(raw_data):
    """Identify whether career data uses the women's format."""
    values = raw_data[16].dropna().astype(str)
    birth_dates = values.str.fullmatch(r"\d{8}")
    return bool(birth_dates.any())


def get_player_matches(player_name):
    """Retrieve and clean a tennis player's career match data."""
    js_text = _download_career_js(player_name)
    raw_data = _parse_career_js(js_text)
    is_female = _is_female_data(raw_data)
    birth_date = _get_player_birth_date(player_name, is_female)

    if is_female:
        matches = _process_female_matches(raw_data, birth_date)
    else:
        matches = _process_male_matches(raw_data, birth_date)

    return matches.reset_index(drop=True)
