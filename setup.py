#!/usr/bin/python
# setup.py - Installs makeblog
# Copyright (C) 2013-2017 Stefan J. Betz <info@stefan-betz.net>

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

from distutils.core import setup

setup(name='makeblog',
      version='0.0.7',
      description='A simple offline Blog.',
      author='Stefan J. Betz',
      author_email='info@stefan-betz.net',
      url='https://github.com/encbladexp/makeblog',
      scripts=['makeblogctl'],
      packages=['makeblog'],
      package_data={'makeblog': ['templates/*.html']}
      )
