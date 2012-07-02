
from viewlib import BaseHandler
from tornroutes import route

# import time side effects ftw. importing the modules creates our routes
import auth
import about
import blog
import pages
import pastebin
import tmp


@route('.*')
class Handle404(BaseHandler):
    def get(self):


        print dir(request)


        self.redirect('/static/lost.html')


# this needs to be the last line after all views are defined
routes = route.get_routes()
