
from viewlib import BaseHandler
from tornroutes import route, generic_route

# import time side effects ftw. importing the modules creates our routes
import auth
import about
import blog
import pages
import pastebin
import tmp

generic_route('/projects/?', 'projects.html')

@route('.*')
class Handle404(BaseHandler):
    def get(self):
        # self.request.path

        # let's look in the pages book to see if this page exists
        from pagelib import Book
        _book = Book(self.application.settings['dbpages'])

        page_maybe = self.request.path[1:]
        if page_maybe in _book:
            return self.redirect('/pages/{}'.format(page_maybe))

        self.render('lost.html')


# this needs to be the last line after all views are defined
routes = route.get_routes()
