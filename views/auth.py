
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
class AuthHandler(BaseHandler, TwitterMixin):

    @asynchronous
    def get(self):
        if self.get_argument("oauth_token", False):
            self.get_authenticated_user(self._on_auth)
            return
        self.authorize_redirect()

    def _on_auth(self, user):
        if not user:
            raise HTTPError(500, "Twitter auth failed")
        self.set_current_user(user)
        self.redirect('/')

