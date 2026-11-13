from unittest.mock import patch, Mock

import pandas as pd
import pytest
import requests

from tennis_career.data import (
    _format_player_name,
    _parse_career_js,
    _calculate_age,
    _process_female_matches,
    _process_male_matches,
    _get_player_birth_date,
    _is_female_data,
    get_player_matches,
)

@pytest.mark.parametrize(
    "player_name, expected",
    [
        ("serena williams", "SerenaWilliams"),
        ("Serena Williams", "SerenaWilliams"),
        ("SerenaWilliams", "SerenaWilliams"),
        ("Rafael Nadal", "RafaelNadal"),
    ],
)
def test_format_player_name(player_name, expected):
    assert _format_player_name(player_name) == expected


@pytest.mark.parametrize("player_name", ["", "   ", None, 123])
def test_invalid_player_name(player_name):
    with pytest.raises(ValueError, match="non-empty string"):
        _format_player_name(player_name)


def test_parse_female_career_js():
    js_text = (
        'var morematchmx = [['
        '"19951030", "Canadian Open", "Carpet", "W", "L", '
        '"", "", "WC", "Q1", "6-1 6-1", "3", "Anne Miller", '
        '"149", "7", "", "R", "19770119"]];'
    )
    result = _parse_career_js(js_text)

    assert len(result) == 1
    assert result.iloc[0, 11] == "Anne Miller"
    assert result.iloc[0, 16] == "19770119"


def test_parse_male_career_js():
    js_text = (
        'var morematchmx = [['
        '"20010910", "Spain F10", "Hard", "S", "L", '
        '"", "", "WC", "R32", "2-6 7-5 6-2", "3", '
        '"Guillermo Platel", "731", "", "", "R", "22.264202601"]];'
    )
    result = _parse_career_js(js_text)

    assert len(result) == 1
    assert result.iloc[0, 11] == "Guillermo Platel"
    assert result.iloc[0, 16] == "22.264202601"


def test_parse_invalid_career_js():
    with pytest.raises(ValueError, match="Could not find"):
        _parse_career_js("This is not valid career data.")



@pytest.mark.parametrize(
    "birth_date, match_date, expected_age",
    [
        ("19810926", "19951030", 14.0917),
        ("19860603", "20010910", 15.2717),
        ("20000101", "20200101", 20.0),
    ],
)
def test_calculate_age(birth_date, match_date, expected_age):
    result = _calculate_age(birth_date, match_date)
    assert result == pytest.approx(expected_age, abs=0.01)


def test_process_female_matches():
    row = [""] * 17
    row[0] = "19951030"
    row[4] = "L"
    row[11] = "Anne Miller"
    row[16] = "19770119"

    raw_data = pd.DataFrame([row])
    result = _process_female_matches(raw_data, "19810926")

    assert len(result) == 1
    assert result.iloc[0]["result"] == "L"
    assert result.iloc[0]["opponent"] == "Anne Miller"
    assert result.iloc[0]["player_age"] == pytest.approx(14.0917, abs=0.01)
    assert result.iloc[0]["opponent_age"] == pytest.approx(18.7762, abs=0.01)
    assert result.iloc[0]["age_difference"] == pytest.approx(-4.6845, abs=0.01)


def test_process_male_matches():
    row = [""] * 17
    row[0] = "20010910"
    row[4] = "L"
    row[11] = "Guillermo Platel"
    row[16] = "22.264202601"

    raw_data = pd.DataFrame([row])
    result = _process_male_matches(raw_data, "19860603")

    assert len(result) == 1
    assert result.iloc[0]["result"] == "L"
    assert result.iloc[0]["opponent"] == "Guillermo Platel"
    assert result.iloc[0]["player_age"] == pytest.approx(15.2717, abs=0.01)
    assert result.iloc[0]["opponent_age"] == pytest.approx(22.2642, abs=0.01)
    assert result.iloc[0]["age_difference"] == pytest.approx(-6.9925, abs=0.01)


@pytest.mark.parametrize(
    "player_name, is_female, birth_date, profile_type",
    [
        ("Serena Williams", True, "19810926", "wplayer"),
        ("Rafael Nadal", False, "19860603", "player"),
    ],
)
def test_get_player_birth_date(
    player_name, is_female, birth_date, profile_type
):
    mock_response = Mock()
    mock_response.text = f"var dob = {birth_date};"

    with patch("tennis_career.data.requests.get", return_value=mock_response) as mock_get:
        result = _get_player_birth_date(player_name, is_female)

    assert result == birth_date
    assert f"/{profile_type}.cgi" in mock_get.call_args.args[0]


def test_get_player_birth_date_missing():
    mock_response = Mock()
    mock_response.text = "No birth date available"

    with patch("tennis_career.data.requests.get", return_value=mock_response):
        with pytest.raises(ValueError, match="Birth date not found"):
            _get_player_birth_date("Unknown Player", False)



@pytest.mark.parametrize(
    "opponent_ages, expected",
    [
        (["19770119", "19800615"], True),
        (["22.264202601", "25.5"], False),
        (["", None], False),
    ],
)
def test_is_female_data(opponent_ages, expected):
    raw_data = pd.DataFrame({16: opponent_ages})
    assert _is_female_data(raw_data) == expected


@pytest.mark.parametrize("is_female", [True, False])
def test_get_player_matches(is_female):
    raw_data = pd.DataFrame([["sample"]])
    expected = pd.DataFrame({"age_difference": [-4.5]})

    with patch("tennis_career.data._download_career_js", return_value="mock_js"):
        with patch("tennis_career.data._parse_career_js", return_value=raw_data):
            with patch("tennis_career.data._is_female_data", return_value=is_female):
                with patch("tennis_career.data._get_player_birth_date", return_value="19810926"):
                    processor = (
                        "_process_female_matches"
                        if is_female else "_process_male_matches"
                    )
                    with patch(f"tennis_career.data.{processor}", return_value=expected):
                        result = get_player_matches("Test Player")

    assert result.equals(expected)


def test_get_player_matches_invalid_name():
    """Check that an invalid player produces a meaningful error."""
    with patch("tennis_career.data.requests.get") as mock_get:
        mock_get.side_effect = requests.RequestException("Not found")

        with pytest.raises(ValueError, match="Could not retrieve career data"):
            get_player_matches("Not A Real Tennis Player")
