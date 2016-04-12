
from datetime import datetime

from tornado.web import HTTPError, authenticated

from . import route
from viewlib import BaseHandler
from bloglib import Blog


class BlogBase(BaseHandler):

    def prepare(self):
        super(BlogBase, self).prepare()
        self.blog = Blog( self.application.settings.get('dbposts') )

    def require_admin(self):
        if not self.current_user:
            raise HTTPError(301)


@route(r'/blog/?(?P<year>\d{4})?$')
class BlogList(BlogBase):

    def get(self, year=None):
        try: year=int(year)
        except: pass
        self.render(
            'blog_title_list.html',
            posts=self.blog.posts(year),
            title = 'posts'
            )


@route(r'/blog/tag/(?P<tag>[%\w]+)/?$')
class BlogTagList(BlogBase):
    def get(self, tag):
        self.render(
            'blog_title_list.html',
            posts= self.blog.posts_with_tag(tag),
            title = 'tag: %s' % tag
            )


@route('/')
class IndexHandler(BlogBase):

    def get(self):
        years, tags = self.blog.meta_lists()
        self.render(
            'blog_list.html',
            posts=self.blog.posts()[:4],
            tag_list = (t for t in tags if t.strip()),
            year_list = years,
            )


@route(r'/blog/new')
class BlogNewPost(BlogBase):

    @authenticated
    def get(self):
        self.require_admin()
        self.render('blog_edit.html', post=None)

    @authenticated
    def post(self):
        self.require_admin()
        p_ = dict(
            title = self.get_argument('_title'),
            tags = self.get_argument('_tags','').split(','),
            content = self.get_argument('_content',''),
            )
        _, post = self.blog.new_post(**p_)
        self.redirect('/blog/%s/edit' % post.slug)


@route(r'/blog/(?P<slug>[a-zA-Z0-9-_]+)/edit/?$')
class BlogPostEdit(BlogBase):

    @authenticated
    def get(self, slug):
        self.require_admin()
        post = self.blog.post(slug) if slug in self.blog else None
        self.render('blog_edit.html', post=post)

    @authenticated
    def post(self, slug):
        self.require_admin()

        if self.get_argument('delete', False):
            self.blog.remove(slug)
            return self.redirect('/?m=done')

        title = self.get_argument('_title')
        tags = self.get_argument('_tags','').split(',')
        content = self.get_argument('_content')
        if slug in self.blog:
            p = self.blog.post(slug)
            p.title = title
            p.tags = tags
            p.content = content
            self.blog.save(p)
        else:
            slug, post = self.blog.new_post(
                title=title,
                content=content,
                tags=tags
                )
        self.redirect('/blog/%s' % slug)


@route(r'/blog/(?P<key>[a-zA-Z0-9-_]+)/?')
class BlogPost(BlogBase):
    def get(self, key):
        self.render('blog_post.html', post=self.blog.post(key))

