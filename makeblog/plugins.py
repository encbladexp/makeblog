# makeblog - A simple offline Blog.
# Copyright (C) 2013-2019 Stefan J. Betz <info@stefan-betz.net>

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

# This Plugin system is directly inspired by:
# http://martyalchin.com/2008/jan/10/simple-plugin-framework/

from operator import attrgetter
from os import walk
from importlib import import_module


def load_plugins(path):
    """
    A small helper to load all plugins from a path.
    """
    for plugindir in walk(path):
        for pluginfile in plugindir[2]:
            if pluginfile.endswith(".py"):
                plugin = "{}.{}".format(plugindir[0].replace("/", "."), pluginfile[:-3])
                import_module(plugin)


class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, "plugins"):
            cls.plugins = []
        else:
            cls.plugins.append(cls)

    def get_plugins(cls, *args, **kwargs):
        return [
            p(*args, **kwargs) for p in sorted(cls.plugins, key=attrgetter("priority"))
        ]


class PluginMixin(object):
    priority = None

    def __init__(self, blog):
        self.blog = blog


class RenderPluginMixin(object):
    def render(self):  # pragma: no cover
        pass


class RunPluginMixin(object):
    def run(self):  # pragma: no cover
        pass


class PreRenderPlugin(PluginMixin, RunPluginMixin, metaclass=PluginMount):
    pass


class RenderPlugin(PluginMixin, RenderPluginMixin, metaclass=PluginMount):
    pass


class PostRenderPlugin(PluginMixin, RunPluginMixin, metaclass=PluginMount):
    pass
