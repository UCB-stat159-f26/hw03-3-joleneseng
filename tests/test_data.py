import pandas as pd
import pytest

from tennis_career.data import (
    _format_player_name,
    _parse_career_js,
    _calculate_age,
    _process_female_matches,
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
