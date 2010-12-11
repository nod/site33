
from viewlib import route, BaseHandler, async_yield

import about
import blog
import pastebin




# this needs to be the last line after all views are defined
routes = route.get_routes()
