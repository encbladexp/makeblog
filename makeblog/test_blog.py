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
from os import mkdir
from shutil import rmtree
from datetime import datetime
from makeblog.blog import *
from makeblog.config import DEFAULT_CONFIG

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

class TestBlog(TestCase):

    def setUp(self):
        for directory in ('posts','drafts'):
            mkdir(directory)

    def test_init(self):
        b = Blog(None)
        self.assertIsInstance(b.authors,list)
        self.assertIsInstance(b.posts,list)
        self.assertIsInstance(b.categoryposts,dict)
        self.assertIsNone(b.config)
        self.assertFalse(b.draft)

    def test_loadposts(self):
        p =LoadPosts(Blog(DEFAULT_CONFIG))
        p.run()
        # 0 Posts if not Posts in drafts/posts directory
        self.assertEqual(len(p.blog.posts),0)
        with open('posts/1-example.html','w') as f:
            f.write(EXAMPLE_POST)
        p.run()
        # 1 Posts if only 1 Post in posts
        self.assertEqual(len(p.blog.posts),1)
        # Reset Posts to avoid duplicates
        p.blog.posts = []
        with open('drafts/1-example.html','w') as f:
            f.write(EXAMPLE_POST)
        p.run()
        # 1 Posts if both  drafts and posts has 1 Post but Draft Mode disabled
        self.assertEqual(len(p.blog.posts),1)
        # Reset Posts again and enable draft mode
        p.blog.posts = []
        p.blog.draft = True
        p.run()
        # 2 Posts if both drafts and posts has 1 Post and Draft Mode enabled
        self.assertEqual(len(p.blog.posts),2)

    def test_loadauthors(self):
        p = LoadAuthors(Blog(DEFAULT_CONFIG))
        p.blog.config['authors'] = { 'testuser2':{'nick':'testuser2nick'},
                                     'testuser1':{'nick':'testuser1nick'}
                                   }
        p.run()
        self.assertEqual(p.blog.authors[0].nick,'testuser1nick')
        self.assertEqual(p.blog.authors[1].nick,'testuser2nick')

    def test_sortposts(self):
        p = SortPosts(Blog(None))

        class AbstractTestPost(object):

            def __init__(self, date):
                self.date = date

        p.blog.posts = [AbstractTestPost(datetime(2014, 1, 1)),AbstractTestPost(datetime(2013, 1, 1))]
        p.run()
        self.assertEqual(p.blog.posts[0].date.year,2013)
        self.assertEqual(p.blog.posts[1].date.year,2014)

    def tearDown(self):
        for directory in ('posts','drafts'):
            rmtree(directory)