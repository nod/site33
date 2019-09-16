
from datetime import datetime
from uuid import uuid4

import tornado
from tornado.web import HTTPError, authenticated
from tornado.util import ObjectDict

from . import route
from .viewlib import BaseHandler

import sqlite3


uuid = lambda: uuid4().hex


class RTBase(BaseHandler):

    def _setup_db(self):
        RTBase._dbconn = dbc = sqlite3.connect(
            self.application.settings.get('dbreadthis') )
        dbc.execute( '''
create table if not exists rt (
    uid text,
    nick text,
    url text,
    tags text,
    text text,
    context text,
    ts text
) ''' )

    def prepare(self):
        super(RTBase, self).prepare()
        if not hasattr(RTBase, '_dbconn'): self._setup_db()
        ct = self.request.headers.get('Content-Type') or ''
        if ct.startswith('application/json'):
            js = tornado.escape.json_decode(self.request.body)
            for key, value in js.items():
                if type(value) is list:
                    self.request.arguments.setdefault(key, []).extend(value)
                elif type(value) is dict:
                    self.request.arguments[key] = value
                else: self.request.arguments.setdefault(key, []).extend([value])


@route(r'/readthis/?$')
class ReadListIncoming(RTBase):

    # XXX STILL NEEDS TO CHECK AUTH HEADER
    def post(self):
        c = self._dbconn.cursor()
        n = self.get_argument('nick') or None
        u = self.get_argument('url') or None
        tags = self.get_argument('tags', '')
        text = self.get_argument('text', '')
        ts = datetime.now().isoformat()
        if not (n and u):
            return self.write('missing params')
        vals = (uuid(), n,u,tags,text,ts)
        c.execute('''
insert into rt (uid, nick, url, tags, text, ts)
values (?, ?, ?, ?, ?, ?) ''',
            vals)
        self._dbconn.commit()
        self.write('ok')


@route(r'/readthis/?(?P<user>\w+)?$')
class ReadList(RTBase):

    def get(self, user):
        c = self._dbconn.cursor()
        print("FETCHING links for ", user)
        if user == 'all':
            # get them all
            c.execute(
                '''select url, tags, ts, uid, text, nick
                from rt order by ts desc limit 250''' )
        else:
            c.execute(
                '''select url, tags, ts, uid, text, nick
                from rt where nick=? order by ts desc limit 250''',
                (user,) )
        rows = [
            ObjectDict(nick=r[5], text=r[4], uid=r[3], url=r[0], tags=r[1],
                       ts=r[2] )
            for r in c ]
        print("FOUND links:", rows)
        self.render(
            'rt_list.html',
            nick=user,
            links=rows,
            title = 'links'
            )
        del c



