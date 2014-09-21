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
from makeblog.author import Author
from makeblog.templating import jinja, render
from makeblog.plugins import PluginMount, PreRenderPlugin, RenderPlugin,\
        PostRenderPlugin
from datetime import datetime
from operator import attrgetter
from os import listdir, system, walk


class Blog(object):
    def __init__(self, config):
        self.config = config
        self.posts = []
        self.categoryposts = {}
        self.authors = []
        self.draft = False

    def build(self, draft=False): # pragma: no cover
        # config
        jinja.globals['blog'] = self
        jinja.globals['now'] = datetime.utcnow()
        self.draft = draft
        # run pre render plugins
        for plugin in PluginMount.get_plugins(PreRenderPlugin, self):
            plugin.run()
        # run render plugins
        for plugin in PluginMount.get_plugins(RenderPlugin, self):
            plugin.render()
        # run post render plugins
        for plugin in PluginMount.get_plugins(PostRenderPlugin, self):
            plugin.run()


class LoadPosts(PreRenderPlugin):
    priority = 10

    def run(self):
        # load all posts
        for filename in listdir('posts'):
            p = Post(self.blog)
            p.load('posts/{}'.format(filename))
            self.blog.posts.append(p)
        if self.blog.draft:
            for filename in listdir('drafts'):
                p = Post(self.blog)
                p.load('drafts/{}'.format(filename))
                self.blog.posts.append(p)


class LoadAuthors(PreRenderPlugin):
    priority = 15

    def run(self):
        # load all authors
        self.blog.authors = sorted(
            [Author(self.blog.config['authors'][item])\
             for item in self.blog.config['authors'].keys()],
            key=attrgetter('nick'))


class SortPosts(PreRenderPlugin):
    priority = 20

    def run(self):
        # sort posts by date
        self.blog.posts = sorted(self.blog.posts, key=attrgetter('date'))


class SortPostsAuthor(PreRenderPlugin):
    priority = 21

    def run(self):
        # sort posts to authors
        for author in self.blog.authors:
            author.posts = [post for post in self.blog.posts if post.author == author.nick]


class CountPostsAuthor(PreRenderPlugin):
    priority = 22

    def run(self):
        # count posts per author
        for author in self.blog.authors:
            author.post_count = len(author.posts)


class FristLastAuthorPosts(PreRenderPlugin):
    priority = 23

    def run(self):
        # first/last post for authors
        for author in self.blog.authors:
            if len(author.posts):
                author.first_post = author.posts[0]
                author.last_post = author.posts[-1]
            else:
                author.first_post = None
                author.last_post = None


class LinkPosts(PreRenderPlugin):
    priority = 30

    def run(self):
        # link next/prev posts
        for post in self.blog.posts:
            i = self.blog.posts.index(post)
            if i:
                post.prev = self.blog.posts[i-1]
            if i != len(self.blog.posts)-1:
                post.next = self.blog.posts[i+1]


class CategorizePosts(PreRenderPlugin):
    priority = 40

    def run(self):
        # categorize posts
        for post in self.blog.posts:
            for category in post.categories:
                if category not in self.blog.categoryposts:
                    self.blog.categoryposts[category] = []
                self.blog.categoryposts[category].append(post)


class RsyncStaticPlugin(PreRenderPlugin):
    priority = 50

    def run(self):
        # rsync src/ to dst/ for static stuff
        system('rsync -a src/ dst')


class ArticleRenderer(RenderPlugin):
    priority = 10

    def render(self):
        # render all post articles
        for post in self.blog.posts:
            post.render()


class IndexRenderer(RenderPlugin):
    priority = 20

    def render(self):
        # render index page
        startposts = self.blog.posts
        startposts.reverse()
        render('chronological.html', 'index.html', posts=startposts)


class FeedRenderer(RenderPlugin):
    priority = 30

    def render(self):
        # render main feed
        feedposts = self.blog.posts[-10:]
        feedposts.reverse()
        render('atom.html', 'feed.atom', posts=feedposts)


class CategoryPageRenderer(RenderPlugin):
    priority = 40

    def render(self):
        # render category pages
        for category in self.blog.categoryposts.keys():
            thisposts = sorted(self.blog.categoryposts[category], key=attrgetter('date'))
            thisposts.reverse()
            render('category.html', 'category/{}/index.html'.format(category),
                   category=category, posts=thisposts)


class CategoryIndexRenderer(RenderPlugin):
    priority = 50

    def render(self):
        # render category index
        categories = list(self.blog.categoryposts.keys())
        categories.sort()
        render('categories.html', 'category/index.html', categories=categories)


class CategoryFeedRenderer(RenderPlugin):
    priority = 60

    def render(self):
        # render category feeds
        for category in self.blog.categoryposts.keys():
            feedposts = sorted(self.blog.categoryposts[category],
                               key=attrgetter('date'))[-10:]
            feedposts.reverse()
            render('atom.html', 'category/{}/feed.atom'.format(category),
                   posts=feedposts)


class ArchiveRenderer(RenderPlugin):
    priority = 70

    def render(self):
        # render archive pages
        timeposts = {}
        for post in self.blog.posts:
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
                       'archive/{}/{}/index.html'.format(year, month),
                       year=year, month=month, posts=archiveposts)
            months = list(timeposts[year].keys())
            months.sort()
            render('archive-annual.html', 'archive/{}/index.html'.format(year),
                   months=months, year=year, yearposts=timeposts[year])
        years = list(timeposts.keys())
        years.sort()
        render('archive.html', 'archive/index.html', years=years)


class StaticRenderer(RenderPlugin):
    priority = 80

    def render(self):
        # static page rendering
        for path, directories, files in walk('src/'):
            for filename in files:
                if filename.endswith('.html'):
                    fname = '{}/{}'.format(path.replace('src/', ''), filename)
                    render('{}/{}'.format(path, filename), fname)


class AuthorIndexRenderer(RenderPlugin):
    priority = 90

    def render(self):
        # render author index
        render('author-index.html', 'author/index.html', authors=self.blog.authors)


class AuthorPageRenderer(RenderPlugin):
    priority = 100

    def render(self):
        # render author pages
        for author in self.blog.authors:
            render('author.html','author/{}/index.html'.format(author.nick), author=author)
