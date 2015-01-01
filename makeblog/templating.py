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
from jinja2 import ChoiceLoader, FileSystemLoader, PackageLoader, Environment,\
    StrictUndefined, PrefixLoader
from makeblog.tools import directorymaker

jinja = Environment(
    loader=ChoiceLoader([
        PrefixLoader({
            'base': PackageLoader('makeblog'),
            'authors': FileSystemLoader('authors'),
            'src': FileSystemLoader('src')
        }),
        FileSystemLoader('templates'),
        PackageLoader('makeblog')
    ]),
    undefined=StrictUndefined)


def render(template, filename, **kwargs):
    """
    Render Content from *argv to filename with template.
    """
    with open(directorymaker(filename), 'w') as f:
        t = jinja.get_template(template)
        f.write(t.render(**kwargs))
