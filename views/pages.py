
from datetime import datetime

import tornado.web
from tornado.escape import xhtml_escape as html_escape

from pagelib import Book
from useful import gen_key, avatar_url
from viewlib import BaseHandler, User
from . import route


class PageBase(BaseHandler):

    def prepare(self):
        super(PageBase, self).prepare()
        self._book = Book(self.application.settings['dbpages'])

    def _page(self, pkey):
        if pkey in ('__new__', None):
            return None
        return self._book.page(pkey) if pkey in self._book else None


@route('/pages/__all')
class AllPages(PageBase):

    def get(self):
        pages = self._book.pages()
        self.render('pages_all.html', pages=pages)


@route('/pages/?(?P<pkey>[a-zA-Z0-9_]*)')
class PageView(PageBase):

    def get(self, pkey=None):
        p_ = self._page(pkey)
        if not p_:
            return self.redirect('/pages/{}/edit'.format(pkey))
        self.render(
            'page.html',
            page_authors=self._book.page_authors(pkey),
            page = p_
            )


@route('/pages/(?P<pkey>[a-zA-Z0-9_]+)/edit/?')
class PageEdit(PageBase):

    def get(self, pkey=None):
        self.render(
                'page_edit.html',
                newslug = pkey,
                page = self._page(pkey)
                )

    def post(self, pkey=None):
	page_edit_pass = self.application.settings['page_edit_passwd']
        if self.current_user:
            uu = self.current_user
        elif self.get_argument('password') == page_edit_pass:
            uu = User('guest@example.com')
        else:
            return self.finish("bzzt. i don't know you.  wrong password?")

        page = self._page(pkey)

        title = self.get_argument('title')
        slug = self.clean(page.slug) if page else self.get_argument('slug')
        text = self.clean(self.get_argument('text'))
        tags_ = self.get_argument('tags', '')
        tags = [self.clean(t.strip()) for t in tags_.split(',')]
        only = self.get_argument('only', False)

        cn,ca = uu.nick, uu.avatar
        self._book.new_page(
                title = title,
                text = text,
                tags = tags,
                slug = slug,
                cr_name = cn,
                cr_avatar = ca,
                owner_only = only,
                )
        self.redirect('/pages/{}'.format(slug))




