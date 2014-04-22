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
from os import mkdir, rmdir, unlink, access, F_OK
from jinja2 import Environment
from jinja2.exceptions import UndefinedError
from makeblog.templating import jinja, render


class TestTemplating(TestCase):

    def setUp(self):
        mkdir('dst')

    def test_jinja(self):
        self.assertIsInstance(jinja, Environment)

    def test_render(self):
        self.assertRaises(UndefinedError, render, 'site.html', 'test.html')
        self.assertTrue(access('dst/test.html', F_OK))

    def tearDown(self):
        try:
            unlink('dst/test.html')
        except FileNotFoundError:
            pass
        rmdir('dst')
