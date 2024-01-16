
- [General](#general)
- [Comparator](#comparator)


Generally, there are two ways to have customized heap based on the scenarios.
One is to place the sorted key in the front, the other is to use `__lt__`.
The first way is fitted in almost any case, while the second is basically for class.
Moreover, it's preferred to apply `__lt__` since it offers more flexibility in comparing string, the first approach can't implement MaxHeap for strings.


## General
The general way to customize a heap is by placing the sorting elements in front, then put all needed elements into the tuple behind.
```py
from heapq import heappush, heappop

heap = []
heappush(heap, (5, ("b", 5)))   # [(5, ('b', 5))]
heappush(heap, (3, ("c", 3)))   # [(3, ('c', 3)), (5, ('b', 5))]
heappush(heap, (4, ("a", 4)))   # [(3, ('c', 3)), (5, ('b', 5)), (4, ('a', 4))]
heappush(heap, (4, ("d", 4)))   # [(3, ('c', 3)), (4, ('d', 4)), (4, ('a', 4)), (5, ('b', 5))]

# "c", "a", "d", "b"
while heap:
    print(heappop(heap)[1][0])
```


## Comparator
Other than the general way, encapsulate elements into a class, then applying the comparator like `__lt__` and `__gt__` is another good approach.
```py
from heapq import heappush, heappop

class Item:
    def __init__(self, word, number):
        self.word = word
        self.number = number

    def __lt__(self, other):
        if self.number == other.number:
            return self.word > other.word

        return self.number < other.number

heap = []
heappush(heap, Item("b", 5))
heappush(heap, Item("c", 3))
heappush(heap, Item("a", 4))
heappush(heap, Item("d", 4))

# "c", "d", "a", "b"
while heap:
    print(heappop(heap).word)
```
