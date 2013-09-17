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
from makeblog.tools import directorymaker, options
from makeblog.post import Post
from makeblog.templating import jinja
from datetime import datetime
from operator import attrgetter
from os import listdir, system, walk
from time import strftime
from urllib.parse import urlparse
import json

class Blog(object):
    def __init__(self):
        with open('config.json','r') as f:
            self.config = json.load(f)
            self.config['blog']['domain'] = urlparse(self.config['blog']['url']).netloc

    def build(self):
        # config
        jinja.globals['blog'] = self
        jinja.globals['now'] = datetime.utcnow()
        # load all posts
        unsortedposts = []
        for filename in listdir('posts'):
            p = Post(self)
            p.load('posts/%s' % filename)
            unsortedposts.append(p)
        if options.draft:
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
        with open(directorymaker('index.html'), 'w') as f:
            t = jinja.get_template('chronological.html')
            startposts = posts[-5:]
            startposts.reverse()
            f.write(t.render(posts=startposts))
        # render main feed
        with open(directorymaker('feed.atom'), 'w') as f:
            t = jinja.get_template('atom.html')
            feedposts = posts[-10:]
            feedposts.reverse()
            f.write(t.render(posts=feedposts))
        # render category pages
        categoryposts = {}
        for post in posts:
            for category in post.categories:
                if not category in categoryposts:
                    categoryposts[category] = []
                categoryposts[category].append(post)
        for category in categoryposts.keys():
            with open(directorymaker('category/%s/index.html'% category), 'w') as f:
                t = jinja.get_template('category.html')
                thisposts = sorted(categoryposts[category], key=attrgetter('date'))
                thisposts.reverse()
                f.write(t.render(category=category, posts=thisposts))
        # render category index
        with open(directorymaker('category/index.html'), 'w') as f:
            t = jinja.get_template('categories.html')
            categories = list(categoryposts.keys())
            categories.sort()
            f.write(t.render(categories=categories))
        # render category feeds
        for category in categoryposts.keys():
            with open(directorymaker('category/%s/feed.atom' % category), 'w') as f:
                t = jinja.get_template('atom.html')
                feedposts = sorted(categoryposts[category], key=attrgetter('date'))[-10:]
                feedposts.reverse()
                f.write(t.render(posts=feedposts))
        # render archive pages
        timeposts = {}
        for post in posts:
            if not post.date.year in timeposts:
                timeposts[post.date.year] = {}
            if not post.date.month in timeposts[post.date.year]:
                timeposts[post.date.year][post.date.month] = []
            timeposts[post.date.year][post.date.month].append(post)
        for year in timeposts.keys():
            for month in timeposts[year].keys():
                with open(directorymaker('archive/%s/%s/index.html' % ( year, month )), 'w') as f:
                    t = jinja.get_template('archive-posts.html')
                    archiveposts = sorted(timeposts[year][month], key=attrgetter('date'))
                    archiveposts.reverse()
                    f.write(t.render(year=year, month=month, posts=archiveposts))
            with open(directorymaker('archive/%s/index.html' % year), 'w') as f:
                t = jinja.get_template('archive-annual.html')
                months = list(timeposts[year].keys())
                months.sort()
                f.write(t.render(months=months, year=year, yearposts=timeposts[year]))
        with open(directorymaker('archive/index.html'), 'w') as f:
            t = jinja.get_template('archive.html')
            years = list(timeposts.keys())
            years.sort()
            f.write(t.render(years=years))
        # static page rendering
        for path, directories, files in walk('src/'):
            for filename in files:
                if filename.endswith('.html'):
                    fname = '%s/%s' % ( path.replace('src/',''), filename )
                    with open(directorymaker(fname), 'w') as f:
                        t = jinja.get_template(fname)
                        f.write(t.render())
