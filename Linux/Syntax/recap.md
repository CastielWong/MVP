
```sh
#!/usr/bin/env bash

# set up environment variable
export demo=demo

# receive input
first_input=$1
echo ${first_input}

# if-else
if [ -n ${first_input} ]; then
    echo "there is no input"
else
    echo "the input is ${first_input}"
fi


```
