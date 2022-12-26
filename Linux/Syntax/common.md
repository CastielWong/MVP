
```sh
#!/bin/bash

# search man pages by key word
man -k {word}

export DEMO="demo line"
unset DEMO

# check which distribution the Linux is
cat /etc/*-release

# check the shell using
echo $SHELL

# convert date to format specified
date --date='2000-12-31 01:23:45.123456+00:00' -u +'%Y%m%dT%H%M%S'

# display disk usage in human readable
du -h
# display disk usage in bytes
du --block-size=1


# check process
ps aux
# search for process via key word
ps -ef | grep {word}

# switch to root
sudo -i
# switch to user
su {user}
# get username/id of the current user
id -un
# list groups of the current user
id -Gn

# terminate a process
kill -15 {ps_id}
# kill a process forcedly
kill -9 {ps_id}

# monitor a running command
watch -n <second_interval> <running_command>

# run process in the background
{command} &
# list current running background jobs
jobs
# list the nth current running background job
jobs %{n}
# switch a background process to foreground
fg %{job_id}
# press "ctrl + Z" to suspend current foreground process
# start paused process running in the background
bg %{job_id}

# find out which process is using a port
netstat -pntl | grep $PORT  # Linux
lsof -nP -i4TCP:$PORT       # Mac
```
