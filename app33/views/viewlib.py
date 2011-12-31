
import tornado.web
from tornado.escape import json_encode, json_decode

from tornroutes import route

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        user = self.get_secure_cookie("authed_user")
        return user or None

    def ok(self, data=None):
        self.write(json_encode({'status':'ok', 'data':data}))

    def fail(self, reason=None):
        self.write(json_decode({'status':'fail', 'reason': reason}))

    def _handle_request_exception(self, e):
        tornado.web.RequestHandler._handle_request_exception(self,e)
        # import pdb
        # pdb.post_mortem()

