
- [Flag](#flag)
- [Named Group](#named-group)
- [Compile](#compile)
- [Match](#match)
- [Search](#search)
- [Find](#find)
- [Substitute](#substitute)
- [Split](#split)
- [Escape](#escape)
- [Reference](#reference)


`re.match()` is identical to `re.search()`, except that `re.search()` returns a match if <regex> matches anywhere in the <string>, whereas `re.match()` returns a match only if <regex> matches at the beginning of <string>.
With `re.match()`, matches are essentially always anchored at the beginning of the string, no mater there is a caret `^` or not.

`re.finadall()`, if <regex> contains a capturing group, then the return list contains only contents of the group, not the entire match.


## Flag


## Named Group
It's the best practice to apply symbolic name to the group, e.g. `(?P<name>xxx)`.

Also, the same named group can be reused via `(?P=name)`.

Syntax for conditional match:
- numbered group: `(?(<n>)<yes-regex>|<no-regex>)`
- named group: `(?(<name>)<yes-regex>|<no-regex>)`

- Lookahead assesion: `(?=<lookahead_rege>)`, ``(?!<lookahead_rege>)``
- Lookbehind assession: `(?<=<lookbehind_rege>)`, `(?<!<lookbehind_rege>)`

comment out: `(?#...)`

Set or remove flag value(s) for the duration of a group: `(?<set_flags>-<remove_flags>:<regex>)`

```py
m = re.search(r"(?P<word>\w+),(?P=word)", "abc,abc")


# use a non-capturing group
m = re.search("(\w+),(?:\w+),(\w+)", "foo,quux,baz")
m.groups()

# conditional match
regex = r"^(###)?foo(?(1)bar|baz)"

re.search(regex, "###foobar")
re.search(regex, "###foobaz")
re.search(regex, "foobar")
re.search(regex, "foobaz")


regex = r"^(?P<ch>\W?foo(?(ch)(?P=ch)|)$"

re.search(regex. "foo")
re.search(regex, "#foo#")
re.search(regex, "@foo#")


# lookahead
m = re.search("foo(?=[a-z])(?P<ch>.)", "foobar")
m = re.search("foo([a-z])(?P<ch>.)", "foobar")
```


## Compile
Advantages of precompiling:
- separate out the regex definition from its uses, which enhances modularity
- more efficient to compile once ahead of time than recompile each time, though minimal difference in practice due to applied cache
- imrpve readability and structure of code

```py
regex = "ba[rz]"
string = "FOOBARBAZ"

r1 = re.search(regex, string, flags=re.I)

re_obj = re.compile(regex, flags=re.I)
r2 = re.search(re_obj, string)
r3 = re_obj.search(string)
```


## Match
Check if pattern exists:
```py
text = "bd check    out"

# extract "ac" or "bd" before "check out"
pattern = r"(?P<first>ac|bd)+.*(?=(?P<second>check\s*out))"
# compile the pattern with regex flags
matcher = re.compile(pattern, flags=re.I | re.M).match(text)

# "group - bd"
print(f"group - {matcher.group()}")

# both are "1 - bd; 2 - check    out"
print(f"1: {matcher.group(1)}; 2: {matcher.group(2)}")
print(f"1: {matcher.group('first')}; 2: {matcher.group('second')}")
```


## Search
Extract substring:
```py
text = "gfgfd-AAAdemoZZZ-uijjk"

# search for the word matched the pattern
searcher = re.search("AAA(?P<found>.+?)ZZZ", text, re.IGNORECASE)
if searcher:
    print(searcher.group(1))        # demo
    print(searcher.group("found"))  # demo
```


## Find
Find all string matched:
```py
text = "guru-00@gmail.com, career.guru12@hotmail.com, demo@yahoo.com"

# retrieve all item matched the text
emails = re.findall(r"[\w\.-]+@[\w\.]+", text)
print(emails)
```


## Substitute
```py
re.sub(
    r"(\d+)",
    r"a\1b",
    "foo 123 ba3",
)

# \1, \g<1>
re.sub(
    r"foo,(\w+),(\w+),qux",
    r"foo,\g<2>,\g<1>,qux",
    "foo,bar,baz,qux",
)

re.sub(
    r"foo,(?P<w1>\w+),(?P<w2>\w+),qux",
    r"foo,\g<w2>,\g<w1>,qux",
    "foo,bar,baz,qux",
)

re.sub(r"\w+", "xxx", "foo.bar.baz.qux", count=2)

```


## Split

```py
regex = "\s*[,;/]\s*"
string = "foo,bar  ;  baz / qux"

re.split(regex, string)
re.split(f"({regex})", string)

```


## Escape

```py
string = "foo^bar(baz)|qux"

re.escape(string)

re.match(string, string)
re.match("foo\^bar\(baz\)\|qux", string)

```


## Reference
- Regexes in Python (Part 1): https://realpython.com/regex-python/
- Regexes in Python (Part 2): https://realpython.com/regex-python-part-2/
