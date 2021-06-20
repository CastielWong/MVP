
- [IO](#io)
- [JSON](#json)
- [Copy](#copy)
- [Directory](#directory)
- [File Size](#file-size)

## IO

```py
import sys

# read input from standard input (command line)
line = sys.stdin.readline()
print(line)

with open("{file}.csv", mode="r") as file_reader:
    # note that it's `readline()` but not `read()`
    line = file_reader.readline()

    while line:
        # skip an empty line
        if not line.strip():
            continue

        arguments = line.strip().split(",")
        print(arguments)

        line = file_reader.readline()
```


## JSON
```py
import json

# convert str to dict
data_str = '{"a": 1, "b": 2}'
data = json.loads(data_str)
print(type(data), data)

# convert dict to str
data_dict = {"a": 1, "b": 2}
data = json.dumps(data_dict)
print(type(data), data)

# load data from file to dict
with open("{file}", "r") as file_reader:
    data = json.load(file_reader)

# write data to file
with open("{file}", "w") as file_writer:
    json.dump(data_dict, file_writer)
```


## Copy
```py
import shutil

shutil.copyfile({file_source}, {file_target})
shutil.copytree({dir_source}, {dir_target}, dirs_exist_ok=True)

```


## Directory
```py
import os
from os.path import realpath, dirname, basename
from pathlib import Path

# check current file name
print(__file__)
print(realpath(__file__))

# check current working directory
print(os.getcwd())
print(dirname(__file__))
print(Path.cwd())

# check home of current user
print(Path.home())

# get the file or directory name
print(basename({file}))
# note that the directory must not ended with "/"
print(basename({directory}))

# check if a directory exists
if os.path.exists("demo_dir"):
    print("The directory is existed")

# make a new directory or new directories
try:
    os.mkdir("demo_dir")
    os.makedirs("a/b/c")
except FileExistsError as error:
    print(error)

# list elements in current directory
curr_path = Path.cwd()

# check if path is existed
print(curr_path.exists())

for f in os.listdir(curr_path):
    full_path = os.path.join(curr_path, f)
    if os.path.isfile(full_path):
        print(f"file - {f}")
    elif os.path.isdir(full_path):
        print(f"folder - {f}")
    elif os.path.islink(full_path):
        print(f"link - {f}")
    else:
        print(f"other - {f}")

# delete a direcotory
import shutil

shutil.rmtree({directory})
```


## File Size
```py
import os

print(os.path.getsize("{file}"))

stats = os.stat("{file}")
print(stats.st_size)

# ---------------------------------------------------------
# Append logs
# 1st way to append
fh = open("{log}", "a")
fh.write("checking\n")

# 2nd way to append
fh = open("{log}", "r+")
fh.seek(0, os.SEEK_END)
fh.write("checking\n")
```
