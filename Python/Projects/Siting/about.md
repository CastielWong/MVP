
This is the demo page to demonstrate markdown syntax.

## Basic Markdown

Embed code - 1:

    print("Embed code generally")

Embed code - 2:
```py
print("Embed with language specified")
```

Quote words:
> Less is More

Unlisted List:
- Inline code via `print ("tick")`
- Italics font via _one underscore_
- Bold font via __two underscore__

Numbered List:
1. a
2. b
3. c

Show link [README](README.md).

Display Image:
- internal: ![Python Logo](images/python-logo.png)
- external: ![Python Logo](https://www.python.org/static/community_logos/python-logo.png)


## MyST
MyST will render reStructuredText below to proper format:

```{image} images/python-logo.png
:alt: Python Logo
:class: bg-primary
:width: 200px
:align: center
```

### Colon Fence
To make below works, ensure MyST's "[colon_fence](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html)" extension is enabled in "conf.py".

"logo-role" can be considered as a linkable role or reference alias, which should work in markdown.

:::{figure-md} logo-role
:class: myclass

<img src="images/python-logo.png" alt="Python Logo" class="bg-primary" width="300px">

Python comes from the _Python Software Foundation_.
:::


### TOC
The normal way to define toc is:
```
    ```{toc}
    :maxdepth: 2
    :caption: "Contents:"
    :glob:

    *
    ```
```

The YAML way is:
```
    ```{toc}
    ---
    maxdepth: 2
    caption: |
        Contents:
    glob:
    ---

    *
    ```
```

### Download

This is what will be like when a downloadable link ({download}`the LOGO <images/python-logo.png>`) is provided.
