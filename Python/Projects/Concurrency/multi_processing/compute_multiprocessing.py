#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import math
import multiprocessing


def do_math(start=0, num=10):
    pos = start
    k_sq = 1_000 * 1_000
    ave = 0
    while pos < num:
        pos += 1
        val = math.sqrt((pos - k_sq) * (pos - k_sq))
        ave += val / num

    return int(ave)


def main():
    do_math(1)

    t0 = datetime.datetime.now()

    print("Doing math on {:,} processors.".format(multiprocessing.cpu_count()))

    pool = multiprocessing.Pool()
    processor_count = multiprocessing.cpu_count()
    tasks = []
    for n in range(1, processor_count + 1):
        task = pool.apply_async(do_math, (30_000_000 * (n - 1) / processor_count,
                                          30_000_000 * n / processor_count))
        tasks.append(task)

    pool.close()
    pool.join()

    dt = datetime.datetime.now() - t0
    print("Done in {:,.2f} sec.".format(dt.total_seconds()))
    print("Our results: ")
    for t in tasks:
        print(t.get())


if __name__ == '__main__':
    main()
