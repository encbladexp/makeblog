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
from makeblog.tools import slugify, newfile
from makeblog.pygments import pygmentify
from makeblog.templating import render
from datetime import datetime
from pytz import timezone
from re import compile, MULTILINE
from uuid import uuid4 as uuidgen
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
        self.date = timezone(self.blog.config["blog"]["timezone"]).localize(
            datetime.now()
        )
        self.updated = None
        self._content = None
        self.next = None
        self.prev = None
        self.filename = None

    def load(self, filename):
        self.filename = filename
        with open(self.filename) as f:
            parts = Post.json_sep.split(f.read(), maxsplit=2)
        header = json.loads(parts[1])
        self.author = header["author"]
        self.title = header["title"]
        if "permalink" in header:
            self.permalink = header["permalink"]
        guid = header["guid"]
        self.guid = guid if guid.startswith("tag:") else "urn:uuid:{}".format(guid)
        if header["categories"]:
            self.categories = [
                category.strip() for category in header["categories"].split(",")
            ]
        self.date = timezone(self.blog.config["blog"]["timezone"]).localize(
            datetime.strptime(header["date"], self.blog.config["blog"]["dateformat"])
        )
        self.updated = self.date
        if "updated" in header:
            self.updated = timezone(self.blog.config["blog"]["timezone"]).localize(
                datetime.strptime(
                    header["updated"], self.blog.config["blog"]["dateformat"]
                )
            )
        if not self.permalink:
            self.permalink = "{}/{}/{}".format(
                self.blog.config["blog"]["url"],
                self.date.strftime("%Y/%m/%d"),
                slugify(self.title),
            )
        self.slug = header["slug"] if "slug" in header else slugify(self.title)
        self._content = parts[2]

    def update(self):
        self.updated = timezone(self.blog.config["blog"]["timezone"]).localize(
            datetime.now()
        )

    def new(self, title, draft=False):
        """
        Create a new Post…
        """
        self.title = title
        self.filename = newfile(slugify(self.title), draft)
        self.guid = str(uuidgen())
        self.author = self.blog.config["blog"]["defaultauthor"]
        self.categories = self.blog.config["blog"]["categories"]
        self.updated = self.date
        self.permalink = "{}/{}/{}".format(
            self.blog.config["blog"]["url"],
            self.date.strftime("%Y/%m/%d"),
            slugify(self.title),
        )
        self.save()
        return self.filename

    def save(self):
        with open(self.filename, "w") as f:
            f.write("---\n")
            headers = {
                "categories": "{}".format(", ".join(self.categories)),
                "permalink": self.permalink,
                "guid": self.guid,
                "title": self.title,
                "author": self.author,
                "date": "{}".format(
                    self.date.strftime(self.blog.config["blog"]["dateformat"])
                ),
            }
            if self.updated is not self.date:
                headers["updated"] = self.updated.strftime(
                    self.blog.config["blog"]["dateformat"]
                )
            json.dump(headers, f, indent=1, ensure_ascii=False, sort_keys=True)
            f.write("\n---")
            if self._content:
                f.write(self._content)
            else:
                f.write("\n")

    def render(self):
        blogurl = self.blog.config["blog"]["url"]
        dirname = self.permalink.replace("{}/".format(blogurl), "")
        render("article.html", "{}/index.html".format(dirname), post=self)

    @property
    @pygmentify
    def content(self):
        return self._content
