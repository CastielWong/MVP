#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
import pandas as pd
from pandas import DataFrame

df = DataFrame()
df.loc[df["{col}"] == "{value}"]
df.loc[df["{col}"].isin(["{value1}", "{value2}"])]
df.loc[~df["{col}"].isin(["{value1}", "{value2}"])]

df.iloc["{index}"]["{col}"]
