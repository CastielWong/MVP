
- [Flag](#flag)
- [Grouping](#grouping)
  - [Non-Capturing](#non-capturing)
  - [Assertion](#assertion)
  - [Comment](#comment)
  - [Flag](#flag-1)
- [Compile](#compile)
- [Match](#match)
  - [Greedy](#greedy)
  - [Conditional](#conditional)
- [Search](#search)
- [Find](#find)
- [Substitute](#substitute)
- [Split](#split)
- [Escape](#escape)
- [Reference](#reference)


`re.match()` is identical to `re.search()`, except that `re.search()` returns a match if <regex> matches anywhere in the <string>, whereas `re.match()` returns a match only if <regex> matches at the beginning of <string>.
With `re.match()`, matches are essentially always anchored at the beginning of the string, no mater there is a caret `^` or not.

`re.findall()`, if <regex> contains a capturing group, then the return list contains only contents of the group, not the entire match.


## Flag


## Grouping
There are two types of grouping, one is "Numbered Group", while the other is "Named Group", which has prefix `?P<{name}>` before the regex pattern. It's the best practice to apply symbolic name to the group, e.g. `(?P<{name}>xxx)`.

To reduce duplication, the same group can be reused via either `\{n}` or `(?P={name})`.

```py
line = "abc,abc"

m_number = re.search(r"(\w+),\1", line)
print(m_number.groups())    # ('abc',)
print(m_number[1])          # abc

m_name = re.search(r"(?P<word>\w+),(?P=word)", line)
print(m_name.groups())      # ('abc',)
print(m_name["word"])       # abc
```

### Non-Capturing

```py
# use a non-capturing group
m = re.search("(\w+),(?:\w+),(\w+)", "foo,qux,baz")
m.groups()
```

### Assertion
> __Lookahead__ and __Lookbehind__ assertions determine the success or failure of a regex match in Python based on what is just behind (to the left) or ahead (to the right) of the parser’s current position in the search string.

| Assertion | positive | negative |
| --- | --- | --- |
| Lookahead  | `(?=<regex>)`  | `(?!<regex>)`  |
| Lookbehind | `(?<=<regex>)` | `(?<!<regex>)` |


```py
line = "foobar"

# without assertion
m = re.search("foo([a-z])(?P<check>.)", line)
print(m)            # <re.Match object; span=(0, 5), match='fooba'>
print(m["check"])   # a

# positive lookahead
m = re.search("foo(?=[a-z])(?P<check>.)", line)
print(m)            # <re.Match object; span=(0, 4), match='foob'>
print(m["check"])   # b

# negative lookahead
m = re.search("foo(?![a-z])(?P<check>.)", line)
print(m)            # None

m = re.search("foo(?![1-9])(?P<check>.)", line)
print(m)            # <re.Match object; span=(0, 4), match='foob'>
print(m["check"])   # b

# without assertion
m = re.search("(?P<check>.)([a-z])bar", line)
print(m)            # <re.Match object; span=(1, 6), match='oobar'>
print(m["check"])   # a

# positive lookbehind
m = re.search("(?P<check>.)(?<=[a-z])bar", line)
print(m)            # <re.Match object; span=(2, 6), match='obar'>
print(m["check"])   # o

# negative lookahead
m = re.search("(?P<check>.)(?<![a-z])bar", line)
print(m)            # None

m = re.search("(?P<check>.)(?<![1-9])bar", line)
print(m)            # <re.Match object; span=(2, 6), match='obar'>
print(m["check"])   # o
```

### Comment
Comments are feasible via: `(?#...)`

```py
m = re.search('bar(?#This is a comment) *baz', 'foo bar baz qux')
print(m)    # <re.Match object; span=(4, 11), match='bar baz'>
```

### Flag
Flag(s) can be set or cleared for the duration of a group:
- set a flag: `(?<flag>:<regex>)`
- clear a flag: `(?-<flag>:<regex>)`

```py
line = "FoObar"

m = re.search("(?i:foo)bar", line)
print(m)    # <re.Match object; span=(0, 6), match='FoObar'>

m = re.search("(foo)bar", line, re.IGNORECASE)
print(m)    # <re.Match object; span=(0, 6), match='FoObar'>

m = re.search("(?-i:foo)bar", line, re.IGNORECASE)
print(m)    # None
```


## Compile
Advantages of precompiling:
- separate out the regex definition from its uses, which enhances modularity
- more efficient to compile once ahead of time than recompile each time, though minimal difference in practice due to applied cache
- improve readability and structure of code

```py
regex = "ba[rz]"
line = "FOOBARBAZ"

re_obj = re.compile(regex, flags=re.I)
print(re_obj)   # re.compile('ba[rz]', re.IGNORECASE)

r1 = re.search(regex, line, flags=re.I)
print(r1)       # <re.Match object; span=(3, 6), match='BAR'>
r2 = re.search(re_obj, line)
print(r2)       # <re.Match object; span=(3, 6), match='BAR'>
r3 = re_obj.search(line)
print(r3)       # <re.Match object; span=(3, 6), match='BAR'>
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
print(f"1: {matcher.group(1)}; 2: {matcher[2]}")
print(f"1: {matcher.group('first')}; 2: {matcher.group('second')}")
```

### Greedy
> The '*', '+', and '?' quantifiers are all greedy; they match as much text as possible.

Adding "?" behind to make the regex pattern non-greedy.
```py
pat_greedy = r"^(?P<alpha>.+)(?P<beta>\d{1,2})?$"
pat_non_greedy = r"^(?P<alpha>.+?)(?P<beta>\d{1,2})?$"

string = "something_10"
print(re.match(pat_greedy, string).group("alpha"))      # something_10
print(re.match(pat_non_greedy, string).group("alpha"))  # something_
```

### Conditional
A Conditional Match matches against one of two specified regexes depends on the condition.

Syntax for conditional match:
- numbered group: `(?({n})<yes-regex>|<no-regex>)`
- named group: `(?({name})<yes-regex>|<no-regex>)`

```py
regex = r"^(###)?foo(?(1)bar|baz)"

# match "bar" since there is "###"
print(re.search(regex, "###foobar"))    # <re.Match object; span=(0, 9), match='###foobar'>
print(re.search(regex, "###foobaz"))    # None
print(re.search(regex, "foobar"))       # None
# match "baz" since there is no "###"
print(re.search(regex, "foobaz"))       # <re.Match object; span=(0, 6), match='foobaz'>

regex = r"^(?P<character>\W)?foo(?(character)(?P=character)|d)$"
print(re.search(regex, "foo"))      # None
# match "!" since group "character" exists
matcher = re.search(regex, "!foo!")
print(matcher)    # <re.Match object; span=(0, 5), match='!foo!'>
print(matcher.group("character"))   # !
print(re.search(regex, "#food#"))   # None
print(re.search(regex, "@food#"))   # None
# match "d" since group "character" doesn't exist
print(re.search(regex, "food"))     # <re.Match object; span=(0, 4), match='food'>
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
print(emails)   # ['guru-00@gmail.com', ..., 'demo@yahoo.com']

# retrieve matched text in tuple
line = "foo, bar, baz, qux, quux, corge"
items = re.findall(r"(\w+), (\w+)", line)
print(items)    # [('foo', 'bar'), ('baz', 'qux'), ('quux', 'corge')]

items = re.findall(r"(\w+), (\w+), (\w+), (\w+)", line)
print(items)    # [('foo', 'bar', 'baz', 'qux')]
```


## Substitute
Substitute characters/words for a string:
```py
check = re.sub(
    r"(\d+)",
    r"-\1-",
    "foo 123 ba3",
)
print(check)    # foo -123- ba-3-

line = "foo,bar,baz,qux"
# \1, \g<1>
check = re.sub(
    r"foo,(\w+),(\w+),qux",
    r"foo,\g<2>,\g<1>,qux",
    line,
)
print(check)    # foo,baz,bar,qux

check = re.sub(
    r"foo,(?P<w1>\w+),(?P<w2>\w+),qux",
    r"foo,\g<w2>,\g<w1>,qux",
    line,
)
print(check)    # foo,baz,bar,qux

# limit the number of substitutions
check = re.sub(r"\w+", "xxx", line, count=2)
print(check)    # xxx,xxx,baz,qux
```


## Split

```py
line = "foo,bar  ;  baz / qux"
regex = "\s*[,;/]\s*"

check = re.split(regex, line)
print(check)    # ['foo', 'bar', 'baz', 'qux']

check = re.split(regex, line, maxsplit=2)
print(check)    # ['foo', 'bar', 'baz / qux']

check = re.split(f"({regex})", line)
print(check)    # ['foo', ',', 'bar', '  ;  ', 'baz', ' / ', 'qux']
```


## Escape
Escape characters in a regex:
```py
line = "foo^bar(baz)|qux"
literal = r"foo\^bar\(baz\)\|qux"

escaped = re.escape(line)
print(escaped)  # "foo\^bar\(baz\)\|qux"

check = re.match(pattern=line, string=literal)
print(check)    # None

check = re.match("foo\^bar\(baz\)\|qux", line)
print(check)    # <re.Match object; span=(0, 16), match='foo^bar(baz)|qux'>
check = re.match(escaped, line)
print(check)    # <re.Match object; span=(0, 16), match='foo^bar(baz)|qux'>
check = re.match(literal, line)
print(check)    # <re.Match object; span=(0, 16), match='foo^bar(baz)|qux'>
```


## Reference
- Regular Expressions in Python (Part 1): https://realpython.com/regex-python/
- Regular Expressions in Python (Part 2): https://realpython.com/regex-python-part-2/
