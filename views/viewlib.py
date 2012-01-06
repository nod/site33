
import json

import tornado.web

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return json.loads(self.get_secure_cookie("authed_user"))

    def set_current_user(self, user):
        self.set_secure_cookie("authed_user", json.dumps(user))

    def ok(self, data=None):
        self.write(json.dumps({'status':'ok', 'data':data}))

    def fail(self, reason=None):
        self.write(json.dumps({'status':'fail', 'reason': reason}))

    def _handle_request_exception(self, e):
        tornado.web.RequestHandler._handle_request_exception(self,e)
        if self.application.settings.get('debug_pdb'):
            import pdb
            pdb.post_mortem()

