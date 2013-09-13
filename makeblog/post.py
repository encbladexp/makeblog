# makeblog - A simple offline Blog.
# Copyright (C) 2013 Stefan J. Betz <info@stefan-betz.net>

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
from makeblog.tools import slugify, directorymaker
from makeblog.pygments import pygmentify
from makeblog.templating import jinja
from datetime import datetime
from pytz import timezone
from re import compile, MULTILINE
from time import strftime
import json

class Post(object):
    json_sep = compile("^---$", MULTILINE)

    def __init__(self, blog):
        self.blog = blog
        self.author = None
        self.title = None
        self.permalink = None
        self.slug = None
        self.guid = None
        self.categories = []
        self.date = timezone(self.blog.config['blog']['timezone']).localize(datetime.now())
        self.updated = None
        self._content = None
        self.next = None
        self.prev = None

    def load(self, filename):
        with open(filename) as f:
            parts = Post.json_sep.split(f.read(), maxsplit=2)
        header = json.loads(parts[1])
        self.author = header['author']
        self.title = header['title']
        if 'permalink' in header:
            self.permalink = header['permalink']
        self.guid = header['guid']
        self.categories = [category.strip() for category in header['categories'].split(',')]
        self.date = timezone(self.blog.config['blog']['timezone']).localize(datetime.strptime(header['date'], self.blog.config['blog']['dateformat']))
        self.updated = self.date
        if 'updated' in header:
            self.updated = timezone(self.blog.config['blog']['timezone']).localize(datetime.strptime(header['updated'], self.blog.config['blog']['dateformat']))
        if not self.permalink:
            self.permalink = '%s/%s/%s' % (self.blog.config['blog']['url'], self.date.strftime('%Y/%m/%d'), slugify(self.title))
        if not self.slug:
            self.slug = slugify(self.title)
        self._content = parts[2]

    def render(self):
        template = jinja.get_template('article.html')
        with open(directorymaker('%s/index.html' % self.permalink.replace('%s/' % self.blog.config['blog']['url'], '')), 'w') as f:
            f.write(template.render(post=self))

    @pygmentify
    def content(self):
        return self._content
