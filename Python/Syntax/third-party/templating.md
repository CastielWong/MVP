
- [String](#string)
- [File](#file)
- [Reference](#reference)

## String
Render from string:
```py
from jinja2 import Template

demo = """
    Demo string: {{ string }}
    Demo number: {{ number }}
"""
params = {"string": "displaying", "number": 123}
template = Template(demo)
rendered = template.render(params)
```

## File
Render from file loading under directory:
```py
from jinja2 import Environment
from jinja2 import FileSystemLoader

file_loader = FileSystemLoader("{directory}")
env = Environment(loader=file_loader)
template = env.get_template("{template}.json")

params = {...}
# either dict or keyword pairs works
rendered = template.render(**params)
```


## Reference
- Python Jinja tutorial: http://zetcode.com/python/jinja/
- Primer on Jinja Templating: https://realpython.com/primer-on-jinja-templating/
