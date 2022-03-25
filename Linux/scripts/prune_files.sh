#!/bin/bash
# set the file list to delete
# note that the last line must be a new line
file_name=$1

coutner=0

while read line; do
    if ! test -e ${line}; then
        echo "${line} doesn't exist"
        continue
    fi

    rm -rf "${line}"
    counter=$((counter+1))
    echo "Removing: ${counter} - ${line}"
done < ${file_name}
