
from tornroutes import route

from viewlib import BaseHandler

# import time side effects ftw. importing the modules creates our routes
import about
import pastebin
import tmp

# this needs to be the last line after all views are defined
routes = route.get_routes()
