
- [Display Setting](#display-setting)
- [Meta](#meta)
- [Indexing](#indexing)
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


## Display Setting
```py
pd.set_option("display.float_format", lambda x: "%.5f" % x)
```


## Meta
```py
# several ways to get the row count
print(len(df.index))
print(len(df.shape[0]))
# though slowest, it avoids counting NaN values at first column
print(df[df.columns[0]].count())
```


## Indexing
```py
df.loc[df["seq"] == "baz"]
df.loc[df["id"].isin([1, 6])]
df.loc[~df["id"].isin([2, 5])]

df.iloc[0:2]["value"]
```


## Reference
- 400x times faster Pandas Data Frame Iteration: https://towardsdatascience.com/400x-time-faster-pandas-data-frame-iteration-16fb47871a0a
