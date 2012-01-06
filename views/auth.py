
import json

from tornado.auth import TwitterMixin
from tornado.web import asynchronous, authenticated, HTTPError

from . import route
from .viewlib import BaseHandler

@route('/auth/?')
class LoginView(BaseHandler):

    def get(self):
        self.render('login.html')

@route('/auth/logout')
class Logout(BaseHandler):

    def get(self):
        self.set_current_user({})
        self.redirect('/')


@route('/auth/twitter/?')
class AuthHandler(TwitterMixin, BaseHandler):

    @asynchronous
    def get(self):
        if not self.get_argument("oauth_token", None):
            if self.application.settings.get('debug'):
                cburi = 'http://localhost:6488/auth/twitter'
            else:
                cburi = 'http://33ad.org/auth/twitter' # build this FIXME
            return self.authorize_redirect( callback_uri= cburi )
        self.get_authenticated_user(self._got_authed)

    def _got_authed(self, user_d):
        if not user_d:
            raise HTTPError(500, "Twitter auth failed")
        admins = self.application.settings.get('twitter_users')
        screen_name = user_d['username']
        if screen_name in admins: self.set_current_user(user_d)
        self.redirect('/')
