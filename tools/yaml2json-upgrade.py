#!/usr/bin/python
# yaml2json-upgrade.py - Upgrades Posts/Drafts from YAML to JSON
# Copyright (C) 2013-2014 Stefan J. Betz <info@stefan-betz.net>

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
from os import listdir
from re import compile, MULTILINE
from yaml import load
from json import dump, dumps

yaml_sep = compile("^---$", MULTILINE)

for directory in ('posts','drafts'):
    for post in listdir(directory):
        with open('%s/%s' % ( directory, post ),'r') as f:
            postparts = yaml_sep.split(f.read(), maxsplit=2)
            headers = load(postparts[1])
            content = postparts[2]
        with open('%s/%s' % ( directory, post ),'w') as f:
            f.write('---\n')
            dump(headers,f,indent=1,ensure_ascii=False)
            f.write('\n---')
            f.write(content)
