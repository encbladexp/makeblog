# makeblog - A simple offline Blog.
# Copyright (C) 2013-2019 Stefan J. Betz <info@stefan-betz.net>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from os import makedirs, listdir
from os.path import dirname, exists
from re import compile
from argparse import ArgumentParser, Namespace

SLUG_ITEMS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
              'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
              'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6',
              '7', '8', '9', '-', ':', '_']
SLUG_REPLACE = {' ': '-', 'ß': 'ss', 'ü': 'ue', 'ö': 'oe', 'ä': 'ae'}
SLUG_EXCLUDE = [':']

opts = ArgumentParser(prog='makeblog', description='A simple offline Blog.')
opts.add_argument('-t', '--title', metavar='TITLE',
                  help='Create a new Article with Title')
opts.add_argument('-d', '--draft', action='store_true',
                  help='Draft mode for --build and --title')
opts.add_argument('-b', '--build', action='store_true',
                  help='Build this Blog')
opts.add_argument('-s', '--serve', action='store_true',
                  help='Serve this Blog')
opts.add_argument('-i', '--init', action='store_true',
                  help='Create required directories')
opts.add_argument('-u', '--update', metavar='FILENAME',
                  help='Update Timestamp from Blog file')
options = Namespace()


def slugify(text):
    """
    Slugifies a string.
    """
    slug = ''
    lowered = text.lower()
    for excludedchar in SLUG_EXCLUDE:
        lowered = lowered.replace(excludedchar, '')
    for char in lowered:
        if char in SLUG_REPLACE:
            slug = slug + SLUG_REPLACE[char]
        elif char in SLUG_ITEMS:
            slug = slug + char
    while '--' in slug:
        slug = slug.replace('--', '-')
    return slug


def newfile(slug, draft=False):
    """
    Return a new file object base on slug and next free id in posts/ or
    drafts/.
    """
    idre = compile("([0-9]*).*")
    dirs = listdir('posts') + listdir('drafts')
    files = sorted([int(idre.match(filename).group(1)) for filename in dirs
                    if idre.match(filename)])
    fileid = 1 if len(files) == 0 else files[-1]+1
    articletype = 'drafts' if draft else 'posts'
    return "{}/{:d}-{}.html".format(articletype, fileid, slug)


def directorymaker(path):
    """
    Creates directories required for path.
    """
    path = 'dst/{}'.format(path)
    directories = dirname(path)
    if not exists(directories):
        makedirs(directories)
    return path


def parse_args():
    opts.parse_args(namespace=options)
