
- [Meta](#meta)
- [Manipulation](#manipulation)
- [Reference](#reference)

A double dash (--) is used in most bash built-in commands and many other commands to signify the end of command options, after which only positional parameters are accepted. For example, `python --help | grep -- "-m"` works, but `python --help | grep -m` doesn't.

Bash accommodates piping and redirection by way of special files. Each process gets it's own set of files (one for STDIN, STDOUT and STDERR respectively) and they are linked when piping or redirection is invoked. Each process gets the following files, where "fd" stands for file descriptor:

- STDIN: "/dev/stdin" or "/proc/<processID>/fd/0"
- STDOUT: "/dev/stdout" or "/proc/<processID>/fd/1"
- STDERR: "/dev/stderr" or "/proc/<processID>/fd/2"

To customize the shell prompt for bash, set environment variable `$PS1` for the purpose:
`export PS1="[\t \u@\h \w]\$ "`. Or set `PS1` in "~/.bashrc" directly for persistency.


## Meta
There are variables automatically set by Bash when it's a Bash script:

- `$0`: name of the script
- `$n`: the nth arguments passed to the script
- `$#`: number of arguments passed to the script
- `$*` / `$@`: all arguments passed to the script
- `$?`: exit status of the most recently run process
- `$$`: process ID of current script
- `$SECONDS`: number of seconds since the script was started
- `$RANDOM`: return a random number
- `$LINENO`: return the current lin number in the script

Run `env` to check other available variables.

For the `if` statement in Bash script, it actually makes use of another command `test`.

```bash
DEMO="demo"

# single quotes will treat ever character literally
myvar='This is $DEMO'   # This is $DEMO
# double quotes allow the variable substitution to take effect
myvar="This is $DEMO"   # This is demo

# apply command substitution
myvar=$( ls /etc | wc -l )

# check the length of a string
echo ${#DEMO}           # 4

# use the function
function print_demo {
    local var1=$1
    var2=$2             # default is global

    echo "Latter variable: ${var2}; Former one is ${var1}"

    return 123
}

print_demo ace cat      # Latter variable: cat; Former one is ace
echo "The status of function returns is: $?"    # 123

echo "var1 is: ${var1}; var2 is: ${var2}"       # var1 is: ; var2 is: cat
```


## Manipulation
```bash
expr 3 \* 2             # 6
expr "3 + 2"            # 3 + 2
expr 3+2                # 3+2

a=$( expr 3 - 1 )       # 2
b=$(( $a + 6 ))         # 8
```

Check the manual of test `man test` for operator description:
```bash
# if-else statement
if [ $1 -ge 10 ]
then
    echo "First variable is larger than or equal to 10"
elif [ $2 == 'yes' ]
then
    echo "Second one is the actual 'yes'"
else
    echo "None of the variables is matched"
fi

# case-switch statement
case $2 in
    "yes")
        echo "Here comes yes"
        ;;
    "no")
        echo "Here comes no"
        ;;
    *)
        echo "Something else: $2"
esac

# while statement
counter=1
while [ $counter -le 10 ]
do
    echo $counter
    ((counter+=2))
done
echo "--------------"

# until statement
counter=1
until [ $counter -gt 10 ]
do
    echo $counter
    ((counter+=2))
done
echo "--------------"

# for statement
numbers="1 1 2 3 5"
for num in $numbers
do
    echo $num
done
echo "--------------"

for num in {10..0..1}
do
    if [ $num -gt 8 ]
    then
        echo "large number"
        continue
    fi

    if [ $num -lt 3 ]
    then
        echo "stop"
        break
    fi

    echo $num
done
echo "--------------"
```

## Reference
- Bash Tutorial: https://ryanstutorials.net/bash-scripting-tutorial/
