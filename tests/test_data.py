import pytest
from tennis_career.data import _format_player_name


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
