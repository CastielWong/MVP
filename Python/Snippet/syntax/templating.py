#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa


# -----------------------------------------------
# render from string
from jinja2 import Template

demo = """
    Demo string: {{ string }}
    Demo number: {{ number }}
"""
params = {"string": "displaying", "number": 123}
template = Template(demo)
rendered = template.render(params)

# -----------------------------------------------
# render file under directory
from jinja2 import Environment
from jinja2 import FileSystemLoader

file_loader = FileSystemLoader("{directory}")
env = Environment(loader=file_loader)
template = env.get_template("{template}.json")

params = {...}
# either dict or keyword pairs works
rendered = template.render(**params)
