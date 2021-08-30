#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import string

import numpy as np
import pandas as pd

_CHARACTER_LIST = list(string.ascii_letters)
_DT_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
_SIZE = 1_000


def roll_to_null(prob: float) -> bool:
    if np.random.uniform() <= prob:
        return True

    return False


def generate_random_string(length: int, prob_nullable: float) -> str:
    if prob_nullable and roll_to_null(prob=prob_nullable):
        return None

    random_characters = []

    for _ in range(length):
        index = np.random.randint(low=0, high=len(_CHARACTER_LIST))

        random_characters.append(_CHARACTER_LIST[index])

    return "".join(random_characters)


def generate_random_datetime(
    dt_start: datetime, day_range: int, prob_nullable: float
) -> str:
    if prob_nullable and roll_to_null(prob=prob_nullable):
        return None

    delta = {
        "days": np.random.randint(low=0, high=day_range),
        "hours": np.random.randint(low=0, high=23),
        "minutes": np.random.randint(low=0, high=59),
        "seconds": np.random.randint(low=0, high=59),
        "microseconds": np.random.randint(low=0, high=999_999),
    }

    new_dt = dt_start + timedelta(**delta)

    return new_dt.strftime(_DT_FORMAT)


def main(size: int):
    start_date = datetime(year=2020, month=1, day=1)

    col_int = np.random.randint(low=-1_000, high=1_000, size=size, dtype="int64")
    col_double = np.random.random(size=size) * 1_000
    col_double = np.around(col_double, decimals=2)

    tmp = {
        "col_str": [],
        "col_dt": [],
        "str_nullable": [],
        "dt_nullable": [],
    }

    # generate a string list for a size of 20
    symbol_list = []
    for _ in range(20):
        symbol = generate_random_string(length=5, prob_nullable=0)
        symbol_list.append(symbol)

    for _ in range(size):
        tmp["col_str"].append(np.random.choice(symbol_list))
        tmp["col_dt"].append(
            generate_random_datetime(dt_start=start_date, day_range=50, prob_nullable=0)
        )
        tmp["str_nullable"].append(generate_random_string(length=5, prob_nullable=0.2))
        tmp["dt_nullable"].append(
            generate_random_datetime(
                dt_start=start_date, day_range=50, prob_nullable=0.4
            )
        )

    col_str = np.array(tmp["col_str"])
    col_dt = np.array(tmp["col_dt"])
    col_str_null = np.array(tmp["str_nullable"])
    col_dt_null = np.array(tmp["dt_nullable"])

    data = {
        "col_int": col_int,
        "col_double": col_double,
        "col_str": col_str,
        "col_dt": col_dt,
        "str_nullable": col_str_null,
        "dt_nullable": col_dt_null,
    }

    df = pd.DataFrame(data=data)

    print(df)

    return df


if __name__ == "__main__":
    main(size=1_000)
