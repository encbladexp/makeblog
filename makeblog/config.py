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

DEFAULT_CONFIG = {
    'blog':{
        'name':'''My's Blog''',
        'url':'http://blog.domain.tld',
        'description':'Because i can!',
        'googleplus':True,
        'twitter':True,
        'categories':['category1', 'category2', 'category4' ],
        'defaultauthor':'me',
        'timezone':'Europe/Berlin',
        'dateformat':'%Y/%m/%d %H:%M:%S'
    },
    'authors':{
        'me':{
            'name':'Full Name',
            'nick':'nickname',
            'googleplus':'http...',
            'twitter':'http...',
            'amazon':None,
            'bitcoin':None,
            'mail':'info@domain.tld'
        }
    }
}
