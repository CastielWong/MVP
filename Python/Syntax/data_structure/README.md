
- [Dictionary](#dictionary)
- [Customized Heap](#customized-heap)

## Dictionary
Normally, the types of key in dictionary are integer or string, but it's acceptable to have either float/double or tuple type as the key.

Note that list or dictionary can not be the key for a dictionary, for the reason that key must be hashable, which also can be considered as immutable (a value can't be hashed if it's volatile).


## Customized Heap

Generally, there are two ways to have customized heap based on the scenarios. One is to place the sorted key in the front, the other is to use `__lt__`. The first way is fitted in almost any case, while the second is basically for class. Moreover, it's preferred to apply `__lt__` since it offers more flexibility in comparing string, the first approach can't implement MaxHeap for strings.

The output of the sample code would be in the order: __['c', 'a', 'd', 'b']__, while that of the second ones would be: __['c', 'd', 'a', 'b']__.
