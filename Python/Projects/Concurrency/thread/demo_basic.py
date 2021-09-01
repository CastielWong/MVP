#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import threading


def greeter(name: str, times: int):
    for n in range(0, times):
        print("{}. Hello there {}".format(n, name))
        time.sleep(1)


def main():
    threads = [
        threading.Thread(target=greeter, args=("Michael", 10), daemon=True),
        threading.Thread(target=greeter, args=("Sarah", 5), daemon=True),
        threading.Thread(target=greeter, args=("Zoe", 2), daemon=True),
        threading.Thread(target=greeter, args=("Mark", 11), daemon=True),
    ]

    [t.start() for t in threads]

    print("This is other work.")
    print(2 * 2)

    [t.join(timeout=1) for t in threads]

    print("Done.")


if __name__ == '__main__':
    main()
