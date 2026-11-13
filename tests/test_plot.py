
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from tennis_career.plot import plot_player_career


def test_plot_player_career():
    """Test that the plotting function creates the expected figure."""
    matches = pd.DataFrame({
        "player_age": [20, 21, 22, 23],
        "age_difference": [-3, 2, -1, 4],
        "result": ["W", "L", "W", "L"],
    })

    fig = plot_player_career(matches, "Test Player")
    ax = fig.axes[0]

    assert isinstance(fig, plt.Figure)
    assert ax.get_xlabel() == "Player Age"
    assert ax.get_ylabel() == "Player Age − Opponent Age"
    assert ax.get_title() == "Test Player: Career Matches"
    assert len(ax.collections) == 2

    plt.close(fig)
