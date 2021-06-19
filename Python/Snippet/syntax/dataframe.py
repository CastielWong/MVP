#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
import pandas as pd
from pandas import DataFrame

# pd.set_option("display.float_format", lambda x: "%.5f" % x)

df = DataFrame()
df.loc[df["{col}"] == "{value}"]
df.loc[df["{col}"].isin(["{value1}", "{value2}"])]
df.loc[~df["{col}"].isin(["{value1}", "{value2}"])]

df.iloc["{index}"]["{col}"]

# several ways to get the row count
print(len(df.index))
print(len(df.shape[0]))
# though slowest, it avoids counting NaN values at first column
print(df[df.columns[0]].count())

# reference to add:
# - https://towardsdatascience.com/400x-time-faster-pandas-data-frame-iteration-16fb47871a0a
