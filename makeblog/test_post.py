# makeblog - A simple offline Blog.
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
from unittest import TestCase
from datetime import datetime
from os import mkdir, rmdir, unlink, access, F_OK
from makeblog.post import Post

EXAMPLE_POST = '''
---
{
 "date": "2008/10/04 19:39:00",
 "author": "authorname",
 "tags": "",
 "guid": "beba81bf-9ac1-4795-9569-c1bbd876677f",
 "categories": "category1, category2",
 "permalink": "http://www.example.com/2009/1/6/example",
 "updated": "2009/01/06 20:12:51",
 "title": "Example"
}
---
<p>Testtext.</p>
'''

class TestBlog(object):
    """
    Simple Blog Instance for Unit Tests.
    """

    def __init__(self):
        self.config = {'blog':{'timezone':'Europe/Berlin',
                               'dateformat':'%Y/%m/%d %H:%M:%S',
                               'url':'http://www.example.com',
                               'defaultauthor':'authorname',
                               'categories':'category1, category2'
                              }
                      }


class TestPost(TestCase):

    def setUp(self):
        mkdir('dst')
        mkdir('posts')
        mkdir('drafts')
        with open('dst/1-example.html','w') as f:
            f.write(EXAMPLE_POST)

    def test_init(self):
        blog = TestBlog()
        post = Post(blog)
        self.assertIsInstance(post.blog,TestBlog)
        self.assertIsInstance(post.date, datetime)

    def test_update(self):
        blog = TestBlog()
        post = Post(blog)
        post.update()
        self.assertIsInstance(post.updated, datetime)

    def test_content(self):
        blog = TestBlog()
        post = Post(blog)
        post._content = 'Example Content'
        self.assertIsInstance(post.content,str)

    def test_load(self):
        blog = TestBlog()
        post = Post(blog)
        post.load('dst/1-example.html')

    def test_save(self):
        blog = TestBlog()
        post = Post(blog)
        post.load('dst/1-example.html')
        post.save()

    def test_new(self):
        blog = TestBlog()
        post = Post(blog)
        post.new('Titel')

    def tearDown(self):
        for post in ['dst/1-example.html','posts/1-titel.html']:
            if access(post, F_OK):
                unlink(post)
        rmdir('dst')
        rmdir('posts')
        rmdir('drafts')

# FIXME: File for new() exists already?
# TODO: render() not tested