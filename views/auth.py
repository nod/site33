
import json

from tornado.auth import TwitterMixin
from tornado.web import asynchronous, authenticated, HTTPError

from . import route
from .viewlib import BaseHandler

@route('/auth/logout')
class Logout(BaseHandler):

    def get(self):
        self.set_current_user({})
        self.redirect('/')


@route('/auth/twitter/?')
class AuthTwitter(BaseHandler, TwitterMixin):

    @asynchronous
    def get(self):
        if not self.get_argument("oauth_token", False):
            cb_uri = self.application.settings.get('twitter_callback_uri')
            return self.authorize_redirect(callback_uri = cb_uri)
        self.get_authenticated_user(self._on_auth)

    def _on_auth(self, user_d):
        if not user_d:
            raise HTTPError(500, "Twitter auth failed")
        self.set_current_user(user_d)
        self.redirect('/')


@route('/auth/?')
class Login(BaseHandler):

    def get(self):
        self.render('login.html')
