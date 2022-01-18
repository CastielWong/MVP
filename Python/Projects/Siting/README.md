
Start the project from very beginning:
0. Install all packages needed via `pip install -r requirements`
1. Run `sphinx-quickstart` to set up the project:
   - "Project name"
   - "Author name(s)"
2. Add `"myst_parser"` to `extensions` inside "conf.py"
3. Create a new markdown page named "xxx.md", then place "xxx" under section "toctree" inside index page, either "index.rst" or "index.md", to add the hyperlink to the page
4. Run `python3 liver_load.py` for testing

Anything else can be blank.
