
- [Match](#match)
- [Search](#search)
- [Find](#find)


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
