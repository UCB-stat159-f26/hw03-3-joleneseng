
# Tennis Career Visualization Package

## Overview

This project creates a Python package for retrieving, cleaning, and visualizing professional tennis players' career match data from Tennis Abstract.

The package provides two public functions:

- `get_player_matches()`: Retrieves career match data for a specified player and returns a cleaned pandas DataFrame.
- `plot_player_career()`: Creates a scatter plot showing a player's age and age difference relative to their opponents, with wins and losses distinguished by color.

## Installation

Install the package directly from GitHub:

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-3-joleneseng.git
```

The package requires Python 3.10 or later and uses pandas, matplotlib, and requests.

## Usage

```python
from tennis_career import get_player_matches, plot_player_career

matches = get_player_matches("Serena Williams")

print(matches.head())

fig = plot_player_career(matches, "Serena Williams")
fig.savefig("serena_career.png", dpi=150, bbox_inches="tight")
```

The package also supports male players:

```python
nadal = get_player_matches("Rafael Nadal")
fig = plot_player_career(nadal, "Rafael Nadal")
fig.savefig("nadal_career.png")
```

## Visualization

The scatter plot uses:

- **X-axis:** Player's age at each match.
- **Y-axis:** Player's age minus opponent's age.
- **Blue points:** Wins.
- **Red points:** Losses.

A negative age difference indicates that the player was younger than their opponent, while a positive difference indicates that the player was older.

## Data Source

Career match data and player birth dates are retrieved from [Tennis Abstract](https://www.tennisabstract.com/).

The package handles different data formats for men's and women's career records.

## Testing

Run the automated tests from the project directory:

```bash
python -m pytest tests/ -v
```

The tests use mocked responses and sample data rather than contacting live websites.

## Project Structure

```text
tennis_career/
    __init__.py
    data.py
    plot.py

tests/
    test_data.py
    test_plot.py

pyproject.toml
README.md
```

## Reflections

This assignment helped me understand how to transform a standalone data analysis project into a reusable Python package. One of the main challenges was handling the differences between men's and women's Tennis Abstract data, since opponent age information is stored in different formats.

I addressed this by separating the data retrieval, parsing, cleaning, and visualization steps into smaller helper functions. This made the code easier to test and helped me stay within the assignment's function-length requirements.

I also learned how to use mocked responses in automated tests so that the package can be tested without relying on an external website. Compared with my previous replication project, I focused more on modular code, reproducibility, and organizing Git commits around specific changes.

One limitation is that the package depends on Tennis Abstract's website structure and the availability of player birth dates. If the website changes its data format, some retrieval functions may need to be updated.
