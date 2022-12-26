
- [Configuration](#configuration)
- [Meta](#meta)
- [Indexing](#indexing)
- [Manipulation](#manipulation)
  - [Table Join](#table-join)
  - [Drop](#drop)
  - [Map](#map)
  - [Pivot](#pivot)
- [GroupBy](#groupby)
- [Null](#null)
- [Regex](#regex)
- [Reference](#reference)


Use example codes below to try if needed:
```py
from pandas import DataFrame
import pandas as pd

data = {
    "id": [1, 3, 5, 6, 7],
    "seq": ["foo", "bar", "baz", "qux", "quux"],
    "value": [.3, .8, .4, 5.9, 2.3]
}
df = DataFrame(data)
```


## Configuration
```py
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.max_colwidth", 30)
pd.set_option("display.width", 120)

pd.set_option("display.float_format", lambda x: "%.5f" % x)

# reset the configuration
pd.reset_option("all")
```


## Meta
```py
# read csv file
df = pd.read_csv("{file}", header="infer", skiprows=[0, 1], skip_blank_lines=True)

# convert list of JSON into DataFrame
df = pd.DataFrame(data={json_list}, columns=["{column1}", "{column2}"])

# set column names
df.columns = ["{column1}", "{column2}"]
# rename specific columns
df.rename(columns={"{oldName1}": "{newName1}", "{oldName2}": "{newName2}"}, inplace=True)

# check columns type
print(df.dtypes)
# update data type
df = df.astype({column_mapping})

# check unique values
df["{column}"].unique()

# there are several ways to get the row count
print(len(df.index))
print(len(df.shape[0]))
# though slowest, it avoids counting NaN values at first column
print(df[df.columns[0]].count())
```


## Indexing
For a DataFrame, use `[[]]` for the subset of DataFrame, while `[]` for the Series.
```py
# sort the df
df.sort_values(by=["{column}"], ascending=False, inplace=True)

# get records in specified index
df.iloc[2]["{col2}"]
df.iloc[[0, 3]]
df.iloc[[ : 9]]

# get the max value of a column
max_value = pd.Series(df["{column}"]).max()
subset = df.loc[df["{column}"] == max_value]

# retrieve candidates under condition
# count the occurrence of each group to get the Series
series = df.groupby("{column}")["{column}"].count()
# set the occurrence to be `NaN` if it's not larger than 1 by applying `where`
candidates = series.where("{column}" > 1)
# filter unqualified ones by negating those `NaN`s
series = series[~candidates.isnull()]

# retrieve data needed, both return the same DataFrame
df[df["{column}"] == 1]
df.loc[df["{column}"] == 1]
# retrieve data needed, both return the same Series, but only second one is mutable
df.loc[df["{col1}"] == 1]["{col2}"]
df.loc[df["{col1}"] == 1, "{col2}"] = {value}

# retrieve data via the index
df.loc[df["{column}"].isin(series.index)]
# extract records under certain conditions
df.loc[(df["{col1}"] == 1) & (df["{col2}"] != 0)]
# add/update values for particular records
df.loc[(df["{col1}"] == 1) & (df["{col2}"] != 0), "{new_col}"] = {value}
# filter out not matched records
df.loc[~df["{column}"].isin(["val_1", "val_2"])]

# count the occurrence of each group to get the DataFrame, group would be the index
subset = df.groupby("{column1}")[["{column2}", "{column3}"]].count()

# print full DataFrame
print(df.to_string())
print(df[["{col1}", "{col2}"]])
print(df.iloc[:, 0:2])
print(df.loc[:, ["{col1}", "{col2}"]])

df.loc["{index}"]
df.loc["{index}", "{col}"]
df.loc[["{index1}", "{index3}"], ["{colB}", "{colC}"]]

df.loc[df["seq"] == "baz"]
df.loc[df["id"].isin([1, 6])]
df.loc[~df["id"].isin([2, 5])]

df.iloc[0:2]["value"]

# retrieve the index who has the maximum value for each column
df.idxmax()
# set index column(s) to column(s) if not drop
df.reset_index(drop=False)

# append a new index level
df.set_index(keys="{col}", append=True, inplace=True)
# reorder indexes if it's MultiIndex
df.reorder_levels(["{index2}", "{index1}"])
```



## Manipulation

### Table Join
It's recommended to apply `concat` over `join` or `merge` when joining multiple tables:
- `concat` performs much quicker than `join` and `merge`, performance of `join` and `merge` are similar
- It accepts a list of Series/DataFrames, which makes the process easier
- It works as full outer join by default to avoid data loss
- However, `join` would be preferred if there are duplicate column names, since `concat` wouldn't be able to tell the difference.

Sample data to test:
```py
series = []
for i in range(100):
    a = pd.Series([1, 2, 3], index=[1, 3, 4], name=f"a_{i}")
    b = pd.Series(["a", "b", "c"], index=[1, 3, 5], name=f"b_{i}")
    c = pd.Series(["apple", "berry", "coco", "date"], index=[1, 2, 3, 4], name=f"c_{i}")
    series.append(a)
    series.append(b)
    series.append(c)

# use `concat`
df_concat = pd.concat(objs=series, axis=1)

# use `join`
df_join = pd.DataFrame(index=[1, 3, 4, 5])
for i in series:
    df_join = df_join.join(other=i, how="left")

# use `merge`
df_merge = pd.DataFrame(index=[1, 3, 4, 5])
for i in series:
    df_merge = df_merge.merge(right=i, how="left", left_index=True, right_index=True)

# # merge two DataFrame
# combined = pd.merge(df1, df2, how="left", on=["{column}"])
```

### Drop
```py
# drop row
df.drop("{row}", axis=0, inplace=True)
# drop column
df.drop("{col}", axis=1, inplace=True)
```

### Map
```py
# one to one mapping
df["{col}"] = df["{col}"].map({"{value1}": 1, "{value2}": 2})

```

### Pivot

```py
df = pd.DataFrame(data={
    "Day": ["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04", "2021-01-05"],
    "Apple": [1, 2, 2, 5, 3],
    "Berry": [.5, .3, .5, .8, 3.8],
    "Coconut": [15.5, 12.3, 13.5, 16.0, 13.6]
})

df_melted = df.melt(
    id_vars=["Day"],
    value_vars=["Berry", "Coconut"],
    var_name=["Fruit"], # can be MultiIndex
    value_name="Price",
)

df_pivot = df_melted.pivot(index="Day", columns=["Fruit"])
# remove the unneeded MultiIndex by resetting
df_pivot = df_pivot["Price"].reset_index()

```


## GroupBy

```py
check = pd.DataFrame(
    data={
        "group": [1, 1, 2, 1, 2],
        "user": ["a", "b", "c", "d", "e"],
        "num": [1, 2, 3, 4, 5],
    },
    index=[1, 2, 3, 8, 9]
)

# reset index based on the group
check.groupby("group").apply(lambda x: x.reset_index(drop=True))

# group nominal values in the same column
check.groupby(by=["group"])[["user"]].agg(lambda x: " | ".join(x))
```


## Null
```py
# check how many null values in each column
df.isnull().sum()
# check the first several rows with null value
df[df.isnull().values.any(axis=1)].head()

df.dropna(subset=["{clumn}"], inplace=True)
```


## Regex
```py
import re

# in order to replace columns value, it's needed to replace column by column but not multiple columns together
for c in ["{col1}", "{col2}"]:
    df[c].replace(r"{regex}", "{replaced}", regex=True, inplace=True)


# filter out data not in certain pattern
pattern = r"{regex}"
# note that `~` is the invert operator
df = df[~df["{column}"].str.contains(pattern, flags=re.I | re.M)]
```


## Reference
- 400x times faster Pandas Data Frame Iteration: https://towardsdatascience.com/400x-time-faster-pandas-data-frame-iteration-16fb47871a0a
- Reshaping Pandas Data frames with Melt & Pivot: https://medium.com/@durgaswaroop/reshaping-pandas-dataframes-melt-and-unmelt-9f57518c7738
- Merge, join, concatenate and compare: https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
