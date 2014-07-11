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
from makeblog.author import Author

class TestProperties(TestCase):

	def test_name(self):
		self.assertIsInstance(Author({"name":"Dummy Name"}).name, str)
		self.assertIsNone(Author({}).name)

	def test_nick(self):
		self.assertIsInstance(Author({'nick':'Dummy Nick'}).nick, str)
		self.assertIsNone(Author({}).nick)

	def test_googleplus(self):
		self.assertIsInstance(Author({'googleplus':'G+ URL'}).googleplus, str)
		self.assertIsNone(Author({}).googleplus)

	def test_twitter(self):
		self.assertIsInstance(Author({'twitter':'Twitter URL'}).twitter, str)
		self.assertIsNone(Author({}).twitter)

	def test_amazon(self):
		self.assertIsInstance(Author({'amazon':'Amazon Wishlist URL'}).amazon, str)
		self.assertIsNone(Author({}).amazon)

	def test_bitcoin(self):
		self.assertIsInstance(Author({'bitcoin':'Bitcoin Wallet'}).bitcoin, str)
		self.assertIsNone(Author({}).bitcoin)

	def test_flattr(self):
		self.assertIsInstance(Author({'flattr':'Flattr Profile'}).flattr, str)
		self.assertIsNone(Author({}).flattr)

	def test_mail(self):
		self.assertIsInstance(Author({'mail':'Mail Address'}).mail, str)
		self.assertIsNone(Author({}).mail)

	def test_has_contact(self):
		self.assertTrue(Author({'twitter':'Test'}).has_contact)
		self.assertTrue(Author({'mail':'Test'}).has_contact)
		self.assertTrue(Author({'googleplus':'Test'}).has_contact)
		self.assertFalse(Author({}).has_contact)

	def test_has_donation(self):
		self.assertTrue(Author({'bitcoin':'Test'}).has_donation)
		self.assertTrue(Author({'amazon':'Test'}).has_donation)
		self.assertTrue(Author({'flattr':'Test'}).has_donation)
		self.assertFalse(Author({}).has_donation)