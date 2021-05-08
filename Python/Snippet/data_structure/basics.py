#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa


def print_cutting_line():
    print("-" * 80)


# ---------------------------------------------------------
a_tuple = (1,)
# a_tuple = 1,
a_tuple = (1, 2)

# ---------------------------------------------------------
a_list = [1, 3, 2, 3, 1, 3, 3]
a_list.append(5)  # [1, 3, 2, 3, 1, 3, 3, 5]
# remove the first 3
a_list.remove(3)  # [1, 2, 3, 1, 3, 3, 5]
# remove the element in index 3
a_list.pop(3)  # [1, 2, 3, 3, 3, 5]
# insert element at index 3
a_list.insert(3, 8)  # [1, 2, 3, 8, 3, 3, 5]

# ---------------------------------------------------------
set_a = {3, 5}
set_b = {1, 3}
print(set_a.difference(set_b))  # {5}
print(set_a.union(set_b))  # {1, 3, 5}
print(set_a.intersection(set_b))  # {3}
set_a.add(1)  # {1, 3, 5}
set_a.remove(3)  # {1, 5}

print_cutting_line()
# ---------------------------------------------------------
a_map = {"a": 1, "c": 3}
a_map["b"] = 2  # {'a': 1, 'c': 3, 'b': 2}
a_map.pop("c")  # {'a': 1, 'b': 2}
del a_map["a"]  # {'b': 2}
a_map.pop("c", None)  # return None since there is no 'c'

# a dictionary follows input order
a_map = {}
a_map["a"] = 1  # {'a': 1}
a_map["c"] = 5  # {'a': 1, 'c': 5}
a_map = {}
a_map["c"] = 5  # {'c': 5}
a_map["a"] = 1  # {'c': 5, 'a': 1}

# ---------------------------------------------------------
stack = []  # use the list as stack
stack.append(1)  # [1]
stack.pop()  # 1

# ---------------------------------------------------------
from collections import deque

queue = deque()
queue.append(1)  # deque([1])
queue.popleft()  # deque([])

# ---------------------------------------------------------
# default is MinHeap, which means the minimum would be the one to pop
from heapq import heappush, heappop

heap = []
heappush(heap, 2)  # [2]
heappush(heap, 1)  # [1, 2]
print(heap[0])  # 1, the one which would be popped
heappop(heap)  # [2]

# ---------------------------------------------------------
from collections import defaultdict

counter = defaultdict(int)
for w in ["a", "b", "a"]:
    counter[w] += 1
