#!/usr/bin/env python

from pathlib import Path
from datetime import datetime
from re import sub
from json import loads
from yaml import dump

SRCDIR='myblog/posts'
DSTDIR='mybloghugo/content/posts'

SLUG_ITEMS = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "-",
    ":",
    "_",
]
SLUG_REPLACE = {" ": "-", "ß": "ss", "ü": "ue", "ö": "oe", "ä": "ae"}
SLUG_EXCLUDE = [":"]

def slugify(text):
    """
    Slugifies a string.
    """
    slug = ""
    lowered = text.lower()
    for excludedchar in SLUG_EXCLUDE:
        lowered = lowered.replace(excludedchar, "")
    for char in lowered:
        if char in SLUG_REPLACE:
            slug = slug + SLUG_REPLACE[char]
        elif char in SLUG_ITEMS:
            slug = slug + char
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug

def clean_list(text, categories=False):
    tags = [each.strip(' ') for each in text.split(',')]
    if categories:
        return [x for x in tags if x in ('opensource', 'ubuntu', 'debian')]
    return tags

def clean_date(date):
    return datetime.strptime(date, '%Y/%m/%d %H:%M:%S')

def clean_permalink(text):
    return text.replace('http://blog.domain.tld', '')

def clean_content(text):
    return sub(r'\$\$code\(lang\=([a-z]*)\)', r'{{< highlight \1 >}}', text).replace('$$/code\n', '{{< / highlight >}}\n').replace('$$code\n','{{< highlight plaintext >}}\n')

for blogfile in Path(SRCDIR).iterdir():
    print(blogfile)
    with blogfile.open() as blogpost:
        blogfile_splitted = blogpost.read().split("---\n")
    header_old = loads(blogfile_splitted[1])
    content = clean_content(blogfile_splitted[2])
    if 'slug' in header_old:
        slug = header_old['slug']
    else:
        slug = slugify(header_old['title'])
    header_new = {
        'slug': slug,
        'title': header_old['title'],
        'author': header_old['author'],
        'date': clean_date(header_old['date']),
        'categories': clean_list(header_old['categories'], True) if 'categories' in header_old else '',
        'tags': clean_list(header_old['categories']) if 'categories' in header_old else ''
    }
    if 'permalink' in header_old:
        header_new['aliases'] = [ clean_permalink(header_old['permalink'])]
    if 'updated' in header_old:
        header_new['lastmod'] = clean_date(header_old['updated'])
    header_new_yaml = dump(header_new)
    target_date = header_new['date'].strftime('%Y%m')
    target = f'{DSTDIR}/{target_date}_{slug}.html'
    with open(target, 'w') as targetpost:
        targetpost.write(f'---\n{header_new_yaml}\n---\n{content}')
