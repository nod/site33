
from datetime import datetime

import rfc3339
from markdown import Markdown
from tornado.web import HTTPError

from . import route
from viewlib import BaseHandler
from bloglib import Blog

# convenience to format a datetime
ts = rfc3339.rfc3339

class BlogHandler(BaseHandler):

    def prepare(self):
        super(BlogHandler, self).prepare()
        self.blog = Blog( self.application.settings.get('dbposts') )
        self.admin_pass = self.application.settings.get('blog_admin')

    def render_string(self, templ, **kwa):
        return BaseHandler.render_string(
            self,
            templ,
            markdown=Markdown(['codehilite']).convert,
            ts=ts,
            **kwa )

    def require_admin(self):
        if self.get_argument('passwd', None) != self.admin_pass:
            raise HTTPError(401)


@route(r'/blog/?(?P<year>\d{4})?$')
class BlogList(BlogHandler):
    def get(self, year=None):
        if year is not None: year=int(year)
        posts = self.blog.all_posts(year)
        self.render(
            'blog_title_list.html',
            posts=posts,
            title = 'posts' )


@route(r'/blog/tag/(?P<tag>[%\w]+)/?$')
class BlogTagList(BlogHandler):
    def get(self, tag):
        posts = self.blog.posts_with_tag(tag)
        self.render(
            'blog_title_list.html',
            posts=posts,
            title = 'tag: %s' % tag )


@route('/')
class IndexHandler(BlogHandler):

    def get(self):
        years, tags = self.blog.meta_lists()
        self.render(
            'blog_list.html',
            posts=self.blog.all_posts()[:4],
            tag_list = tags,
            year_list = years,
            )


@route(r'/blog/new')
class BlogNewPost(BlogHandler):

    def get(self):
        self.render('blog_edit.html', post=None)

    def post(self):
        self.require_admin()

        p = {'date':datetime.now()}
        p['title'] = self.get_argument('_title','')
        p['tags'] = self.get_argument('_tags','').split(',')
        p['content'] = self.get_argument('_content','')
        post = self.blog.new_post(**p)
        self.redirect('/blog/%s/edit' % post.slug)


@route(r'/blog/(?P<key>[a-zA-Z0-9-_]+)/edit/?$')
class BlogPostEdit(BlogHandler):

    def get(self, key):
        post = self.blog.post(key) if key in self.blog else None
        self.render('blog_edit.html', post=post)

    def post(self, key):
        self.require_admin()

        if self.get_argument('delete', False):
            self.blog.remove_post(key)
            return self.redirect('/')

        title = self.get_argument('_title','')
        tags = self.get_argument('_tags','').split(',')
        content = self.get_argument('_content','')
        if key in self.blog:
            p = self.blog.post(key)
            p.title = title
            p.tags = tags
            p.content = content
            self.blog.update(p)
        else:
            key, post = self.blog.new_post(
                title=title,
                content=content,
                tags=tags
                )
        self.redirect('/blog/%s' % key)


@route(r'/blog/(?P<key>[a-zA-Z0-9-_]+)/?$')
class BlogPost(BlogHandler):
    def get(self, key):
        self.render('blog_post.html', post=self.blog.post(key))

