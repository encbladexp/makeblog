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

from os import access, F_OK, makedirs
from os.path import exists
from urllib.parse import urlparse
import json

DEFAULT_CONFIG = {
    'blog': {
        'name': '''My's Blog''',
        'url': 'http://blog.domain.tld',
        'description': 'Because i can!',
        'googleplus': True,
        'twitter': True,
        'flattr': True,
        'categories': ['category1', 'category2', 'category4'],
        'defaultauthor': 'me',
        'timezone': 'Europe/Berlin',
        'dateformat': '%Y/%m/%d %H:%M:%S'
    },
    'authors': {
        'me': {
            'name': 'Full Name',
            'nick': 'nickname',
            'googleplus': None,
            'twitter': None,
            'amazon': None,
            'bitcoin': None,
            'mail': None,
            'flattr': None
        }
    }
}


def readconfig():
    """
    Load the configuration, to create a reliable loading of config.json
    on startup.
    """
    if not access('config.json', F_OK):
        return False
    with open('config.json', 'r') as f:
        config = json.load(f)
        config['blog']['domain'] = urlparse(config['blog']['url']).netloc
    return config


def writedefaultconfig():
    """
    Create a configuration with sane defaults.
    """
    for directory in ('src', 'posts', 'drafts', 'authors', 'plugins'):
        if not exists(directory):
            makedirs(directory)
    if not access('config.json', F_OK):
        with open('config.json', 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=1, ensure_ascii=False,
                      sort_keys=True)
        return False
    return True
