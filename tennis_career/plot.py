
import matplotlib.pyplot as plt


def plot_player_career(matches, player_name):
    """Plot a player's career matches by age difference."""
    fig, ax = plt.subplots(figsize=(12, 6))

    colors = {"W": "#4C78A8", "L": "#E45756"}
    for result, color in colors.items():
        subset = matches[matches["result"] == result]
        ax.scatter(
            subset["player_age"],
            subset["age_difference"],
            c=color,
            label="Win" if result == "W" else "Loss",
            alpha=0.6,
            s=15,
        )

    ax.axhline(0, color="gray", linestyle="--", linewidth=1)
    ax.set_xlabel("Player Age")
    ax.set_ylabel("Player Age − Opponent Age")
    ax.set_title(f"{player_name}: Career Matches")
    ax.legend()
    return fig
