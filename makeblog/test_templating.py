# makeblog - A simple offline Blog.
# Copyright (C) 2013-2017 Stefan J. Betz <info@stefan-betz.net>

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
from os import mkdir, access, F_OK
from shutil import rmtree
from datetime import datetime
from jinja2 import Environment
from makeblog.templating import jinja, render


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


class TestTemplating(TestCase):

    def setUp(self):
        mkdir('dst')

    def test_jinja(self):
        self.assertIsInstance(jinja, Environment)

    def test_render(self):
        # Workaround for Python < 3.4
        if 'blog' not in jinja.globals:
            jinja.globals['blog'] = TestBlog()
            jinja.globals['now'] = datetime.utcnow()
        render('site.html', 'test.html')
        self.assertTrue(access('dst/test.html', F_OK))

    def tearDown(self):
        rmtree('dst')
