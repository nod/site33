
import rfc3339
from markdown import Markdown
from viewlib import route, BaseHandler, async_yield
from bloglib import Blog
from datetime import datetime

def ts(d):
    return rfc3339.rfc3339(d)

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
            markdown=Markdown().convert,
            ts=ts,
            **kwa )


@route('/')
class IndexHandler(BlogHandler):

    def get(self):
        self.render('blog_list.html', posts=self.blog()[:4])


@route(r'/blog/(?P<key>[a-zA-Z0-9-_]+)/edit/?$')
class BlogPost(BlogHandler):
    def get(self, key):
        blog = self.blog()
        if key in blog: post = blog[str(key)]
        else: post = {}
        print "key",key,"post=",post
        self.render('blog_edit.html', post=post)

    def post(self, key):
        if self.get_argument('passwd','') != 'ub3rleet':
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
        p['content'] = self.get_argument('_content','')
        blog_[key] = p
        self.redirect('/blog/%s' % key)


@route(r'/blog/(?P<key>[a-zA-Z0-9-_]+)/?$')
class BlogPost(BlogHandler):
    def get(self, key):
        self.render('blog_post.html', post=self.blog()[key])

