#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------
# Time conversion
import time
from datetime import datetime

import pytz

# retrieve current time
now = datetime.now()
print(now)

# display current time in specific format
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
# display current time in epoch (seconds)
# note that epoch starts since "1970-01-01 00:00:00"
# epoch time is also referred to POSIX/Unix time
print(time.time())  # 1_601_234_567.12345

# convert epoch time
epoch = 1_601_234_567_123  # epoch in milliseconds (13 bits)
# epoch for `utcfromtimestamp` is in second
print(datetime.utcfromtimestamp(epoch / 1000))  # 2020-09-27 19:22:47.123000

# check all available timezones
print(pytz.all_timezones)
# retrieve time of the specified timezone
timezone = pytz.timezone("Australia/South")
print(datetime.now(timezone))

# ---------------------------------------------------------
# Timer for a command
import timeit

command = "'-'.join(str(n) for n in range(100))"
# time elapsed to run the command for 10,000 time
print(timeit.timeit(command, number=10000))
