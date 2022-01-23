
This is the demo page to demonstrate markdown syntax.

- [Markdown](#markdown)
- [MyST](#myst)
  - [Colon Fence](#colon-fence)
  - [Linkage Role](#linkage-role)
  - [TOC](#toc)
  - [Download](#download)
- [Sphinx](#sphinx)
  - [Code Block](#code-block)
  - [Include File](#include-file)
  - [Document Module](#document-module)

## Markdown

Embed code:

    print("Embed code generally")

Fenced code block:
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
- internal: ![Python Logo](contents/python-logo.png)
- external: ![Python Logo](https://www.python.org/static/community_logos/python-logo.png)


## MyST
MyST will render reStructuredText below to proper format:

```{image} contents/python-logo.png
:alt: Python Logo
:class: bg-primary
:width: 200px
:align: center
```

### Colon Fence
To make below works, ensure MyST's "[colon_fence](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html)" extension is enabled in "conf.py".

:::{figure-md} logo-role
:class: myclass

<img src="contents/python-logo.png" alt="Python Logo" class="bg-primary" width="300px">

Python comes from the _Python Software Foundation_
:::

"logo-role" can be considered as a linkable role or reference alias, which should work in markdown.

(linkage)=
### Linkage Role
Similar to the Colon Fence, a linkage role can be used to connect to the link quickly by placing `(<role_name>)=` before a heading.

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

This is what will be like when a downloadable link ({download}`the LOGO <contents/python-logo.png>`) is provided.


## Sphinx
### Code Block
Sphinx has directives to render the code block.
Here is the example enabling directives via YAML format, for whose native form is `:linenos:`:
```{code-block} python
---
linenos: true
---
def demo(msg: str):
    return f"Printing {msg}"
```

### Include File
Below is the way to link the content of a file directly:
```{literalinclude} contents/sample.py
---
language: python
lines: 3, 7-
linenos: true
emphasize-lines: 1, 9-11
---
```

The `:lines:` matches lines in the original file, while `:linenos:` is generate new line numbers in sequence based on the lines specified.
And `:emphasize-lines:` is based on `:linenos:` other than `:lines:`.


### Document Module
Sphinx has a feature to include documentation from docstring within the code.
To turn on such feature, add `"sphinx.ext.autodoc"` under `extensions` in "conf.py".

Since there is no a direct wrapper for "autodoc" to be expressed in markdown, reStructureText is needed for the case.

```{eval-rst}
.. autoclass:: sample.Demo
    :members:
```
