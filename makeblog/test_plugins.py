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
from makeblog.plugins import load_plugins, PluginMount, PreRenderPlugin, PostRenderPlugin, RenderPlugin


class TestPluginMount(TestCase):

    def test_get_plugins(self):
        self.assertIsInstance(PluginMount.get_plugins(PreRenderPlugin, None), list)
        self.assertIsInstance(PluginMount.get_plugins(PostRenderPlugin, None), list)
        self.assertIsInstance(PluginMount.get_plugins(RenderPlugin, None), list)


class TestPluginLoader(TestCase):

    def setUp(self):
        mkdir('plugins')
        with open('plugins/test.py','w') as f:
            f.write('')

    def test_load_plugins(self):
        load_plugins('plugins')

    def tearDown(self):
        rmtree('plugins')