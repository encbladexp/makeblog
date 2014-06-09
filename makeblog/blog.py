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
from makeblog.post import Post
from makeblog.author import authors
from makeblog.templating import jinja, render
from datetime import datetime
from operator import attrgetter
from os import listdir, system, walk, access, F_OK


class Blog(object):
    def __init__(self, config):
        self.config = config

    def build(self, draft=False):
        # config
        jinja.globals['blog'] = self
        jinja.globals['now'] = datetime.utcnow()
        # load all posts
        unsortedposts = []
        for filename in listdir('posts'):
            p = Post(self)
            p.load('posts/%s' % filename)
            unsortedposts.append(p)
        if draft:
            for filename in listdir('drafts'):
                p = Post(self)
                p.load('drafts/%s' % filename)
                unsortedposts.append(p)
        # sort posts by date
        posts = sorted(unsortedposts, key=attrgetter('date'))
        # link next/prev posts
        for post in posts:
            i = posts.index(post)
            if i:
                post.prev = posts[i-1]
            if i != len(posts)-1:
                post.next = posts[i+1]
        # rsync src/ to dst/ for static stuff
        system('rsync -a src/ dst')
        # render all post articles
        for post in posts:
            post.render()
        # render index page
        startposts = posts[-5:]
        startposts.reverse()
        render('chronological.html', 'index.html', posts=startposts)
        # render main feed
        feedposts = posts[-10:]
        feedposts.reverse()
        render('atom.html', 'feed.atom', posts=feedposts)
        # render category pages
        categoryposts = {}
        for post in posts:
            for category in post.categories:
                if category not in categoryposts:
                    categoryposts[category] = []
                categoryposts[category].append(post)
        for category in categoryposts.keys():
            thisposts = sorted(categoryposts[category], key=attrgetter('date'))
            thisposts.reverse()
            render('category.html', 'category/%s/index.html' % category,
                   category=category, posts=thisposts)
        # render category index
        categories = list(categoryposts.keys())
        categories.sort()
        render('categories.html', 'category/index.html', categories=categories)
        # render category feeds
        for category in categoryposts.keys():
            feedposts = sorted(categoryposts[category],
                               key=attrgetter('date'))[-10:]
            feedposts.reverse()
            render('atom.html', 'category/%s/feed.atom' % category,
                   posts=feedposts)
        # render archive pages
        timeposts = {}
        for post in posts:
            if post.date.year not in timeposts:
                timeposts[post.date.year] = {}
            if post.date.month not in timeposts[post.date.year]:
                timeposts[post.date.year][post.date.month] = []
            timeposts[post.date.year][post.date.month].append(post)
        for year in timeposts.keys():
            for month in timeposts[year].keys():
                archiveposts = sorted(timeposts[year][month],
                                      key=attrgetter('date'))
                archiveposts.reverse()
                render('archive-posts.html',
                       'archive/%s/%s/index.html' % (year, month),
                       year=year, month=month, posts=archiveposts)
            months = list(timeposts[year].keys())
            months.sort()
            render('archive-annual.html', 'archive/%s/index.html' % year,
                   months=months, year=year, yearposts=timeposts[year])
        years = list(timeposts.keys())
        years.sort()
        render('archive.html', 'archive/index.html', years=years)
        # static page rendering
        for path, directories, files in walk('src/'):
            for filename in files:
                if filename.endswith('.html'):
                    fname = '%s/%s' % (path.replace('src/', ''), filename)
                    render('%s/%s' % (path, filename), fname)
        # render author index
        render('author-index.html', 'author/index.html', authors=authors(self.config))
        # render author pages
        for author in authors(self.config):
            if access('authors/%s.html' % author.nick, F_OK):
                render('authors/%s.html' % author.nick, 'author/%s/index.html' % author.nick, author=author)
            else:
                render('author.html','author/%s/index.html' % author.nick, author=author)
