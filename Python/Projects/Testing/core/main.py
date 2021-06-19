#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subpart import auxiliary


if __name__ == "__main__":
    liner = "-" * 10
    print(f"{liner}Main Entry{liner}")

    res = auxiliary.get_url("https://httpbin.org/image")
    print(res)
    print(res.url)
    print(res.headers)
