# makeblog - A simple offline Blog.
# Copyright (C) 2013-2015 Stefan J. Betz <info@stefan-betz.net>

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
from unittest import TestCase, skip
from os import rmdir, mkdir
from makeblog.server import Server


class TestServer(TestCase):

    def setUp(self):
        mkdir('dst')

    def test_server_init(self):
        s = Server()
        self.assertIsInstance(s, Server)
        s.httpd.socket.close()

    def tearDown(self):
        rmdir('dst')
