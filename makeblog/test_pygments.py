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
from shutil import rmtree
from makeblog.pygments import *

CONTENT_WITHOUT_CODE = """
This is content
without any code.
"""

CONTENT_WIHT_CODE = """
This is content
$$code(lang=sh)
#!/bin/bash
echo "bla"
$$/code
with code in it.
"""

CONTENT_WITH_MISSING_LEXER = """
This content has a missing lexer
$$code(lang=nerverexisting)
bla
$$/code
"""


class TestPygments(TestCase):

    def test_pygmentify(self):

        @pygmentify
        def render(content):
            return content

        self.assertIsInstance(render(CONTENT_WIHT_CODE),str)
        self.assertIsInstance(render(CONTENT_WITHOUT_CODE),str)
        self.assertIsInstance(render(CONTENT_WITH_MISSING_LEXER),str)

    def tearDown(self):
        rmtree('dst')