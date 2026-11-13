import pytest
from tennis_career.data import _format_player_name, _parse_career_js


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
