
```py
from collections import namedtuple

Row = namedtuple("Row", ["a", "b", "c"])
rows = []
rows.append(Row(20210101, 1, 100))
rows.append(Row(20210102, 2, 20))
rows.append(Row(20210103, 3, 33))

Result = namedtuple("Result", ["date", "id", "size"])
results = map(Result._make, rows)
print(results)

for r in results:
    print(r)
```
