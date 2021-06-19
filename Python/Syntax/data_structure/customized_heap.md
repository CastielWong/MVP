


```py
def print_cutting_line():
    print("-" * 80)


# ---------------------------------------------------------
from heapq import heappush, heappop

heap = []
heappush(heap, (5, ("b", 5)))  # [(5, ('b', 5))]
heappush(heap, (3, ("c", 3)))  # [(3, ('c', 3)), (5, ('b', 5))]
heappush(heap, (4, ("a", 4)))  # [(3, ('c', 3)), (5, ('b', 5)), (4, ('a', 4))]
heappush(
    heap, (4, ("d", 4))
)  # [(3, ('c', 3)), (4, ('d', 4)), (4, ('a', 4)), (5, ('b', 5))]

# "c", "a", "d", "b"
while heap:
    print(heappop(heap)[1][0])

print_cutting_line()


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

while heap:
    print(heappop(heap).word)
```
