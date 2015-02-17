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


class Author(object):

    def __init__(self, data):
        self.data = data

    @property
    def name(self):
        return self.data['name'] if 'name' in self.data else None

    @property
    def nick(self):
        return self.data['nick'] if 'nick' in self.data else None

    @property
    def googleplus(self):
        return self.data['googleplus'] if 'googleplus' in self.data else None

    @property
    def twitter(self):
        return self.data['twitter'] if 'twitter' in self.data else None

    @property
    def amazon(self):
        return self.data['amazon'] if 'amazon' in self.data else None

    @property
    def bitcoin(self):
        return self.data['bitcoin'] if 'bitcoin' in self.data else None

    @property
    def mail(self):
        return self.data['mail'] if 'mail' in self.data else None

    @property
    def flattr(self):
        return self.data['flattr'] if 'flattr' in self.data else None

    @property
    def has_contact(self):
        if self.mail or self.googleplus or self.twitter:
            return True
        else:
            return False

    @property
    def has_donation(self):
        if self.flattr or self.bitcoin or self.amazon:
            return True
        else:
            return False
