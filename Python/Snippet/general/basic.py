#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa


def print_cutting_line():
    print("-" * 80)


# ---------------------------------------------------------
# Operator
a = 3 / 2  # 1.5
a = 3 // 2  # 1
a = 3 ** 2  # 9
a = 3 << 1  # 6
a = 2.99e8  # 299,000,000.0
a = 100_000  # 100,000

# logical operator
a = "a"
b = "b"
print(a and b)  # "b"
print(a and "")  # ""
print("" and a)  # ""

print(a or b)  # "a"
print(a or "")  # "a"
print("" or a)  # "a"


print(True is 1)  # False   # noqa: F632
print(True == 1)  # True    # noqa: E712

# in-built function
a = float("inf")  # infinite number
a = abs(1 - 3)  # 2

# is operator
a = ["a", "b"]
b = ["a", "b"]
print(a is b)  # False

# walrus operator (Assignment Expressions)
with open(__file__, "r") as fr:
    # output content of current file
    while text := fr.readline():
        print(text.strip("\n"))

print_cutting_line()
# ---------------------------------------------------------
# String Manipulation
s = "\tabc\nd\n"
print(s.strip())  # abc\nd
print(repr(s))  # "\tabc\nd\n"

s = """this is a string
    This can
        be
            a long string
"""
# find the first occurrence of "is"
s.find("is")  # 2
# find the first occurrence of "is" since index 5
s.find("is", 5)  # 5
s.find("that")  # -1

# use the walrus operator
if (n := len(s)) > 10:  # noqa: E203, E231
    print(f"The string is too long ({n} elements, expected <= 10)")

# convert string to an array in reversed order
print(list(s.strip())[::-1])

s = "3"
s.isalpha()  # false
s.isdigit()  # true
s.isalnum()  # true

print_cutting_line()
# ---------------------------------------------------------
# Loop
a_list = [i for i in range(3, 0, -1)]  # [3, 2, 1]

# 1 -> 2 -> 3
for i in range(len(a_list) - 1, -1, -1):
    print(a_list[i])

# (0, 3) -> (1, 2) -> (2, 1)
for index, number in enumerate(a_list):
    print(index, number)

print_cutting_line()
# ---------------------------------------------------------
# Sorting
a = [1, 5, 3, 2]

# sorted is copied
b = sorted(a, key=lambda x: -x)

print(a)  # [1, 5, 3, 2]

# sort is done in-place, so it would print nothing for the list
a.sort()  # None

print(a)  # [1, 2, 3, 5]
print(b)  # [5, 3, 2, 1]

print_cutting_line()
# ---------------------------------------------------------
# Copy
# note that string and tuple have no copy() method
a = [1, 2, 3]  # [1, 2, 3]
b = a.copy()  # [1, 2, 3]
a[1] = 5  # a: [1, 5, 3], b: [1, 2, 3]

print(f"{a = }\n{b = }")
print_cutting_line()

print_cutting_line()
# ---------------------------------------------------------
# Try-Catch
checking = [
    "red:14.2",
    "yellow.band",
    "23",
    "purple:-3",
    "blue:0",
    "green: band",
]

valid = 0
value_error = 0
index_error = 0
pass_else = 0
processed = 0

for item in checking:
    try:
        l = item.split(":")
        value = 1 / int(l[1])
        valid += 1
    except ValueError:
        value_error += 1
    except IndexError:
        index_error += 1
    except Exception as ex:
        # catch ZeroDivisionError
        print(f"Other exception: {ex}")
        processed -= 1
    else:
        pass_else += 1
    finally:
        processed += 1

# valid = 1, value_error = 2, index_error = 2, pass_else = 1, processed = 5
print(
    f"{valid = }\n"
    f"{value_error = }, {index_error = }, {pass_else = }\n"
    f"{processed = }"
)
