
import json

from tornado.auth import TwitterMixin
from tornado.web import asynchronous, authenticated, HTTPError

from . import route
from .viewlib import BaseHandler

@route('/auth/?')
class LoginView(BaseHandler):

    def get(self):
        self.render('login.html')


@route('/auth/twitter/?')
class AuthHandler(TwitterMixin, BaseHandler):

    @asynchronous
    def get(self):
        if not self.get_argument("oauth_token", None):
            return self.authorize_redirect(
                callback_uri='http://localhost:6488/auth/twitter'
                )
        self.get_authenticated_user(self._got_authed)

    def _got_authed(self, user_d):
        if not user_d:
            raise HTTPError(500, "Twitter auth failed")
        self.set_current_user(user_d)
        print user_d
        self.redirect('/')
