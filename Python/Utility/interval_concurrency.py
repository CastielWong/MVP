#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Find out the concurrency between intervals."""
from datetime import datetime
from heapq import heappop, heappush
from typing import List, Optional, Tuple

from matplotlib.axes import Axes
from pandas import DataFrame
import matplotlib.pyplot as plt
import pandas as pd

TS_READABLE = "%Y-%m-%d %H:%M:%S"


class Interval:
    """Interval for time."""

    # pylint: disable=R0903(too-few-public-methods)

    def __init__(self, start: str, end: str):
        """Initialize an Interval.

        Args:
            start: Start timestamp string, which is formatted in "%Y-%m-%d %H:%M:%S"
            end: End timestamp string, which is formatted in "%Y-%m-%d %H:%M:%S"
        """
        self.start = start
        self.end = end

    def __lt__(self, other) -> bool:
        """Set for comparison.

        Args:
            other: Another Interval to compare

        Returns:
            Whether current Interval is lower than the other
        """
        if self.start == other.start:
            return self.end < other.end

        return self.start < other.start


def count_concurrency(intervals: List[Interval], time_stick: datetime) -> int:
    """Count the concurrency at a specified timestamp.

    Args:
        intervals: List of Interval
        time_stick: The timestamp for the concurrency

    Returns:
        Amount of concurrency
    """
    counter = 0

    for interval in intervals:
        dt_start = datetime.strptime(interval.start, TS_READABLE)
        dt_end = datetime.strptime(interval.end, TS_READABLE)

        if dt_start > time_stick or dt_end < time_stick:
            continue
        counter += 1

    return 0


def search_maximum_concurrency(
    intervals: List[Interval],
) -> Tuple[Optional[datetime], int]:
    """Search for the timestamp when there were at most concurrency.

    Args:
        intervals: List of Interval
        time_stick: The timestamp for the concurrency

    Returns:
        The timestamp and amount when the most concurrency happened
    """
    if not intervals:
        return None, 0

    heap_for_order: List[Interval] = []
    # sort the interval first
    for i in intervals:
        heappush(heap_for_order, i)

    # reorder `intervals``
    index = 0
    while heap_for_order:
        intervals[index] = heappop(heap_for_order)
        index += 1

    counter = 0
    flag_ts = None
    heap: List[Tuple[str, Interval]] = []

    for i in intervals:
        while heap:
            earliest_end, _ = heap[0]

            if earliest_end >= i.start:
                break
            heappop(heap)
        heappush(heap, (i.end, i))

        if counter >= len(heap):
            continue

        counter = len(heap)
        flag_ts = datetime.strptime(i.start, TS_READABLE)

    return flag_ts, counter


def consolidate_timing(raw_df: DataFrame, columns: list) -> DataFrame:
    """Consolidate values from multiple columns into one column.

    Args:
        raw_df: Raw DataFrame of the metric data
        columns: Columns of datetime to consolidate

    Returns:
        Metrics of consolidated timing in DataFrame
    """
    if raw_df.empty:
        return raw_df

    # reset index to differentiate individual runs
    raw_df.reset_index(inplace=True)
    raw_df.drop(columns=["index"], inplace=True)

    column_consolidated = "timing"
    df_cols = []
    for col_name in columns:
        # construct new DataFrame for the single column
        df_col = raw_df[col_name].to_frame()
        df_col["type"] = col_name
        df_col.rename(columns={col_name: column_consolidated}, inplace=True)

        df_cols.append(df_col)

    # values from the same row would share the same index
    df_combined = pd.concat(df_cols)
    # reset and extract index out for labeling
    df_combined.reset_index(level=0, inplace=True)
    # convert column "index" from int to str
    df_combined["index"] = df_combined["index"].astype(str)
    # convert column "timing" from str to datetime
    df_combined[column_consolidated] = pd.to_datetime(
        df_combined[column_consolidated], format=f"{TS_READABLE}.%f"
    )

    return df_combined


def label_plot(axes: Axes = None, **kwargs) -> None:
    """Set up labels for the plot.

    Args:
        axes: Axes meta for the plot
        **kwargs: Labeling values passed to `axes`
    """
    if not axes:
        return

    # set up default value to avoid exception
    labeling = {
        "title": "",
        "x": "",
        "y": "",
    }
    labeling.update(kwargs)

    axes.set_title(labeling["title"])
    axes.set_xlabel(labeling["x"])
    axes.set_ylabel(labeling["y"])

    return


def display_timing_overlap(raw_df: DataFrame, columns: list, **kwargs) -> None:
    """Draw the swim-lane chart to visualize the concurrent execution of multiple runs.

    Args:
        raw_df: Raw DataFrame of the metric data
        columns: Columns of datetime to consolidate, it's assumed the first one is
            for start time, while the second is for end time
        **kwargs: Labeling values passed to `ax`
    """
    # pylint: disable=R0914(too-many-locals)
    if raw_df.empty or not columns:
        return

    # convert selected columns to datetime type
    df = raw_df.copy()
    for col in columns:
        df[col] = pd.to_datetime(df[col])

    intervals = []
    col_start, col_end = columns
    # construct interval row by row
    for row in df.iterrows():
        interval = Interval(row[1][col_start], row[1][col_end])
        intervals.append(interval)

    time_stick = None
    # count the number of concurrency if timestamp is specified
    if "timestamp" in kwargs:
        timestamp = kwargs["timestamp"]
        # convert the timestamp from string to datetime
        time_stick = datetime.strptime(timestamp, TS_READABLE)
        counter = count_concurrency(intervals, time_stick)
    # check the maximum number of concurrency when not
    else:
        time_stick, counter = search_maximum_concurrency(intervals)

    df_timing = consolidate_timing(raw_df, columns)

    width = 5
    if df_timing.shape[0] > 100:
        width = df_timing.shape[0] // 20

    _, ax = plt.subplots(figsize=(10, width))
    plt.rc("ytick", labelsize=2)

    labeling = {
        "title": kwargs["title"] if "title" in kwargs else "Query Concurrency",
        "x": kwargs["x_label"] if "x_label" in kwargs else "Running Time",
        "y": kwargs["y_label"] if "y_label" in kwargs else "Individual Run",
    }
    label_plot(ax, **labeling)

    # hide the grid lines
    ax.grid(False)

    # draw each run with a horizontal line
    for i in df_timing["index"].unique():
        ax.plot("timing", "index", data=df_timing.loc[df_timing["index"] == i])

    # draw a vertical line for the maximum concurrency, or the time when specify
    ax.axvline(x=time_stick, alpha=0.5, color="black", linewidth=0.3)
    # label the concurrency amount
    ax.text(
        x=time_stick,
        y=df_timing.shape[0] / 2 - 1,  # set the label at the top of the plot
        s=str(counter),
    )

    # y tick doesn't matter
    ax.set_yticks("")

    plt.show()
    return
