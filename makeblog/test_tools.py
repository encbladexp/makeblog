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
from makeblog.tools import slugify

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
