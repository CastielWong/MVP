#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa


def print_cutting_line():
    print("-" * 80)


# ---------------------------------------------------------
a = ["a", "b"]
b = [1, 2]

# zip two arrays
for i, j in zip(a, b):
    print(f"{i} - {j}")  # ["a" - 1, "b" - 2]

print_cutting_line()

# get cartesian product
import itertools

alphabet = ["alpha", "beta", "gamma"]
lists = [a, b, alphabet]
for element_tuple in itertools.product(*lists):
    print(element_tuple)  # ("a", 1, "alpha"), ..., ('b', 2, 'gamma')

print_cutting_line()
# ---------------------------------------------------------
# Sort by value in Dictionary
mapping = {"a": 3, "b": 5, "c": 5, "d": 2}
print(mapping)

# sort the dictionary based on value
sorted_items = sorted(
    mapping.items(), key=lambda item: (-item[1], item[0]), reverse=True,
)
print(sorted_items)  # [('d', 2), ('a', 3), ('c', 5), ('b', 5)]

# convert the array back to dictionary
mapping_sorted = {k: v for k, v in sorted_items}  # {'d': 2, 'a': 3, 'c': 5, 'b': 5}
print(mapping_sorted)

print_cutting_line()
# ---------------------------------------------------------
# Conversion between chr and int
print(ord("A"))  # 65
print(ord("a"))  # 97
print(ord("2"))  # 50
print(chr(51))  # '3'
print(chr(38))  # '&'

print_cutting_line()
# ---------------------------------------------------------
# String checking
print("a".isalpha())  # True
print("a".isnumeric())  # False
print("1".isalpha())  # False
print("1".isnumeric())  # True
print("a1".isalpha())  # False
print("a1".isnumeric())  # False
print("a1".isalnum())  # True
print("ab".isalpha())  # True
print("12".isnumeric())  # True

print_cutting_line()
# ---------------------------------------------------------
# String generation
import string
import random

strings = random.choices(string.ascii_lowercase + string.digits, k=8)
randomized_string = "".join(strings)
print(f"{randomized_string = }")

print_cutting_line()
# ---------------------------------------------------------
# Type checking
a_set = set()
a_dict = {}

print(isinstance(a_set, set))  # True
print(isinstance(a_dict, dict))  # True

print(type(a_set) is set)  # True
print(type(a_dict) is dict)  # True

print_cutting_line()
# ---------------------------------------------------------
# Function signature
def demo(x=[]):
    print(id(x))
    x.append("a")
    return x


x = []
print(id(x))  # xxxxxx1
# the new list would be passed in
print(demo(x))  # xxxxxx1, ["a"]
print("-----------")
print(demo())  # xxxxxx2, ["a"]
# the list would be the one initiated when `demo()` is called
print(demo())  # xxxxxx2, ["a", "a"]

print_cutting_line()
# ---------------------------------------------------------
# Package checking
import pkg_resources

# check all available packages
package_list = sorted([f"{p.key}=={p.version}" for p in pkg_resources.working_set])
print(package_list)

print_cutting_line()
# ---------------------------------------------------------
# Module reload
from importlib import reload

reload({module})

print_cutting_line()
