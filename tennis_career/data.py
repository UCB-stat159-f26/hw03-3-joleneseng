def _format_player_name(player_name):
    """Convert a player's name to Tennis Abstract's filename format."""
    if not isinstance(player_name, str) or not player_name.strip():
        raise ValueError("Player name must be a non-empty string.")

    if " " not in player_name.strip():
        return player_name.strip()[0].upper() + player_name.strip()[1:]

    return "".join(word.capitalize() for word in player_name.split())
