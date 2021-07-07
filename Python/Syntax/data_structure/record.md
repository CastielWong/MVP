
- [Named Tuple](#named-tuple)

## Named Tuple
```py
from collections import namedtuple
from typing import NamedTuple

Row = namedtuple("Row", ["a", "b", "c"])
rows = []
rows.append(Row("apple", 1, 1.95))
rows.append(Row("banana", 2, 2.85))
rows.append(Row("Cherry", 3, 5.99))
print(rows)
print("-" * 80)

Result = NamedTuple("Result", [("name", str), ("id", int), ("price", float)])
results = map(Result._make, rows)
for r in results:
    print(r)
```
