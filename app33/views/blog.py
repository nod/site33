
from datetime import datetime

import rfc3339
from markdown import Markdown

from viewlib import BaseHandler
from bloglib import Blog

from . import route

# convenience to format a datetime
ts = rfc3339.rfc3339

class BlogHandler(BaseHandler):
    def blog(self, writeable=False):
        return Blog(
                self.application.settings.get('dbposts'),
                self.application.settings.get('dbmeta'),
                writeable=writeable,
                )

    def render_string(self, templ, **kwa):
        return BaseHandler.render_string(
            self,
            templ,
            markdown=Markdown(['codehilite']).convert,
            ts=ts,
            **kwa )


@route(r'/blog/?(?P<year>\d{4})?$')
class BlogList(BlogHandler):
    def get(self, year=None):
        blog = self.blog()
        if year is not None: year=int(year)
        posts = blog.all_posts(year)
        self.render(
            'blog_title_list.html',
            posts=posts,
            title = 'posts' )


@route(r'/blog/tag/(?P<tag>[%\w]+)/?$')
class BlogTagList(BlogHandler):
    def get(self, tag):
        blog = self.blog()
        posts = blog.posts_with_tag(tag)
        self.render(
            'blog_title_list.html',
            posts=posts,
            title = 'tag: %s' % tag )


@route('/')
class IndexHandler(BlogHandler):

    def get(self):
        blog = self.blog()
        years, tags = blog.meta_list()
        self.render(
            'blog_list.html',
            posts=blog[:4],
            tag_list = tags,
            year_list = years,
            )


@route(r'/blog/new')
class BlogNewPost(BlogHandler):

    def get(self):
        blog = self.blog()
        post = {}
        self.render('blog_edit.html', post=post)

    def post(self):
        if self.get_argument('passwd','') != admin_pass:
            print "failed pass", self.get_argument('passwd')
            return self.finish()
        p = {'date':datetime.now()}
        p['title'] = self.get_argument('_title','')
        p['tags'] = self.get_argument('_tags','').split(',')
        p['content'] = self.get_argument('_content','')
        blog_ = self.blog(writeable=True)
        post = blog_.new(**p)
        self.redirect('/blog/%s/edit' % post['key'])


@route(r'/blog/(?P<key>[a-zA-Z0-9-_]+)/edit/?$')
class BlogPost(BlogHandler):

    def get(self, key):
        blog = self.blog()
        if key in blog: post = blog[str(key)]
        else: post = {}
        self.render('blog_edit.html', post=post)

    def post(self, key):
        if self.get_argument('passwd','') != admin_pass:
            print "failed pass", self.get_argument('passwd')
            return self.finish()

        blog_ = self.blog(writeable=True)

        if self.get_argument('delete', False):
            blog_.remove_post(key)
            return self.redirect('/')

        if key in blog_:
            p = blog_[key]
        else:
            p = {'date':datetime.now(), 'key':key}
        p['title'] = self.get_argument('_title','')
        p['tags'] = self.get_argument('_tags','').split(',')
        p['content'] = self.get_argument('_content','')
        blog_[key] = p
        self.redirect('/blog/%s' % key)


@route(r'/blog/(?P<key>[a-zA-Z0-9-_]+)/?$')
class BlogPost(BlogHandler):
    def get(self, key):
        self.render('blog_post.html', post=self.blog()[key])

