
import json

import tornado.web
from markdown import Markdown

from useful import avatar_url

class User(object):
    """
    convenience object to make it easy to unify login settings
    """
    def __init__(self, email):
        self.nick = email.split('@')[0]
        self.email = email
        print "END USER"
        self.avatar = avatar_url(email)
        self.source = 'local' # str giving hint. twitter? local? etc

    def uniq_id(self):
        return '{}::{}'.format(self.source, self.email)


class BaseHandler(tornado.web.RequestHandler):

    def clean(self, s):
        s = s.replace('<', '&lt;')
        s = s.replace('>', '&gt;')
        return s

    def render_string(self, templ, **kwa):
        return super(BaseHandler, self).render_string(
            templ,
            markdown=Markdown(['codehilite']).convert,
            current_user=self.current_user,
            **kwa
            )

    def get_current_user(self):
        try:
            u_ = self.get_secure_cookie("authed_user")
            u = User(u_) if u_ else None
            return u
        except TypeError:
            pass

    def set_current_user(self, user):
        """
        to be called AFTER the user has authenticated successfully.  Right now
        we assume it's twitter auth.

        `user` should be an email addr or None
        """
        if user is not None:
      	    self.set_secure_cookie("authed_user", user)
        else:
            self.clear_cookie('authed_user')

    def ok(self, data=None):
        self.write(json.dumps({'status':'ok', 'data':data}))

    def fail(self, reason=None):
        self.write(json.dumps({'status':'fail', 'reason': reason}))

    def write_error(self, status_code, **kwargs):
        self.redirect('/static/oops.html')

    def _handle_request_exception(self, e):
        tornado.web.RequestHandler._handle_request_exception(self,e)
        if self.application.settings.get('debug_pdb'):
            import pdb
            pdb.post_mortem()

