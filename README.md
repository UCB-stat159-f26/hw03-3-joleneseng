
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

For this homework, I built on my previous assignment where I recreated a visualization of Serena Williams's tennis career. This time, instead of just making a graph for one player, I had to turn the code into a Python package that could be used for different tennis players. I found this more challenging because I had to think about how to make my code reusable and understandable for someone else.

One of the biggest challenges was figuring out how to work with the Tennis Abstract data. I realized that the men's and women's datasets stored opponent age information differently, so I couldn't process them in exactly the same way. I ended up writing separate helper functions for each format and figuring out how to retrieve player birth dates from their profiles. It took some trial and error, but breaking the process into smaller functions made it easier to identify problems and fix them.

I also learned a lot more about testing. In my previous assignments, I usually checked whether my code worked by running it and looking at the results. For this homework, I learned how to use mock data to test functions without having to access the website every time. I also got more practice working with `pyproject.toml`, organizing files into a package, and making sure the package could actually be installed from GitHub.

Another thing I tried to improve from my previous homework was my Git workflow. I made an effort to commit smaller changes separately instead of putting everything into one large commit. This made it easier to keep track of what I was adding and changing throughout the assignment.

I think this homework helped me better understand the difference between writing code that works for one project and writing code that other people can reuse. One limitation of my package is that it depends on how Tennis Abstract organizes its data, so changes to the website could affect whether the functions work correctly.