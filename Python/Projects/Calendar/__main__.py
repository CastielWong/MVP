#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Entrypoint to calendar highlighting visualization."""
from datetime import date, datetime
from typing import Any, List
import calendar

import yaml


def generate_dates_for_a_year(year: int) -> List[date]:
    """Generate all dates for a year.

    Args:
        year: the year integer

    Returns:
        List of dates for that year.
    """
    all_dates = []

    cal = calendar.Calendar()
    year_calendar: List[List[Any]] = cal.yeardatescalendar(year=year, width=3)

    for quarter_calendar in year_calendar:
        for month_calendar in quarter_calendar:
            for week_calendar in month_calendar:
                for date_obj in week_calendar:
                    # skip any date not in the year
                    if date_obj.year != year:
                        continue

                    all_dates.append(date_obj)

    return all_dates


def highlight_dates_in_a_week(week: List[date], highlighted: List[date]):
    r"""Highlight dates in a week.

    The way to highlight a number is via escaping characters like `\033[a;b;cm`, where
    `a;b;c` is optional.
    For instance, applying `\033[1;32;40m{highlighted_text}\033[m`, where:
    - \033: signal the following characters are part of an escape sequence
    - [1: set the text style to bold
    - ;32: set the text color to green, 32 represents green in ANSI color codes
    - ;40m: set the background color to black, 40 represents black in ANSI color codes
    - \033[m: reset text color to the default

    Args:
        week: list of dates for a week
        highlighted: dates
    """
    for date_obj in week:
        # escape sequence that changes the color of the text that follows it
        if date_obj in highlighted:
            print(f"\033[1;32;40m{date_obj.day:2}\033[m", end=" ")
        else:
            print(f"{date_obj.day:2}", end=" ")
    return


def highlight_dates_in_a_year(year: int, highlighted: List[date]):
    """Highlight dates in a year.

    Args:
        year: the year integer
        highlighted: dates
    """
    cal = calendar.Calendar()
    year_calendar: List[List[Any]] = cal.yeardatescalendar(year=year, width=3)

    earliest = min(highlighted)
    latest = max(highlighted)

    # Create a calendar with the highlighted dates
    for quarter_calendar in year_calendar:
        for month_calendar in quarter_calendar:
            # no need to output months out of the range
            if month_calendar[-1][-1] < earliest or month_calendar[0][0] > latest:
                continue

            # first element of the second list must be for the month
            month_ = month_calendar[1][0].month

            print(calendar.month_name[month_])
            print("Mo Tu We Th Fr Sa Su")

            for week_calendar in month_calendar:
                # skip the week which is included in previous month
                if week_calendar[0].month != month_:
                    continue

                highlight_dates_in_a_week(week=week_calendar, highlighted=highlighted)

                # output newline after a week
                print()

            # a blank line after a month
            print()
    return


def main(file_name: str, start_year: int, end_year: int):
    """Set up for main function.

    Args:
        file_name: name to the file with highlighted dates list
        start_year: year to start, inclusive
        end_year: year to end, exclusive
    """
    # Load the dates from the YAML file
    with open(file_name, "r") as f_r:
        dates_str = yaml.safe_load(f_r)

    date_objs = [datetime.strptime(date_, "%Y.%m.%d").date() for date_ in dates_str]

    for year in range(start_year, end_year):
        print("-" * 100)
        print(year)
        highlight_dates_in_a_year(year=year, highlighted=date_objs)


if __name__ == "__main__":
    main("check.yaml", 2010, 2024)
