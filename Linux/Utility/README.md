
This directory contains scripts for common utility.

## Common Command
```sh
# get all files inside a directory with their size
find "${directory}/" -type f -exec stat --format="%n --- %s" {} + | sort > tmp.log

```


## Directory Removal
Remove a list of files/directories:
```sh
sh prune_dirs.sh {file.txt}
```
