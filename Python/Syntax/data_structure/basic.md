
- [Tuple](#tuple)
- [List](#list)
  - [Normal](#normal)
  - [Stack](#stack)
- [Set](#set)
- [Dictionary](#dictionary)
  - [Inbuilt](#inbuilt)
  - [Default Dictionary](#default-dictionary)
- [Deque](#deque)
- [Heap](#heap)


## Tuple
```py
a_tuple = (1,)
# a_tuple = 1,
a_tuple = (1, 2)
```


## List
### Normal
```py
a_list = [1, 3, 2, 3, 1, 3, 3]

a_list.append(5)        # [1, 3, 2, 3, 1, 3, 3, 5]
# remove the first 3
a_list.remove(3)        # [1, 2, 3, 1, 3, 3, 5]
# remove the element in index 3
a_list.pop(3)           # [1, 2, 3, 3, 3, 5]
# insert element at index 3
a_list.insert(3, 8)     # [1, 2, 3, 8, 3, 3, 5]
```

### Stack
List is also used as Stack in Python.
```py
stack = []

stack.append(1) # [1]
stack.pop() # 1
```


## Set
```py
set_a = {3, 5}
set_b = {1, 3}

set_a.add(1)                        # {1, 3, 5}
set_a.remove(3)                     # {1, 5}

print(set_a.difference(set_b))      # {5}
print(set_a.union(set_b))           # {1, 3, 5}
print(set_a.intersection(set_b))    # {1}
```


## Dictionary
Normally, the types of key in dictionary are integer or string, but it's acceptable to have either float/double or tuple type as the key.

Note that list or dictionary can not be the key for a dictionary, for the reason that key must be hashable, which also can be considered as immutable (a value can't be hashed if it's volatile).

### Inbuilt
```py
a_map = {"a": 1, "c": 3}

a_map["b"] = 2      # {'a': 1, 'c': 3, 'b': 2}
a_map.pop("c")      # {'a': 1, 'b': 2}
del a_map["a"]      # {'b': 2}

a_map.pop("c", None)    # return None since there is no 'c'

# dictionary follows input order
a_map = {}
a_map["a"] = 1      # {'a': 1}
a_map["c"] = 5      # {'a': 1, 'c': 5}

a_map = {}
a_map["c"] = 5      # {'c': 5}
a_map["a"] = 1      # {'c': 5, 'a': 1}
```

### Default Dictionary
```py
from collections import defaultdict

counter = defaultdict(int)
for w in ["a", "b", "a"]:
    counter[w] += 1
print(counter)  # defaultdict(<class 'int'>, {'a': 2, 'b': 1})
```


## Deque
```py
from collections import deque

queue = deque()

queue.append(1)  # deque([1])
queue.popleft()  # deque([])
```


## Heap
```py
# default is MinHeap, which means the minimum would be the one to pop
from heapq import heappush, heappop

heap = []

heappush(heap, 2)   # [2]
heappush(heap, 1)   # [1, 2]
print(heap[0])  # 1, the one which would be popped
heappop(heap)       # [2]
```
