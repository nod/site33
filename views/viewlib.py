
import json

import tornado.web
from markdown import Markdown


class User(object):
    """
    convenience object to make it easy to unify login settings
    """
    def __init__(self, nick, name, avatar, source, is_admin=False):
        self.nick = nick # short name
        self.name = name # long name
        self.avatar = avatar # url to their avatar
        self.source = source # str giving hint. twitter? local? etc
        self.is_admin = is_admin

    def uniq_id(self):
        return '{}::{}'.format(self.source, self.nick)


class BaseHandler(tornado.web.RequestHandler):

    def clean(self, s):
        s = s.replace('<', '&lt;')
        s = s.replace('>', '&gt;')
        return s

    def render_string(self, templ, **kwa):
        return super(BaseHandler, self).render_string(
            templ,
            markdown=Markdown(['codehilite']).convert,
            **kwa
            )

    def _instantiate_user(self, d):
        """
        accepts a twitter oauth'd user object and builds a User
        """
        return User(
            d['username'],
            d.get('name', d['username']),
            d.get('profile_image_url', '/static/images/dunno.png'),
            'twitter',
            d['username'] in self.application.settings.get(
                'twitter_admins', [] )
            )

    def get_current_user(self):
        try:
            u_ = json.loads(self.get_secure_cookie("authed_user"))
            return self._instantiate_user(u_) if u_ else None
        except TypeError:
            pass

    def set_current_user(self, user):
        """
        to be called AFTER the user has authenticated successfully.  Right now
        we assume it's twitter auth.

        `user` should be a dictionary returned from successful oauth
        """
        u_ = json.dumps(user)
        self.set_secure_cookie("authed_user", u_)
        # seed the _current_user method in case it's cached with nothing by now
        if user:
            self._current_user = self._instantiate_user(user)

    def ok(self, data=None):
        self.write(json.dumps({'status':'ok', 'data':data}))

    def fail(self, reason=None):
        self.write(json.dumps({'status':'fail', 'reason': reason}))

    def _handle_request_exception(self, e):
        tornado.web.RequestHandler._handle_request_exception(self,e)
        if self.application.settings.get('debug_pdb'):
            import pdb
            pdb.post_mortem()

