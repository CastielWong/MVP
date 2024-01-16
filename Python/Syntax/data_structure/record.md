
- [Named Tuple](#named-tuple)
- [Data Class](#data-class)

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

## Data Class
```py
from dataclasses import dataclass

@dataclass
class Item:
    name: str
    identifier: int
    price: float

    def __str__(self) -> str:
        return f"{self.name} - {self.price}"

items = []
items.append(Item("apple", 1, 1.95))
items.append(Item("banana", 2, 2.85))
items.append(Item("Cherry", 3, 5.99))
print(items)
```
