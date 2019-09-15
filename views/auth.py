
import json

from tornado.auth import TwitterMixin
from tornado.web import authenticated, HTTPError

from . import route
from .viewlib import BaseHandler


@route('/logout')
class Logout(BaseHandler):

    def get(self):
        self.set_current_user(None)
        self.redirect('/')


@route('/login/?')
class AuthLogin(BaseHandler):

    def get(self):
        return self.render('login.html')

    def post(self):
        users = self.application.settings.get('users', {})
        email = self.get_argument('email', '')
        paswd = self.get_argument('password', '')
        if email in users and users[email] == paswd:
            self.set_current_user(email)
            self.redirect('/')
        else:
            self.redirect('/login')

