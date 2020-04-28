#!/usr/bin/env python3

# Copyright 2020 David Kern
# Released under the MIT license (see LICENSE)

import csv
import datetime
from collections import namedtuple
import matplotlib.pyplot as plt


# Plot options

FILENAME = 'covid-19-data/us-states.csv'
HIGHLIGHT = None        # The state name to highlight on the graph, or None for no highlight
SAME_ORIGIN = True              # Align first case dates
CASES = True                    # True = cases, False = deaths
if CASES:
    TITLE = "Covid-19 Cases by State (data from The New York Times)"
else:
    TITLE = "Covid-19 Deaths by State (data from The New York Times)"

# Implementation

Datum = namedtuple('Datum', 'date cases deaths')
by_state = {}

first_case_by_state = {}
dates_by_state = {}
cases_by_state = {}
deaths_by_state = {}

# read and store by state
with open(FILENAME) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        d = Datum(datetime.date.fromisoformat(row['date']), int(row['cases']), int(row['deaths']))
        state = row['state']
        if state not in first_case_by_state:
            first_case_by_state[state] = d.date
        try:
            by_state[state].append(d)
        except KeyError:
            by_state[state] = [d]

# reorder into arrays
for key, value in by_state.items():
    dates_by_state[key] = []
    cases_by_state[key] = []
    deaths_by_state[key] = []
    for row in value:
        if SAME_ORIGIN:
            d = (row.date - first_case_by_state[key]).days
        else:
            d = row.date
        dates_by_state[key].append(d)
        cases_by_state[key].append(row.cases)
        deaths_by_state[key].append(row.deaths)

# plot non-highlighted data
for state in dates_by_state.keys():
    plt.plot(
        dates_by_state[state],
        cases_by_state[state] if CASES else deaths_by_state[state],
        label=key,
        color='grey',
        linewidth=1,
        alpha=0.4
    )
    plt.text(
        dates_by_state[state][-1],
        cases_by_state[state][-1] if CASES else deaths_by_state[state][-1],
        state,
        horizontalalignment='left',
        size='small',
        color='grey'
    )

# plot highlighted data
if HIGHLIGHT is not None:
    plt.plot(
        dates_by_state[HIGHLIGHT],
        cases_by_state[HIGHLIGHT] if CASES else deaths_by_state[HIGHLIGHT],
        label=HIGHLIGHT,
        color='orange',
        linewidth=2,
        alpha=0.7
    )

plt.ylabel('cases' if CASES else 'deaths')
plt.yscale('log')
plt.xlabel('days since first case' if SAME_ORIGIN else 'date')
plt.title(TITLE)
plt.show()
