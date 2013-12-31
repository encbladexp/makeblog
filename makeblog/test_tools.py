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
from unittest import TestCase
from os import access, rmdir, mkdir, unlink, F_OK
from makeblog.tools import slugify, directorymaker, newfile, options, parse_args

class TestSlugify(TestCase):

    def test_simpleslug(self):
        self.assertEqual(slugify("Test"),"test")

    def test_umlaute(self):
        self.assertEqual(slugify("ä"),"ae")
        self.assertEqual(slugify("ü"),"ue")
        self.assertEqual(slugify("ö"),"oe")
        self.assertEqual(slugify("ß"),"ss")

    def test_whitespace(self):
        self.assertEqual(slugify(" "),"-")

    def test_slug_exclude(self):
        self.assertEqual(slugify(":"),"")

class TestDirectorymaker(TestCase):

    def test_simpledir(self):
        self.assertEqual(directorymaker("test"),"dst/test")
        self.assertTrue(access("dst",F_OK))
        self.assertFalse(access("dst/test",F_OK))

    def tearDown(self):
        rmdir("dst")

class TestNewfile(TestCase):
    
    def setUp(self):
        mkdir('posts')
        mkdir('drafts')
        parse_args()

    def test_newfile(self):
        self.assertEqual(newfile('test'),'posts/1-test.html')
        with open('posts/1-test.html','w') as f:
            f.write('test')
        self.assertEqual(newfile('test'),'posts/2-test.html')

    def test_draft(self):
        self.assertEqual(newfile('test',True),'drafts/1-test.html')

    def tearDown(self):
        if access('posts/1-test.html',F_OK):
            unlink('posts/1-test.html')
        if access('drafts/1-test.html',F_OK):
            unlink('drafts/1-test.html')
        rmdir('posts')
        rmdir('drafts')
