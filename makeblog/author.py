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

def authors(config):
    authorlist = list(config['authors'].keys())
    authorlist.sort()
    for item in authorlist:
        yield Author(config['authors'][item])

class Author(object):
    
    def __init__(self, data):
        self.data = data

    @property
    def name(self):
        return self.data['name']

    @property
    def nick(self):
        return self.data['nick']

    @property
    def googleplus(self):
        return self.data['googleplus']

    @property
    def twitter(self):
        return self.data['googleplus']

    @property
    def amazon(self):
        return self.data['googleplus']

    @property
    def bitcoin(self):
        return self.data['googleplus']

    @property
    def mail(self):
        return self.data['googleplus']
