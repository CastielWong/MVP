#!/bin/bash

coutner=0

# remove directories which are listed inside a file
while read line; do
    rm -rf "$line"
    echo "Removing: $counter - $line"
    counter=$((counter+1))
done < file_list.txt
