
import shelve
from viewlib import route, BaseHandler
from bloglib import Blog

@route('/')
class IndexHandler(BaseHandler):
    def get(self):
        blog = Blog(
                self.application.settings.get('dbposts'),
                self.application.settings.get('dbmeta'),
                )
        self.render('index.html', posts=blog[:10])
