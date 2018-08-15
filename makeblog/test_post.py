# makeblog - A simple offline Blog.
# Copyright (C) 2013-2018 Stefan J. Betz <info@stefan-betz.net>

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
from os import mkdir
from shutil import rmtree
from makeblog.post import Post
from makeblog.templating import jinja

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

EXAMPLE_POST_WITHOUT_PERMALINK = '''
---
{
 "date": "2008/10/05 19:39:00",
 "author": "authorname",
 "tags": "",
 "guid": "d2564857-e604-406b-8db7-e72824ecf150",
 "categories": "category1, category2",
 "updated": "2009/01/06 20:12:51",
 "title": "Example"
}
---
<p>Testtext.</p>
'''

EXAMPLE_POST_WITH_GUID_TAG = '''
---
{
 "date": "2008/10/04 19:39:00",
 "author": "authorname",
 "tags": "",
 "guid": "tag:some-old-content-from-zine",
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
        self.config = {'blog': {'timezone': 'Europe/Berlin',
                                'dateformat': '%Y/%m/%d %H:%M:%S',
                                'url': 'http://www.example.com',
                                'defaultauthor': 'authorname',
                                'categories': 'category1, category2',
                                'name': 'My TestBlog',
                                'description': 'My Description'
                                }
                       }


class TestPost(TestCase):

    def setUp(self):
        mkdir('dst')
        mkdir('posts')
        mkdir('drafts')
        with open('posts/1-example.html', 'w') as f:
            f.write(EXAMPLE_POST)
        with open('posts/2-example.html', 'w') as f:
            f.write(EXAMPLE_POST_WITHOUT_PERMALINK)
        with open('posts/3-example.html', 'w') as f:
            f.write(EXAMPLE_POST_WITH_GUID_TAG)

    def test_init(self):
        blog = TestBlog()
        post = Post(blog)
        self.assertIsInstance(post.blog, TestBlog)
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
        self.assertIsInstance(post.content, str)

    def test_load(self):
        blog = TestBlog()
        post = Post(blog)
        post.load('posts/1-example.html')

    def test_load_without_permalink(self):
        blog = TestBlog()
        post = Post(blog)
        post.load('posts/2-example.html')

    def test_save(self):
        blog = TestBlog()
        post = Post(blog)
        post.load('posts/1-example.html')
        post.save()

    def test_new(self):
        blog = TestBlog()
        post = Post(blog)
        rvalue = post.new('Titel')
        self.assertIsInstance(rvalue, str)

    def test_render(self):
        blog = TestBlog()
        post = Post(blog)
        post.load('posts/1-example.html')
        jinja.globals['blog'] = blog
        jinja.globals['now'] = datetime.utcnow()
        post.render()

    def test_uuid(self):
        blog = TestBlog()
        post_uuid = Post(blog)
        post_uuid.load('posts/1-example.html')
        self.assertEqual(post_uuid.guid, 'urn:uuid:beba81bf-9ac1-4795-9569-c1bbd876677f')
        post_tag = Post(blog)
        post_tag.load('posts/3-example.html')
        self.assertEqual(post_tag.guid, 'tag:some-old-content-from-zine')

    def tearDown(self):
        rmtree('dst')
        rmtree('posts')
        rmtree('drafts')
