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
from os import access, F_OK, unlink, rmdir
from makeblog.config import readconfig, writedefaultconfig


class TestWritedefaultconfig(TestCase):

    def test_firstrun(self):
        """
        writedefaultconfig() creates all directories and config files on the
        first run. After that False is returned.
        """
        self.assertFalse(writedefaultconfig())
        self.assertTrue(access('src', F_OK))
        self.assertTrue(access('posts', F_OK))
        self.assertTrue(access('drafts', F_OK))
        self.assertTrue(access('config.json', F_OK))

    def test_secondrun(self):
        """
        writedefaultconfig() returns True in case a config.json already exists.
        """
        writedefaultconfig()
        self.assertTrue(writedefaultconfig())

    def tearDown(self):
        unlink('config.json')
        for directory in ('src', 'posts', 'drafts'):
            rmdir(directory)


class TestReadconfig(TestCase):

    def test_readconfig(self):
        self.assertFalse(readconfig())
        writedefaultconfig()
        self.assertTrue(readconfig())
        self.assertIsInstance(readconfig(), dict)

    def tearDown(self):
        if access('config.json', F_OK):
            unlink('config.json')
